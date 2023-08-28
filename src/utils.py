"""
Утилиты проекта.
"""
import logging
from typing import Optional, Any
from urllib.error import HTTPError, URLError
from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url: str) -> Optional[Any]:
    """
    Получает ответ от вебприложения.
    :param session: кешированная сессия
    :param url: строка с url адресом
    :return: объект response
    """
    try:
        response = session.get(url, timeout=3)
        response.encoding = 'utf-8'
        return response
    except HTTPError:
        logging.exception(
            msg=f'{url}: страница не найдена.',
            stack_info=True
        )
    except URLError:
        logging.exception(
            msg=f'{url}: cервер не отвечает.',
            stack_info=True
        )
    except RequestException:
        logging.exception(
            msg=f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )
    raise SystemExit(f'URL адрес {url} недоступен.')


def find_tag(soup,
             tag: str = None,
             attrs: Any = None,
             string: str = None) -> Any:
    """
    Забирает содержимое тега из объекта BeautifulSoup
    :param soup: объект BeautifulSoup
    :param tag: опциональный аргумент - строка с тегом
    :param attrs: опциональные атрибуты тега
    :param string: опциональный аргумент - искомая строка в теге
    :return: объект BeautifulSoup
    """
    try:
        searched_tag = soup.find(tag, attrs=(attrs or {}), string=string)
        if searched_tag:
            return searched_tag
    except AttributeError:
        pass
    raise ParserFindTagException(f'Не найден тег {tag} {attrs} {string}')
