import math
import os.path

import pandas
from typing import Literal
from .validator import DirectoryPathValidator, FileFormatValidator, CountRowValidator


FileFormal = Literal["xlsx", "csv"]


class Shredder:
    file_format = FileFormatValidator(allowed_formats=["xlsx", "csv"])
    output_dir = DirectoryPathValidator()

    def __init__(self, dataframe: pandas.DataFrame, output_dir: str, file_name: str, file_format: FileFormal = 'xlsx', count_line: int = 1000):
        """

        :param dataframe: Набор данных, который необходимо нарезать
        :param output_dir: Директория, в которую будет сохранен результат
        :param file_name: Имя для файла с результатом (к каждому файлу будет добавлен префикс "Номер_")
        :param file_format: Формат выходного файла
        :param count_line: Количество строк в одном выходном файле. От этого параметра зависит количество выходных файлов.
        :raise UnsupportedFileFormatError: В ситуации если в file_format задан не поддерживаемый формат файла.
        :raise DirectoryDoesNotExistError: В ситуации если заданный в output_dir путь не существует или не является каталогом.
        :raise PortionSizeLargerThanEntireArrayError: В ситуации если значение count_line превышает количество строк в исходном наборе данных.
        """
        self.file_format = file_format
        self.output_dir = output_dir
        self.df_length = len(dataframe)
        CountRowValidator(count_line, self.df_length)
        self.df = dataframe.copy(deep=True)
        self.file_name = file_name
        self.count_line = count_line
        self.count_file = math.ceil(self.df_length / self.count_line)

    def __save(self, df: pandas.DataFrame, path: str, **kwargs):
        match self.file_format:
            case "xlsx":
                df.to_excel(path, **kwargs)
            case "csv":
                df.to_csv(path, **kwargs)

    def grinding(self, **kwargs) -> None:
        """
        Нарезать текущий набор данных на заданное количество строк с сохранением результата в файлы.

        :param kwargs: Любые ключевые аргументы, которые поддерживаются методами DataFrame.to_csv() и DataFrame.to_excel()
        :return: None
        """

        for i in range(self.count_file):
            file_num = i + 1
            file_path = os.path.join(self.output_dir, f"{file_num}_{self.file_name}.{self.file_format}")
            batch = self.df.iloc[:self.count_line, :]
            self.__save(batch, file_path, **kwargs)
            self.df = self.df.iloc[self.count_line:, :]



