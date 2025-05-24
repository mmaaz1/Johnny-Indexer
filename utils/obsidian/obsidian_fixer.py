from utils.config.config_helper import ConfigHelper
import re

class ObsidianFixer:
    """
    A utility class for maintaining and fixing references in Obsidian Markdown files.
    Provides methods to update wiki-style links when files are renamed or moved.
    """

    @staticmethod
    def update_weblinks(file, old_file_ref, new_file_ref):
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
    def _update_weblinks_for_file(file, old_file_ref, new_file_ref):
        old_name = old_file_ref.get_name_without_extension()
        new_name = new_file_ref.get_name_without_extension()

        # Pattern to match [[old_name*]] where * is any content before closing brackets
        escaped_old_name = re.escape(old_name)
        pattern = fr'\[\[{escaped_old_name}([^\]]*)\]\]'

        # Replacement preserves whatever was after the name
        replacement = f'[[{new_name}\\1]]'

        with open(file.get_abs_path(), 'r', encoding='utf-8') as f:
            old_content = f.read()

        updated_content = re.sub(pattern, replacement, old_content)

        if old_content != updated_content:
            with open(file.get_abs_path(), 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated references of {old_file_ref.name} in: {file}")