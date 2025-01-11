from utils.index.index_helper import IndexHelper as ih
from utils.config_helper import ConfigHelper as ch

class IndexFixer:
    '''
    This class holds the create index algorithm
    '''

    @staticmethod
    def _main_index_sort_key(file):
        if not file.is_indexed(proper = False):
            return (float('inf'), file.get_creation_time())
        
        main_index = ih.get_main_index(file)
        try:
            return (float(main_index), file.get_creation_time())
        except ValueError:
            return (float('inf'), file.get_creation_time())

    @staticmethod
    def _prefix_zeroes(file, main_index):
        '''This ensures that all indexes in one directory are the same length'''
        if ih.is_category(file.get_parent(), proper = True): # Topics are special where we want the main index to have 2 digits (Eg: 12.01)
            desired_main_index_len = 2
        else:
            num_indexed_files = sum(1 for file in file.get_siblings() if not ch.excluded_from_indexing(file)) - 1
            desired_main_index_len = len(str(num_indexed_files))

        return str(main_index).zfill(desired_main_index_len)

    @staticmethod
    def _compute_new_main_index(file):
        '''Main index is computed as a series of consecutive numbers + some prefixed zeroes'''
        # We don't need to compute main index for extensions since they are strings
        if ih.is_extension(file, proper = False):
            return ih.get_main_index(file)

        sibling_files = file.get_siblings()
        indexed_files_in_dir = [sibling_file for sibling_file in sibling_files if not ch.excluded_from_indexing(file)]
        indexed_files_in_dir.sort(key = IndexFixer._main_index_sort_key)

        # ToDo: We need to validate that only 10 areas and categories, or 100 topics, subtopics and extensions can exist

        file_position = indexed_files_in_dir.index(file)
        main_index = IndexFixer._prefix_zeroes(file, file_position)
        return main_index
    
    @staticmethod
    def _compute_parent_index(child_file):
        parent_file = child_file.get_parent()
        if ih.is_area(parent_file, proper = True):
            return ih.get_main_index(parent_file)
        elif ih.is_subtopic(parent_file, proper = True):
            return ""
        elif ih.is_index(parent_file, proper = True):
            return parent_file.index()
        else:
            raise ValueError(f"Invalid parent index: File={child_file.name}, ParentIndex={parent_file.index()}")
    
    @staticmethod
    def fix_index(file):
        '''Creates new index from parent_index and main_index'''
        if file.name.startswith("32.00-0+0"):
            print("asdf")
        if ch.excluded_from_indexing(file):
            return
        parent_index = IndexFixer._compute_parent_index(file)
        main_index = IndexFixer._compute_new_main_index(file)
        ih.update_index_from_portions(file, parent_index, main_index)
    