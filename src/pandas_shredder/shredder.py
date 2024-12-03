import math
import os.path
from datetime import datetime
from typing import Literal, Optional

import pandas

from .component.validator import FileFormatValidator, DirectoryPathValidator, CountRowValidator

FileFormal = Literal["xlsx", "csv"]


class Shredder:
    extension = FileFormatValidator(allowed_formats=["xlsx", "csv"])
    directory = DirectoryPathValidator()

    def __init__(self, result_directory: str, file_format: FileFormal = "csv"):
        """
        Измельчитель DataFrame'ов Pandas.

        Позволяет некоторый набор данных разделить на несколько выходных файлов формата CSV / XLSX с заданным количеством строк.

        Для начала создайте экземпляр измельчителя и сохраните его в переменную:

        >>> shredder = Shredder(result_directory="C:\\Program Files", file_format="xlsx")

        Вызовете созданный экземпляр как функцию, передав соответствующие аргументы

        >>> import pandas as pd

        >>> df = pd.read_csv("C:\\Program Files\\test.csv")
        >>> shredder(dataframe=df, lines_per_serving=100, file_name="slice")

        Для сохранения данных в файлы, "под капотом" используются стандартные методы pandas:

        `to_excel()`_.

        `to_csv()`_.

        Через *args и **kwargs можно передать дополнительный параметры для этих методов.

        Например:

        >>> shredder(dataframe=df, lines_per_serving=100, file_name="slice", index=False, decimal=",")


        .. _to_excel(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
        .. _to_csv(): https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

        :param result_directory: Путь до каталога, в которой будут сохранены результирующие файлы
        :param file_format: Формат выходных файлов. Доступные варианты CSV, XLSX. По умолчанию CSV.
        :raise UnsupportedFileFormatError: В ситуации если в file_format задан не поддерживаемый формат файла.
        :raise DirectoryDoesNotExistError: В ситуации если заданный в result_directory путь не существует или не является каталогом.
        """
        self.extension = file_format
        self.directory = result_directory

    def __call__(self, dataframe: pandas.DataFrame, lines_per_serving: int, file_name: Optional[str] = None, *args, **kwargs) -> None:
        """
        Нарезать набор данных на файлы с заданным количеством строк в каждом.

        :param dataframe: Набор данных (pandas.DataFrame)
        :param lines_per_serving: Предельное количество строк в одном выходном файле
        :param file_name: Имя для выходного файла. К имени будет добавлен префикс с номером файла. Если имя файла не задано, будет сгенерировано имя по умолчанию, содержащее текущую дату и время.
        :param args: Произвольные позиционные аргументы, которые будут переданы методу to_excel(), to_csv() вызванному на pandas.DataFrame
        :param kwargs: Произвольные именованные аргументы, которые будут переданы методу to_excel(), to_csv() вызванному на pandas.DataFrame
        :raise LineLimitHasBeenExceededError: В ситуации если значение lines_per_serving превышает количество строк в исходном наборе данных.
        :raise NegativeNumberOfRowsError: В ситуации если значение lines_per_serving имеет отрицательное значение.
        :return:
        """
        dataframe_length = len(dataframe)
        # Валидируем количество строк в выходном файле
        CountRowValidator(lines_per_serving, dataframe_length)
        # Рассчитываем количество выходных файлов
        number_output_files = math.ceil(dataframe_length / lines_per_serving)
        buffer = dataframe.copy(deep=True)
        file = ".".join([file_name, self.extension]) if file_name else ".".join([self.__get_default_file_name(), self.extension])
        for i in range(number_output_files):
            file_num = i + 1
            file_path = os.path.join(self.directory, f"{file_num}_{file}")
            file_data = buffer.iloc[:lines_per_serving, :]
            match self.extension:
                case "xlsx":
                    file_data.to_excel(file_path, *args, **kwargs)
                case "csv":
                    file_data.to_csv(file_path, *args, **kwargs)
            buffer = buffer.iloc[lines_per_serving:, :]

    @staticmethod
    def __get_default_file_name() -> str:
        return f"Result {datetime.now().strftime('%d.%m.%Y %H-%M-%S')}"
