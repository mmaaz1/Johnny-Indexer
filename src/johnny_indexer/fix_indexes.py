import sys
from collections import deque

from johnny_indexer.config import ConfigHelper as ch
from johnny_indexer.create_jdex import create_jdex
from johnny_indexer.file import File
from johnny_indexer.git_committer import GitCommitter
from johnny_indexer.index.fixer import IndexFixer as idx_f
from johnny_indexer.index.helper import IndexHelper as ih
from johnny_indexer.obsidian_fixer import ObsidianFixer as of

"""
fix_indexes.py

Fixes the indexes of files in a hierarchical directory system, so files are consistently
and properly indexed. It:

1. Auto-commits the notes to git, if enabled.
2. Walks the hierarchy breadth-first, one level at a time, starting from the Areas.
3. Proposes a rename for each file whose index doesn't match its expected index.
4. Optionally prompts the user to approve each rename, then applies them and updates
   wiki links to the renamed files, if enabled.
5. Regenerates JDex files, if enabled.

Key Components:
- ProposedChange: Tracks old and new file states during index corrections.
- propose_index_update: Proposes a rename if a file's index is incorrect.
- bfs_fix_indexes: Performs breadth-first search to apply index corrections across files.
- fix_indexes: Entry point for the `fix` command.
- IndexFixer (index/fixer.py): Computes the expected parent and main indexes of a file.

Usage:
    johnny-indexer fix <notes_path>
"""


class ProposedChange:
    def __init__(self, old_file: File, new_file: File) -> None:
        self.old_file = old_file
        self.new_file = new_file


def propose_index_update(old_file: File) -> ProposedChange | None:
    """Fix parent and main portions of indexes for files in the given directory"""
    new_file = old_file.create_copy()
    idx_f.fix_index(new_file)

    if old_file != new_file:
        return ProposedChange(old_file, new_file)
    else:
        return None


def prompt_user(old_file: File, new_file: File) -> None:
    while True:
        print(f"\nParent: {old_file.get_parent()}")
        print("Siblings:")
        for iter_file in [
            sibling
            for sibling in ih.sorted_files(old_file.get_siblings())
            if not ch.excluded_from_indexing(sibling)
        ]:
            if iter_file != old_file:
                print(f"- {iter_file}")
            else:
                print(f"-> {iter_file} => {new_file}")
        print("")

        user_input = (
            input(f"'{old_file.name}' => '{new_file.name}' (y/n): ").strip().lower()
        )
        if user_input == "y":
            print("Proceeding.")
            break
        elif user_input == "n":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def should_prompt() -> bool:
    """Prompts are only shown when enabled and someone is at a terminal to answer them."""
    if not ch.load_from_config("prompt_for_approval"):
        return False
    if not sys.stdin.isatty():
        print("Non-interactive run: applying renames without prompting.")
        return False
    return True


def bfs_fix_indexes(root_file: File, area_files: list[File], prompt: bool) -> None:
    queue: deque[File] = deque(area_files)

    while queue:
        proposed_changes: list[ProposedChange] = []
        for _ in range(len(queue)):
            parent_file = queue.popleft()
            for file in ih.sorted_files(parent_file.get_children()):
                if file.is_dir():
                    queue.append(file)
                proposal = propose_index_update(file)
                if proposal is not None:
                    proposed_changes.append(proposal)

        proposed_changes.sort(key=lambda proposal: ih.sort_key(proposal.new_file))

        for proposal in proposed_changes:
            old_file = proposal.old_file
            new_file = proposal.new_file

            if new_file.exists():
                print(f"\n❌ CONFLICT: '{new_file.name}' already exists")
                sys.exit(1)

            if prompt:
                prompt_user(old_file, new_file)

            old_file.rename(new_file)

        # Batch update wiki links for all changes at once, after all renames applied
        if ch.load_from_config("fix_wikilinks") and proposed_changes:
            file_changes = {
                proposal.old_file: proposal.new_file for proposal in proposed_changes
            }
            of.update_wikilinks_batch(root_file, file_changes)


def fix_indexes(root_path: str) -> None:
    root_file = File.from_abs_path(root_path, -1)
    areas = ih.get_areas_in_dir(root_file)

    GitCommitter.auto_commit(root_file)
    bfs_fix_indexes(root_file, areas, should_prompt())
    if ch.load_from_config("generate_jdex"):
        create_jdex(root_file)
