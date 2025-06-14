import sys
from utils.file import File
from utils.index.index_helper import IndexHelper as ih
from utils.config.config_helper import ConfigHelper as ch
from datetime import datetime

def _should_exclude(file):
    if file.level == 0 and not ih.is_area(file, proper = True): # De-clutter base directory by removing non-areas
        return True
    if file.name.startswith("."):
        return True

    return False

def _print_line(file, base_level):
    indent = "    " * (file.level - base_level - 1)
    markdown_content = f"{indent}{file.level}. "
    
    if file.is_dir():
        markdown_content += f"**{file.name}** "
    else:
        markdown_content += f"[[{file.name}]] "

    if not ih.is_index(file, proper = True) and not ch.excluded_from_indexing(file):
        markdown_content += "**(NOT INDEXED)** "

    markdown_content += "\n"
    return markdown_content

def _traverse_dir(parent_file, base_level) -> str:
    """
    Recursively traverse the directory and generate markdown content.
    """
    markdown_content = ""
    for file in parent_file.get_children():
        if _should_exclude(file):
            continue
        markdown_content += _print_line(file, base_level)
        if file.is_dir():
            markdown_content += _traverse_dir(file, base_level)
    
    return markdown_content

def _generate_markdown_index(file: str) -> None:
    """
    Generates a markdown index of the directory structure.
    """
    markdown_content = f"> [!info] **Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown_content += _traverse_dir(file, file.level)
    
    for child_file in file.get_children():
        if child_file.name.startswith("Index of ") and child_file.name.endswith(".md"):
            child_file.delete()

    output_file = file.create_child(f"Index of {file.name}.md")
    with open(output_file.get_abs_path(), "w", encoding="utf-8") as f:
        f.write(markdown_content)

def create_jdex(root_file):
    area_files = ih.get_areas_in_dir(root_file)
    
    files_to_index = [root_file] + area_files
    print("Updating all JIndexes.")
    for file in files_to_index:
        _generate_markdown_index(file)
    print("JIndexes Updated.")

def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python fix_indexes.py <root_path>")
    
    root_path = sys.argv[1]
    root_file = File.from_abs_path(root_path, -1)
    
    create_jdex(root_file)

if __name__ == "__main__":
    main()
