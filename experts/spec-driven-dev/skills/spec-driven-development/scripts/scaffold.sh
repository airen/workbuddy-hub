#!/usr/bin/env bash
# Spec-Driven Development 脚手架
#
# 用法：
#   bash scaffold.sh init    <项目根>              铺 .specify/ 与 specs/ 结构
#   bash scaffold.sh feature <项目根> <feature-slug>  建下一个编号的功能目录并拷 spec 模板
#   bash scaffold.sh bug     <项目根> <bug-slug>      建 bug 修复目录
#   bash scaffold.sh assess  <项目根> <idea-slug>     建想法评估目录
#
# 幂等：已存在的目录和文件不会被覆盖。

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES="$SKILL_DIR/templates"

die() { echo "❌ $*" >&2; exit 1; }
ok()  { echo "  ✅ $*"; }

[ $# -ge 2 ] || die "用法: bash scaffold.sh <init|feature|bug|assess> <项目根> [slug]"

CMD="$1"
ROOT="$2"
SLUG="${3:-}"

[ -d "$ROOT" ] || die "项目根不存在: $ROOT"
ROOT="$(cd "$ROOT" && pwd)"

copy_if_absent() {
  # $1=源  $2=目标
  if [ -f "$2" ]; then
    echo "  ↷ 已存在，跳过: ${2#$ROOT/}"
  else
    cp "$1" "$2"
    ok "${2#$ROOT/}"
  fi
}

case "$CMD" in
  init)
    echo "🚀 初始化 SDD 结构: $ROOT"
    mkdir -p "$ROOT/.specify/memory" "$ROOT/.specify/templates" \
             "$ROOT/.specify/bugs" "$ROOT/.specify/assessments" \
             "$ROOT/specs"
    ok ".specify/{memory,templates,bugs,assessments}"
    ok "specs/"

    for t in spec-template.md plan-template.md tasks-template.md \
             checklist-template.md constitution-template.md; do
      copy_if_absent "$TEMPLATES/$t" "$ROOT/.specify/templates/$t"
    done

    if [ ! -f "$ROOT/.specify/memory/constitution.md" ]; then
      cp "$TEMPLATES/constitution-template.md" "$ROOT/.specify/memory/constitution.md"
      ok ".specify/memory/constitution.md （待填：请先立章程）"
    else
      echo "  ↷ 已存在，跳过: .specify/memory/constitution.md"
    fi

    cat <<'EOF'

下一步：
  1. 填 .specify/memory/constitution.md（项目章程，每项目一次）
  2. bash scaffold.sh feature <项目根> <feature-slug>
  3. 按 specify → clarify → plan → checklist → tasks → analyze → implement → converge 推进
EOF
    ;;

  feature)
    [ -n "$SLUG" ] || die "feature 需要 <feature-slug>（kebab-case）"
    [ -d "$ROOT/.specify" ] || die "先跑 init: bash scaffold.sh init \"$ROOT\""
    case "$SLUG" in
      *[!a-z0-9-]*) die "slug 必须是 kebab-case（小写字母/数字/连字符）: $SLUG" ;;
    esac

    # 取下一个编号（目录名零填充，字典序即数值序）
    N=1
    if [ -d "$ROOT/specs" ]; then
      LAST=$(for d in "$ROOT/specs"/*/; do basename "$d"; done 2>/dev/null | sort | tail -1 || true)
      case "$LAST" in
        [0-9][0-9][0-9]-*) N=$(( 10#$(printf '%s' "$LAST" | cut -c1-3) + 1 )) ;;
      esac
    fi
    NUM=$(printf '%03d' "$N")
    DIR="$ROOT/specs/$NUM-$SLUG"

    [ -e "$DIR" ] && die "目录已存在: $DIR"

    mkdir -p "$DIR/checklists" "$DIR/contracts"
    cp "$TEMPLATES/spec-template.md" "$DIR/spec.md"
    cp "$TEMPLATES/checklist-template.md" "$DIR/checklists/requirements.md"

    # 把模板里的 $ARGUMENTS 占位符换成实际 slug
    if sed --version >/dev/null 2>&1; then
      sed -i "s|\$ARGUMENTS|$SLUG|" "$DIR/spec.md"
    else
      sed -i '' "s|\$ARGUMENTS|$SLUG|" "$DIR/spec.md"
    fi

    echo "🚀 已创建功能目录"
    ok "specs/$NUM-$SLUG/spec.md"
    ok "specs/$NUM-$SLUG/checklists/requirements.md"
    ok "specs/$NUM-$SLUG/contracts/"
    echo
    echo "目录: $DIR"
    echo "下一步: 填 spec.md（聚焦 WHAT/WHY，不写技术栈）"
    ;;

  bug)
    [ -n "$SLUG" ] || die "bug 需要 <bug-slug>"
    DIR="$ROOT/.specify/bugs/$SLUG"
    mkdir -p "$DIR"
    echo "🚀 Bug 修复目录: .specify/bugs/$SLUG"
    echo "流程: bug-assess → bug-fix → bug-test"
    echo "产物: assessment.md / fix.md / verification.md"
    echo "判定: verified | partial | failed"
    ;;

  assess)
    [ -n "$SLUG" ] || die "assess 需要 <idea-slug>"
    DIR="$ROOT/.specify/assessments/$SLUG"
    mkdir -p "$DIR"
    echo "🚀 想法评估目录: .specify/assessments/$SLUG"
    echo "流程: intake → research → define → shape → decide"
    echo "产物: intake.md / research.md / definition.md / shape.md / decision.md"
    echo "决策: go | needs-clarification | kill"
    ;;

  *)
    die "未知子命令: $CMD（支持 init | feature | bug | assess）"
    ;;
esac
