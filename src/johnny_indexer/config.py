import os
import re
from typing import Any

import yaml

from johnny_indexer.file import File
from johnny_indexer.paths import CONFIG_PATH


class ConfigHelper:
    @staticmethod
    def load_from_config(key: str) -> Any:
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(
                f"{CONFIG_PATH} not found. Copy config.example.yaml to config.yaml."
            )

        with open(CONFIG_PATH) as config_file:
            config = yaml.safe_load(config_file)
        if key not in config:
            raise ValueError(f"Invalid key {key} in {CONFIG_PATH}")

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
