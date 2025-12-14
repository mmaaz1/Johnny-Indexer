import os
import copy
import sys
from typing import List
from utils.index.index_helper import IndexHelper as ih
from functools import total_ordering

@total_ordering  # Automatically fills in all comparison methods
class File:
    '''
    This class contains information about a file and its index, or the lack thereof.
    '''
    name: str
    dir_path: str
    level: int

    ### Constants
    @staticmethod
    def get_root_path() -> str:
        script_path = os.path.abspath(sys.argv[0])
        return os.path.dirname(script_path)

    ### Constructors
    @classmethod
    def from_name_and_path(cls, name: str, path: str, level: int = 0) -> "File":
        """Create instance from name, path, and level."""
        instance = cls.__new__(cls)
        instance.name = name
        instance.dir_path = path
        instance.level = level

        if not os.path.isabs(instance.get_abs_path()):
            raise ValueError(f"The resulting path '{instance.get_abs_path()}' is not an absolute path.")
        return instance

    @classmethod
    def from_abs_path(cls, abs_path: str, level: int = 0) -> "File":
        """Create instance from absolute path and level."""
        if not os.path.isabs(abs_path):
            raise ValueError(f"'{abs_path}' is not an absolute path.")

        name = os.path.basename(abs_path)
        dir_path = os.path.dirname(abs_path)
        return cls.from_name_and_path(name, dir_path, level)

    def __init__(self, *args, **kwargs) -> None:
        raise TypeError("Cannot instantiate directly. Use from_abs_path or from_name_and_path methods.")

    def create_copy(self) -> "File":
        return copy.deepcopy(self)

    ## Tranversing Functions
    def create_child(self, name: str) -> "File":
        return File.from_name_and_path(name, self.get_abs_path(), self.level + 1)

    def get_parent(self) -> "File":
        parent_dir_name = os.path.basename(self.dir_path)
        parent_path = os.path.dirname(os.path.abspath(self.dir_path))
        return File.from_name_and_path(parent_dir_name, parent_path, self.level - 1)

    def get_children(self) -> List["File"]:
        child_files = []
        for child_file_name in os.listdir(self.get_abs_path()):
            child_file = File.from_name_and_path(child_file_name, self.get_abs_path(), self.level + 1)
            child_files.append(child_file)

        return sorted(child_files)

    def get_siblings(self) -> List["File"]:
        return sorted(self.get_parent().get_children())
    

    ### Copy Functions
    def copy_from(self, other_file: "File") -> None:
        self.__dict__.update(other_file.__dict__)


    ### Index Functions
    def index(self) -> str:
        return ih.get_index(self)

    def index_type(self):  # type: ignore  # Returns ProperIndexType, but importing creates circular dependency
        # TODO: Avoid circular import - consider refactoring index_helper imports
        return ih.get_index_type(self)

    def is_indexed(self, proper) -> bool:
        return ih.is_index(self, proper)
    

    ### Getters
    def get_abs_path(self) -> str:
        return os.path.join(self.dir_path, self.name)

    def is_file(self) -> bool:
        return os.path.isfile(self.get_abs_path())

    def is_dir(self) -> bool:
        return os.path.isdir(self.get_abs_path())

    def get_extension(self) -> str:
        # Returns empty string if extension doesn't exist
        return os.path.splitext(self.name)[1]

    def get_name_without_extension(self) -> str:
        return os.path.splitext(self.name)[0]

    def get_creation_time(self) -> float:
        return os.stat(self.get_abs_path()).st_birthtime

    def exists(self) -> bool:
        return os.path.exists(self.get_abs_path())
    
    ### File Modification Functions
    def delete(self) -> None:
        if self.is_file():
            os.remove(self.get_abs_path())
        else:
            raise ValueError(f"Can't delete. {self.name} is a directory.")

    def rename(self, new_file: "File") -> None:
        os.rename(self.get_abs_path(), new_file.get_abs_path())
        self.copy_from(new_file)

    @staticmethod
    def index_sort_key(file: "File") -> tuple:
        parent_file_index = float('inf')
        try:
            parent_file = file.get_parent()
            parent_file_index = float(ih.get_index(parent_file))
        except:
            pass

        main_index = float('inf')
        try:
            main_index = float(ih.get_main_index(file))
        except:
            pass

        creation_time = float('inf')
        if file.exists():
            creation_time = file.get_creation_time()

        return (parent_file_index, main_index, creation_time)
            

    ### Class functions
    def __eq__(self, other: object) -> bool:
        if isinstance(other, File):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __lt__(self, other: object) -> bool:
        """Compare files by index, falling back to creation time."""
        if not isinstance(other, File):
            return NotImplemented

        # Use 'index_sort_key' method as default
        return File.index_sort_key(self) < File.index_sort_key(other)

    def __str__(self) -> str:
        return f"{self.name}"
