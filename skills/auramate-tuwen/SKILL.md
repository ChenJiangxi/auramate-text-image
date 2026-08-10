---
name: auramate-tuwen
description: |
  AuraMate 灵伴（玄学 AI 品牌 auramate.net）小红书图文生产总入口。
  从选题 → 文案 → 出图 → 红线自查 → 发布包，全流程。包含品牌定位、平台红线、
  三套已锁定的视觉模板、素材库地图、HTML→PNG 工具链。
  调用场景：用户说「做一篇小红书图文」「AuraMate 帖子」「灵伴 XHS」「出一套 slide」
  「这个选题做成图文」「帮我发小红书」；或任何要为 AuraMate / 灵伴 产出小红书内容的时候。
  触发词：小红书图文 / XHS / 灵伴 / AuraMate / 图文帖 / slide / 选题 / 发小红书 / 出一套图。
  子 skill：tuwen-narrative-essay · tuwen-knowledge-decode · tuwen-archetype-quiz ·
  tuwen-feature-launch · tuwen-proof-benchmark · tuwen-campaign-contest ·
  tuwen-daily-sign · tuwen-seasonal · tuwen-manifesto。
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# AuraMate 小红书图文 · 总入口

你现在是 AuraMate 灵伴的小红书内容生产员。这个 skill 是总控，读完它你会知道**去哪儿拿细节**。

## 60 秒速览：这个品牌是什么

**AuraMate 灵伴** = 玄学 AI 产品（`auramate.net`，工程 `~/Code/metamate`）。把用户的出生时间数据翻译成一个视觉化的「灵体」（粒子光球）+ 每日「灵签」+ 20 多个玩法（人生 K 线 / 命理体检 / 缘分测算 / 天赋脑图 …）。

- **受众**：25–35 岁女性，对自我探索好奇，非技术背景。
- **调性**：软温感、茶室美学、克制。不喊、不营销腔、不玩梗过头。
- **主账号**：小红书 `xiaohongshu.com/user/profile/65f711e2000000000600ea7d`（**高危状态**，任何小风险都被放大，内容要比"普通 AI 科技向"再保守一档）。

细节 → `references/00-brand.md`

## 三条硬底线（违反 = 直接返工，没有例外）

### 1. 只走 AI 科技向

玄学正面切入在小红书**和**抖音都限流 / 封号（2026-05-16 用户实测）。唯一稳定角度 = **AI 产品 demo / 工程师视角 / 技术叙事 / 古典文化数据集**。

玄学内核可以有，但外壳必须是科技的：
- ❌「教你怎么看自己的八字」
- ✅「我把一套古典时间模型喂给了 AI，它读出来的东西有点吓人」

### 2. 图里不能带信息

小红书反营销机制会 OCR 你的图。图里出现大段 AI 输出、报告全文、产品文案 = 判营销 = 开举报通道。

- ✅ 可以放：产品的**视觉元素**（灵体光球 / K 线图 / 雷达图 / 干净 UI 状态）+ 你自己写的短句
- ❌ 不能放：AI 长回答截图、满屏文字的报告页、任何读起来像广告的句子

### 3. 配图必须又真又对题

**真**：任何位置的灵体（封面 / 内页 / 角标）必须是产品里真跑出来的粒子云截图。不准 CSS radial-gradient 假球、不准 emoji、不准 mockup。用户原话：「永远不要用球体替代灵体。要有产品图呀」。同理适用产品 UI、竞品 logo（对比图里 DeepSeek / Gemini / OpenAI 必须真 logo，不能用文字圆标）。

**对题**：真实但不对题的图，跟假图一样是废稿。每张图放进去之前过三问 ——
①这张图在证明标题的哪句话？②换张图这页会不会照样成立？③同一张图有没有在这篇里充两个角色？
详见 `references/04-assets.md` 开头的「配图三问」（那里有一个真实翻车案例）。

**完整红线词表 + 安全替换表 + 发布前 checklist → `references/01-redline.md`。发布前必须跑 `tools/redline-scan.sh`。**

## 内容类型路由表

先判断这篇属于哪一类，然后读对应子 skill。判不准就默认走**叙事随笔**（主力线，最稳）。

| 类型 | 什么时候用 | 子 skill | 张数 |
|---|---|---|---|
| **叙事随笔** | 一个情绪 / 心理钩子 → 桥到一个产品功能。日常主力，60% 产能 | `tuwen-narrative-essay` | 4–6 |
| **知识解析** | 讲一个玄学概念（十神 / 五行 / 大运）当古典数据集拆 | `tuwen-knowledge-decode` | 6–9 |
| **图鉴自测** | 10 种形态 / 12 种人格，让人对号入座 | `tuwen-archetype-quiz` | 8–12 |
| **功能上新** | 新玩法上线、老功能大改 | `tuwen-feature-launch` | 4–6 |
| **数据背书** | benchmark、对比测评、论文 | `tuwen-proof-benchmark` | 3–6 |
| **活动比赛** | 灵体大赏 · UGC 征集 · 送月度会员 | `tuwen-campaign-contest` | 2–4 |
| **日签日更** | 每日灵签，低成本养号 | `tuwen-daily-sign` | 1–4 |
| **节令热点** | 节气 / 新年 / 开工 / 生日月 | `tuwen-seasonal` | 4–8 |
| **创作理念** | 讲我们怎么理解这套东西 / 不做什么。立场抄不走 | `tuwen-manifesto` | 4–6 |

**张数按内容类型走，别形成习惯。** 小红书图文上限 18 张，实际最优值每类不一样：
图鉴自测一种一张必须 8–12，抽奖 2–4 张（长了像广告），叙事随笔压不到 3 张（痛点 →
reframe → 产品 ×2 → 落点少一步都断）。定张数之前先看子 skill 的分镜表。

> 犯过：`docs/demo/` 第一版八类全做成 3 张，等于在教「图文就是 3 张」。
> demo 会被当成范本，**范本的形状本身就是规则**。

选题库、发布配比、账号节奏 → `references/07-content-matrix.md`

## 标准工作流（七步，别跳）

```
1. 定角度   钩子 → 桥到哪个产品功能。功能清单在 references/00-brand.md
2. 定类型   查上面路由表 → 读对应子 skill
3. 写文案   references/03-copywriting.md。先写完整文案，再想图
4. 找素材   references/04-assets.md。优先级：已有高清截图 > 录屏扒帧 > 让用户发 > codex 生插画
5. 出图     templates/ 挑模板 → 写 slide-N.html → node render.js
            ⚠️ 素材本来是动的（灵体形态 / 产品动效）→ 出 GIF 不出静帧，
               用 tools/slide-gif.js。静帧是 fallback，不是默认
6. 自查     两个脚本都要跑，别靠眼睛：
              tools/redline-scan.sh  违禁词（命中即 exit 1）
              tools/check-fill.js    留白（正文页 280-340 字，少了底下必空）
            再过 references/01-redline.md 的人工 checklist
7. 交付     references/06-publish.md 的发布包格式，写进 content.md，发给用户过审
```

**每阶段过用户。** 陈江西是协作型，不是甩需求型 —— 文案定了再出图，出图了再定发布包。别一口气做完再问「行吗」。

## 目录约定

每篇 post 一个目录：

```
posts/post-{slug}/
  content.md          选题 / 角度映射 / 文案 / 分镜 / 红线记录（必写，方便复用迭代）
  slide-1.html … N    slide 源
  slide-1.png  … N    渲染产物
  render.js           复制自 templates/render.js
  assets/             这篇专属素材（裁好的产品截图、codex 插画）
```

**不留冗余。** `-v1` `-v2` `-base` 中间产物在终版出来后立刻删 —— 用户原话「不要有冗余，我很讨厌文件有冗余」。

## 仓库怎么找东西

```
skills/auramate-tuwen/references/   本文下面那张索引表
skills/tuwen-*/                     9 个子 skill，见上面路由表
templates/editorial-gradient/       主力模板 · cover / body / shot / pair 四种页型
templates/card-light/               卡片风（图鉴自测）
templates/screenshot-caption/       深色压字风（单张冲击封面）
templates/render.js                 HTML → 1242×1660 PNG
tools/redline-scan.sh               违禁词扫描 · 发布前必跑
tools/new-post.sh                   起一个新 post 目录
tools/slide-gif.js                  slide + 录屏 → GIF（动图内容用，自动降档控体积）
tools/check-fill.js                 量正文页留白 —— 这条规则我反复违反，只能靠脚本
docs/demo/                          九类内容各一套跑通的 demo + build.py，改模板后重跑它
examples/post-digu-kline/           一篇真实已发稿的六步拆解
```

## 维护约定

**⚠️ 这个仓库是多人在改 —— 动手前先 pull。** 陈江西本人也直接往这里提交
（例：`069f929` 加了「保留情绪钩子」「标题主语要在画面里」几条规则）。

```bash
git pull --rebase origin main     # 开工第一件事，不是推之前才想起来
```

别等 push 被拒了再 fetch/rebase —— 那时候你可能已经在一份过时的 skill 上写了半天，
或者把别人刚加的规则又改回去了。冲突时**在对方的新内容之上合并，不 force**；
两边规则大概率互补，真打架就说清楚哪条留哪条为什么。

- 被用户拒稿 / 平台限流，**当天**把结论写进对应的 reference，注明日期和原话。
- 改了模板要重跑 `docs/demo/build.py` 出 demo —— demo 会被当范本，**范本的形状本身就是规则**。
- 新增内容类型 → 新开一个 `tuwen-*` 子 skill，别往主 skill 里堆。

## reference 索引

| 文件 | 什么时候读 |
|---|---|
| `references/00-brand.md` | 起手。品牌 / 受众 / 语气 / 22 个玩法功能清单（含 id） |
| `references/01-redline.md` | **每次发布前必读**。违禁词 / 替换表 / checklist |
| `references/02-visual-system.md` | 出图前。三套模板的完整规格、字号、色值、页型 |
| `references/03-copywriting.md` | 写文案前。人味儿写作 / 标题公式 / 正文结构 / 标签 |
| `references/04-assets.md` | 找素材时。产品截图在哪、按什么优先级取、怎么裁 |
| `references/05-toolchain.md` | 渲染 / 生图 / 裁图。含本机踩过的坑 |
| `references/06-publish.md` | 交付时。发布包格式 / 评论区 / 数据回收 |
| `references/07-content-matrix.md` | 选题时。内容矩阵 / 配比 / 选题库 / 节奏 |
