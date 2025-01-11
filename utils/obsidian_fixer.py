import os
import re

class ObsidianFixer:
    @staticmethod 
    def _remove_extension(filename):
        filename_without_extension, _ = os.path.splitext(filename)
        return filename_without_extension

    @staticmethod
    def update_weblinks(root_file, old_file, new_file):
        old_pattern = f"[[{ObsidianFixer._remove_extension(old_file.name)}]]"
        new_pattern = f"[[{ObsidianFixer._remove_extension(new_file.name)}]]"

        for root, _, files in os.walk(root_file.get_abs_path()):
            for file in files:
                if not file.endswith('.md'): # Obsidian only opens supports files
                    continue

                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                updated_content = content.replace(old_pattern, new_pattern)

                if content != updated_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Updated references of {old_file.name} in: {file}")
