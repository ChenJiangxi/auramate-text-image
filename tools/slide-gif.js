/**
 * 动图 slide：把一段产品录屏合成进渲染好的 slide，出 GIF。
 *
 *   node tools/slide-gif.js <slide.html> <源录屏.mov|.webm> <out.gif> [秒数]
 *
 * 用在「灵体形态」这类**本来就是动的**内容上 —— 十种形态是粒子在运动，
 * 扒成静帧等于把最有意思的部分丢了。小红书图文支持 GIF，长按会播。
 *
 * 原理：
 *   1. Playwright 渲染 slide → 静态底图，同时读出 id="slot" 那个元素的位置和圆角
 *   2. PIL 生成同尺寸的圆角 alpha 蒙版（不然叠上去四角是方的，跟卡片对不上）
 *   3. ffmpeg 把录屏 scale+crop 进那个槽位、叠到底图上 → palettegen 出 GIF
 *
 * 要动图的元素在模板里必须带 id="slot"。
 */
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');

function loadPlaywright() {
  const c = ['playwright',
    path.join(__dirname, '../node_modules/playwright'),
    '/Users/macmini003/ops-auramate/node_modules/playwright'];
  for (const p of c) { try { return require(p); } catch (e) {} }
  console.error('找不到 playwright：npm i playwright && npx playwright install chromium');
  process.exit(1);
}
const { chromium } = loadPlaywright();

const [htmlPath, srcVideo, outGif, secsArg] = process.argv.slice(2);
if (!htmlPath || !srcVideo || !outGif) {
  console.error('用法: node tools/slide-gif.js <slide.html> <录屏> <out.gif> [秒数=4]');
  process.exit(2);
}
const SECS = Number(secsArg || 4);
const W = 1242, H = 1660;
const MAX_MB = Number(process.env.GIF_MAX_MB || 5.5);   // 单张预算
const FORCE_W = Number(process.env.GIF_WIDTH || 0);     // 只为 README 缩略时才用

// 降档梯子：从最好的画质往下退，直到进预算。
// 动图面积越大越吃体积 —— 十种形态这类满屏光球，1080 宽 4s 10fps 能到 11MB。
const LADDER = [
  { secs: SECS, fps: 10, colors: 192, w: 1080 },
  { secs: SECS, fps: 8,  colors: 160, w: 1000 },
  { secs: Math.min(SECS, 3), fps: 8, colors: 128, w: 960 },
  { secs: Math.min(SECS, 3), fps: 8, colors: 128, w: 860 },
];

(async () => {
  const tmp = fs.mkdtempSync('/tmp/slide-gif-');
  const base = path.join(tmp, 'base.png');
  const mask = path.join(tmp, 'mask.png');

  // ── 1. 渲染底图 + 读槽位 ──
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: W, height: H });
  await page.goto('file://' + path.resolve(htmlPath), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready).catch(() => {});
  await page.waitForTimeout(1200);

  const slot = await page.evaluate(() => {
    const el = document.querySelector('#slot');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    // 圆角常挂在里面的 img 上而不是容器上，往下找一层
    const kid = el.firstElementChild;
    const radius = parseFloat(getComputedStyle(el).borderTopLeftRadius)
                || (kid ? parseFloat(getComputedStyle(kid).borderTopLeftRadius) : 0) || 0;
    // 宽高取偶数：ffmpeg 缩放/编码在奇数尺寸上容易差 1px，跟蒙版对不上直接报错
    const even = n => Math.round(n) - (Math.round(n) % 2);
    return { x: Math.round(r.x), y: Math.round(r.y), w: even(r.width), h: even(r.height), radius: Math.round(radius) };
  });
  if (!slot) {
    console.error(`${path.basename(htmlPath)} 里没有 id="slot" 的元素 —— 要合成动图的容器必须带这个 id`);
    await browser.close(); process.exit(3);
  }
  await page.screenshot({ path: base });
  await browser.close();
  console.log(`槽位 ${slot.w}×${slot.h} @ (${slot.x},${slot.y}) 圆角 ${slot.radius}`);

  // ── 2. 圆角蒙版 ──
  execFileSync('/usr/bin/python3', ['-c', `
from PIL import Image, ImageDraw
m = Image.new('L', (${slot.w}, ${slot.h}), 0)
ImageDraw.Draw(m).rounded_rectangle([0,0,${slot.w-1},${slot.h-1}], radius=${slot.radius}, fill=255)
m.save('${mask}')
`], { stdio: 'inherit' });

  // ── 3. 合成 GIF ──
  // fps 和缩放都放在 overlay **之后** —— 放在前面的话输出会跟着底图的 25fps 走，
  // 帧数翻 2.5 倍、体积跟着翻。第一版就是这么炸到 18MB 的。
  const build = ({ secs, fps, colors, w }) => [
    // 末尾再 scale 一次是兜底：force_original_aspect_ratio 的取整会差 1px，
    // 跟蒙版尺寸对不上 ffmpeg 直接 alphamerge 报错退出。
    `[1:v]scale=${slot.w}:${slot.h}:force_original_aspect_ratio=increase:flags=lanczos,` +
      `crop=${slot.w}:${slot.h},scale=${slot.w}:${slot.h},setsar=1[v]`,
    `[2:v]scale=${slot.w}:${slot.h},format=gray[m]`,
    `[v][m]alphamerge[va]`,
    `[0:v][va]overlay=${slot.x}:${slot.y}:format=auto,` +
      `fps=${fps},scale=${FORCE_W || w}:-2:flags=lanczos,split[a][b]`,
    `[a]palettegen=max_colors=${colors}:stats_mode=diff[p]`,
    `[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle`,
  ].join(';');

  let mb = 0, used = null;
  for (const step of LADDER) {
    execFileSync('ffmpeg', [
      '-loop', '1', '-t', String(step.secs), '-i', base,
      '-stream_loop', '-1', '-t', String(step.secs), '-i', path.resolve(srcVideo),
      '-loop', '1', '-t', String(step.secs), '-i', mask,
      '-filter_complex', build(step),
      '-loop', '0', '-y', path.resolve(outGif),
    ], { stdio: ['ignore', 'ignore', 'ignore'] });
    mb = fs.statSync(outGif).size / 1048576;
    used = step;
    if (mb <= MAX_MB) break;
    console.log(`  ${step.secs}s/${step.fps}fps/${step.colors}色/${FORCE_W || step.w}px → ${mb.toFixed(1)}MB 超预算，降一档`);
  }

  fs.rmSync(tmp, { recursive: true, force: true });

  console.log(`${path.basename(outGif)}  ${mb.toFixed(1)} MB  ` +
    `${used.secs}s @ ${used.fps}fps · ${used.colors} 色 · ${FORCE_W || used.w}px 宽`);
  if (mb > MAX_MB) {
    console.log(`  ⚠ 梯子走到底仍超 ${MAX_MB}MB —— 这一版的动图面积太大，` +
                `要么把 slot 做小，要么这张改静图`);
  }
})().catch(e => { console.error(e.message); process.exit(1); });
