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


ring_logger = logging.getLogger(config.LOGNAME + "_RING")

ring_logger.setLevel(logging.DEBUG)
ring_handler = logging.handlers.RotatingFileHandler(
             config.RINGLOG, maxBytes=config.LOGSIZE, backupCount=5)
ring_logger.addHandler(ring_handler)
ring_formatter = logging.Formatter("%(asctime)s - %(message)s")
ring_handler.setFormatter(formatter)



def log(info):
    my_logger.debug(info)

def ring():
    ring_logger.debug('RING')
if __name__ == "__main__":
    log("asdf")
    log("asdf")
    log("asdf")  
    ring()
    ring()
    ring()
    ring()
    ring()
