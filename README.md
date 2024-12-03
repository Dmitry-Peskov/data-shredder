# data-shredder
Пакет, предоставляющий интерфейс для нарезки Pandas.DataFrame на отдельные файлы с заданным количеством строк в каждом из них


Инициализируйте экземпляр измельчителя:

```python
from src.pandas_shredder import Shredder

shredder = Shredder(
    result_directory="C:\\Program Files",
    file_format="csv"
)
```
Далее вызовете его как функцию, передав в качестве аргументов:  
- **dataframe** - pandas.DataFrame который необходимо нарезать на файлы заданного размера
- **lines_per_serving** - максимально количество строк в одном выходном файле
- **file_name** - имя для выходных файлов. К каждому будет добавлен префикс с его номером.
- ***args**, ****kwargs** - опциональные настройки, которые будут переданы методу [df.to_csv()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html) / [df.to_excel()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html) в зависимости от выбранного формата выходного файла.

```python
import pandas as pd
from src.pandas_shredder import Shredder

# Создаём набор данных на основе произвольного большого файла
df = pd.read_excel("test.xlsx")
# Инициализируем измельчитель
shredder = Shredder(
    result_directory="C:\\Program Files",
    file_format="csv"
)
# Нарезаем набор данных на файлы csv по 1000 строк в каждом.
# Обратите внимание на дополнительные настройки (index, decimal, header), которые будут переданы методу to_csv()
shredder(
    dataframe=df,
    lines_per_serving=1000,
    file_name="test_1000_row",
    index=False,
    decimal=",",
    header=False
)
```
