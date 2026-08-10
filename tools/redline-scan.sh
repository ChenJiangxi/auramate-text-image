#!/usr/bin/env bash
# 小红书违禁词扫描 —— 发布前必跑
#
#   tools/redline-scan.sh posts/post-xxx/        扫目录下所有 html/md/txt/json
#   tools/redline-scan.sh content.md slide-1.html
#
# 命中即 exit 1 并打印词 + 文件 + 行号。
# 注意：扫不到图片里的字。图内文字靠人眼 + 01-redline.md 的 checklist。

set -uo pipefail

# 高危词 —— 命中即 fail
BANNED=(
  # 命理类
  八字 命理 算命 命格 命主 紫微 紫薇斗数 排盘 看相 面相 手相 盲派 因果 业力
  伤官 月柱
  # 效果承诺类
  改运 转运 招财 旺夫 化解 破解 灵验 准爆 必准 包灵验
  # 身份类
  大师 师傅 神婆 仙人指路
  # 平台/元词
  迷信 抖音 快手
  # 引导类
  评论区扣 评论区告诉我 私信我 加我V 加我 V 主页置顶 找我看
  # 夸大类
  "100%准" 全球首个 重磅
)

# 灰区词 —— 只警告，不 fail（语境决定安全性）
GRAY=( 测 缘分 贵人 灵签 十神 时柱 五行 大运 流年 运势 风水 玄学 )

RED='\033[0;31m'; YEL='\033[0;33m'; GRN='\033[0;32m'; NC='\033[0m'

if [ $# -eq 0 ]; then
  echo "用法: $0 <文件或目录> [更多...]"
  exit 2
fi

# 收集要扫的文件
FILES=()
for target in "$@"; do
  if [ -d "$target" ]; then
    while IFS= read -r f; do FILES+=("$f"); done < <(
      find "$target" -maxdepth 3 -type f \( -name '*.md' -o -name '*.html' -o -name '*.txt' -o -name '*.json' \) 2>/dev/null
    )
  elif [ -f "$target" ]; then
    FILES+=("$target")
  else
    echo "跳过（不存在）: $target"
  fi
done

if [ ${#FILES[@]} -eq 0 ]; then
  echo "没有可扫的文件"
  exit 2
fi

echo "扫描 ${#FILES[@]} 个文件…"
echo

HITS=0
for word in "${BANNED[@]}"; do
  out=$(grep -n -F "$word" "${FILES[@]}" 2>/dev/null || true)
  if [ -n "$out" ]; then
    HITS=$((HITS+1))
    echo -e "${RED}✗ 违禁词「${word}」${NC}"
    echo "$out" | sed 's/^/    /'
    echo
  fi
done

WARN=0
for word in "${GRAY[@]}"; do
  out=$(grep -n -F "$word" "${FILES[@]}" 2>/dev/null || true)
  if [ -n "$out" ]; then
    WARN=$((WARN+1))
    echo -e "${YEL}⚠ 灰区词「${word}」—— 看语境判断${NC}"
    echo "$out" | head -5 | sed 's/^/    /'
    echo
  fi
done

echo "────────────────────────────"
if [ $HITS -gt 0 ]; then
  echo -e "${RED}命中 ${HITS} 个违禁词 —— 不能发。替换表见 references/01-redline.md${NC}"
  exit 1
fi

if [ $WARN -gt 0 ]; then
  echo -e "${YEL}${WARN} 个灰区词，人工确认语境${NC}"
fi
echo -e "${GRN}✓ 文字部分通过${NC}"
echo
echo "还没查的（脚本查不了，人工过）："
echo "  □ 图片里的字（含产品截图里露出的词）"
echo "  □ 灵体是真截图不是渐变球"
echo "  □ 截图完整、铺满、无大片留白"
echo "  □ kicker/foot 不是「真实产品截图」这类自我标注"
echo "  □ 不预测疾病 / 死亡 / 灾祸"
exit 0
