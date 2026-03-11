# TODO переписать реализацию ini-файла в формате dict-конфигурации.
dict_config_ini = {
    'version': 1,
    'formatters': {
        'fileFormatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z',
        },
        'consoleFormatter': {
            'format': '%(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S%Z',
        },
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'consoleFormatter',
            'stream': 'ext://sys.stdout',
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'fileFormatter',
            'filename': 'logfile.log',
        },
    },
    'loggers': {
        'appLogger': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler'],
            'propagate': 0,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['consoleHandler'],
    },
}