from enum import Enum
import copy
import re

'''
This file contains the source of truth for my index formatting system. What is a valid proper/improper area/category, etc.
'''

# Separators between parents and main indexes
_INDEX_SEPARATOR = " "

# Regex patterns for index formats
_WILDCARD_INDEX_PATTERN = r'^(?P<m_idx>[0-9]+)$'
_IMPROPER_WILDCARD_INDEX_PATTERN = r'^(?P<m_idx>[0-9]+)\.(?P<s_idx>[0-9]+)$'

_AREA_INDEX_PATTERN = r'^(?P<m_idx>[0-9])0-\1[9]$'
_IMPROPER_AREA_INDEX_PATTERN = r'^(?P<m_idx>[0-9])0-\1[9]\.(?P<s_idx>[0-9]+)$'

_CATEGORY_INDEX_PATTERN = r'^(?P<p_idx>[0-9])(?P<m_idx>[0-9])$'
_IMPROPER_CATEGORY_INDEX_PATTERN = r'^(?P<p_idx>[0-9])(?P<m_idx>[0-9])\.(?P<s_idx>[0-9]+)$'

_TOPIC_INDEX_PATTERN = r'^(?P<p_idx>[0-9]{2})\.(?P<m_idx>[0-9]{2})$'
_IMPROPER_TOPIC_INDEX_PATTERN = r'^(?P<p_idx>[0-9]{2})\.(?P<m_idx>[0-9]{2,})\.(?P<s_idx>[0-9]+)$'

# Extensions are not sorted so no need for improper
_EXTENSION_INDEX_PATTERN = r'^(?P<p_idx>[0-9]{2}\.[0-9]{2})\+(?P<m_idx>[A-Z]+)$'

_SUPTOPIC_INDEX_PATTERN_1 = r'^(?P<p_idx>[0-9]{2}\.[0-9]{2})-(?P<m_idx>[0-9]+)$'
_IMPROPER_SUPTOPIC_INDEX_PATTERN_1 = r'^(?P<p_idx>[0-9]{2}\.[0-9]{2})-(?P<m_idx>[0-9]+)\.(?P<s_idx>[0-9]+)$'

_SUBTOPIC_INDEX_PATTERN_2 = r'^(?P<p_idx>[0-9]{2}\.[0-9]{2}\+[A-Z]+)-(?P<m_idx>[0-9]+)$'
_IMPROPER_SUBTOPIC_INDEX_PATTERN_2 = r'^(?P<p_idx>[0-9]{2}\.[0-9]{2}\+[A-Z]+)-(?P<m_idx>[0-9]+)\.(?P<s_idx>[0-9]+)$'

_IMPROPER_INDEX_PATTERNS = [
    _AREA_INDEX_PATTERN,                    # Y0-Y9
    _IMPROPER_AREA_INDEX_PATTERN,           # Y0-Y9.S*
    
    _CATEGORY_INDEX_PATTERN,                # XY
    _IMPROPER_CATEGORY_INDEX_PATTERN,       # XY.S*

    _TOPIC_INDEX_PATTERN,                   # XX.YY
    _IMPROPER_TOPIC_INDEX_PATTERN,          # XX.YY.S*
    
    _SUPTOPIC_INDEX_PATTERN_1,              # XX.XX-Y*
    _IMPROPER_SUPTOPIC_INDEX_PATTERN_1,     # XX.XX-Y*.S*

    _SUBTOPIC_INDEX_PATTERN_2,              # XX.XX+SUFF-Y*
    _IMPROPER_SUBTOPIC_INDEX_PATTERN_2,     # XX.XX+SUFF-Y*.S*

    _WILDCARD_INDEX_PATTERN,                # Y*
    _IMPROPER_WILDCARD_INDEX_PATTERN,       # Y*.S*
]

class BaseIndexType(Enum):
    AREA = {
        "proper_index_patterns": [
            _AREA_INDEX_PATTERN                             # Y0-Y9
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [0],
        "type": lambda: BaseIndexType.AREA,
        "parents": lambda: [BaseIndexType.NOT_INDEXED], # ToDo: This is a lambda due to cyclic dependency. Look for a more elegant solution
        "separator": ""
    }
    CATEGORY = {
        "proper_index_patterns": [
            _CATEGORY_INDEX_PATTERN                         # XY
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [1],
        "type": lambda: BaseIndexType.CATEGORY,
        "parents": lambda: [BaseIndexType.AREA],
        "separator": ""
    }
    TOPIC = {
        "proper_index_patterns": [
            _TOPIC_INDEX_PATTERN                            # XX.YY
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [2],
        "type": lambda: BaseIndexType.TOPIC,
        "parents": lambda: [BaseIndexType.CATEGORY],
        "separator": "."
    }
    EXTENSION = {
        "proper_index_patterns": [
            _EXTENSION_INDEX_PATTERN                        # XX.XX+SUFF
        ],
        "improper_index_patterns": [],
        "levels": [3],
        "type": lambda: BaseIndexType.EXTENSION,
        "parents": lambda: [BaseIndexType.TOPIC],
        "separator": "+"
    }
    SUBTOPIC_1 = {
        "proper_index_patterns": [
            _SUPTOPIC_INDEX_PATTERN_1                       # XX.XX-Y*
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [3],
        "type": lambda: BaseIndexType.SUBTOPIC_1,
        "parents": lambda: [BaseIndexType.TOPIC],
        "separator": "-"
    }
    SUBTOPIC_2 = {
        "proper_index_patterns": [
            _SUBTOPIC_INDEX_PATTERN_2                       # XX.XX+SUFF-Y*
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [4],
        "type": lambda: BaseIndexType.SUBTOPIC_1,
        "parents": lambda: [BaseIndexType.EXTENSION],
        "separator": "-"
    }
    THE_REST = {
        "proper_index_patterns": [
            _WILDCARD_INDEX_PATTERN                       # Y*
        ],
        "improper_index_patterns": _IMPROPER_INDEX_PATTERNS,
        "levels": [4, 5, 6, 7, 8, 9, 10],
        "type": lambda: BaseIndexType.THE_REST,
        "parents": lambda: [BaseIndexType.SUBTOPIC_1, BaseIndexType.SUBTOPIC_2],
        "separator": ""
    }
    NOT_INDEXED = None

class Proper:
    def __init__(self, proper):
        self.proper = proper
    
    def __eq__(self, other):
        if isinstance(other, bool):
            other_proper = other
        elif isinstance(other, Proper):
            other_proper = other.proper
        else:
            raise ValueError("You shouldn't be comparing proper with others")
        return self.proper or (self.proper == other_proper)
    
    def __bool__(self):
        return self.proper

class ProperIndexType:
    def __init__(self, idx_type, proper):
        self.idx_type = idx_type
        self.proper = Proper(proper)
    
    def is_indexed(self, proper):
        return self != PROPER_NOT_INDEXED and self.proper == proper

    def get_index_config(self):
        if self == PROPER_NOT_INDEXED:
            raise ValueError("No configuration for Not Indexed files")
        it = self.idx_type.value
        return _IndexConfigurator(self.proper, it["proper_index_patterns"], it["improper_index_patterns"], it["levels"], it["type"](), it["parents"](), it["separator"])

    def __str__(self):
        proper_text = "proper" if self.proper else "improper"
        return f"'{self.idx_type} ({proper_text})'"

    def __eq__(self, other):
        if not isinstance(other, ProperIndexType):
            return False
        if not self.proper == other.proper:
            return False
        return self.idx_type == other.idx_type

class _IndexConfigurator:
    def __init__(self, proper, proper_index_patterns, improper_index_patterns, levels, index_type, parent_index_types, separator):
        self._patterns = copy.deepcopy(proper_index_patterns)
        for pattern in improper_index_patterns:
            if not proper and pattern not in self._patterns:
                self._patterns.append(pattern)

        self._levels = levels
        self._index_type = index_type
        self._parent_index_types = [ProperIndexType(parent_index_type, proper=True) for parent_index_type in parent_index_types]
        self._separator = separator
    
    def validate(self, file):
        index = self._get_index_without_validation(file)
        if index is None:
            return False
        if file.level not in self._levels:
            return False
        if file.get_parent().index_type() not in self._parent_index_types:
            return False

        return any(re.match(pattern, index) for pattern in self._patterns)

    def get_index(self, file):
        index = self._get_index_without_validation(file)
        if not self.validate(file):
            return None
        return index
    
    def get_parent_index(self, file):
        return self._get_index_portions(file)['p_idx']
    
    def get_main_index(self, file):
        index_portion = self._get_index_portions(file)
        if index_portion['s_idx'] is None:
            return index_portion['m_idx']
        else:
            return f"{index_portion['m_idx']}.{index_portion['s_idx']}"
        
    def update_index_from_portions(self, file, parent_index, main_index):
        new_index = parent_index + self._separator + main_index
        self.update_index(file, new_index)
    
    def update_index(self, file, new_index):
        if self.validate(file):
            old_index = file.index()
            file.name = file.name.replace(old_index, new_index, 1)
        else:
            file.name = new_index + _INDEX_SEPARATOR + file.name
        
        if not self.validate(file):
            raise ValueError(f"Only updating into proper indexes is supported. File: {file}")
    
    def _get_index_portions(self, file):
        if not self.validate(file):
            return (None, None)
        
        index = self.get_index(file)
        for pattern in self._patterns:
            match = re.compile(pattern).match(index)
            if not match:
                continue
            
            groups = match.groupdict()
            return {
                'p_idx': groups.get('p_idx'),
                'm_idx': groups.get('m_idx'),
                's_idx': groups.get('s_idx')
            }
    
    def _get_index_without_validation(self, file):
        return file.name.split(_INDEX_SEPARATOR)[0]

# Parents
PROPER_NOT_INDEXED = ProperIndexType(BaseIndexType.NOT_INDEXED, proper = False)