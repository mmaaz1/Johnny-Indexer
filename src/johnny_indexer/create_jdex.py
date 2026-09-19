import logging
import os

from johnny_indexer.config import ConfigHelper as ch
from johnny_indexer.file import File
from johnny_indexer.index.helper import IndexHelper as ih

logger = logging.getLogger(__name__)


def _should_exclude(file: File) -> bool:
    if file.level == 0 and not ih.is_area(
        file, proper=True
    ):  # De-clutter base directory by removing non-areas
        return True
    if file.name.startswith("."):
        return True

    return False


def _print_line(file: File, base_level: int) -> str:
    indent = "    " * (file.level - base_level - 1)
    markdown_content = f"{indent}{file.level}. "

    if file.is_dir():
        markdown_content += f"**{file.name}** "
    else:
        markdown_content += f"[[{file.name}]] "

    if not ih.is_index(file, proper=True) and not ch.excluded_from_indexing(file):
        markdown_content += "**(NOT INDEXED)** "

    markdown_content += "\n"
    return markdown_content


def _traverse_dir(parent_file: File, base_level: int) -> str:
    """
    Recursively traverse the directory and generate markdown content.
    """
    markdown_content = ""
    for file in ih.sorted_files(parent_file.get_children()):
        if _should_exclude(file):
            continue
        markdown_content += _print_line(file, base_level)
        if file.is_dir():
            markdown_content += _traverse_dir(file, base_level)

    return markdown_content


def _generate_markdown_index(file: File) -> None:
    """
    Generates a markdown index of the directory structure. The file is only written when
    its content changes, so runs that change nothing leave nothing to commit.
    """
    markdown_content = _traverse_dir(file, file.level)
    output_file = file.create_child(f"Index of {file.name}.md")

    # Remove index files left behind by an earlier name of this directory
    for child_file in file.get_children():
        if (
            child_file.name.startswith("Index of ")
            and child_file.name.endswith(".md")
            and child_file != output_file
        ):
            child_file.delete()

    if os.path.exists(output_file.get_abs_path()):
        with open(output_file.get_abs_path(), encoding="utf-8") as f:
            if f.read() == markdown_content:
                return

    with open(output_file.get_abs_path(), "w", encoding="utf-8") as f:
        f.write(markdown_content)
    logger.debug("Wrote %s", output_file)


def create_jdex(root_file: File) -> None:
    area_files = ih.get_areas_in_dir(root_file)

    # Areas first, so the root lists their current index files rather than stale ones
    files_to_index = [*area_files, root_file]
    for file in files_to_index:
        _generate_markdown_index(file)
    logger.info("JDex files updated")
