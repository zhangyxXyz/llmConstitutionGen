#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分发入口：加载配置，调用 Distributor
"""

import sys
from pathlib import Path
from scripts.config_loader import ConfigLoader
from scripts.distributor import Distributor
from scripts import settings_gen


def main():
    script_dir = Path(__file__).parent

    # 支持命令行参数传递配置文件路径
    if len(sys.argv) > 1:
        config_file = Path(sys.argv[1])
        if not config_file.is_absolute():
            config_file = script_dir / config_file
    else:
        config_file = script_dir / "configs" / "rules_config.json"

    if not config_file.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        print(f"\n用法: python distribute_rules.py [配置文件路径]")
        print(f"默认: python distribute_rules.py  (使用 configs/rules_config.json)")
        sys.exit(1)

    loader = ConfigLoader(config_file)
    print(f"⚙️  已加载配置: {config_file}")

    def settings_resolver(**kwargs):
        return settings_gen.process(**kwargs)

    distributor = Distributor(
        workpath=loader.workpath,
        cleanpath=loader.cleanpath,
        content_rules=loader.content_rules,
        tasks=loader.tasks,
        settings_resolver=settings_resolver,
    )
    distributor.run()


if __name__ == "__main__":
    main()

