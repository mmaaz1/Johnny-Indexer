import os
import copy
from utils.index_helper import IndexHelper as ih

class File:
    '''
    This class contains information about a file and its index, or the lack thereof.
    '''
    def __init__(self, name, dir_path, level):
        self.name = name
        self.dir_path = dir_path
        self.level = level # Root directory is 0

    def create_copy(self):
        return copy.deepcopy(self)
    
    def create_child(self, name):
        return File(name, self.get_abs_path(), self.level + 1)
    
    def copy_from(self, other_file):
        self.__dict__.update(other_file.__dict__)
    
    def index(self):
        return ih.get_index(self)
    
    def index_type(self):
        return ih.get_index_type(self)
        
    def is_indexed(self, proper):
        return ih.is_index(self, proper)

    def get_parent_file(self):
        parent_dir_name = os.path.basename(self.dir_path)
        parent_path = os.path.dirname(os.path.abspath(self.dir_path))
        return File(parent_dir_name, parent_path, self.level - 1)
    
    def get_child_files(self):
        child_files = []
        for child_file_name in sorted(os.listdir(self.get_abs_path())):
            child_file = File(child_file_name, self.get_abs_path(), self.level + 1)
            child_files.append(child_file)

        return child_files
    
    def get_sibling_files(self):
        return self.get_parent_file().get_child_files()
    
    def get_abs_path(self):
        return os.path.join(self.dir_path, self.name)
        
    def is_file(self):
        return os.path.isfile(self.get_abs_path())
        
    def is_directory(self):
        return os.path.isdir(self.get_abs_path())

    def get_creation_time(self):
        return os.stat(self.get_abs_path()).st_birthtime
    
    def delete(self):
        if self.is_file():
            os.remove(self.get_abs_path())
        else:
            raise ValueError(f"Can't delete. {self.name} is a directory.")

    def __eq__(self, other):
        if isinstance(other, File):
            return self.__dict__ == other.__dict__
        return NotImplemented
    
    def __str__(self):
        return f"{self.name}"
