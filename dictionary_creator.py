#!/usr/bin/env python3

import argparse
import sys
import re

splitter = re.compile(r"[^\w'-]")
number = re.compile(r"[0-9]+")
dash = re.compile(r"-")
line_break_detector = re.compile(r"(\w+)-$")
word_getter = re.compile(r"^\w+")


def is_not_none_or_number_or_dash(string):
    return string and not number.search(string) and not \
        dash.match(string)


def detect_line_break(string):
    line_break_word = line_break_detector.search(string)
    if line_break_word and is_not_none_or_number_or_dash(line_break_word.group(1)):
        return line_break_word.group(1)
    return None


def get_first_word_from_line(string):
    first_word = word_getter.search(string)
    if first_word and is_not_none_or_number_or_dash(first_word.group(0)):
        return first_word.group(0)
    return None


def get_words_from_text(file):
    words = set()
    line_break_word = None
    for line in file:
        if line_break_word:
            first_word = get_first_word_from_line(line)
            if first_word:
                line = line[len(first_word):]
                line_break_word += first_word
                words.add(line_break_word.casefold())
        line_break_word = detect_line_break(line)
        if line_break_word:
            line = line[:-(len(line_break_word) + 2)]
        for word in filter(is_not_none_or_number_or_dash, splitter.split(line)):
            words.add(word.casefold())
    return words


def get_words_from_dict(file):
    return {word.rstrip() for word in file}


def create(args):
    with open(args.text, 'r', encoding=args.encoding) as f:
        words = get_words_from_text(f)
    with open(args.output_file, 'w', encoding='utf8') as f:
        for word in sorted(words):
            print(word, file=f)


def merge(args):
    with open(args.first_dict, 'r', encoding='utf8') as f:
        dict1 = get_words_from_dict(f)
    with open(args.second_dict, 'r', encoding='utf8') as f:
        dict2 = get_words_from_dict(f)
    with open(args.output_file, 'w', encoding='utf8') as f:
        for word in sorted(dict1 | dict2):
            print(word, file=f)


def append(args):
    args.output_file = args.first_dict
    merge(args)


def add(args):
    if splitter.search(args.word) or not is_not_none_or_number_or_dash(args.word):
        print("Given string is not a word")
        return
    with open(args.dict, 'r', encoding='utf8') as f:
        _dict = get_words_from_dict(f)
    _dict.add(args.word.casefold())
    with open(args.dict, 'w', encoding='utf8') as f:
        for word in sorted(_dict):
            print(word, file=f)


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(
        description='Utility for creating, appending, merging dictionaries')
    subparsers = parser.add_subparsers(dest='Mode')
    subparsers.required = True

    parser_add = subparsers.add_parser('add', help='Adds word to dictionary')
    parser_add.add_argument('word')
    parser_add.add_argument('dict')
    parser_add.set_defaults(func=add)

    parser_append = subparsers.add_parser(
        'append', help='Appends one dictionary to another')
    parser_append.add_argument('first_dict', help='First dictionary')
    parser_append.add_argument(
        'second_dict', help='Second dictionary(to be appended)')
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

    parser_merge.set_defaults(func=merge)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
