/**
 * HTML → PNG 渲染器
 *
 * 用法：把这个文件复制到 post 目录，然后 `node render.js`
 * 渲染目录下所有 .html → 同名 .png（1242×1660）
 *
 * 依赖 playwright。找不到就装：npm i playwright && npx playwright install chromium
 */
const path = require('path');
const fs = require('fs');

// playwright 解析顺序：本地 node_modules → ops-auramate → 全局
function loadPlaywright() {
  const candidates = [
    'playwright',
    path.join(__dirname, 'node_modules/playwright'),
    path.join(__dirname, '../node_modules/playwright'),
    path.join(__dirname, '../../node_modules/playwright'),
    '/Users/macmini003/ops-auramate/node_modules/playwright',
  ];
  for (const c of candidates) {
    try { return require(c); } catch (e) { /* next */ }
  }
  console.error('找不到 playwright。跑一下：npm i playwright && npx playwright install chromium');
  process.exit(1);
}

const { chromium } = loadPlaywright();

const DIR = __dirname;
const WIDTH = Number(process.env.SLIDE_W || 1242);
const HEIGHT = Number(process.env.SLIDE_H || 1660);

(async () => {
  const files = fs.readdirSync(DIR).filter(f => f.endsWith('.html')).sort();
  if (!files.length) { console.log('目录里没有 .html'); return; }

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  for (const f of files) {
    await page.setViewportSize({ width: WIDTH, height: HEIGHT });
    await page.goto(`file://${path.join(DIR, f)}`, { waitUntil: 'networkidle' });

    // 等字体加载（Google Fonts @import 需要联网；断网会 fallback 到系统字体）
    await page.evaluate(() => document.fonts.ready).catch(() => {});

    // 等所有图片加载完，否则截出来是空框
    await page.evaluate(() => Promise.all(
      Array.from(document.images).map(img =>
        img.complete ? null : new Promise(r => { img.onload = r; img.onerror = r; })
      )
    ));

    await page.waitForTimeout(1500);

    const out = path.join(DIR, f.replace('.html', '.png'));
    await page.screenshot({ path: out, fullPage: false });
    console.log('rendered', f, '→', path.basename(out));
  }

  await browser.close();
})().then(() => process.exit(0)).catch(e => { console.error(e); process.exit(1); });
