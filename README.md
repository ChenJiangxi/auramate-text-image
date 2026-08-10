# auramate-text-image

AuraMate 灵伴（`auramate.net`）**小红书图文**生产手艺，打包成一组 Claude Code / Codex / OpenClaw 通用的 skill。

目标：**一个完全没有 context 的 agent，clone 这个仓库、装上 skill，就能独立选题 → 写文案 → 出图 → 过红线 → 交发布包**，产出质量和跑了半年的老 agent 一致。

这里的每一条规则都不是拍脑袋写的，是 2026-05 到 2026-07 之间在真账号上被拒稿、被限流、被用户打回来换出来的。

---

## 快速开始

```bash
git clone git@github.com:ChenJiangxi/auramate-text-image.git
cd auramate-text-image
./install.sh          # 软链到 ~/.claude/skills/，装 playwright
```

装完在会话里说「做一篇 AuraMate 小红书图文」，`auramate-tuwen` 会被触发，它会把你路由到对应的子 skill。

不想装也行 —— 直接让 agent `Read skills/auramate-tuwen/SKILL.md` 起手。

---

## 仓库结构

```
skills/
  auramate-tuwen/            主 skill · 总入口 · 铁律 · 路由表
    references/              品牌 / 红线 / 视觉系统 / 文案 / 素材 / 工具链 / 发布 / 选题矩阵
  tuwen-narrative-essay/     叙事随笔（主力线，60% 产能放这）
  tuwen-knowledge-decode/    知识解析（十神 / 五行 / 术语科普）
  tuwen-archetype-quiz/      图鉴 · 对号入座 · 自测
  tuwen-feature-launch/      功能上新 · 新玩法
  tuwen-proof-benchmark/     数据背书 · 对比测评
  tuwen-campaign-giveaway/   抽奖 · 活动
  tuwen-daily-sign/          日签日更 · 养号
  tuwen-user-story/          用户故事 · 口碑
  tuwen-seasonal/            节令 · 热点借势
templates/
  editorial-gradient/        ★ 定版模板（渐变编辑风）· 封面 / 正文 / 产品图 三种页型
  card-light/                浅底卡片结构风（数据 / 结构化内容）
  screenshot-caption/        深色压字风（单张冲击封面）
  render.js                  HTML → 1242×1660 PNG（Playwright）
tools/
  redline-scan.sh            违禁词扫描 · 发布前必跑 · 命中即 exit 1
  new-post.sh               起一个新 post 目录（模板 + render.js + content.md 骨架）
examples/
  post-digu-kline/           一篇完整 6 图帖的全过程拆解（真实已发稿）
```

---

## 三条不能破的底线

任何 agent 接手前先记这三条，其他都可以商量：

1. **只走 AI 科技向。** 玄学正面切入（算命 / 改运 / 风水 / 命理）在小红书和抖音都限流甚至封号。壳子必须是「AI 产品 / 工程师视角 / 古典文化数据集」。
2. **图里不能带信息。** 小红书图文里塞满 AI 输出文字、报告全文、营销话术 = 被判营销内容，开举报通道。图里只放视觉元素 + 你自己写的短句。
3. **灵体永远用产品真截图。** 不准 CSS 渐变球、不准 emoji、不准 mockup。这条比第 1 条还紧。

完整红线见 `skills/auramate-tuwen/references/01-redline.md`。

---

## 这套东西为谁写的

- 接手 AuraMate 小红书运营的任何 agent 或人
- 兄弟品牌（fatecouncil / mangpai）想复用这套图文方法论的
- 未来的我自己 —— 半年后忘了为什么某个字号是 44 而不是 46 时，回来查

---

## 维护约定

- 每次被用户拒稿 / 平台限流，**当天**把结论写进对应的 reference，注明日期和原话。
- 模板改了要同步改 `templates/` 里的样板文件，不要只在某一篇 post 里改。
- 新增内容类型 → 新开一个 `tuwen-*` 子 skill，别往主 skill 里堆。
