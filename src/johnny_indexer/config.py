import os
import re
from functools import cache
from typing import Any

import yaml

from johnny_indexer.file import File
from johnny_indexer.paths import DEFAULTS_CONFIG_PATH, OVERRIDE_CONFIG_PATH


def _read_yaml(path: str) -> dict[str, Any]:
    with open(path) as config_file:
        return yaml.safe_load(config_file) or {}


class ConfigHelper:
    @staticmethod
    @cache
    def _load() -> dict[str, Any]:
        """Reads the defaults once, with the optional overrides on top."""
        defaults = _read_yaml(DEFAULTS_CONFIG_PATH)
        if not os.path.exists(OVERRIDE_CONFIG_PATH):
            return defaults

        config = dict(defaults)
        for key, value in _read_yaml(OVERRIDE_CONFIG_PATH).items():
            if key in defaults:
                config[key] = value
            else:
                print(f"⚠️  Unknown option '{key}' in {OVERRIDE_CONFIG_PATH} is ignored")
        return config

    @staticmethod
    def load_from_config(key: str) -> Any:
        config = ConfigHelper._load()
        if key not in config:
            raise ValueError(f"Invalid config key {key}")

        return config[key]

    @staticmethod
    def excluded_from_indexing(file: File) -> bool:
        for prefix in ConfigHelper.load_from_config("prefixes_excluded_from_indexing"):
            if file.name.startswith(prefix):
                return True
        for pattern in ConfigHelper.load_from_config("patterns_excluded_from_indexing"):
            if re.match(pattern, file.name):
                return True
        return False
