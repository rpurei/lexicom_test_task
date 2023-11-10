DEBUG = True

LOG_FOLDER = 'logs'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
LOG_FILE = 'app.log'
LOG_MAX_BYTES = 1048576
LOG_COUNT = 10

APP_LOG_ERROR = 0
APP_LOG_WARN = 1
APP_LOG_INFO = 2

REDIS_URL = 'redis'
REDIS_PORT = 6379
