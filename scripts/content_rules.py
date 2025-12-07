#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容规则应用
"""

import re
import fnmatch

from scripts.filters import passes_filters, check_scope


def build_task_rules(content_rules, task_name):
    task_rules = {}
    for pattern, rule_group in content_rules.items():
        if isinstance(rule_group, list):
            process_rules = [r for r in rule_group if check_scope(r, task_name)]
            filter_rules = []
        else:
            process_rules = [r for r in rule_group.get("process", []) if check_scope(r, task_name)]
            filter_rules = [r for r in rule_group.get("filter", []) if check_scope(r, task_name)]

        if process_rules or filter_rules:
            task_rules[pattern] = {"process": process_rules, "filter": filter_rules}
    return task_rules


def apply_process_rules(rules, content, file_path_obj, link_rewriter=None):
    if not rules:
        return content

    for i, rule in enumerate(rules, 1):
        operation = rule.get("operation", "replace")
        description = rule.get("description", f"规则 {i}")

        try:
            if operation == "append_start":
                append_content = rule.get("content", "")
                if append_content:
                    content = append_content + content
                    print(f"      ✓ {description} (开头追加)")

            elif operation == "append_end":
                append_content = rule.get("content", "")
                if append_content:
                    content = content + append_content
                    print(f"      ✓ {description} (末尾追加)")

            elif operation == "replace":
                pattern = rule.get("pattern")
                replacement = rule.get("replacement", "")
                flags_list = rule.get("flags", [])
                if not pattern:
                    continue
                flags = 0
                for flag_name in flags_list:
                    if flag_name == "DOTALL":
                        flags |= re.DOTALL
                    elif flag_name == "MULTILINE":
                        flags |= re.MULTILINE
                    elif flag_name == "IGNORECASE":
                        flags |= re.IGNORECASE
                new_content = re.sub(pattern, replacement, content, flags=flags)
                if new_content != content:
                    print(f"      ✓ {description} (正则替换)")
                    content = new_content
                else:
                    print(f"      - {description} (未匹配)")

            elif operation == "rewrite_links_to_claude" and link_rewriter:
                new_content = link_rewriter(content, file_path_obj, rule)
                if new_content != content:
                    print(f"      ✓ {description} (链接重写)")
                    content = new_content
                else:
                    print(f"      - {description} (无链接重写)")

        except Exception as e:
            print(f"      ❌ {description} - {e}")

    return content


def process_content(config_path, file_path_obj, content, task_rules, link_rewriter=None):
    matched_groups = []

    if config_path in task_rules:
        matched_groups.append(task_rules[config_path])

    for pattern, group in task_rules.items():
        if pattern == config_path:
            continue
        if "**" in pattern or "*" in pattern:
            if "**" in pattern:
                pattern_base = pattern.split("**")[0].rstrip("/")
            else:
                pattern_base = pattern.rsplit("/", 1)[0] if "/" in pattern else ""

            if pattern_base:
                if config_path.startswith(pattern_base):
                    matched_groups.append(group)
            else:
                if fnmatch.fnmatch(file_path_obj.name, pattern):
                    matched_groups.append(group)

    if not matched_groups:
        return content

    print(f"    🔧 应用 {len(matched_groups)} 组内容规则")

    for group in matched_groups:
        filters = group.get("filter", [])
        process_rules = group.get("process", [])

        if not passes_filters(filters, content, verbose=True):
            print(f"      ⏭️ 过滤未通过，跳过该组")
            continue

        content = apply_process_rules(process_rules, content, file_path_obj, link_rewriter)

    return content


def process(task_name: str, ctx: dict):
    """
    统一入口：
    ctx 需要包含:
      - config_path
      - file_path_obj
      - content
      - task_rules
      - link_rewriter（可选）
    """
    return process_content(
        ctx.get("config_path"),
        ctx.get("file_path_obj"),
        ctx.get("content", ""),
        ctx.get("task_rules", {}),
        ctx.get("link_rewriter"),
    )


