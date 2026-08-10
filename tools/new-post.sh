#!/usr/bin/env bash
# 起一个新 post 目录
#
#   tools/new-post.sh <slug> [template] [张数]
#   tools/new-post.sh digu-kline editorial-gradient 6
#
# template: editorial-gradient(默认) | card-light | screenshot-caption

set -euo pipefail

SLUG="${1:?用法: $0 <slug> [editorial-gradient|card-light|screenshot-caption] [张数]}"
TPL="${2:-editorial-gradient}"
N="${3:-6}"

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TPL_DIR="$REPO/templates/$TPL"
[ -d "$TPL_DIR" ] || { echo "没有这个模板: $TPL"; exit 1; }

OUT="${POSTS_DIR:-$PWD/posts}/post-$SLUG"
[ -e "$OUT" ] && { echo "已存在: $OUT"; exit 1; }

mkdir -p "$OUT/assets"
cp "$REPO/templates/render.js" "$OUT/render.js"

# slide-1 = 封面，其余按模板可用页型轮流铺
for i in $(seq 1 "$N"); do
  if [ "$i" -eq 1 ] && [ -f "$TPL_DIR/cover.html" ]; then
    cp "$TPL_DIR/cover.html" "$OUT/slide-$i.html"
  elif [ -f "$TPL_DIR/body.html" ]; then
    cp "$TPL_DIR/body.html" "$OUT/slide-$i.html"
  else
    cp "$TPL_DIR/cover.html" "$OUT/slide-$i.html"
  fi
done

cat > "$OUT/content.md" <<EOF
# post — {标题}（{功能中文名} / {feature-id}）

{第几篇 / 模板 / 用户怎么提的（引原话）/ 发出去没}

## 概念 / 角度映射
钩子来源：
映射到功能：（metamate \`{id}\`，{分类}）
逻辑桥：

## 素材
- 插画：\`assets/illustration.png\`（codex 生成，prompt 要点：…；session 已关）
- 产品截图：
  - \`{源路径}\` → \`assets/pf-chart.png\`（裁剪 {x,y,w,h}，选它因为…）
  - 备用：

## 文案
封面：
（slide-2 痛点）
（slide-3 reframe+功能）
（slide-N 落点）

## 分镜 · 视觉
${N} 张，模板 ${TPL}。1 封面 / 2 … / 3 …
正文 44px，portrait 截图 height:100% 居中。

## 红线
命中风险词：
扫描：redline-scan.sh 已过 / 图内文字已肉眼核

## 发布信息
标题：
正文：
标签：
EOF

echo "建好了: $OUT"
echo "  slide-1..$N.html  ($TPL)"
echo "  content.md  render.js  assets/"
echo
echo "下一步：写 content.md 的文案 → 填 slide html → cd $OUT && node render.js"
