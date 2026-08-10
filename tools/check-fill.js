/**
 * 留白检查：渲染每张 slide，量正文块底部到容器底部的空隙。
 *
 *   node tools/check-fill.js <目录或 slide.html ...>
 *
 * 「每张写满字、别大片留白」是写在 skill 里的规则，但反复被违反 ——
 * 因为「满不满」靠肉眼估，一忙就放过去了。这个脚本把它变成一个数字。
 *
 * 量的是 .body（正文页，flex:1 撑满的那块）：
 *   容器底部 - 最后一个子元素底部 = 空隙
 * 空隙 > 阈值就报 —— 说明这一张字没写够，不是排版问题，是文案短了。
 *
 * 封面 / 纯图页不检查（它们的空间由图占，本来就没有正文块）。
 */
const path = require('path');
const fs = require('fs');

function loadPlaywright() {
  const c = ['playwright',
    path.join(__dirname, '../node_modules/playwright'),
    '/Users/macmini003/ops-auramate/node_modules/playwright'];
  for (const p of c) { try { return require(p); } catch (e) {} }
  console.error('找不到 playwright：npm i playwright && npx playwright install chromium');
  process.exit(1);
}
const { chromium } = loadPlaywright();

const GAP_LIMIT = Number(process.env.FILL_GAP_LIMIT || 110);  // px，约 1.3 行
const W = 1242, H = 1660;

const args = process.argv.slice(2);
if (!args.length) {
  console.error('用法: node tools/check-fill.js <目录或 slide.html ...>');
  process.exit(2);
}

const files = [];
for (const a of args) {
  if (fs.existsSync(a) && fs.statSync(a).isDirectory()) {
    for (const f of fs.readdirSync(a).filter(f => f.endsWith('.html')).sort()) {
      files.push(path.join(a, f));
    }
  } else if (fs.existsSync(a)) {
    files.push(a);
  }
}
if (!files.length) { console.error('没有可检查的 html'); process.exit(2); }

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: W, height: H });

  const bad = [];
  let checked = 0;

  for (const f of files) {
    await page.goto('file://' + path.resolve(f), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready).catch(() => {});
    await page.waitForTimeout(400);

    const r = await page.evaluate(() => {
      // 只量 .body —— 它是 flex:1 撑满的正文块，空隙才有意义。
      // .note 是横图产品页下方的解读段，高度由内容决定，量不出「留白」。
      const box = document.querySelector('.body');
      if (!box || !box.children.length) return null;
      const bb = box.getBoundingClientRect();
      const last = box.children[box.children.length - 1].getBoundingClientRect();
      const text = (box.innerText || '').replace(/\s/g, '');
      return { boxH: bb.height, gap: bb.bottom - last.bottom, chars: text.length };
    });
    if (!r) continue;                       // 封面 / 纯图页，跳过
    checked++;

    const fill = ((r.boxH - r.gap) / r.boxH * 100).toFixed(0);
    const name = path.basename(f);
    if (r.gap > GAP_LIMIT) {
      bad.push({ name, gap: Math.round(r.gap), fill, chars: r.chars });
      console.log(`✗ ${name.padEnd(24)} 填充 ${fill}%  底部空 ${Math.round(r.gap)}px  ${r.chars} 字`);
    } else {
      console.log(`✓ ${name.padEnd(24)} 填充 ${fill}%  ${r.chars} 字`);
    }
  }

  await browser.close();

  console.log('────────────────────────────');
  if (bad.length) {
    console.log(`${bad.length}/${checked} 张没写满（底部空隙 > ${GAP_LIMIT}px）`);
    console.log('修法：**加字，不是改排版**。正文页 44px/lh1.9，每行约 24 字、每行占 84px，');
    console.log('正文块可用高度约 1290px ≈ 15 行 ≈ 340 字。低于 260 字基本一定空。');
    process.exit(1);
  }
  console.log(`${checked} 张全部写满 ✓`);
})().catch(e => { console.error(e.message); process.exit(1); });
