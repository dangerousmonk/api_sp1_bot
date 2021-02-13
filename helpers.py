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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
                'level': 'DEBUG',
                'handlers': [
                    'debug_rotating_file_handler',
                ]
             },
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['debug_rotating_file_handler'],
        }
    },
    'formatters': {
        'token': {
            '()': TokenFormatter,
            'format': '%(asctime)s, %(levelname)s, %(message)s, %(name)s',
        },
    },
    'handlers': {
        'debug_rotating_file_handler': {
            'level': 'DEBUG',
            'formatter': 'token',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'program.log',
            'mode': 'a',
            'maxBytes': 50000000,
            'backupCount': 5,
        },
    },
}
