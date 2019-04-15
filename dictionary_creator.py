#!/usr/bin/env python3

import argparse
import sys
import re

splitter = re.compile(r"[^\w']")
number = re.compile(r"[0-9]+")


def is_not_none_or_number(string):
    if not string or number.match(string):
        return False
    return True


def get_words_from_text(file):
    return {word.casefold() for line in file
            for word in filter(is_not_none_or_number, splitter.split(line))}


def get_words_from_dict(file):
    return {word for word in file}


def create(args):
    with open(args.text, 'r', encoding=args.encoding) as f:
        words = get_words_from_text(f)
    with open(args.output_file, 'w', encoding=args.encoding) as f:
        for word in sorted(words):
            print(word, file=f)


def merge(args):
    with open(args.first_dict, 'r', encoding=args.encoding) as f:
        dict1 = get_words_from_dict(f)
    with open(args.second_dict, 'r', encoding=args.encoding) as f:
        dict2 = get_words_from_dict(f)
    dict1 = dict1.union(dict2)
    with open(args.output_file, 'w', encoding=args.encoding) as f:
        for word in sorted(dict1):
            print(word, file=f)


def append(args):
    with open(args.first_dict, 'r', encoding=args.encoding) as f:
        dict1 = get_words_from_dict(f)
    with open(args.second_dict, 'r', encoding=args.encoding) as f:
        dict2 = get_words_from_dict(f)
    dict1 = dict1.union(dict2)
    with open(args.first_dict, 'a', encoding=args.encoding) as f:
        for word in sorted(dict1):
            print(word, file=f)


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(
        description='Utility for creating, appending, merging dictionaries')
    subparsers = parser.add_subparsers(dest='Mode')
    subparsers.required = True
    parser_append = subparsers.add_parser(
        'append', help='Appends one dictionary to another')
    parser_append.add_argument('first_dict', help='First dictionary')
    parser_append.add_argument(
        'second_dict', help='Second dictionary(to be appended)')
    parser_append.add_argument('encoding', nargs='?', default='utf8')
    parser_append.set_defaults(func=append)
    parser_create = subparsers.add_parser(
        'create', help='Creates a dictionary from given text')
    parser_create.add_argument('text', help='Text file')
    parser_create.add_argument('output_file', help='File to store dictionary')
    parser_create.add_argument('encoding', nargs='?', default='utf8')
    parser_create.set_defaults(func=create)
    parser_merge = subparsers.add_parser(
        'merge', help='Merges two dictionaries and creates a new file')
    parser_merge.add_argument('first_dict', help='First dictionary')
    parser_merge.add_argument('second_dict', help='Second dictionary')
    parser_merge.add_argument('output_file', help='File to be stored in')
    parser_merge.add_argument('encoding', nargs='?', default='utf8')
    parser_merge.set_defaults(func=merge)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
