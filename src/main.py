"""
Главный файл проекта.
"""
from urllib.parse import urljoin
from pathlib import Path
from typing import Final, Optional, Any
import re
import logging
from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, MAIN_DOC_URL, PEPS_URL, EXPECTED_STATUS,
                       RESULT_COLUMN_TITLES)
from outputs import control_output
from utils import get_response, find_tag
from exceptions import EmptyTagsList


def whats_new(session: object) -> Optional[list]:
    """
    Собирает url адреса статей про обновления в последних версиях Питона,
    названия статей и их автора.
    :param session: кешированная сессия.
    :return: список кортежей с данными.
    """
    whats_new_url: str = urljoin(MAIN_DOC_URL, 'whatsnew/')

    response = get_response(session, whats_new_url)

    soup = BeautifulSoup(response.text, features='lxml')

    # забираю главный раздел
    main_div = find_tag(soup,
                        tag='section',
                        attrs={'id': 'what-s-new-in-python'})
    # забираю список новостей обновлений
    div_with_ul = find_tag(main_div,
                           tag='div',
                           attrs={'class': 'toctree-wrapper'})
    # забираю главные пункты
    tag: str = 'li'
    sections_by_python = div_with_ul.find_all(tag,
                                              attrs={'class': 'toctree-l1'})
    if not sections_by_python:
        raise EmptyTagsList(f'{whats_new_url}: в ходе парсинга не найдены '
                            f'теги {tag}.')

    # список для сохранения информации, первый кортеж - имена столбцов для
    # вывода в табличном виде
    results: list[tuple] = [RESULT_COLUMN_TITLES['whats_new'], ]

    for section in tqdm(sections_by_python):
        # забираю из списка url адреса обновлений
        version_a_tag = find_tag(section, tag='a')
        href: str = version_a_tag['href']
        version_link: str = urljoin(whats_new_url, href)

        response = get_response(session, version_link)

        soup = BeautifulSoup(response.text, features='lxml')
        # сохраняю в список url адрес, название обновления и его автора
        title = find_tag(soup, tag='h1').text.rstrip('¶')
        author = find_tag(soup, tag='dl').p.text
        results.append((version_link, title, author))

    return results


def latest_versions(session) -> Optional[list]:
    """
    Собирает url адреса последних версий Питона, их номера и статус.
    :param session: кешированная сессия.
    :return: список кортежей с данными
    """
    response = get_response(session, MAIN_DOC_URL)

    soup = BeautifulSoup(response.text, features='lxml')

    # забираю боковое меню
    sidebar = find_tag(soup, tag='div', attrs={'class': 'menu-wrapper'})
    # забираю подпункт, который касается документации версий
    docs_by_version_ul = find_tag(sidebar, tag='a',
                                  string='All versions').find_parent('ul')
    # забираю теги с информацией по каждой версии
    tag: str = 'a'
    a_tags = docs_by_version_ul.find_all(tag)
    if not a_tags:
        raise EmptyTagsList(f'{MAIN_DOC_URL}: в ходе парсинга не найдены '
                            f'теги {tag}.')

    # строка для поиска номера версии и ее статуса
    pattern: str = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    # список для сохранения информации, первый кортеж - имена столбцов для
    # вывода в табличном виде
    results: list[tuple] = [RESULT_COLUMN_TITLES['latest_versions'], ]
    for a_tag in a_tags:
        link = a_tag['href']
        version_status = re.search(pattern, a_tag.text)
        # если есть номер версии и ее статус, помещаю их в список
        version: str
        status: str
        if not version_status:
            version, status = a_tag.text, ''
        else:
            version, status = version_status.groups()

        results.append((link, version, status, ))

    return results


def download(session) -> None:
    """
    Скачивает архив документации в формате пдф текущей версии Питона.
    :param session: кешированная сессия
    :return: None
    """
    downloads_url: str = urljoin(MAIN_DOC_URL, 'download.html')

    response = get_response(session, downloads_url)

    soup = BeautifulSoup(response.text, features='lxml')

    # забираю таблицу со ссылками на скачивание
    table = find_tag(soup, tag='table', attrs={'class': 'docutils'})
    # искомый файл - архив в формате пдф размера А4
    pattern: str = r'.+pdf-a4\.zip$'
    # забираю ссылку и создаю путь до нужного архива
    pdf_a4_tag = find_tag(table, tag='a', attrs={'href': re.compile(pattern)})
    archive_url: str = urljoin(downloads_url, pdf_a4_tag['href'])

    # забираю имя файла для сохранения
    file_name: str = Path(archive_url).name
    # создаю директорию для сохраняемого файла
    downloads_dir: Path = Path.joinpath(BASE_DIR, 'downloads')
    Path(downloads_dir).mkdir(exist_ok=True)
    # создаю путь для сохранения файла в директорию
    archive_path: Path = Path.joinpath(downloads_dir, file_name)

    # скачиваю и сохраняю файл
    response = get_response(session, archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(msg=f'Архив был загружен и сохранён: {archive_path}')


def pep(session) -> Optional[list]:
    """
    Собирает статусы всех PEP, подсчитывает количество PEP в каждом статусе
    и общее количество PEP.
    :param session: кешированная сессия.
    :return: список кортежей с данными.
    """
    response = get_response(session, PEPS_URL)

    soup = BeautifulSoup(response.text, features='lxml')

    # забираю раздел со всеми PEP
    all_peps_table = find_tag(soup,
                              tag='section',
                              attrs={'id': 'numerical-index'}).tbody
    # собираю все PEP в список
    tag: str = 'tr'
    all_peps_list: list = all_peps_table.find_all(tag)
    if not all_peps_list:
        raise EmptyTagsList(f'{PEPS_URL}: в ходе парсинга не найдены '
                            f'теги {tag}.')

    # словарь для подсчета количества PEP каждого статуса
    pep_statuses_totals: dict[str:int] = {}

    # прохожу по списку PEP со статусбаром
    for a_pep in tqdm(all_peps_list):

        # забираю аббревиатуру статуса
        status_abbr = find_tag(a_pep, tag='abbr').text
        status_abbr = status_abbr[-1] if len(status_abbr) > 1 else ''

        # определяю url адрес страницы PEP
        pep_info = find_tag(a_pep,
                            tag='a',
                            attrs={'class': 'pep reference internal'})
        pep_path: str = urljoin(PEPS_URL, pep_info['href'])

        # забираю данные со страницы PEP
        response = get_response(session, pep_path)
        soup = BeautifulSoup(response.text, features='lxml')

        # забираю статус PEP из основной информации о нем
        pep_info = find_tag(soup, tag='dl')
        status: str = find_tag(
            pep_info,
            string='Status',
        ).find_parent().find_next_sibling().abbr.text

        # сравниваю статус со страницы с буквенным стасум из общей таблицы
        if status not in EXPECTED_STATUS[status_abbr]:
            pep_title: str = find_tag(pep_info, tag='abbr')['title']
            logging.warning(
                msg=(
                    f'Несовпадающие статусы {pep_title} по адресу {pep_path}:'
                    f'\nстатус на странице {status}'
                    f'\nстатус в таблице {EXPECTED_STATUS[status_abbr]}')
            )
        # обновляю количество в соответствующем статусе
        if status in pep_statuses_totals:
            pep_statuses_totals[status] += 1
        else:
            pep_statuses_totals[status]: int = 1

    # список кортежей для заполнения результатами
    results: list[tuple] = []
    # добавляю в список кортежи: статус и его количество
    for status, quantity in pep_statuses_totals.items():
        results.append((status, quantity))
    results.sort()
    # вставляю заголовки столбцов и общее количество PEP
    results.insert(0, RESULT_COLUMN_TITLES['pep'])
    results.append(('Итого', sum(pep_statuses_totals.values())))

    return results


# Аргументы парсера: имя аргумента и соответствующая ему фукнция
MODE_TO_FUNCTION: Final[dict[str, Any]] = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main() -> None:
    """
    Точка входа. Забирает аргумент через парсер командной строки и вызывает
    соответствующую аргументу функцию. Полученный результат передает функции
    вывода информации.
    :return: None
    """
    # конфигурирую логи
    configure_logging()
    logging.info(msg='Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(msg=f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    # в зависимости от mode обращаюсь к функции, проверяю наличие
    # результирующих данных и перенаправляю результаты в функцию, отвечающую
    # за output
    results: list[tuple] = MODE_TO_FUNCTION[args.mode](session)
    logging.info(msg='Аргументы переданы в функцию.')
    if len(results) <= 2:
        error_msg = (f'Не удалось получить результирующие данные от парсера'
                     f' {args.mode}.')
        logging.exception(msg=error_msg, stack_info=True)
        raise SystemExit(error_msg)
    logging.info(msg='Результирующие данные получены.')
    control_output(results, args)
    logging.info(msg='Парсер завершил работу.')


if __name__ == '__main__':
    main()
