#!/usr/bin/env bash
# 把这个仓库的 skill 装到 ~/.claude/skills/（软链，改仓库即生效）
#
#   ./install.sh              装 skill + 检查依赖
#   ./install.sh --copy       用复制代替软链
#   ./install.sh --uninstall  卸载

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="link"

case "${1:-}" in
  --copy)      MODE="copy" ;;
  --uninstall) MODE="uninstall" ;;
  "")          ;;
  *)           echo "未知参数: $1"; exit 2 ;;
esac

mkdir -p "$DEST"

for d in "$REPO"/skills/*/; do
  name="$(basename "$d")"
  target="$DEST/$name"

  if [ "$MODE" = "uninstall" ]; then
    if [ -L "$target" ] || [ -d "$target" ]; then
      rm -rf "$target"; echo "卸载 $name"
    fi
    continue
  fi

  [ -e "$target" ] && rm -rf "$target"
  if [ "$MODE" = "copy" ]; then
    cp -R "$d" "$target"; echo "复制 $name"
  else
    ln -s "${d%/}" "$target"; echo "软链 $name"
  fi
done

[ "$MODE" = "uninstall" ] && { echo "卸载完成"; exit 0; }

chmod +x "$REPO"/tools/*.sh 2>/dev/null || true

echo
echo "装好了 → $DEST"
echo

# ── 依赖检查 ──
echo "依赖检查："

if node -e "require('playwright')" 2>/dev/null \
  || node -e "require('/Users/macmini003/ops-auramate/node_modules/playwright')" 2>/dev/null; then
  echo "  ✓ playwright"
else
  echo "  ✗ playwright —— 出图要用。装: npm i playwright && npx playwright install chromium"
fi

if /usr/bin/python3 -c "from PIL import Image" 2>/dev/null; then
  echo "  ✓ /usr/bin/python3 + PIL（裁图用这个，别用 brew 的 python3）"
else
  echo "  ⚠ /usr/bin/python3 没有 PIL —— 裁图改用 sips"
fi

command -v codex >/dev/null 2>&1 \
  && echo "  ✓ codex（AI 插画）" \
  || echo "  ⚠ 没有 codex —— 生插画的路径不可用，配图改用产品截图"

echo
echo "起手：在会话里说「做一篇 AuraMate 小红书图文」"
echo "或直接 Read $REPO/skills/auramate-tuwen/SKILL.md"
