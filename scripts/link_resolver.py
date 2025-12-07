#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接重写工具
"""

import re
from pathlib import Path


def rewrite_links_to_task(content, file_path_obj, rule, resolver):
    """
    使用映射表 resolver(config_path) 获取目标路径
    rule 需包含 target_task, link_prefix, rewrite_text
    """
    target_task = rule.get("target_task", "claude")
    link_prefix = rule.get("link_prefix", "../..")
    rewrite_text = rule.get("rewrite_text", True)

    source_dir = file_path_obj.parent

    def repl(match):
        text = match.group(1)
        rel_path = match.group(2)

        ref_file = (source_dir / rel_path).resolve()
        try:
            ref_config_path = str(ref_file.relative_to(Path(".").resolve())).replace("\\", "/")
        except ValueError:
            return match.group(0)

        target_path = resolver(target_task, ref_config_path)
        if target_path:
            new_path = f"{link_prefix}/{target_path}"
            if rewrite_text:
                parts = target_path.split("/")
                new_text = "/".join(parts[-2:]) if len(parts) >= 2 else parts[-1]
            else:
                new_text = text
            return f"[{new_text}]({new_path})"

        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(\./([^)]+)\)", repl, content)


def process(task_name: str, ctx: dict):
    """
    ctx:
      - content
      - file_path_obj
      - rule
      - resolver
    """
    return rewrite_links_to_task(
        ctx.get("content", ""),
        ctx.get("file_path_obj"),
        ctx.get("rule", {}),
        ctx.get("resolver"),
    )


