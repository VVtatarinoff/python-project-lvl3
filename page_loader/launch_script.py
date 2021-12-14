#!/usr/bin/env python3
import os
import argparse
import logging
import sys

from page_loader.loader import download

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


def main():
    logger = logging.getLogger('page_loader')
    logger.setLevel(logging.DEBUG)
    fn = logging.FileHandler('page_loader.log', mode='w')
    formatter = logging.Formatter('%(asctime)s :: %(name)s :'
                                  ': %(levelname)s :: %(message)s')
    fn.setFormatter(formatter)
    fn.setLevel('DEBUG')
    logger.addHandler(fn)
    sm = logging.StreamHandler(stream=sys.stdout)
    sm.setFormatter(formatter)
    sm.setLevel('DEBUG')
    logger.addHandler(sm)
    logger.info("program started")
    args = prepare_argparse_object().parse_args()
    result = download(args.site, args.output)
    logger.info(f'program fininshed, recieved path {result}')


if __name__ == '__main__':
    main()
