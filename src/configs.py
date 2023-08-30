"""
Конфигарутор проекта.
"""
import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from constants import BASE_DIR, LOG_FORMAT, DT_FORMAT


def configure_argument_parser(modes: dict.keys) -> Any:
    """
    Конфигурирует парсер аргументов командной строки.
    :param modes: аргументы парсера.
    :return: парсер
    """
    parser = argparse.ArgumentParser(
        description=('Парсер документации Python и Python Enhancement '
                     'Proposal (PEP)')
    )
    parser.add_argument(
        'mode',
        choices=modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    parser.add_argument(
        '-o',
        '--output',
        choices=('pretty', 'file'),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging() -> None:
    """
    Конфигурирует логирование.
    :return: None
    """
    # создаю директорию для логов
    log_dir: Path = Path.joinpath(BASE_DIR, 'logs')
    Path(log_dir).mkdir(exist_ok=True)
    # создаю путь для сохранения файла в директорию
    log_file: Path = Path.joinpath(log_dir, 'parser.log')

    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
