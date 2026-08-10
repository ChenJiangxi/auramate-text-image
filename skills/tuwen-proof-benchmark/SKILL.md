---
name: tuwen-proof-benchmark
description: |
  AuraMate 小红书图文 · 数据背书 / 对比测评型。benchmark 图、灵伴 vs 通用大模型、
  论文、RAG 技术叙事。把「又一个算命 app」和「认真做的 AI 产品」分开的唯一武器。
  调用场景：用户说「做一张对比图」「benchmark」「跟其他模型比」「讲讲技术」「论文那个」。
  触发词：benchmark / 对比图 / 测评 / 数据 / 论文 / 准确率 / RAG / 技术向 / vs 大模型。
  ⚠️ 含数据诚实红线：核心结论只在特定数据集里成立，不能混榜、不能臆造模型。
  前置：先读 auramate-tuwen 的 SKILL.md 和 references/04-assets.md。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# 数据背书 · 唯一能证明「我们不一样」的东西

C 端玄学赛道全是玄学话术，你们有别人没有的：一篇论文、一个 benchmark、一组真实测出来的数字。

**一个月一篇。** 少了不够建立认知，多了太硬没人看。

## ⚠️ 数据诚实红线（最重要，先读这段）

核心叙事「灵伴 37.5%，超过所有通用大模型（最强 DeepSeek-V3 35.7%），逼近人类冠军 42.5%」

**这个结论只在竞赛 xlsx 那 5 个模型里成立**：deepseek-chat-v3 / deepseek-r1 / gemini-2.5-flash / gemini-3-pro / gpt-5.1-chat。

**我们自己更新的 live benchmark 里，Gemini-3.1-Pro 40.3%、Claude-Opus-4.6 39.8% 已经反超灵伴**，而且那张榜没有 ours 列。

所以：

- 做「灵伴碾压大模型」的对比图，**只能用竞赛 xlsx 的 5 模型数据**，别混 live 榜
- 想加 Claude / Grok / Kimi / 豆包 **必须先补测**。用户问过「claude 呢」—— 正确回答是「本地竞赛数据没测 Claude，Claude 只存在于 live 榜且反超了我们，要显示 Claude 又让灵伴在上，现有数据做不到」，然后给两条路（补测 / 换口径），**不是**编一个数
- 口径要对齐年份：2021 年没有人类成绩，四届（2022–2025）宏平均口径下灵伴是 **37.1%** 不是 37.5%

**宁可 story 弱一点，不能编数据。** 这条没有商量余地 —— 一旦被人扒出来，整个"认真做产品"的人设就没了。

## 现成资产

**成品图直接用**：
```
~/ops-auramate/assets/charts/灵伴-benchmark-vs大模型-人类专家.png
```

**要改数据 / 加模型 → 重建管线**：
```
~/ops-auramate/assets/_chart-build/
  build_chart.py    ← bars 列表就是数据，改这里
  chart.html        ← 生成产物
  render.js         ← node 跑 Playwright 2x → chart_2x.png 3200×1640
  logos/            ← deepseek.svg / gemini.svg / openai.svg / lingbeon-orb.png
```
```bash
cd ~/ops-auramate/assets/_chart-build
# 编辑 build_chart.py 的 bars
python3 build_chart.py && node render.js
sips -Z 1600 chart_2x.png --out ../charts/xxx.png
```
渲染只用 node，不碰坏掉的 python（见 `auramate-tuwen/references/05-toolchain.md`）。

**原始数据**：`~/HermitAgents/auramate-shared/concept-docs/mingli-competition-results.xlsx`
**论文**：`~/HermitAgents/auramate-shared/reference-pdfs/auramate-paper-published.pdf`

## 竞品 logo 必须是真的

对比图里 DeepSeek / Gemini / OpenAI **必须用官方矢量 logo**，不能用「DS」「G」「GPT」文字圆标。

用户 2026-06-16 原话：「其他模型的照片不要敷衍，要真实的logo」。文字占位徽标显得糊弄，直接削弱整张图的可信度。

矢量源在 `_chart-build/logos/`：
- DeepSeek 官方品牌蓝 `#4D6BFE` 鲸鱼标
- Gemini 蓝→紫→粉渐变星芒
- OpenAI 黑色花结（simple-icons 已下架，path 内联在 `openai.svg`）
- 灵伴用 `lingbeon-orb.png`（橙球）

## 分镜（4 张标准版）

| # | 内容 |
|---|---|
| 1 | 封面：结论先行。「我们做了个测试，结果有点意外」 |
| 2 | **图表**（占满整张）。这是全篇核心 |
| 3 | 方法：怎么测的、题从哪来、为什么这么比。诚实说明局限 |
| 4 | 落点：这说明什么。不吹，落在「为什么专用模型能赢通用模型」 |

**单张版**：只发 benchmark 图 + 长正文。图够强的时候这样最好。

## 红线特别提醒

1. **「准确率」可以说，「准」不行。**「准确率 37.5%」是数据表述；「很准」「灵验」是效果承诺。
2. 图表里的题目样例 **不能露出八字 / 命理原文**。用「测试题」「样本」代称。
3. **不说「全球首个」「最强」**。说「在这组测试里排在前面」。
4. 论文可以提，但别放论文截图（满屏英文 = 图里带信息）。
5. 「人类专家」比「命理师」安全 —— 对外一律用「人类专家」。

## 技术叙事变体（没有新数据时）

不是每个月都有新 benchmark。技术向还能写：

- 我们的知识库里装了什么（五运六气 / 古籍 → 向量库，讲"古典数据集"）
- 为什么通用大模型答不好这类问题（上下文 / 专业语料）
- 一个 agent 怎么记住你（灵体校准闭环：用户反馈 → 调整自我认知）
- 我们怎么防止 AI 胡说（RAG / 引用 / 约束）

这类零红线，是账号被限流后用来洗白的最佳内容。
