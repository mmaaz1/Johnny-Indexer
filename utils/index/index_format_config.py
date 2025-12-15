from enum import Enum
from dataclasses import dataclass
import copy
import re
from typing import Dict, List, Optional, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from utils.file.file import File

'''
This file contains the source of truth for my index formatting system. What is a valid proper/improper area/category, etc.
'''


@dataclass(frozen=True)
class IndexTypeConfig:
    """Configuration for an index type"""
    proper_index_patterns: List[str]
    improper_index_patterns: List[str]
    levels: List[int]
    parents: Callable[[], List['BaseIndexType']]
    separator: str

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
    AREA = IndexTypeConfig(
        proper_index_patterns=[_AREA_INDEX_PATTERN],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[0],
        parents=lambda: [BaseIndexType.NOT_INDEXED],
        separator=""
    )
    CATEGORY = IndexTypeConfig(
        proper_index_patterns=[_CATEGORY_INDEX_PATTERN],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[1],
        parents=lambda: [BaseIndexType.AREA],
        separator=""
    )
    TOPIC = IndexTypeConfig(
        proper_index_patterns=[_TOPIC_INDEX_PATTERN],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[2],
        parents=lambda: [BaseIndexType.CATEGORY],
        separator="."
    )
    EXTENSION = IndexTypeConfig(
        proper_index_patterns=[_EXTENSION_INDEX_PATTERN],
        improper_index_patterns=[],
        levels=[3],
        parents=lambda: [BaseIndexType.TOPIC],
        separator="+"
    )
    SUBTOPIC_1 = IndexTypeConfig(
        proper_index_patterns=[_SUPTOPIC_INDEX_PATTERN_1],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[3],
        parents=lambda: [BaseIndexType.TOPIC],
        separator="-"
    )
    SUBTOPIC_2 = IndexTypeConfig(
        proper_index_patterns=[_SUBTOPIC_INDEX_PATTERN_2],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[4],
        parents=lambda: [BaseIndexType.EXTENSION],
        separator="-"
    )
    THE_REST = IndexTypeConfig(
        proper_index_patterns=[_WILDCARD_INDEX_PATTERN],
        improper_index_patterns=_IMPROPER_INDEX_PATTERNS,
        levels=[4, 5, 6, 7, 8, 9, 10],
        parents=lambda: [BaseIndexType.SUBTOPIC_1, BaseIndexType.SUBTOPIC_2],
        separator=""
    )
    NOT_INDEXED = IndexTypeConfig(
        proper_index_patterns=[],
        improper_index_patterns=[],
        levels=[],
        parents=lambda: [],
        separator=""
    )

class Proper:
    def __init__(self, proper: bool) -> None:
        self.proper = proper

    def __eq__(self, other: object) -> bool:
        if isinstance(other, bool):
            other_proper = other
        elif isinstance(other, Proper):
            other_proper = other.proper
        else:
            raise ValueError("You shouldn't be comparing proper with others")
        return self.proper or (self.proper == other_proper)

    def __bool__(self) -> bool:
        return self.proper

class ProperIndexType:
    def __init__(self, idx_type: BaseIndexType, proper: bool) -> None:
        self.idx_type = idx_type
        self.proper = Proper(proper)

    def is_indexed(self, proper: bool) -> bool:
        return self != PROPER_NOT_INDEXED and self.proper == proper

    def get_index_config(self) -> "IndexConfigurator":
        if self == PROPER_NOT_INDEXED:
            raise ValueError("No configuration for Not Indexed files")
        config = self.idx_type.value
        return IndexConfigurator(self.proper, config.proper_index_patterns, config.improper_index_patterns, config.levels, self.idx_type, config.parents(), config.separator)

    def __str__(self) -> str:
        proper_text = "proper" if self.proper else "improper"
        return f"'{self.idx_type} ({proper_text})'"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProperIndexType):
            return False
        if not self.proper == other.proper:
            return False
        return self.idx_type == other.idx_type

class IndexConfigurator:
    def __init__(
        self,
        proper: Proper,
        proper_index_patterns: List[str],
        improper_index_patterns: List[str],
        levels: List[int],
        index_type: BaseIndexType,
        parent_index_types: List[BaseIndexType],
        separator: str,
    ) -> None:
        self._patterns = copy.deepcopy(proper_index_patterns)
        for pattern in improper_index_patterns:
            if not proper and pattern not in self._patterns:
                self._patterns.append(pattern)

        self._levels = levels
        self._index_type = index_type
        self._parent_index_types = [ProperIndexType(parent_index_type, proper=True) for parent_index_type in parent_index_types]
        self._separator = separator

    def validate(self, file: "File") -> bool:
        index = self._get_index_without_validation(file)
        if index is None:
            return False
        if file.level not in self._levels:
            return False
        if file.get_parent().index_type() not in self._parent_index_types:
            return False

        return any(re.match(pattern, index) for pattern in self._patterns)

    def get_index(self, file: "File") -> Optional[str]:
        index = self._get_index_without_validation(file)
        if not self.validate(file):
            return None
        return index

    def get_parent_index(self, file: "File") -> Optional[str]:
        return self._get_index_portions(file)['p_idx']

    def get_main_index(self, file: "File") -> Optional[str]:
        index_portion = self._get_index_portions(file)
        if index_portion['s_idx'] is None:
            return index_portion['m_idx']
        else:
            return f"{index_portion['m_idx']}.{index_portion['s_idx']}"

    def update_index_from_portions(self, file: "File", parent_index: str, main_index: str) -> None:
        new_index = parent_index + self._separator + main_index
        self.update_index(file, new_index)

    def update_index(self, file: "File", new_index: str) -> None:
        if self.validate(file):
            old_index = file.index()
            assert old_index is not None  # Guaranteed by validate() returning True
            file.name = file.name.replace(old_index, new_index, 1)
        else:
            file.name = new_index + _INDEX_SEPARATOR + file.name

        if not self.validate(file):
            raise ValueError(f"Only updating into proper indexes is supported. File: {file}")

    def _get_index_portions(self, file: "File") -> Dict[str, Optional[str]]:
        if not self.validate(file):
            return {"p_idx": None, "m_idx": None, "s_idx": None}

        index = self.get_index(file)
        assert index is not None  # Guaranteed by validate() returning True
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
        return {"p_idx": None, "m_idx": None, "s_idx": None}

    def _get_index_without_validation(self, file: "File") -> Optional[str]:
        parts = file.name.split(_INDEX_SEPARATOR)
        return parts[0] if parts else None

# Parents
PROPER_NOT_INDEXED = ProperIndexType(BaseIndexType.NOT_INDEXED, proper = False)