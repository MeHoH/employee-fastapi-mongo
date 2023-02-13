from datetime import date
from os import getenv
from functools import wraps
from logging import getLogger

LOGGING_LEVEL = getenv('LOGGING_LEVEL', 'DEBUG')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': f'./logs/debug-{date.today().strftime("%Y-%m-%d")}.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },

    'loggers': {
        'logger_file': {
            'handlers': ['file', ],
            'level': 'INFO',
            'propagate': True
        },
        '': {
            'handlers': ['console', ],
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    'logger_console': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': ['console', ],
    },
}

logger = getLogger('python-logstash-logger')
logger.setLevel(LOGGING_LEVEL)


def log_error():
    def error_log(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = f'Error has occurred at func="{func.__name__}" with args={args} and kwargs={kwargs}\n\n'
                logger.exception(error_msg)
                return e

        return wrapper

    return error_log


def log_func():
    def func_log(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            msg = f'func="{func.__name__}" with args={args} and kwargs={kwargs}\n\n'
            logger.debug(msg)
            return func(*args, **kwargs)

        return wrapper

    return func_log
