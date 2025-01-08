import os
import sys
from collections import deque
from utils import File
from utils import IndexHelper as ih
from utils import IndexFixer as idx_f
from generate_index_file import generate_index_file

'''
fix_indexes.py
    
This script manages and corrects file indexes in a hierarchical directory system. It ensures that files are consistently and properly indexed, enabling better organization and retrieval. The script:

1. Computes parent and main indexes for files based on their location in the hierarchy.
2. Constructs new indexes by appending parent and main indexes with appropriate separators.
3. Proposes updates for file names when their indexes are incorrect.
4. Interactively prompts the user to approve renaming of files to maintain integrity.
5. Uses a breadth-first search to process files iteratively, starting from the root directory.

Key Components:
- ProposedChange: Tracks old and new file states during index corrections.
- compute_parent_index: Retrieves the index of a file's parent.
- compute_main_index: Assigns a unique and properly formatted main index to a file.
- append_indexes: Combines parent and main indexes to form the complete index.
- bfs_fix_indexes: Performs breadth-first search to apply index corrections across files.

Usage:
Run the script to automatically process and correct indexes in a specified directory hierarchy.
'''

class ProposedChange:
    def __init__(self, old_file, new_file):
        self.old_file = old_file
        self.new_file = new_file

def propose_index_update(old_file):
    """ Fix parent and main portions of indexes for files in the given directory """
    new_file = old_file.create_copy()
    idx_f.fix_index(new_file)

    if old_file != new_file:
        return ProposedChange(old_file, new_file)
    else:
        return None

def prompt_user(old_file, new_file):
    while True:
        print(f"\nParent: {old_file.get_parent_file()}")
        print("Siblings:")
        for iter_file in old_file.get_sibling_files():
            arrow = " ->" if iter_file == old_file else " -"
            print(f"{arrow} {iter_file}")
        print("")

        user_input = input(f"'{old_file.name}' => '{new_file.name}' (y/n): ").strip().lower()
        if user_input == 'y':
            print("Proceeding.\n")
            break
        elif user_input == 'n':
            print("Exiting.\n")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'y' or 'n'.\n")

def bfs_fix_indexes(area_files):
    queue = deque(area_files)

    while queue:
        proposed_changes = []
        for _ in range(len(queue)):
            parent_file = queue.popleft()
            for file in parent_file.get_child_files():
                if file.is_directory():
                    queue.append(file)
                proposal = propose_index_update(file)
                if proposal is not None:
                    proposed_changes.append(proposal)
        
        proposed_changes.sort(key=lambda proposal: proposal.new_file.index())
        for proposal in proposed_changes:
            old_file = proposal.old_file
            new_file = proposal.new_file
            prompt_user(old_file, new_file)
            os.rename(old_file.get_abs_path(), new_file.get_abs_path())
            old_file.copy_from(new_file)

def main():
    '''Creating a main function to minimize the number of global variables'''
    if len(sys.argv) != 2:
        raise ValueError("Usage: python fix_indexes.py <root_path>")
    root_path = os.path.abspath(sys.argv[1])
    root_file = File(os.path.basename(root_path), os.path.dirname(root_path), -1)
    areas = ih.get_areas_in_dir(root_file)
    bfs_fix_indexes(areas)
    generate_index_file(root_file)

if __name__ == "__main__":
    main()
