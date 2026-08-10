# 04 · 素材地图

**做图前先查这里复用，别重造。** 用户讨厌重复劳动和文件冗余。

---

## 配图三问 —— 每张图放进去之前都要过

「素材是真的」只是及格线，不是终点。真实但**不对题**的图，跟假图一样是废稿。

```
问 1  这张图在证明标题说的哪句话？
      答不上来 → 换图，或者换标题。不要放"反正挺好看的"。

问 2  换成另一张图，这一页会不会照样成立？
      会 → 说明这张图没在干活，是装饰。找一张只有它能干的。

问 3  同一张图有没有在这篇里出现第二次、还充着不同的角色？
      有 → 至少有一处是错的。一张图只能证明一件事。
      跨帖也算：两篇不同的帖复用同一条素材，读者会觉得你在糊弄。

问 4  这是「信息图」还是「氛围图」？
      信息图（图表 / 产品截图 / 数据）= 不可裁。裁掉一块就是残的。
      氛围图（插画 / 光球 / 质感图）= 可裁，怎么好看怎么来。
      放进封面横带时：信息图用 object-fit:contain + 配底色；氛围图才用 cover。
```

**真实翻车案例（2026-08-10，就在这个仓库里）**：做十神解析 demo，封面和「顿悟日」那页用了同一张通用光球。
问题不是图假——图是真产品截图；问题是**封面那张不可能同时代表十种形态，又代表其中一种**。
而且素材库里 `shishen-mov/` 有十段一形态一段的录屏，扒帧就有对应形态图，我没去用。

修法：封面换成五个形态拼的横带（呼应「五对/十种」），单个形态页换成那个形态**自己**的帧，
成对讲的时候左右各用各的（`templates/editorial-gradient/pair.html`）。

**懒是这里最大的失败源**：手边有什么就用什么，而不是先问这一页需要展示什么。

**第二次翻车（2026-08-10 同日）**：benchmark 对比图和天赋雷达按 `object-fit:cover` 放进封面
横带，柱子标签和雷达顶点数字都被切掉了，用户一眼看出「插图被截得不完整」。
同一批里 `pentagon` 还在抽奖和节令两篇里各用了一次 —— 问 3 白写了。
**规则写下来不等于会执行，出图后必须逐张肉眼过一遍。**

---

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
  shishen-mov/          10 段形态录屏（hezuo/fenxiang/meishi/fafeng/gaoqian/
                        jianlou/juanwang/yali/xuexi/dunwu 各一段）★ 讲形态必用
                        扒帧：ffmpeg -ss 2 -i <f>.mov -frames:v 1 out.png
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

### 陪伴类功能：灵体放封面，UI 放内页

当标题的情绪主体是「灵伴 AI」—— 例如对话、陪伴、回忆、收藏、长期记录 —— 素材不要只按
“这个功能发生在哪个页面”来选，还要按每张 slide 的职责来选：

| 位置 | 首选素材 | 它要证明什么 |
|---|---|---|
| 封面 | 真实产品生成、构图好看的灵体 | 谁在陪伴我、谁说中了我；品牌和情绪 |
| 操作内页 | 真实 UI 截图 | 日期怎么选、收藏怎么筛、按钮在哪里 |
| 结果内页 | 真实成品 / 报告 / 导出文件截图 | 功能确实产出了什么 |

**“配产品图”不等于把 UI 弹窗塞到封面。** UI 有真实性，但未必有情绪；灵体有情绪和品牌辨识，
但不能代替功能证据。两者都要有，各自只干一件事。

封面灵体属于氛围图，可以 `object-fit:cover`；渲染后必须肉眼确认粒子主体没有被横带切没。
内页 UI / PDF 预览属于信息图，必须 `object-fit:contain`，关键按钮、日期、收藏状态和版面不可裁。

> **真实返工（2026-08-10）**：对话导出 PDF 帖，用户先说「配上产品图」，后又说
> 「配上好看的灵体」。正确解不是拿其中一句覆盖另一句，而是封面用真实灵体、内页用导出选择页 / 收藏筛选 /
> PDF 成品。最终标题提到「灵伴 AI」，封面画面也必须让这个主语出现。

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
