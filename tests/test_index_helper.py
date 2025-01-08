import pytest
import copy
from utils import File, IndexHelper as ih
from utils.index_format_config import ProperIndexType, BaseIndexType, PROPER_NOT_INDEXED

INDEX_TYPE_ATTRS = ["areas", "categories", "topics", "extensions", "subtopics_1", "subtopics_2"]
VALIDITY_TYPE_ATTRS = ["proper", "invalid", "improper", "improper_exclusive"]

EXPECTATION_MATRIX = [
    ("proper", True, True),
    ("proper", False, True),
    ("improper", False, True),
    ("improper_exclusive", True, False),
    ("improper_exclusive", False, True),
    ("invalid", True, False),
    ("invalid", False, False),
]

class IndexTestInputs:
    def __init__(self):
        self.proper = []
        self.invalid = []
        self.improper = [] # proper + improper_exclusive = improper
        self.improper_exclusive = []

class OuterTestInputs:
    def __init__(self):
        self.areas = IndexTestInputs()
        self.categories = IndexTestInputs()
        self.topics = IndexTestInputs()
        self.extensions = IndexTestInputs()
        self.subtopics_1 = IndexTestInputs()
        self.subtopics_2 = IndexTestInputs()
        self.proper = []
        self.invalid = []
        self.improper = []
        self.improper_exclusive = []

@pytest.fixture
def test_inputs():
    """Fixture providing all test file configurations"""
    test_inputs = OuterTestInputs()

    # Area level files (level 0)
    test_inputs.areas.proper = [
        File("10-19 My Area", "/root", 0),
        File("40-49 My Area2", "/blah", 0),
    ]
    test_inputs.areas.invalid = [
        File("1a-19 Wrong Area", "/root", 0),
        File("12-19 Wrong Area", "/root", 0),
        File("10-29 Wrong Area", "/root", 0),
        File("1a-19 Wrong Area", "/root", 0),
    ]
    test_inputs.areas.improper_exclusive = [
        File("1 Area", "/root", 0),
    ]

    # Category level files (level 1)
    area_path = test_inputs.areas.proper[0].get_abs_path()
    test_inputs.categories.proper = [
        File("12 My Category", area_path, 1),
        File("00 My Category", area_path, 1),
    ]
    test_inputs.categories.invalid = [
        File("1a Category", area_path, 1),
        File("10.10 Category", area_path, 1),
    ]
    test_inputs.categories.improper_exclusive = [
        File("1 Category", area_path, 1),
        File("1234567 Category", area_path, 1),
    ]

    # Topic level files (level 2)
    category_path = test_inputs.categories.proper[0].get_abs_path()
    test_inputs.topics.proper = [
        File("12.01 My Topic", category_path, 2),
        File("00.00 My Topic", category_path, 2),
    ]
    test_inputs.topics.invalid = [
        File("12.1 Wrong Topic", category_path, 2),
        File("0.01 Wrong Topic", category_path, 2),
    ]
    test_inputs.topics.improper_exclusive = [
        File("1 Topic", category_path, 2),
        File("12.01234 Topic", category_path, 2),
    ]

    # Extension files (level 3)
    topic_path = test_inputs.topics.proper[0].get_abs_path()
    test_inputs.extensions.proper = [
        File("12.01+EXT My Extension", topic_path, 3),
        File("12.02+A My Extension", topic_path, 3),
    ]
    test_inputs.extensions.invalid = [
        File("12.01+ext Wrong Extension", topic_path, 3),
        File("12.01+123 Wrong Extension", topic_path, 3),
        File("12.01 Wrong Extension", topic_path, 3),
    ]
    test_inputs.extensions.improper_exclusive = [
    ]

    # Subtopic files (level 3)
    test_inputs.subtopics_1.proper = [
        File("12.01-1234 My Subtopic", topic_path, 3),
        File("12.01-1 My Subtopic", topic_path, 3),
    ]
    test_inputs.subtopics_1.invalid = [
        File("12.01-a Wrong Subtopic", topic_path, 3),
        File("12.01 Wrong Subtopic", topic_path, 3),
    ]
    test_inputs.subtopics_1.improper_exclusive = [
        File("1 Subtopic", topic_path, 3),
    ]

    # Subtopic files (level 4)
    extension_path = test_inputs.extensions.proper[0].get_abs_path()
    test_inputs.subtopics_2.proper = [
        File("12.01+EXT-1 My Subtopic", extension_path, 4),
        File("12.01+EXT-1234 My Subtopic", extension_path, 4),
    ]
    test_inputs.subtopics_2.invalid = [
        File("12.01+EXT-a My Subtopic", extension_path, 4),
        File("12.01+EXT My Subtopic", extension_path, 4),
    ]
    test_inputs.subtopics_2.improper_exclusive = [
        File("1 My Subtopic", extension_path, 4),
    ]

    for index_type_attr in INDEX_TYPE_ATTRS:
        index_test_inputs = getattr(test_inputs, index_type_attr)
        
        index_test_inputs.improper = index_test_inputs.improper_exclusive + index_test_inputs.proper
        
        test_inputs.proper += index_test_inputs.proper
        test_inputs.improper_exclusive += index_test_inputs.improper_exclusive
        test_inputs.improper += index_test_inputs.improper
        test_inputs.invalid += index_test_inputs.invalid
        
    return test_inputs

    
@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_indexed(test_inputs, validity_type, proper, expected):
    """Test if files are properly indexed"""
    test_files = getattr(test_inputs, validity_type)
    _test_file_indexing(test_files, ih.is_index, proper, expected)

def _test_file_indexing(test_files, test_function, proper, expected):
    for file in test_files:
        result = test_function(file, proper=proper)
        if result != expected:
            pytest.fail(f"Failed '{test_function.__name__}(proper={proper})' check for file: '{file}'\n"
                       f"Expected: {expected}, Got: {result}\n")

def _test_excluded_indexes(test_inputs, excluded_index, test_function):
    if excluded_index not in INDEX_TYPE_ATTRS:
        raise ValueError(f"{excluded_index} is not a valid index type")

    excluded_index_types = [it for it in INDEX_TYPE_ATTRS if it != excluded_index]
    for idx_type in excluded_index_types:
        excluded_idx_test_inputs = getattr(test_inputs, idx_type)
        for validity in VALIDITY_TYPE_ATTRS:
            non_area_files = getattr(excluded_idx_test_inputs, validity)
            for proper in [False, True]:
                _test_file_indexing(non_area_files, test_function, proper, False)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_area(test_inputs, validity_type, proper, expected):
    """Test area validation"""
    area_files = getattr(test_inputs.areas, validity_type)
    _test_file_indexing(area_files, ih.is_area, proper, expected)
    _test_excluded_indexes(test_inputs, "areas", ih.is_area)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_category(test_inputs, validity_type, proper, expected):
    """Test category validation"""
    category_files = getattr(test_inputs.categories, validity_type)
    _test_file_indexing(category_files, ih.is_category, proper, expected)
    _test_excluded_indexes(test_inputs, "categories", ih.is_category)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_topic(test_inputs, validity_type, proper, expected):
    """Test topic validation"""
    topic_files = getattr(test_inputs.topics, validity_type)
    _test_file_indexing(topic_files, ih.is_topic, proper, expected)
    _test_excluded_indexes(test_inputs, "topics", ih.is_topic)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_extension(test_inputs, validity_type, proper, expected):
    """Test extension validation"""
    extension_files = getattr(test_inputs.extensions, validity_type)
    _test_file_indexing(extension_files, ih.is_extension, proper, expected)
    _test_excluded_indexes(test_inputs, "extensions", ih.is_extension)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_subtopic_1(test_inputs, validity_type, proper, expected):
    """Test subtopic 1 validation"""
    subtopic_1_files = getattr(test_inputs.subtopics_1, validity_type)
    _test_file_indexing(subtopic_1_files, ih._is_subtopic_1, proper, expected)
    _test_excluded_indexes(test_inputs, "subtopics_1", ih._is_subtopic_1)

@pytest.mark.parametrize("validity_type,proper,expected", EXPECTATION_MATRIX)
def test_is_subtopic_2(test_inputs, validity_type, proper, expected):
    """Test subtopic 2 validation"""
    subtopic_2_files = getattr(test_inputs.subtopics_2, validity_type)
    _test_file_indexing(subtopic_2_files, ih._is_subtopic_2, proper, expected)
    _test_excluded_indexes(test_inputs, "subtopics_2", ih._is_subtopic_2)

# @pytest.mark.parametrize("validity_type,proper,expected", [
#     ("areas", "proper", True, True),
#     ("areas", "improper", True, True),
#     ("areas", "invalid", True, True),
#     ("proper", False, True),
#     ("improper", False, True),
#     ("improper_exclusive", True, False),
#     ("improper_exclusive", False, True),
#     ("invalid", True, False),
#     ("invalid", False, False),
# ])
# def test_get_index_type(self):
#     """Test index type identification"""
#     self.assertEqual(ih.get_index_type(self.valid_area), ProperIndexType(BaseIndexType.AREA, proper = True))
#     self.assertEqual(ih.get_index_type(self.valid_category), ProperIndexType(BaseIndexType.CATEGORY, proper = True))
#     self.assertEqual(ih.get_index_type(self.valid_topic), ProperIndexType(BaseIndexType.TOPIC, proper = True))
#     self.assertEqual(ih.get_index_type(self.valid_extension), ProperIndexType(BaseIndexType.EXTENSION, proper = True))
#     self.assertEqual(ih.get_index_type(self.valid_subtopic_1), ProperIndexType(BaseIndexType.SUBTOPIC_1, proper = True))
#     self.assertEqual(ih.get_index_type(self.valid_subtopic_2), ProperIndexType(BaseIndexType.SUBTOPIC_2, proper = True))
    # self.assertEqual(ih.get_index_type(self.invalid_area), PROPER_NOT_INDEXED)

# def test_get_main_index(self):
#     """Test main index extraction"""
#     self.assertEqual(ih.get_main_index(self.valid_area), "1")
#     self.assertEqual(ih.get_main_index(self.valid_category), "2")
#     self.assertEqual(ih.get_main_index(self.valid_topic), "01")
#     self.assertEqual(ih.get_main_index(self.valid_extension), "EXT")
#     self.assertEqual(ih.get_main_index(self.valid_subtopic_1), "1")

# def test_combine_index_portions(self):
#     """Test index combination"""
#     self.assertEqual(
#         ih.create_index(self.valid_topic, "12", "01"),
#         "12.01"
#     )
#     self.assertEqual(
#         ih.create_index(self.valid_extension, "12.01", "EXT"),
#         "12.01+EXT"
#     )
#     self.assertEqual(
#         ih.create_index(self.valid_subtopic_1, "12.01", "1"),
#         "12.01-1"
#     )
