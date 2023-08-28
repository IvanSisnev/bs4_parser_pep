"""
Кастомные исключения.
"""
import logging


class ParserFindTagException(Exception):
    """Кастомная ошибка не найденного HTML тега."""
    def __init__(self, error_msg):
        self.msg = error_msg
        logging.error(msg=self.msg, stack_info=True)


class EmptyTagsList(ParserFindTagException):
    """Кастомная ошибка не найденных HTML тегов - пустой список."""
