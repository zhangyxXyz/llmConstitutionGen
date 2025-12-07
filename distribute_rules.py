#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分发入口：加载配置，调用 Distributor
"""

from pathlib import Path
from scripts.config_loader import ConfigLoader
from scripts.distributor import Distributor
from scripts import settings_gen


def main():
    script_dir = Path(__file__).parent
    config_file = script_dir / "rules_config.json"
    loader = ConfigLoader(config_file)
    print(f"⚙️  已加载配置: {config_file.name}")

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

