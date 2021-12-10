#!/usr/bin/env python3
import os
import argparse

from page_loader.loader import download

current_path = os.getcwd()
ARGUMENTS = [[('-out', '--output'), {'metavar': 'OUTPUT',
                                     'help': 'path to save output html file',
                                     'default': current_path, }],
             [('site', ), {'help': 'url link to website'}]]


def prepare_argparse_object():
    parser = argparse.ArgumentParser(description='page-loader',
                                     prog='page_loader')
    for argument in ARGUMENTS:
        parser.add_argument(*argument[0], **argument[1])
    return parser


def main():
    args = prepare_argparse_object().parse_args()
    download(args.site, args.output)


if __name__ == '__main__':
    main()
