from typing import TYPE_CHECKING

from utils.index.index_format_config import (
    PROPER_NOT_INDEXED,
    BaseIndexType,
    IndexConfigurator,
    ProperIndexType,
)

if TYPE_CHECKING:
    from utils.file.file import File


class IndexHelper:
    """
    This class serves as a layer of abstraction on top of IndexConfigs. It holds functions related to index
    """

    @staticmethod
    def is_index(file: "File", proper: bool) -> bool:
        """Checks if the file is indexed. Set proper to True to validate that the script correctly set the index.
        Set proper to false to check if a file is eligible to for indexing. This has less restrictions in the validation.
        """
        return IndexHelper.get_index_type(file).is_indexed(proper)

    @staticmethod
    def get_index(file: "File") -> str | None:
        return IndexHelper._get_index_config_from_file(file).get_index(file)

    @staticmethod
    def get_index_type(file: "File") -> ProperIndexType:
        for proper in [True, False]:
            for index_type in BaseIndexType:
                if index_type == BaseIndexType.NOT_INDEXED:
                    continue

                index_type = ProperIndexType(index_type, proper)
                if index_type.get_index_config().validate(file):
                    return index_type

        return PROPER_NOT_INDEXED

    @staticmethod
    def _get_all_index_configs(proper: bool | None = None) -> list["IndexConfigurator"]:
        if proper is None:
            propers = [True, False]
        else:
            propers = [proper]

        all_index_types: list[IndexConfigurator] = []
        for proper in propers:
            for index_type in BaseIndexType:
                if index_type == BaseIndexType.NOT_INDEXED:
                    continue
                all_index_types.append(
                    ProperIndexType(index_type, proper).get_index_config()
                )

        return all_index_types

    @staticmethod
    def get_main_index(file: "File") -> str | None:
        return IndexHelper._get_index_config_from_file(file).get_main_index(file)

    @staticmethod
    def update_index_from_portions(
        og_file: "File", parent_index: str, main_index: str
    ) -> None:  # ToDo: Pretty bad code
        for index_config in IndexHelper._get_all_index_configs(False):
            file = og_file.create_copy()
            try:
                index_config.update_index_from_portions(file, parent_index, main_index)
                if IndexHelper.is_index(file, True):
                    og_file.copy_from(file)
                    return
            except ValueError:
                pass

        raise ValueError("Only updating proper index is supported.")

    @staticmethod
    def update_index(og_file: "File", new_index: str) -> None:  # ToDo: Pretty bad code
        for index_config in IndexHelper._get_all_index_configs(False):
            file = og_file.create_copy()
            try:
                index_config.update_index(file, new_index)
                if IndexHelper.is_index(file, True):
                    og_file.copy_from(file)
                    return
            except ValueError:
                pass

        raise ValueError("Only updating proper index is supported.")

    @staticmethod
    def is_area(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.AREA, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def is_category(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.CATEGORY, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def is_topic(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.TOPIC, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def is_extension(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.EXTENSION, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def is_subtopic(file: "File", proper: bool) -> bool:
        return IndexHelper._is_subtopic_1(file, proper) or IndexHelper._is_subtopic_2(
            file, proper
        )

    @staticmethod
    def is_the_rest(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.THE_REST, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def get_areas_in_dir(file: "File") -> list["File"]:
        areas = [
            child_file
            for child_file in file.get_children()
            if IndexHelper.is_area(child_file, proper=True)
        ]
        if len(areas) == 0:
            raise ValueError("Received empty areas directory")

        return areas

    @staticmethod
    def _is_subtopic_1(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.SUBTOPIC_1, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def _is_subtopic_2(file: "File", proper: bool) -> bool:
        index_type = ProperIndexType(BaseIndexType.SUBTOPIC_2, proper)
        return index_type.get_index_config().validate(file)

    @staticmethod
    def _get_index_config_from_file(file: "File") -> IndexConfigurator:
        return file.index_type().get_index_config()
