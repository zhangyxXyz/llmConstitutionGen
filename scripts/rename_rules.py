#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重命名规则原子操作
"""

from pathlib import Path


def apply_rename_rule(source_path, rename_rule):
    path = Path(source_path)

    apply_to = rename_rule.get("apply_to", ["file"])

    if rename_rule.get("foldername"):
        result = path.parent.name
    else:
        parts = []
        combine = rename_rule.get("combine", ["filename"])
        for part_type in combine:
            if part_type == "filename":
                parts.append(path.stem)
            elif part_type == "parent_dir":
                parts.append(path.parent.name)
        result = "-".join(parts)

    if "file" in apply_to:
        if rename_rule.get("lowercase", False):
            result = result.lower()
        for repl in rename_rule.get("replacements", []):
            result = result.replace(repl.get("from", ""), repl.get("to", ""))

    return result


def apply_parent_dir_rule(parent_name, rename_rule):
    apply_to = rename_rule.get("apply_to", ["file"])
    if "parent" not in apply_to and not rename_rule.get("apply_to_parent_dir", False):
        return parent_name
    new_name = parent_name
    if rename_rule.get("lowercase", False):
        new_name = new_name.lower()
    for repl in rename_rule.get("replacements", []):
        new_name = new_name.replace(repl.get("from", ""), repl.get("to", ""))
    return new_name


def compute_target_path(source_path, dist_config):
    """
    返回相对于 workpath 的目标路径字符串
    """
    source_path = Path(source_path)

    # 文件名
    if "rename" in dist_config:
        target_name = dist_config["rename"]
    elif "rename_rule" in dist_config:
        rename_rule = dist_config["rename_rule"]
        apply_to = rename_rule.get("apply_to", ["file"])
        if "file" in apply_to or rename_rule.get("foldername"):
            base_name = apply_rename_rule(source_path, rename_rule)
            suffix = dist_config.get("suffix")
            target_name = f"{base_name}.{suffix}" if suffix else f"{base_name}{source_path.suffix}"
        else:
            target_name = source_path.name
    else:
        target_name = source_path.name

    # 目录
    copy_to = dist_config.get("copy", "").rstrip("/")
    target_dir = copy_to

    if dist_config.get("use_parent_dir"):
        parent_name = source_path.parent.name
        if "rename_rule" in dist_config:
            parent_name = apply_parent_dir_rule(parent_name, dist_config["rename_rule"])
        target_dir = f"{target_dir}/{parent_name}" if target_dir else parent_name

    return f"{target_dir}/{target_name}" if target_dir else target_name


def process(task_name: str, ctx: dict):
    """
    ctx:
      - source_path
      - dist_config
    返回: target_path (相对 workpath 的路径字符串)
    """
    return compute_target_path(ctx.get("source_path"), ctx.get("dist_config", {}))


