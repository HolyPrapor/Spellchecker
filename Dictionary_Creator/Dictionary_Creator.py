#!/usr/bin/env python3

import sys
import regex

help = "Usage: Dictionary_Creator.py Mode Arguments [Encoding]\n" \
       "Modes:\n" \
       "Create: Creates a dictionary from given text. Arguments: input output\n" \
       "Merge: Merges two dictionaries into one. Arguments: first_dict second_dict output"

usage = "Usage: Dictionary_Creator.py Mode Arguments [Encoding]\n" \
        "Use Dictionary_Creator.py help for additional info"


splitter = regex.compile(r'[\W^0-9]+')


def parse_arguments(mode):
    if mode == 'Create':
        input = sys.argv[2]
        output = sys.argv[3]
        if sys.argv[4]:
            encoding = sys.argv[4]
        else:
            encoding = 'utf8'
        return input, output, encoding
    elif mode == 'Merge':
        first_file = sys.argv[2]
        second_file = sys.argv[3]
        output = sys.argv[4]
        if sys.argv[5]:
            encoding = sys.argv[5]
        else:
            encoding = 'utf8'
        return first_file, second_file, output, encoding


def get_words_from_text(file):
    words = set()
    for line in file:
        for word in filter(None, splitter.split(line)):
            words.add(word.lower())
    return words


def get_words_from_dict(file):
    words = set()
    for line in file:
        words.add(line)
    return words


def main():
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print(help)
        return
    mode = sys.argv[1]
    if mode == 'Create':
        input, output, encoding = parse_arguments(mode)
        with open(input, 'r', encoding=encoding) as f:
            words = get_words_from_text(f)
        with open(output, 'w', encoding=encoding) as f:
            for word in sorted(words):
                f.write(word + '\n')
    elif mode == 'Merge':
        first_file, second_file, output, encoding = parse_arguments(mode)
        with open(first_file, 'r', encoding=encoding) as f:
            dict1 = get_words_from_dict(f)
        with open(second_file, 'r', encoding=encoding) as f:
            dict2 = get_words_from_dict(f)
        dict1 = dict1.union(dict2)
        with open(output, 'w', encoding=encoding) as f:
            for word in sorted(dict1):
                f.write(word)
    else:
        print(usage)



if __name__ == '__main__':
    main()
