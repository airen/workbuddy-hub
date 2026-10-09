#!/usr/bin/env python3
"""验证所有资产是否符合 open.workbuddy.cn 平台上传要求。"""

import json
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent


def validate_expert(expert_dir: Path) -> list[str]:
    """验证专家配置是否符合平台要求。"""
    issues = []
    
    plugin_path = expert_dir / ".codebuddy-plugin" / "plugin.json"
    if not plugin_path.exists():
        issues.append(f"缺少 plugin.json")
        return issues
    
    with plugin_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 检查必填字段
    required_fields = ["name", "displayName", "profession", "displayDescription"]
    for field in required_fields:
        if field not in config:
            issues.append(f"缺少必填字段: {field}")
    
    # 检查 defaultInitPrompt 与 quickPrompts[0] 一致性（平台核心校验规则）
    if "defaultInitPrompt" in config and "quickPrompts" in config and len(config["quickPrompts"]) > 0:
        default = config["defaultInitPrompt"]
        first_prompt = config["quickPrompts"][0]
        
        if default.get("zh") != first_prompt.get("zh"):
            issues.append(
                f"defaultInitPrompt.zh 与 quickPrompts[0].zh 不一致\n"
                f"  defaultInitPrompt.zh:   \"{default.get('zh')}\"\n"
                f"  quickPrompts[0].zh:     \"{first_prompt.get('zh')}\""
            )
        
        if default.get("en") != first_prompt.get("en"):
            issues.append(
                f"defaultInitPrompt.en 与 quickPrompts[0].en 不一致\n"
                f"  defaultInitPrompt.en:   \"{default.get('en')}\"\n"
                f"  quickPrompts[0].en:     \"{first_prompt.get('en')}\""
            )
    
    return issues


def validate_team(team_dir: Path) -> list[str]:
    """验证专家团配置。"""
    issues = []
    
    plugin_path = team_dir / ".codebuddy-plugin" / "plugin.json"
    if not plugin_path.exists():
        issues.append(f"缺少 plugin.json")
        return issues
    
    with plugin_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    
    if "defaultInitPrompt" in config and "quickPrompts" in config and len(config["quickPrompts"]) > 0:
        default = config["defaultInitPrompt"]
        first_prompt = config["quickPrompts"][0]
        
        if default.get("zh") != first_prompt.get("zh"):
            issues.append(
                f"defaultInitPrompt.zh 与 quickPrompts[0].zh 不一致\n"
                f"  defaultInitPrompt.zh:   \"{default.get('zh')}\"\n"
                f"  quickPrompts[0].zh:     \"{first_prompt.get('zh')}\""
            )
        
        if default.get("en") != first_prompt.get("en"):
            issues.append(
                f"defaultInitPrompt.en 与 quickPrompts[0].en 不一致\n"
                f"  defaultInitPrompt.en:   \"{default.get('en')}\"\n"
                f"  quickPrompts[0].en:     \"{first_prompt.get('en')}\""
            )
    
    return issues


def main():
    """主函数。"""
    print("=" * 70)
    print("🔍 验证资产是否符合 open.workbuddy.cn 平台上传要求")
    print("=" * 70)
    
    all_issues = {}
    
    # 验证专家
    experts_dir = WORKSPACE / "experts"
    if experts_dir.exists():
        for expert_dir in sorted(experts_dir.iterdir()):
            if expert_dir.is_dir() and not expert_dir.name.startswith('.'):
                issues = validate_expert(expert_dir)
                if issues:
                    all_issues[f"expert:{expert_dir.name}"] = issues
    
    # 验证专家团
    teams_dir = WORKSPACE / "teams"
    if teams_dir.exists():
        for team_dir in sorted(teams_dir.iterdir()):
            if team_dir.is_dir() and not team_dir.name.startswith('.'):
                issues = validate_team(team_dir)
                if issues:
                    all_issues[f"team:{team_dir.name}"] = issues
    
    # 输出结果
    if all_issues:
        print(f"\n❌ 发现 {len(all_issues)} 个资产存在问题：\n")
        for asset, issues in all_issues.items():
            print(f"  📦 {asset}")
            for issue in issues:
                print(f"     ⚠️  {issue}")
            print()
        sys.exit(1)
    else:
        print("\n✅ 所有资产均符合平台上传要求！\n")
        print("📋 平台校验规则：")
        print("   • defaultInitPrompt.zh 必须与 quickPrompts[0].zh 一致")
        print("   • defaultInitPrompt.en 必须与 quickPrompts[0].en 一致")
        print("   • 包含 name、displayName、profession、displayDescription 等必填字段")
        sys.exit(0)


if __name__ == "__main__":
    main()
