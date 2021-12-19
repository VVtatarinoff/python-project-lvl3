from page_loader.loader import download  # noqa F401
import logging
import sys


def init_logger():
    logger = logging.getLogger('page_loader')
    logger.setLevel(logging.DEBUG)
    sm = logging.StreamHandler(stream=sys.stderr)
    formatter = logging.Formatter('%(asctime)s :: %(name)s :'
                                  ': %(levelname)s :: %(message)s')
    sm.setFormatter(formatter)
    fn = logging.FileHandler('logs/page_loader.log', mode='w')
    fn.setFormatter(formatter)
    fn.setLevel('DEBUG')
    logger.addHandler(fn)
    sm.setLevel('CRITICAL')
    logger.addHandler(sm)
    return logger


__all__ = ('download', 'init_logger')
