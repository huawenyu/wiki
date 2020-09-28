"""."""


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            #'format': '%(asctime)s [%(levelname)-4.4s] %(name)-12s.%(funcName)s: %(message)s',
            #'format': '[%(asctime)s] [%(levelname)-4.4s] [%(funcName)-18s]',
            #'format':  '[%(asctime)s] [%(levelname)-4.4s] %(name)-12s.%(funcName)-18s(): %(message)s',
            'format':  '[%(asctime)s] [%(levelname)-4.4s] %(name)s.%(funcName)s(): %(message)s',
            #'datefmt': '%Y-%m-%d %H:%M:%S',
            'datefmt': '%M:%S',
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },

        'console': {
            'level':       'INFO',
            'formatter':   'standard',
            'class':       'logging.StreamHandler',
            'stream':      'ext://sys.stdout',
        },

        'file': {
            'level':       'DEBUG',
            'formatter':   'standard',
            'class':       'logging.handlers.RotatingFileHandler',    # logging.FileHandler
            'filename':    '/tmp/pyscript.log',    # os.path.join(BASE_DIR, 'logs/database.log'
            'mode':        'a',
            'maxBytes':    5 * 1024 * 1024,
            'backupCount': 0,
            'encoding':    None,
            'delay':       False,
        },
    },

    'loggers': {
        # root logger: 'INFO', 'DEBUG'
        #   used when the <name> not exist here: logging.getLogger(<name>)
        '': {
            'level':     'INFO',  # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
            'handlers':  ['file', 'console'],
            'propagate': False
        },
    }
}


