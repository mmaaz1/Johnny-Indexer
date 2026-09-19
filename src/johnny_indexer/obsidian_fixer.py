import logging
import re

from johnny_indexer.config import ConfigHelper
from johnny_indexer.file import File

# Matches the rest of a wiki link after the file name: an optional .md extension, then an
# optional heading/block (#) or alias (|), then the closing brackets. Requiring one of these
# after the name stops [[12.33 Notes]] from also matching [[12.33 Notes archive]].
_LINK_SUFFIX_PATTERN = r"((?:\.md)?(?:[#|][^\]]*)?)\]\]"

logger = logging.getLogger(__name__)


class ObsidianFixer:
    """
    A utility class for maintaining and fixing references in Obsidian Markdown files.
    Provides methods to update wiki-style links when files are renamed or moved.
    """

    @staticmethod
    def update_wikilinks(file: File, old_file_ref: File, new_file_ref: File) -> None:
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
            ObsidianFixer._update_wikilinks_for_file(file, old_file_ref, new_file_ref)
        elif file.is_dir():
            for child_file in file.get_children():
                ObsidianFixer.update_wikilinks(child_file, old_file_ref, new_file_ref)

    @staticmethod
    def update_wikilinks_batch(file: File, file_changes: dict[File, File]) -> int:
        """
        Updates wiki-style links in Markdown files for multiple file renames in a single tree traversal.
        This is more efficient than calling update_wikilinks() multiple times, as it scans the tree
        only once and applies all replacements in a single pass per file.

        Args:
            file: File or directory object to process (typically the root)
            file_changes: Dictionary mapping old_file_ref -> new_file_ref for all pending renames

        Returns:
            The number of files whose links were updated
        """

        if ConfigHelper.excluded_from_indexing(file):
            return 0

        if file.is_file() and file.get_extension() in [".md"]:
            return int(
                ObsidianFixer._update_wikilinks_for_file_batch(file, file_changes)
            )
        if file.is_dir():
            return sum(
                ObsidianFixer.update_wikilinks_batch(child_file, file_changes)
                for child_file in file.get_children()
            )
        return 0

    @staticmethod
    def _update_wikilinks_for_file(
        file: File, old_file_ref: File, new_file_ref: File
    ) -> None:
        old_name = old_file_ref.get_name_without_extension()
        new_name = new_file_ref.get_name_without_extension()

        pattern = rf"\[\[{re.escape(old_name)}{_LINK_SUFFIX_PATTERN}"

        # Replacement preserves whatever was after the name
        replacement = f"[[{new_name}\\1]]"

        with open(file.get_abs_path(), encoding="utf-8") as f:
            old_content = f.read()

        updated_content = re.sub(pattern, replacement, old_content)

        if old_content != updated_content:
            with open(file.get_abs_path(), "w", encoding="utf-8") as f:
                f.write(updated_content)
            logger.info("Updated references of %s in: %s", old_file_ref.name, file)

    @staticmethod
    def _update_wikilinks_for_file_batch(
        file: File, file_changes: dict[File, File]
    ) -> bool:
        """
        Updates wiki-style links in a single file for all pending renames.
        This applies all replacements in a single regex pass instead of multiple passes.

        Args:
            file: The markdown file to update
            file_changes: Dictionary mapping old_file_ref -> new_file_ref

        Returns:
            Whether the file was updated
        """
        name_changes = {
            old_file_ref.get_name_without_extension(): new_file_ref.get_name_without_extension()
            for old_file_ref, new_file_ref in file_changes.items()
        }
        if not name_changes:
            return False

        # Match every old name in one pass so a link is never renamed twice when renames
        # chain (eg: 12.33 -> 12.34 and 12.34 -> 12.35). Longest names first so a name
        # that is a prefix of another doesn't win the alternation.
        old_names = sorted(name_changes, key=len, reverse=True)
        alternation = "|".join(re.escape(name) for name in old_names)
        pattern = rf"\[\[({alternation}){_LINK_SUFFIX_PATTERN}"

        updated_names: set[str] = set()

        def replace(match: re.Match[str]) -> str:
            old_name, suffix = match.group(1), match.group(2)
            updated_names.add(old_name)
            return f"[[{name_changes[old_name]}{suffix}]]"

        with open(file.get_abs_path(), encoding="utf-8") as f:
            content = f.read()

        updated_content = re.sub(pattern, replace, content)

        # Write file once if any changes were made
        if updated_content == content:
            return False
        with open(file.get_abs_path(), "w", encoding="utf-8") as f:
            f.write(updated_content)
        logger.info(
            "Updated references in %s: %s", file, ", ".join(sorted(updated_names))
        )
        return True
