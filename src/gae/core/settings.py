from __future__ import annotations

from pathlib import Path

import yaml


class Settings:

    def __init__(self, config_path: Path):

        self.path = config_path

        with open(config_path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get(self, key, default=None):
        return self.data.get(key, default)
