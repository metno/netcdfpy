import sys
import logging


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

def error(message):
    logger = logging.getLogger('root')
    logger.error(message)

    """ Write error message to console and abort """
    print "\033[1;31mError: " + message + "\033[0m"
    sys.exit(1)

def log(level,message):
    logger = logging.getLogger('root')
    logger.log(level,message)

    #TODO Set this globally
    if level <= 1:
        """ Write a information message to console """
        print "\033[1;92mLEVEL"+str(level)+": " + message + "\033[0m"

def info(message):
    logger = logging.getLogger('root')
    logger.info(message)

    """ Write a information message to console """
    print "\033[1;92mINFO: " + message + "\033[0m"

def warning(message):
    logger = logging.getLogger('root')
    logger.warning(message)

    """ Write a warning message to console """
    print "\033[1;33mWarning: " + message + "\033[0m"

