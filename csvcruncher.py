
"""
CSVCruncher CLI
----------------
Утилита для обработки CSV-файлов из командной строки.

Поддерживает операции:
    - фильтрация
    - агрегация (avg, min, max, median)
    - сортировка
    - ограничение вывода (head).
"""

import csv
import argparse
import re
from statistics import mean, median
import tabulate


def parse_args():
    """
    Парсит аргументы командной строки.

    Returns:
        argparse.Namespace:
            Объект с атрибутами:
              - file (str): Путь к CSV файлу для обработки
              - head (int): Количество отображаемых записей
              - where (str, optional): Условие фильтрации по колонке
              - aggregate (str, optional): Операция агрегации по колонке
              - order_by (str, optional): Колонка для сортировки
    """
    parser = argparse.ArgumentParser(description="CSV Cruncher")
    parser.add_argument(
        "--file", required=True, help="Имя или путь к файлу для обработки"
    )
    parser.add_argument("--head", help="Количество отображаемых записей")
    parser.add_argument("--where", help="Фильтрация по условию - `column{=<>}value`")
    parser.add_argument(
        "--aggregate", help="Агрегация по уловию `column={min/max/avg}`"
    )
    parser.add_argument("--order-by", help="Сортировка по условию `column={desc/asc}`")
    return parser.parse_args()


def csv_reader(file_path: str) -> list[dict[str, str]] | None:
    """
    Читает данные из переданного csv-файла.

    :param str `file_name`: Имя файла или путь к нему
    :return `list[dict[str, str]]`: Извлеченные данные - список словарей со строками,
        где ключ-имя колонки, значение-соответствующее поле в строке.
    """
    try:
        with open(file_path, "r", encoding="utf8") as file:
            data = list(csv.DictReader(file))
        return data
    except Exception as e:
        print(f"Не удалось прочитать файл: {e}")
        return


def filter_by(data: list[dict[str, str]], condition: str) -> list[dict[str, str]]:
    """
    Фильтрует данные по указанной колонке и значению.

    Args:
        data (list[dict[str, str]]): Список словарей с данными
        expression (str): Выражение фильтрации, поддерживаемый формат "column{=<>}value"

    Returns:
        list[dict[str, str]]: Отфильтрованный список словарей
    """
    if "<" in condition:
        column, value = condition.split("<")
        if re.match(r"\d+\.*\d*", value):
            return [row for row in data if float(row[column]) < float(value)]
        else:
            return [row for row in data if row[column] < value]
    elif ">" in condition:
        column, value = condition.split(">")
        if re.match(r"\d+\.*\d*", value):
            return [row for row in data if float(row[column]) > float(value)]
        else:
            return [row for row in data if row[column] > value]
    elif "=" in condition:
        column, value = condition.split("=")
        if re.match(r"\d+\.*\d*", value):
            return [row for row in data if float(row[column]) == float(value)]
        else:
            return [row for row in data if row[column] == value]
    else:
        print("Операция не поддерживается или неправильный ввод!")
        return data


def aggregate(
    data: list[dict[str, str]], column: str, ops: str
) -> dict[str, str | float] | None:
    """
    Аггрегация по колонке.
    Доступные операции:
      - avg (среднее значение по колонке)
      - min (минимальное по колонке)
      - max (максимально по колонке)
      - median (медиана по колонке)

    Args:
        data (list[dict[str, str]]): Данные для обработки
        column (str): Имя колонки, по которой будем вычислять значение
        ops (str): Имя применяемой операции

    Returns:
        dict[str, str | float] | None:
    """
    if ops not in ("avg", "min", "max", "median"):
        print(f"Операция не поддерживается: {ops}")
        return

    try:
        values = [float(row[column]) for row in data]
    except Exception as e:
        print(f"Не удалось собрать значения по колонке: {e}")
        return

    match ops:
        case "avg":
            return {"column": column, "avg": round(mean(values), 2)}
        case "min":
            return {"column": column, "min": min(values)}
        case "max":
            return {"column": column, "max": max(values)}
        case "median":
            return {"column": column, "median": median(values)}


def sort_by(data: list[dict[str, str]], condition: str) -> list[dict[str, str]]:
    """
    Сортировка данных по колонке.

    Args:
        data (list[dict[str, str]]): Список словарей с данными
        column (str): Имя колонки для сортировки

    Returns:
        list[dict[str, str]]: Отсортированный список словарей
    """
    column, order = condition.split("=")
    match order:
        case "desc":
            return sorted(
                data,
                key=lambda row: (
                    float(row[column])
                    if re.match(r"\d+\.*\d*", row[column])
                    else row[column]
                ),
                reverse=True,
            )
        case "asc":
            return sorted(
                data,
                key=lambda row: (
                    float(row[column])
                    if re.match(r"\d+\.*\d*", row[column])
                    else row[column]
                ),
            )
        case _:
            print(f"Неизвестный параметр сортировки: {order}")
            return data

def cli():

    """
    Основная точка входа для командной строки.
    Обрабатывает аргументы, выполняет фильтрацию, сортировку, агрегацию и ограничение вывода (head).
    
    Порядок применения:
      1. Чтение данных из файла
      2. Фильтрация (--where)
      3. Сортировка (--order-by)
      4. Агрегация (--aggregate, завершает выполнение)
      5. Ограничение вывода (--head)
      6. Вывод результата в виде таблицы
    """
    args = parse_args()

    data = csv_reader(args.file)
    if not data:
        print("Нет данных для обработки")
        return

    result = data  # начальное значение

    if args.where:
        try:
            result = filter_by(result, args.where)  # ⬅ здесь и далее используем result
        except Exception as e:
            print(f"Ошибка выполнения операции фильтрации: {e}")
            return

    if args.order_by:
        try:
            result = sort_by(result, args.order_by)
        except Exception as e:
            print(f"Ошибка выполнения сортировки: {e}")
            return

    if args.aggregate:
        try:
            column, operation = args.aggregate.split("=")
            agg_result = aggregate(result, column.strip(), operation.strip())
            if agg_result:
                print(tabulate.tabulate([agg_result], headers="keys"))
            return  # агрегация финализирует вывод
        except Exception as e:
            print(f"Ошибка выполнения агрегации: {e}")
            return

    # Применяем head только после всех других операций
    if args.head:
        try:
            result = result[: int(args.head)]
        except Exception as e:
            print(f"Ошибка применения head: {e}")
            return

    # Выводим итоговую таблицу
    if result:
        print(tabulate.tabulate(result, headers="keys"))
    else:
        print("Нет данных для отображения")


if __name__ == "__main__":
    cli()
