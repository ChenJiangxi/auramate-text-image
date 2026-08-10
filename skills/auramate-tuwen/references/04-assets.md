# 04 · 素材地图

**做图前先查这里复用，别重造。** 用户讨厌重复劳动和文件冗余。

## 取素材的优先级（从上往下试）

### 1. 现成高清手机图 ★ 最优
```
~/ops-bilibili/projects/auramate-*/assets/shots/*.png     1080×1920 手机竖图
```
按功能分目录，例如 `auramate-shizhu`（反推时柱）、`auramate-life-kline`（人生 K 线）。

### 2. 4K 功能全套图
```
~/ops-bilibili/projects/auramate-bilibili/v3-plugins/clips/assets-net/pg-*.png
```
3840×2160，每个功能一张。命名 `pg-{分类}-{功能}.png`（`pg-choice-*` / `pg-destiny-*` / `pg-fortune-*` / `pg-relation-*`）。裁 4K 原图能保清晰。

### 3. 跨 agent 共享原料库
```
~/HermitAgents/auramate-shared/
  lingti-orbs/          15 张本命灵体光球原图 ★ 灵体首选
  shishen-mov/          10 段十神日光球录屏
  ui-screenshots/       10 张产品 UI 截图
  ui-recordings/        4 段产品录屏
  plugin-screenshots/   33 张 pg-*.png（注意：只是首屏）
  plugin-recordings/    22 段 plugin webm（首屏之外的内容在这）
  paper-figures/        12 张论文 / benchmark 图
  brand/                16 个 logo / 海报 / iPhone mockup
  concept-docs/         产品概念 / 定价 / 比赛数据（含 benchmark xlsx）
```

### 4. 录屏扒帧（次选，画质糊）
`plugin-screenshots/pg-*.png` 只是**首屏**。页面往下滚的内容要去同名录屏扒：

```bash
# 扒最深滚动帧（末 3 秒 6fps，取编号最大的）
ffmpeg -sseof -3 -i <f>.webm -vf fps=6 /tmp/end/e_%03d.png
# 通览滚动结构做 contact sheet
ffmpeg -i <f>.webm -vf "fps=1,scale=1400:-1" /tmp/frames/f_%03d.png
```
注意录屏可能没滚到底。扒不全就走第 5 条。

### 5. 本机高清截产品页
metamate 在 `/Users/macmini003/Code/metamate`，dev server `localhost:3000`。详细配方 → `05-toolchain.md`。

### 6. 让用户发
截不到就直接说，别硬造。用户提供的真原图**直接用，不要再加工**（不 iframe、不加注释列、不切边）—— 2026-05-10 用户原话：「用原图不需要再加工了」。

### 7. codex-image 生插画
只用于**氛围插画 / 概念配图**，绝不用来生成产品 UI 或灵体。→ `05-toolchain.md`

---

## 灵体素材（最高优先级规则）

灵体 = 产品 identity，是用户认出这个品牌的关键视觉。

- **必须**用产品里真跑出来的粒子云截图
- 首选 `~/HermitAgents/auramate-shared/lingti-orbs/`（15 张原图）
- 其次从各项目的录屏 / cover 抽帧
- 找不到就让用户提供
- **绝不 fake**：不用 CSS radial-gradient、不用 emoji、不用任何 mockup

这条比「AI 科技向」还紧。视觉再炫，不是真的就是错的。

---

## benchmark 数据 / 对比图

**成品直接用**：
```
~/ops-auramate/assets/charts/灵伴-benchmark-vs大模型-人类专家.png
```

**要改数据 / 加模型 → 重建管线**：
```
~/ops-auramate/assets/_chart-build/
  build_chart.py     bars 列表 = 数据源，改这里
  chart.html         生成产物
  render.js          node 跑 Playwright 2x → chart_2x.png 3200×1640
  logos/             deepseek / gemini / openai svg + lingbeon-orb.png（灵伴橙球）
```

### ⚠️ 数据诚实红线

核心结论「灵伴 37.5% 超过所有通用大模型、逼近人类冠军 42.5%」**只在竞赛 xlsx 那 5 个模型里成立**（deepseek-chat-v3 / deepseek-r1 / gemini-2.5-flash / gemini-3-pro / gpt-5.1-chat）。

我们自己更新的 live benchmark 里 **Gemini-3.1-Pro 40.3%、Claude-Opus-4.6 39.8% 已经反超灵伴**，而且那张榜没有 ours 列。

所以：
- 做「灵伴碾压大模型」的对比图，**只能用竞赛 xlsx 的 5 模型数据**，别混 live 榜
- 想加 Claude / Grok / Kimi / 豆包 **必须先补测**，不能臆造
- 人类专家口径要对齐年份（2021 无人类成绩，四届宏平均口径下灵伴是 37.1%）

宁可 story 弱一点，不能编数据。

原始数据：`~/HermitAgents/auramate-shared/concept-docs/mingli-competition-results.xlsx`

---

## 裁图铁律

- 热力图 / 地图 / 宽报告：**裁紧到内容边缘**，去掉黑边 void
- portrait 手机图：`height:100%` 居中
- landscape / 近方图：`width:100%` 或 `max-w/max-h:100%`
- app 内容常只占录屏左 ~40%，裁内容栏
- **宁可不放，也别放截断的半张**

裁图工具见 `05-toolchain.md`（本机默认 python3 坏了，用 `/usr/bin/python3` 或 `sips`）。
