import re

class CommonFunctions:
    _EXCLUDED_PREFIXES = [
        ".", 
        "Index of "
    ]
    _EXCLUDED_PATTERNS = [
        r"^\d{4}-\d{2}-\d{2}",
        r"^\d{2}-\d{2}-\d{2}"
    ]
    
    @staticmethod
    def excluded_from_indexing(file):
        for prefix in CommonFunctions._EXCLUDED_PREFIXES:
            if file.name.startswith(prefix):
                return True
        for pattern in CommonFunctions._EXCLUDED_PATTERNS:
            if re.match(pattern, file.name):
                return True
        return False