import os
import copy
from utils.index.index_helper import IndexHelper as ih

class File:
    '''
    This class contains information about a file and its index, or the lack thereof.
    '''
    ### Constructors
    def __init__(self, *args):
        if len(args) == 2:
            self._init_with_abs_path(*args)
        elif len(args) == 3:
            self._init_with_name_and_path(*args)
        else:
            raise ValueError(f"Invalid number of arguments. Given: {len(args)}. Expected: 3")

    def _init_with_abs_path(self, abs_path, level):
        if not os.path.isabs(abs_path):
            raise ValueError(f"'{abs_path}' is not an absolute path.")

        self.name = os.path.basename(abs_path)
        self.dir_path = os.path.dirname(abs_path)
        self.level = level

    def _init_with_name_and_path(self, name, path, level):
        self.name = name
        self.dir_path = path
        self.level = level

        if not os.path.isabs(self.get_abs_path()):
            raise ValueError(f"The resulting path '{self.get_abs_path()}' is not an absolute path.")

    def create_copy(self):
        return copy.deepcopy(self)
    
    def create_child(self, name):
        return File(name, self.get_abs_path(), self.level + 1)

    def get_parent(self):
        parent_dir_name = os.path.basename(self.dir_path)
        parent_path = os.path.dirname(os.path.abspath(self.dir_path))
        return File(parent_dir_name, parent_path, self.level - 1)
    
    def get_children(self):
        child_files = []
        for child_file_name in sorted(os.listdir(self.get_abs_path())):
            child_file = File(child_file_name, self.get_abs_path(), self.level + 1)
            child_files.append(child_file)

        return child_files
    
    def get_siblings(self):
        return self.get_parent().get_children()
    

    ### Copy Functions
    def copy_from(self, other_file):
        self.__dict__.update(other_file.__dict__)
    

    ### Index Functions
    def index(self):
        return ih.get_index(self)
    
    def index_type(self):
        return ih.get_index_type(self)
        
    def is_indexed(self, proper):
        return ih.is_index(self, proper)
    

    ### Getters
    def get_abs_path(self):
        return os.path.join(self.dir_path, self.name)
        
    def is_file(self):
        return os.path.isfile(self.get_abs_path())
        
    def is_dir(self):
        return os.path.isdir(self.get_abs_path())

    def get_extension(self):
        # Returns empty string if extension doesn't exist
        return os.path.splitext(self.name)[1]

    def get_name_without_extension(self):
        return os.path.splitext(self.name)[0]

    def get_creation_time(self):
        return os.stat(self.get_abs_path()).st_birthtime
    
    ### File Modification Functions
    def delete(self):
        if self.is_file():
            os.remove(self.get_abs_path())
        else:
            raise ValueError(f"Can't delete. {self.name} is a directory.")
    
    def rename(self, new_file):
        os.rename(self.get_abs_path(), new_file.get_abs_path())
        self.copy_from(new_file)
            

    ### Class functions
    def __eq__(self, other):
        if isinstance(other, File):
            return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __str__(self):
        return f"{self.name}"
