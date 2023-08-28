"""
Константы проекта.
"""
from pathlib import Path
from typing import Final

# путь до директории проекта
BASE_DIR: Final[Path] = Path(__file__).parent

# url адрес с документацией Python
MAIN_DOC_URL: Final[str] = 'https://docs.python.org/3/'

# url адрес с PEP
PEPS_URL: Final[str] = 'https://peps.python.org/'

# словарь статусов PEP: соответствие буквенных обозначений полным наименованиям
EXPECTED_STATUS: Final[dict[str:tuple]] = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

# формат даты и времени для сохранения файлов
DATETIME_FORMAT: Final[str] = '%Y-%m-%d_%H-%M-%S'

# формат логов
LOG_FORMAT: Final[str] = '%(asctime)s - [%(levelname)s] - %(message)s'

# формат даты и времени для логов
DT_FORMAT: Final[str] = '%d.%m.%Y %H:%M:%S'

# названия столбцов результирующих данных: парсер - колонки
RESULT_COLUMN_TITLES: Final[dict[str:tuple]] = {
    'whats_new': ('Ссылка на статью', 'Заголовок', 'Редактор, Автор'),
    'latest_versions': ('Ссылка на документацию', 'Версия', 'Статус'),
    'pep': ('Статус', 'Количество'),
}
