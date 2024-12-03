import math
import os.path
from datetime import datetime
from typing import Literal, Optional

import pandas

from .component.validator import FileFormatValidator, DirectoryPathValidator, LinesPerServingValidator, NegativeLinesPerServingValidator

Extensions = Literal["xlsx", "csv"]


class Shredder:
    extension = FileFormatValidator(allowed_formats=["xlsx", "csv"])
    directory = DirectoryPathValidator()
    lines_per_serving = NegativeLinesPerServingValidator()

    def __init__(
            self,
            directory: str,
            extension: Extensions = "csv",
            lines_per_serving: int = 1000
    ):
        self.extension = extension
        self.directory = directory
        self.lines_per_serving = lines_per_serving

    def run(
            self,
            dataframe: pandas.DataFrame,
            file_name: Optional[str] = None,
            *args,
            **kwargs
    ) -> None:
        number_output_files = self.__get_number_of_output_files(dataframe)
        base_file_name = self.__get_output_file_name(file_name)
        dataframe_copy = dataframe.copy(deep=True)
        for idx in range(number_output_files):
            file_num = idx + 1
            file_path = self.__get_output_file_path(base_file_name, file_num)
            content = dataframe_copy.iloc[:self.lines_per_serving, :]
            self.__save_content_to_file(content, file_path, *args, **kwargs)
            dataframe_copy = dataframe_copy.iloc[self.lines_per_serving:, :]

    def __get_number_of_output_files(self, dataframe: pandas.DataFrame) -> int:
        dataframe_length = len(dataframe)
        validator = LinesPerServingValidator()
        validator(self.lines_per_serving, dataframe_length)
        return math.ceil(dataframe_length / self.lines_per_serving)

    def __get_output_file_name(self, file_name: str) -> str:
        if file_name:
            return ".".join([file_name, self.extension])
        return ".".join([f"Shredder run {datetime.now().strftime('%d.%m.%Y in %H-%M-%S')}", self.extension])

    def __get_output_file_path(self, file_name, file_num) -> str:
        return os.path.join(self.directory, f"{file_num}_{file_name}")

    def __save_content_to_file(self, dataframe: pandas.DataFrame, path: str, *args, **kwargs) -> None:
        match self.extension:
            case "xlsx":
                dataframe.to_excel(path, *args, **kwargs)
            case "csv":
                dataframe.to_csv(path, *args, **kwargs)

    @staticmethod
    def __get_default_file_name() -> str:
        return f"Result {datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(directory="{self.directory}", extension="{self.extension}, lines_per_serving={self.lines_per_serving}")'
