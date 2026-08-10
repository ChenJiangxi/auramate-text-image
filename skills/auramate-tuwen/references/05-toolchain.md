# 05 · 工具链

## 一、HTML → PNG（主力路径）

写 `slide-N.html`，跑 `render.js`，出 `slide-N.png`。

```bash
cp templates/render.js posts/post-{slug}/render.js
cd posts/post-{slug} && node render.js
```

`render.js` 会渲染目录下所有 `.html`，输出同名 `.png`，1242×1660，等字体和图片都加载完才截。

**依赖**：`playwright`。装在 `~/ops-auramate/node_modules/playwright`，`render.js` 里是绝对路径引用 —— 换机器要改这一行，或在仓库根 `npm i playwright && npx playwright install chromium`。

**字体**：模板用 Google Fonts `@import`。**需要联网**。断网时会 fallback 到系统字体，中文会变样 —— 渲染完一定肉眼看一眼 PNG，别盲发。本机可靠 fallback：`'PingFang SC'`。

### 为什么是 HTML 而不是设计工具

- 文字精确、排版可控、品牌色一致
- 全自主，不依赖人工操作
- 改一版只要改 CSS 重跑
- 缺点：纯插画做不出来 → 那部分交给 codex-image

---

## 二、codex-image（AI 插画）

只用于**氛围插画 / 概念配图**（封面下半那张图）。不用来生产品 UI。

skill 在 `~/.claude/skills/codex-image`。前提：`codex login status` = Logged in via ChatGPT；`codex features list | grep image_generation` = stable true。

> ⚠️ **2026-08-10 实测本机 codex 已不可用**：登录状态正常、`image_generation` 也显示 stable，
> 但实际调用返回 `The 'gpt-5.6-sol' model requires a newer version of Codex`，
> 指定 `-m gpt-5.1` 也拿不到 session。**要生插画得先升级 codex CLI。**
> 在那之前，封面配图改用真实产品视觉（见 `04-assets.md` 取素材优先级）。

```bash
SKILL=/Users/macmini003/.claude/skills/codex-image
TMP=$(mktemp -d /tmp/codex-image-XXXXXX); RAW="$TMP/raw.png"
codex exec --sandbox workspace-write --skip-git-repo-check --color never \
  --add-dir /Users/macmini003/.codex/generated_images -C "$TMP" \
  - <<'PROMPT' 2>&1 | tee "$TMP/stdout.log" | tail -8
Use the image_gen tool exactly once to generate a single image for the description below. Do not write files, run shell, write code, or report paths — just generate.

Description:
<英文 prompt。写实 / 编辑风。结尾一定加 "No text, no letters, no words.">
PROMPT
SID=$(grep -oE 'session id: [0-9a-f-]+' "$TMP/stdout.log" | awk '{print $3}' | tail -1)
python3 "$SKILL/scripts/extract_imagegen.py" "$SID" "$RAW"
cp "$RAW" assets/illustration.png
# 用完关会话（用户要求 + 清 ~1.5MB jsonl）
SESS=$(find ~/.codex/sessions -name "rollout-*${SID}*.jsonl" | head -1); [ -n "$SESS" ] && rm -f "$SESS"; rm -rf "$TMP"
```

**坑**：
- 别加 `--ephemeral`（jsonl 要留着抽图，抽完自己删）
- `--add-dir generated_images` 少了会 silent 失败
- codex 回复里说的路径是幻觉，**只信 `extract_imagegen.py` 写出的文件**
- prompt 里必须写 no text —— AI 生中文字必翻车
- stderr 的 `rmcp ... AuthorizationRequired` 是无关 MCP 噪音，忽略
- 要风格一致可以 `-i /abs/ref.png` 传参考图
- **出完关会话**（用户明确要求）

插画风格约定：暖色调、编辑感、无字、抽象或背影人物，跟渐变模板的淡紫暖橘对得上。

---

## 三、本机高清截产品页

metamate `/Users/macmini003/Code/metamate`，dev server 常在 `:3000`。查是否在跑：
```bash
lsof -iTCP -sTCP:LISTEN -P | grep :3000
```

**清晰的关键 = `deviceScaleFactor: 2`**（viewport 1920×1080 → 截出 3840×2160）。

配方（Playwright）：
1. `newContext({ viewport:{width:1920,height:1080}, deviceScaleFactor:2, locale:'zh-CN' })`
2. 登录：goto `/login` → 点「密码登录」tab → 点 `button[type=submit]`（dev 自动填 13111111111）→ 等 URL 到 `/app`
3. 功能路由 `/play/[id]`，id 见 `00-brand.md` 功能表
4. `page.screenshot({ fullPage: true })`

**卡点**：像 `fortune-2026` 这种要「开始生成」的功能，dev 账号没生成过就是起始页；现场生成要积分 + 跑 LLM + 出来是新数据（跟旧报告对不上）。要**现成报告的高清**，就登已经生成过那份报告的账号。

参考脚本：`ops-bilibili/projects/auramate-bilibili/v3-plugins/clips/scripts/explore-metamate.js`

---

## 四、图像处理（本机踩过的坑）

### ⚠️ 默认 python3 是坏的

`/opt/homebrew/bin/python3`（Homebrew 3.14）没装 Pillow，且 `pyexpat` 链接的 libexpat 符号对不上 —— `from PIL import Image` 和 `import xml.etree` **都会崩**。`pip3 install` 也会触发同样的报错，**别用**。

**改用**：

```bash
# 系统 python 3.9.6，PIL + xml 都正常
/usr/bin/python3 -c "from PIL import Image; im=Image.open('a.png'); im.crop((0,0,800,600)).save('b.png')"

# 或 macOS 原生 sips（无需 python）
sips -g pixelWidth -g pixelHeight f.png      # 取尺寸
sips -Z 1600 in.png --out out.png            # 等比缩到长边 1600
sips -c 900 700 in.png --out out.png         # 居中裁剪 高 宽
```

解析 xlsx：正则啃 `zipfile.read()` 出来的 XML（sharedStrings + sheetN），别用 openpyxl。

渲染只用 node，不碰坏掉的 python。

### ⚠️ 图片安全（会 wedge 整个会话）

长边 > 2000px 的图片直接 `Read` 会让会话之后所有 API 调用返回 400，直到 `/compact` 或重启。

**Read 任何图片前先跑**：
```bash
~/ops-auramate/scripts/safe-image.sh <path>
```
它会生成缩过的 sidecar。**如果 `safe-image.sh` 非零退出，停手，不要 fallback 去 Read 原图。**

（`ops-auramate` 里有 PreToolUse hook 自动挡；在别的目录没有这层保护，手动跑。）

---

## 五、违禁词扫描

```bash
tools/redline-scan.sh posts/post-{slug}/          # 扫目录下所有 html/md
tools/redline-scan.sh content.md slide-1.html     # 或指定文件
```

命中即 exit 1 并打印命中的词和行号。**发布前必跑。**

图片里的字扫不到 —— 那部分靠人眼 + `01-redline.md` 的 checklist。

---

## 六、起一个新 post

```bash
tools/new-post.sh digu-kline editorial-gradient 6
# → posts/post-digu-kline/{content.md, render.js, slide-1..6.html, assets/}
```
