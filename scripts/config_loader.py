#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载与访问工具
"""

import json
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_file: Path):
        self.config_file = Path(config_file)
        self.config = self._load()

    def _load(self):
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        with open(self.config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def workpath(self) -> Path:
        return Path(self.config.get("workpath", "."))

    @property
    def cleanpath(self):
        return self.config.get("cleanpath", [])

    @property
    def content_rules(self):
        return self.config.get("content_rules", {})

    @property
    def tasks(self):
        return self.config.get("tasks", [])


