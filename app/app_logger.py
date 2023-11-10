from config import (LOG_FOLDER, LOG_FORMAT, LOG_FILE, LOG_MAX_BYTES, LOG_COUNT,
                    APP_LOG_ERROR, APP_LOG_WARN, APP_LOG_INFO)

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import traceback

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_formatter = logging.Formatter(LOG_FORMAT)
file_handler = RotatingFileHandler(os.path.join(LOG_FOLDER, LOG_FILE), maxBytes=LOG_MAX_BYTES, backupCount=LOG_COUNT)
file_handler.setFormatter(log_formatter)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def logger_output(message: str, debug_mode: bool, error_level: int):
    lf = '\n'
    if debug_mode is True:
        error_message = f'{traceback.format_exc().replace(lf, " ")} : {message}'
    else:
        error_message = f'{str(message)}'
    if error_level == APP_LOG_ERROR:
        logger.error(error_message)
    elif error_level == APP_LOG_WARN:
        logger.warning(f'{message}')
    elif error_level == APP_LOG_INFO:
        logger.info(error_message)
    else:
        logger.error('Unknown error level, check http_exception() function params')
