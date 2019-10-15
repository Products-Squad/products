# coding:utf-8

import os
import logging
import json
import datetime
import traceback
import logging.config
import sys
from flask.logging import default_handler
from app import app


class RobustFormatter(logging.Formatter):
    """
    Display Json format. The Json includes: { message, extra args }
    Regarding to exception, it will display few info (exception name, location, etc.)
    """

    def format(self, record):
        extra = record.__dict__
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Other formater will use the exception info, so don't cache it in
            # record.exc_text
            exc_text = self.formatException(record.exc_info)
            if s[-1:] != "\n":
                s = s + "\n"
            s = exc_text + s

        s = {
            "action": extra.get("action", "undefined"),
            "message": s,
            "process": extra.get("process", "undefined"),
            '@timestamp': datetime.datetime.utcnow().strftime(
                '%Y-%m-%dT%H:%M:%S.%fZ'),
            'levelname': extra.get("levelname", "undefined"),
        }
        if "schema" in extra:
            s["schema"] = extra["schema"]
        return json.dumps(s)

    def formatException(self, ei):
        type, value, tb = ei
        r = traceback.extract_tb(tb, limit=None)[-1]
        s = "Exception in file {} line {}, Reason: {} Message: ".format(
            r.filename, r.lineno, value)
        return s


def get_logger_settings(log_dir, console_output=True):
    logger_settings = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # For Normal log, info, debug, error...
            'logstash_log': {
                '()': "loggin.logger.RobustFormatter"
            },
            'debug': {
                'format': ('[%(asctime) - 6s]: %(name)s - %(levelname)s - '
                           '%(filename)s - %(funcName)s :\n'
                           '%(message)s;'),
                'datefmt': "%Y-%m-%d %H:%M:%S",
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'debug',
            },
            'info_file': {
                'level': 'INFO',
                'class': 'logging.handlers.WatchedFileHandler',
                'formatter': 'logstash_log',
                'filename': os.path.join(log_dir, 'info.log'),
            },
            'debug_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.WatchedFileHandler',
                'formatter': 'debug',
                'filename': os.path.join(log_dir, 'debug.log'),
            },
            'error_file': {
                'level': 'ERROR',
                'class': 'logging.handlers.WatchedFileHandler',
                'formatter': 'debug',
                'filename': os.path.join(log_dir, 'error.log'),
            },
        },
        'loggers': {
        },
        'root': {
            'handlers': ['info_file', 'debug_file', 'error_file'],
            'level': 'DEBUG',
        }
    }

    if console_output:
        logger_settings["root"]["handlers"].insert(0, "console")
    return logger_settings

# Setting up Logger


def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        dirname = os.path.join(os.getcwd(), "data/log/")
        #logging.config.dictConfig(get_logger_settings(dirname, True))
