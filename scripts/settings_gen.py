#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
settings.local.json 生成（claude 专用逻辑由调用方决定是否使用）
"""

import json
import re
from pathlib import Path

from scripts.filters import passes_filters_silent


def extract_frontmatter_field(content, field, regex):
    """从 frontmatter 中提取字段值"""
    m = regex.match(content)
    if not m:
        return None
    fm_body = m.group(1)
    match = re.search(rf"^{re.escape(field)}\s*:\s*(.+)$", fm_body, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def generate_settings_permissions(task, workpath, default_permission, target_file, collect_source, get_target_path, frontmatter_re):
    """
    生成/更新 settings.local.json 的 permissions
    （是否调用由上层根据 task 决定）
    """
    generate_settings_cfg = task.get("generate_settings")
    if not generate_settings_cfg:
        return None

    task_name = task.get("name", "unnamed")
    target_file = generate_settings_cfg.get("target", target_file)
    default_permission = generate_settings_cfg.get("default_permission", default_permission)

    permissions = {"allow": [], "deny": [], "ask": []}

    for dist_rule in task.get("distribute", []):
        source_config = dist_rule.get("source")
        if not source_config:
            continue

        if isinstance(source_config, dict) and source_config.get("type") == "directory":
            files = collect_source(source_config)

            for file_path, config_path in files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except:
                    continue

                dist_filters = dist_rule.get("filter", [])
                if dist_filters and not passes_filters_silent(dist_filters, content):
                    continue

                permission = extract_frontmatter_field(content, "permission", frontmatter_re) or default_permission

                target_path = get_target_path(task_name, config_path)
                if target_path:
                    parts = target_path.split("/")
                    if len(parts) >= 2:
                        skill_name = parts[-2]
                        skill_ref = f"Skill({skill_name})"
                        if permission in permissions and skill_ref not in permissions[permission]:
                            permissions[permission].append(skill_ref)

    target_path = workpath / target_file
    target_path.parent.mkdir(parents=True, exist_ok=True)

    settings_content = {}
    if target_path.exists():
        try:
            with open(target_path, "r", encoding="utf-8") as f:
                settings_content = json.load(f)
            print(f"    📝 更新现有 {target_file}")
        except:
            settings_content = {}

    settings_content["permissions"] = permissions

    try:
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(settings_content, f, indent=2, ensure_ascii=False)
        print(f"    📤 {target_file}")
        print(f"       allow: {len(permissions['allow'])} skills")
        print(f"       deny: {len(permissions['deny'])} skills")
        print(f"       ask: {len(permissions['ask'])} skills")
    except Exception as e:
        print(f"    ❌ 生成失败: {e}")
        return None

    return settings_content


def process_default(task_name: str, ctx: dict):
    """无特化时的默认行为：不生成 settings"""
    return None


def process_claude(task_name: str, ctx: dict):
    """claude 特化：生成 permissions"""
    return generate_settings_permissions(
        task=ctx.get("task"),
        workpath=ctx.get("workpath"),
        default_permission=ctx.get("default_permission"),
        target_file=ctx.get("target_file"),
        collect_source=ctx.get("collect_source"),
        get_target_path=ctx.get("get_target_path"),
        frontmatter_re=ctx.get("frontmatter_re"),
    )


def process_codebuddy(task_name: str, ctx: dict):
    """codebuddy 特化：生成 permissions"""
    return generate_settings_permissions(
        task=ctx.get("task"),
        workpath=ctx.get("workpath"),
        default_permission=ctx.get("default_permission"),
        target_file=ctx.get("target_file"),
        collect_source=ctx.get("collect_source"),
        get_target_path=ctx.get("get_target_path"),
        frontmatter_re=ctx.get("frontmatter_re"),
    )


def process(task_name: str, ctx: dict):
    """
    统一入口：根据 task_name 选择特化处理函数
    支持命名：process_<task>，找不到则用 process_default
    """
    name = (task_name or "").lower()
    func = globals().get(f"process_{name}", process_default)
    return func(task_name, ctx)


