import re

from utils.config.config_helper import ConfigHelper
from utils.file.file import File


class ObsidianFixer:
    """
    A utility class for maintaining and fixing references in Obsidian Markdown files.
    Provides methods to update wiki-style links when files are renamed or moved.
    """

    @staticmethod
    def update_weblinks(file: File, old_file_ref: File, new_file_ref: File) -> None:
        """
        Updates wiki-style links in Markdown files, replacing references
        to an old_file_ref with references to new_file_ref.

        Args:
            file: File or directory object to process
            old_file_ref: Reference to the old file that needs to be updated (Eg: 12.33 filename.md)
            new_file_ref: Reference to the new file that will replace old references

        Returns:
            None
        """

        if ConfigHelper.excluded_from_indexing(file):
            return

        if file.is_file() and file.get_extension() in [".md"]:
            ObsidianFixer._update_weblinks_for_file(file, old_file_ref, new_file_ref)
        elif file.is_dir():
            for child_file in file.get_children():
                ObsidianFixer.update_weblinks(child_file, old_file_ref, new_file_ref)

    @staticmethod
    def update_weblinks_batch(file: File, file_changes: dict[File, File]) -> None:
        """
        Updates wiki-style links in Markdown files for multiple file renames in a single tree traversal.
        This is more efficient than calling update_weblinks() multiple times, as it scans the tree
        only once and applies all replacements in a single pass per file.

        Args:
            file: File or directory object to process (typically the root)
            file_changes: Dictionary mapping old_file_ref -> new_file_ref for all pending renames

        Returns:
            None
        """

        if ConfigHelper.excluded_from_indexing(file):
            return

        if file.is_file() and file.get_extension() in [".md"]:
            ObsidianFixer._update_weblinks_for_file_batch(file, file_changes)
        elif file.is_dir():
            for child_file in file.get_children():
                ObsidianFixer.update_weblinks_batch(child_file, file_changes)

    @staticmethod
    def _update_weblinks_for_file(
        file: File, old_file_ref: File, new_file_ref: File
    ) -> None:
        old_name = old_file_ref.get_name_without_extension()
        new_name = new_file_ref.get_name_without_extension()

        # Pattern to match [[old_name*]] where * is any content before closing brackets
        escaped_old_name = re.escape(old_name)
        pattern = rf"\[\[{escaped_old_name}([^\]]*)\]\]"

        # Replacement preserves whatever was after the name
        replacement = f"[[{new_name}\\1]]"

        with open(file.get_abs_path(), encoding="utf-8") as f:
            old_content = f.read()

        updated_content = re.sub(pattern, replacement, old_content)

        if old_content != updated_content:
            with open(file.get_abs_path(), "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Updated references of {old_file_ref.name} in: {file}")

    @staticmethod
    def _update_weblinks_for_file_batch(file: File, file_changes: dict[File, File]) -> None:
        """
        Updates wiki-style links in a single file for all pending renames.
        This applies all replacements in a single regex pass instead of multiple passes.

        Args:
            file: The markdown file to update
            file_changes: Dictionary mapping old_file_ref -> new_file_ref
        """
        with open(file.get_abs_path(), encoding="utf-8") as f:
            content = f.read()

        original_content = content
        updated_files: list[str] = []

        # Apply all replacements in sequence
        for old_file_ref, new_file_ref in file_changes.items():
            old_name = old_file_ref.get_name_without_extension()
            new_name = new_file_ref.get_name_without_extension()

            # Pattern to match [[old_name*]] where * is any content before closing brackets
            escaped_old_name = re.escape(old_name)
            pattern = rf"\[\[{escaped_old_name}([^\]]*)\]\]"

            # Replacement preserves whatever was after the name
            replacement = f"[[{new_name}\\1]]"

            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                updated_files.append(old_file_ref.name)

        # Write file once if any changes were made
        if content != original_content:
            with open(file.get_abs_path(), "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated references in {file}: {', '.join(updated_files)}")
