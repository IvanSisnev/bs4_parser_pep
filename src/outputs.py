"""
Обработку выходных данных
"""
import csv
import datetime
import logging
from pathlib import Path
from typing import Any

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def default_output(results: list) -> None:
    """
    Выводит результирующие данные в терминал.
    :param results: список с результирующими данными.
    :return: None
    """
    for row in results:
        print(*row)


def pretty_output(results: list) -> None:
    """
    Выводит результирующие данные в терминал в виде таблицы.
    :param results: список с результирующими данными.
    :return: None
    """
    table = PrettyTable()
    # забираю названия столбцов из первого кортежа списка
    column_titles = results[0]
    table.field_names = column_titles
    table.align = 'l'
    # вырваниваю числовые значения по правому краю
    if 'Количество' in column_titles:
        table.align['Количество'] = 'r'
    # добавляю все записи из кортежей, начиная со 2-го.
    table.add_rows(results[1:])
    print(table)


def file_output(results: list, cli_args) -> None:
    """
    Сохраняет результирующие данные в формате csv.
    :param results: список с результирующими данными.
    :param cli_args: аргументы командной строки.
    :return: None
    """
    # создаю директория для сохранения файла
    results_dir: Path = Path.joinpath(BASE_DIR, 'results')
    Path(results_dir).mkdir(exist_ok=True)

    # определяю имя файла и путь для его сохранения
    current_date_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    file_name = f'{cli_args.mode}_{current_date_time}.csv'
    results_path: Path = Path.joinpath(results_dir, file_name)

    try:
        with open(results_path, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='unix')
            writer.writerows(results)

        logging.info(msg=f'Файл с результатами был сохранён: {results_path}')
        return None
    except IOError as exc:
        error_msg: str = ('Не удалось записать файл с результирующими '
                          f'данными парсера {cli_args.mode}.')
        logging.exception(msg=error_msg, stack_info=True)
        raise SystemExit(error_msg) from exc


def control_output(results: list, cli_args) -> Any:
    """
    Определяет обработчик выходных данных по переданному аргументу.
    :param results: список с результирующими данными.
    :param cli_args: аргументы командной строки.
    :return: функция, соответсвующая аргументу
    """
    output = cli_args.output
    # вывод в терминал в табличном виде
    if output == 'pretty':
        return pretty_output(results)
    # сохранение в файл
    if output == 'file':
        return file_output(results, cli_args)
    # стандартный вывод в терминал
    return default_output(results)
