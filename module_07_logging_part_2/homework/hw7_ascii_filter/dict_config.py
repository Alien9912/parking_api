dict_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'ascii_filter': {
            '()': 'filters.AsciiFilter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
            'filters': ['ascii_filter'],
        },
        'level_file': {
            'class': 'logger_helper.LevelFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'path_template': 'calc_{level}.log',
            'filters': ['ascii_filter'],
        },
        'utils_rotating': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': 'utils.log',
            'when': 'H',
            'interval': 1,
            'backupCount': 10,
            'filters': ['ascii_filter'],
        },
    },
    'loggers': {
        'app': {
            'level': 'DEBUG',
            'handlers': ['console', 'level_file'],
            'propagate': False,
        },
        'utils': {
            'level': 'DEBUG',
            'handlers': ['console', 'utils_rotating', 'level_file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
}