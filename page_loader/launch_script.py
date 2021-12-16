#!/usr/bin/env python3
import os
import argparse
import logging
import sys

from page_loader.loader import download
from page_loader.errors import MyError

current_path = os.getcwd()
ARGUMENTS = [[('-o', '--output'), {'metavar': '[dir]',
                                   'help': 'output dir (default: "/app")',
                                   'default': current_path, }],
             [('site', ), {'help': 'url link to website'}]]


def prepare_argparse_object():
    parser = argparse.ArgumentParser(usage='page-loader [options] <url>',
                                     prog='page_loader')
    for argument in ARGUMENTS:
        parser.add_argument(*argument[0], **argument[1])
    return parser


def init_logger():
    logger = logging.getLogger('page_loader')
    logger.setLevel(logging.DEBUG)
    fn = logging.FileHandler('logs/page_loader.log', mode='w')
    formatter = logging.Formatter('%(asctime)s :: %(name)s :'
                                  ': %(levelname)s :: %(message)s')
    fn.setFormatter(formatter)
    fn.setLevel('DEBUG')
    logger.addHandler(fn)
    sm = logging.StreamHandler(stream=sys.stderr)
    sm.setFormatter(formatter)
    sm.setLevel('CRITICAL')
    logger.addHandler(sm)
    return logger


def main():
    logger = init_logger()
    logger.info("program started")
    args = prepare_argparse_object().parse_args()
    n = 0
    try:
        result = download(args.site, args.output)
    except MyError:
        # logger.critical(f'program finished with known error {MyError}')
        Error_class, Error_instanse, trace = sys.exc_info()
        # print(str(trace.tb_next))
        # print(sys.last_traceback)
        print(f'unable to upload {args.site}')
        n = 1
        logger.exception(msg=f'Unable to download {args.site}')

    except Exception:
        logger.critical(f'program finished with  error {Exception}')
        n = 1
        raise Exception
    else:
        logger.info(f'program fininshed, recieved path {result}')
        print(f'page succesfully downloaded into {result}')
    sys.exit(n)


if __name__ == '__main__':
    main()
