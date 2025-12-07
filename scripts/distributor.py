#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分发主流程
"""

from pathlib import Path

from scripts import filters
from scripts.content_rules import build_task_rules, process_content, apply_process_rules
from scripts.rename_rules import (
    apply_rename_rule,
    apply_parent_dir_rule,
    process as rename_process,
)
from scripts.paths import (
    process as paths_process,
    precompute_all_path_mappings,
)
from scripts.link_resolver import process as link_process
from scripts.filters import process as filters_process, process_silent as filters_process_silent
from scripts import settings_gen


class Distributor:
    def __init__(self, workpath: Path, cleanpath, content_rules, tasks, settings_resolver=None):
        self.workpath = Path(workpath)
        self.cleanpath = cleanpath or []
        self.content_rules = content_rules or {}
        self.tasks = tasks or []
        self.path_mappings = {}
        self.settings_resolver = settings_resolver

    # 基础工具
    def get_target_path(self, task_name, config_path):
        return self.path_mappings.get(task_name, {}).get(config_path)

    # 清理
    def clean_targets(self):
        if not self.cleanpath:
            return
        print(f"\n🧹 清理 {len(self.cleanpath)} 个目标路径...")
        for path_str in self.cleanpath:
            target = self.workpath / path_str
            if not target.exists():
                print(f"  ⏭️  {path_str} (不存在，跳过)")
                continue
            try:
                if target.is_file():
                    target.unlink()
                    print(f"  🗑️  {path_str} (文件)")
                elif target.is_dir():
                    import shutil

                    shutil.rmtree(target)
                    print(f"  🗑️  {path_str} (目录)")
            except Exception as e:
                print(f"  ❌ 删除 {path_str} 失败: {e}")

    # 链接重写适配器
    def _make_link_rewriter(self, target_task):
        def resolver(task_name, config_path):
            return self.get_target_path(task_name, config_path)

        def rewriter(content, file_path_obj, rule):
            return rewrite_links_to_task(content, file_path_obj, rule, resolver)

        return rewriter

    # 分发
    def distribute_file(self, source_path, content, dist_config):
        from scripts.rename_rules import apply_rename_rule, apply_parent_dir_rule

        # 确定目标文件名
        if "rename" in dist_config:
            target_name = dist_config["rename"]
        elif "rename_rule" in dist_config:
            rename_rule = dist_config["rename_rule"]
            apply_to = rename_rule.get("apply_to", ["file"])
            if "file" in apply_to or rename_rule.get("foldername"):
                base_name = apply_rename_rule(source_path, rename_rule)
                suffix = dist_config.get("suffix")
                target_name = f"{base_name}.{suffix}" if suffix else f"{base_name}{Path(source_path).suffix}"
            else:
                target_name = Path(source_path).name
        else:
            target_name = Path(source_path).name

        # 目标目录
        copy_to = dist_config.get("copy", "")
        target_dir = self.workpath / copy_to if copy_to else self.workpath

        if dist_config.get("use_parent_dir"):
            parent_name = Path(source_path).parent.name
            if "rename_rule" in dist_config:
                parent_name = apply_parent_dir_rule(parent_name, dist_config["rename_rule"])
            target_dir = target_dir / parent_name

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / target_name
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"    📤 {target_name} -> {target_dir.relative_to(self.workpath) if copy_to else '.'}")
        except Exception as e:
            print(f"    ❌ 写入文件失败: {e}")

    def run_task(self, task):
        task_name = task.get("name", "unnamed")
        print(f"\n{'='*60}")
        print(f"📦 执行任务: {task_name}")
        print(f"{'='*60}")

        task_rules = build_task_rules(self.content_rules, task_name)
        print(f"  📐 内容规则数: {sum(len(g.get('process', [])) + len(g.get('filter', [])) for g in task_rules.values())}")

        dist_rules = task.get("distribute", [])
        print(f"  📦 分发单元数: {len(dist_rules)}")

        processed_count = 0
        for dist_idx, dist_rule in enumerate(dist_rules, 1):
            source_config = dist_rule.get("source")
            if not source_config:
                print(f"\n  ⚠️  分发单元 {dist_idx} 缺少 source 配置，跳过")
                continue

            files = paths_process(task_name, {"source_config": source_config})
            if not files:
                print(f"\n  ⏭️  分发单元 {dist_idx}: 无匹配文件")
                continue

            print(f"\n  📁 分发单元 {dist_idx}: {len(files)} 个文件")

            for file_path, config_path in files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    print(f"    ❌ 读取文件失败: {file_path} - {e}")
                    continue

                print(f"\n    📝 {config_path}")

                dist_filters = dist_rule.get("filter", [])
                if not filters_process(task_name, {"filters": dist_filters, "content": content, "verbose": True}):
                    print(f"      ⏭️  过滤未通过，跳过")
                    continue

                def link_rewriter_fn(content_val, file_path_obj, rule):
                    return link_process(
                        task_name,
                        {
                            "content": content_val,
                            "file_path_obj": file_path_obj,
                            "rule": rule,
                            "resolver": lambda t_name, cfg: self.get_target_path(t_name, cfg),
                        },
                    )

                processed_content = process_content(
                    config_path,
                    Path(file_path),
                    content,
                    task_rules,
                    link_rewriter_fn,
                )

                dist_process = dist_rule.get("process", [])
                final_content = apply_process_rules(dist_process, processed_content, Path(file_path)) if dist_process else processed_content

                self.distribute_file(file_path, final_content, dist_rule)
                processed_count += 1

        if self.settings_resolver:
                self.settings_resolver(
                    task_name=task_name,
                    ctx={
                        "task": task,
                        "workpath": self.workpath,
                        "default_permission": "allow",
                        "target_file": ".claude/settings.local.json",
                        "collect_source": lambda sc: paths_process(task_name, {"source_config": sc}),
                        "get_target_path": self.get_target_path,
                        "frontmatter_re": filters.FRONTMATTER_RE,
                    },
                )

        print(f"\n  ✨ 任务 '{task_name}' 完成，处理 {processed_count} 个文件")

    def run(self):
        print("\n" + "=" * 60)
        print("🚀 通用 LLM 规则分发工具")
        print("=" * 60)
        print(f"📂 工作路径: {self.workpath.absolute()}")
        print(f"📋 任务数量: {len(self.tasks)}")

        self.path_mappings = precompute_all_path_mappings(
            self.tasks,
            lambda task_name, ctx: filters_process_silent(task_name, ctx),
            lambda source_path, dist_config: rename_process(
                task_name="",
                ctx={"source_path": source_path, "dist_config": dist_config},
            ),
        )
        self.clean_targets()

        for task in self.tasks:
            try:
                self.run_task(task)
            except Exception as e:
                task_name = task.get("name", "unnamed")
                print(f"\n❌ 任务 '{task_name}' 执行失败: {e}")

        print("\n" + "=" * 60)
        print("✅ 所有任务完成")
        print("=" * 60)


