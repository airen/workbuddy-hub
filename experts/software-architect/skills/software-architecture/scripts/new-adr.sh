#!/usr/bin/env bash
#
# new-adr.sh — 从模板脚手架一份新的 ADR
#
# 用法:
#   ./new-adr.sh "采用 Outbox 模式保证事件与写入的原子性"
#   ./new-adr.sh "订单服务按限界上下文拆分" ./docs/adr
#
# 行为:
#   1. 在目标目录（默认 ./docs/adr）中查找现有 ADR，自动确定下一个序号
#   2. 生成 NNNN-kebab-case-title.md，从 templates/adr.md 复制模板
#   3. 替换模板中的标题与日期占位
#
# 依赖: bash, sed, date（macOS/Linux 均可）

set -euo pipefail

TITLE="${1:-}"
OUT_DIR="${2:-./docs/adr}"

if [ -z "$TITLE" ]; then
  echo "用法: $0 \"<决策标题>\" [输出目录]" >&2
  echo "示例: $0 \"采用 Outbox 模式保证事件与写入的原子性\" ./docs/adr" >&2
  exit 1
fi

# 定位模板：优先同级 templates/adr.md，其次脚本上级的 templates/adr.md
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE=""
for candidate in \
  "$SCRIPT_DIR/adr.md" \
  "$SCRIPT_DIR/../templates/adr.md" \
  "$OUT_DIR/../templates/adr.md"
do
  if [ -f "$candidate" ]; then
    TEMPLATE="$candidate"
    break
  fi
done

mkdir -p "$OUT_DIR"

# 确定下一个序号
NEXT=1
if compgen -G "$OUT_DIR/[0-9][0-9][0-9][0-9]-*.md" > /dev/null; then
  LAST=$(ls "$OUT_DIR"/[0-9][0-9][0-9][0-9]-*.md 2>/dev/null | sed -E 's|.*/([0-9]{4})-.*|\1|' | sort -n | tail -1)
  NEXT=$((10#$LAST + 1))
fi
NUM=$(printf "%04d" "$NEXT")

# 标题转 kebab-case slug（保留 ASCII 字母数字，中文标题退化为 adr）
SLUG=$(echo "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')
[ -z "$SLUG" ] && SLUG="adr"

FILE="$OUT_DIR/$NUM-$SLUG.md"
TODAY=$(date +%Y-%m-%d)

if [ -f "$FILE" ]; then
  echo "❌ 文件已存在: $FILE" >&2
  exit 1
fi

if [ -n "$TEMPLATE" ]; then
  # 替换模板首行的标题与日期占位
  # 注意：必须用 ${NUM} 花括号形式——全角冒号是多字节字符，
  # 在某些 locale 下会被 bash 当作变量名的一部分（$NUM： → 变量 "NUM："）。
  sed -e "1s|.*|# ADR-${NUM}：${TITLE}|" \
      -e "s|YYYY-MM-DD|${TODAY}|" \
      "$TEMPLATE" > "$FILE"
else
  cat > "$FILE" <<EOF
# ADR-${NUM}：${TITLE}

- **状态**：Proposed
- **日期**：${TODAY}
- **决策者**：
- **参与者**：
- **相关**：

## 背景与问题（Context）

## 决策（Decision）

## 备选方案（Alternatives Considered）

## 后果（Consequences）

### 正面

### 负面

## 可逆性

- **类型**：单向门 / 双向门
- **重估触发点**：

## 实施要点

- **落地第一步**：
EOF
fi

echo "✅ 已创建 $FILE"
echo "   模板来源: ${TEMPLATE:-（内置模板）}"
echo
echo "下一步: 填写背景、备选方案与后果。记住——"
echo "  ⚠️  负面后果是必填项；只列一个方案的 ADR 等于没有做决策。"
