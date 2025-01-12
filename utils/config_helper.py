import os
import re
import yaml

_CONFIG_FILE_NAME = "config.yaml"

class ConfigHelper:

    @staticmethod    
    def load_from_config(key):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(current_dir)
        config_path = os.path.join(root_path, 'config.yaml')
        
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        if key not in config:
            raise ValueError(f"Invalid key {key} in {_CONFIG_FILE_NAME}")

        return config[key]


    @staticmethod
    def excluded_from_indexing(file):
        for prefix in ConfigHelper.load_from_config("prefixes_excluded_from_indexing"):
            if file.name.startswith(prefix):
                return True
        for pattern in ConfigHelper.load_from_config("patterns_excluded_from_indexing"):
            if re.match(pattern, file.name):
                return True
        return False