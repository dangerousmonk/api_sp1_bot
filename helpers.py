import logging
import re


class TokenFormatter(logging.Formatter):
    """Прячем токен из логов"""
    @staticmethod
    def _filter(record):
        return re.sub(r'\/(.*?)\/', r'/hidden_data/', record)

    def format(self, record):
        original = logging.Formatter.format(self, record)
        return self._filter(original)
