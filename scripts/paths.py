#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径收集与预计算
"""

import json
from pathlib import Path


def collect_source(source_config):
    files = []

    # 兼容字符串形式
    if isinstance(source_config, str):
        source_str = source_config
        if "**" in source_str or "*" in source_str:
            matched = list(Path(".").glob(source_str))
            for file_path in matched:
                if file_path.is_file():
                    config_path = str(file_path).replace("\\", "/")
                    files.append((file_path, config_path))
        else:
            file_path = Path(source_str)
            if file_path.exists() and file_path.is_file():
                config_path = str(file_path).replace("\\", "/")
                files.append((file_path, config_path))
        return files

    # dict 形式
    source_type = source_config.get("type")
    path = source_config.get("path")

    if source_type == "file":
        file_path = Path(path)
        if file_path.exists():
            config_path = str(file_path).replace("\\", "/")
            files.append((file_path, config_path))
    elif source_type == "directory":
        dir_path = Path(path)
        pattern = source_config.get("pattern", "**/*.md")
        if dir_path.exists():
            for file_path in dir_path.glob(pattern):
                if file_path.is_file():
                    config_path = str(file_path).replace("\\", "/")
                    files.append((file_path, config_path))
    return files


def process(task_name: str, ctx: dict):
    """
    ctx:
      - source_config
    返回: [(file_path, config_path)]
    """
    return collect_source(ctx.get("source_config"))


def precompute_all_path_mappings(tasks, filter_proc, compute_target_path):
    """
    返回 {task_name: {config_path: target_path}}
    """
    mappings = {}
    print("\n📊 预计算路径映射...")

    for task in tasks:
        task_name = task.get("name", "unnamed")
        task_mapping = {}

        for dist_rule in task.get("distribute", []):
            source_config = dist_rule.get("source")
            if not source_config:
                continue

            files = collect_source(source_config)

            for file_path, config_path in files:
                dist_filters = dist_rule.get("filter", [])
                if dist_filters:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        if not filter_proc(
                            task_name,
                            {
                                "filters": dist_filters,
                                "content": content,
                                "verbose": False,
                            },
                        ):
                            continue
                    except:
                        continue

                target_path = compute_target_path(file_path, dist_rule)
                task_mapping[config_path] = target_path

        mappings[task_name] = task_mapping
        print(f"  📦 {task_name}: {len(task_mapping)} 个文件映射")

    return mappings


