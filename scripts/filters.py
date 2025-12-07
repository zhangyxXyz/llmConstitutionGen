#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
过滤器原子操作
"""

import re

FRONTMATTER_RE = re.compile(r"^---\s*\n([\s\S]*?)\n---\s*\n", re.MULTILINE)


def _frontmatter_has(content, fields):
    m = FRONTMATTER_RE.match(content)
    if not m:
        return False
    fm_body = m.group(1)
    missing = [f for f in fields if re.search(rf"^{re.escape(f)}\s*:", fm_body, flags=re.MULTILINE) is None]
    return len(missing) == 0


def passes_filters(filters, content, verbose=True):
    """过滤规则：全部满足才通过，支持 negate"""
    if not filters:
        return True

    for i, rule in enumerate(filters, 1):
        operation = rule.get("operation")
        description = rule.get("description", f"过滤 {i}")
        negate = rule.get("negate", False)

        passed = False
        reason = ""

        if operation == "frontmatter_has":
            fields = rule.get("fields", ["name", "description"])
            passed = _frontmatter_has(content, fields)
            if not passed:
                reason = "无frontmatter或缺字段"
        else:
            if verbose:
                print(f"      - {description} (未知过滤类型: {operation})")
            return False

        if negate:
            passed = not passed
            if not passed:
                reason = f"取反后未通过"

        if not passed:
            if verbose:
                print(f"      - {description} ({reason})")
            return False
        else:
            if verbose:
                print(f"      ✓ {description}")

    return True


def passes_filters_silent(filters, content):
    """静默版过滤检查"""
    if not filters:
        return True
    for rule in filters:
        operation = rule.get("operation")
        negate = rule.get("negate", False)
        passed = False

        if operation == "frontmatter_has":
            fields = rule.get("fields", ["name", "description"])
            passed = _frontmatter_has(content, fields)
        else:
            return False

        if negate:
            passed = not passed
        if not passed:
            return False
    return True


def process(task_name: str, ctx: dict):
    """
    统一入口：根据 ctx 里的 filters/content/verbose（默认True）判断是否通过
    """
    filters_cfg = ctx.get("filters", [])
    content = ctx.get("content", "")
    verbose = ctx.get("verbose", True)
    return passes_filters(filters_cfg, content, verbose=verbose)


def process_silent(task_name: str, ctx: dict):
    """静默版入口"""
    ctx = dict(ctx)
    ctx["verbose"] = False
    return process(task_name, ctx)


def check_scope(rule, task_name):
    """scope/exclude 检查"""
    scope = rule.get("scope")
    exclude = rule.get("exclude")

    if scope:
        if "*" in scope:
            return True
        return task_name in scope

    if exclude:
        return task_name not in exclude

    return True


