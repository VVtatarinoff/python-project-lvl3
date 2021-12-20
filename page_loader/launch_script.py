#!/usr/bin/env python3
import os
import argparse
import sys
from page_loader import init_logger

from page_loader.loader import download
from page_loader.errors import MyError

current_path = os.getcwd()
ARGUMENTS = [[('-o', '--output'), {'metavar': '[dir]',
                                   'help': 'output dir'
                                   f'(default: {current_path})',
                                   'default': current_path, }],
             [('url', ), {'help': 'url link to website'}]]


def prepare_argparse_object():
    parser = argparse.ArgumentParser(usage='page-loader [options] <url>',
                                     prog='page_loader')
    for argument in ARGUMENTS:
        parser.add_argument(*argument[0], **argument[1])
    return parser


def main():
    logger = init_logger()
    logger.info("program started")
    args = prepare_argparse_object().parse_args()
    n = 0
    try:
        result = download(args.url, args.output)
    except MyError as e:
        print(f'unable to upload {args.url}')
        if e.args:
            msg = e.args[0]
            print(f'during execution the following error occurs "{msg}"')
        n = 1
        logger.exception(msg=f'Unable to download {args.url}')

    except Exception as e:
        logger.critical(f'program finished with  error {e}')
        n = 1
        raise Exception
    else:
        logger.info(f'program fininshed, recieved path {result}')
        print(f'page succesfully downloaded into {result}')
    sys.exit(n)


if __name__ == '__main__':
    main()
