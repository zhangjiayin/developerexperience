import glob
import logging
import logging.handlers
import config

LOG_FILENAME = config.RUNLOG
my_logger = logging.getLogger(config.LOGNAME)

my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=config.LOGSIZE, backupCount=5)
my_logger.addHandler(handler)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

def log(info):
    my_logger.debug(info)

if __name__ == "__main__":
    log("asdf")
