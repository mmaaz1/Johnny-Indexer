from utils import ConfigHelper as cf

class ObsidianFixer:
    @staticmethod
    def update_weblinks(file, old_file_ref, new_file_ref):
        if cf.excluded_from_indexing(file):
            return
        
        old_pattern = f"[[{old_file_ref.get_name_without_extension()}]]"
        new_pattern = f"[[{new_file_ref.get_name_without_extension()}]]"

        if file.is_file() and file.get_extension() in [".md"]:
            with open(file.get_abs_path(), 'r', encoding='utf-8') as f:
                content = f.read()
            updated_content = content.replace(old_pattern, new_pattern)

            if content != updated_content:
                with open(file.get_abs_path(), 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Updated references of {old_file_ref.name} in: {file}")
        
        elif file.is_dir():
            for child_file in file.get_children():
                ObsidianFixer.update_weblinks(child_file, old_file_ref, new_file_ref)
