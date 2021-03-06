#!/usr/bin/env python3
import argparse
import logging
import os
import sys

from page_loader.loader import download

current_path = os.getcwd()
ARGUMENTS = [[('-o', '--output'), {'metavar': '[dir]',
                                   'help': 'output dir'
                                   f'(default: {current_path})',
                                   'default': current_path, }],
             [('url', ), {'help': 'url link to website'}]]

logger = logging.getLogger(__name__)


def prepare_argparse_object():
    parser = argparse.ArgumentParser(usage='page-loader [options] <url>',
                                     prog='page_loader')
    for argument in ARGUMENTS:
        parser.add_argument(*argument[0], **argument[1])
    return parser


def main():
    logger.info("program started")
    args = prepare_argparse_object().parse_args()
    n = 0
    try:
        result = download(args.url, args.output)
    except Exception as e:
        print(f'unable to upload {args.url}')
        print(f'during execution the following error occurs: {e}')
        n = 1
        logger.exception(msg=f'Unable to download {args.url}')
    else:
        logger.info(f'program finished, received path {result}')
        print(f'page successfully downloaded into {result}')
    sys.exit(n)


if __name__ == '__main__':
    main()
