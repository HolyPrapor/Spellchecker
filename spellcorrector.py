#!/usr/bin/env python3

import sys
import argparse


if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(1)

try:
    from SpellCorrector import levenshtein_distance_counter
except Exception as e:
    print('SpellCorrector not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(2)


def write_mispellings(args):
    pass


def find_mistakes(args):
    pass


def try_to_find_line_break(args):
    pass


def try_to_find_missed_space(args):
    pass


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(
        description='Utility for spellchecking and spellcorrecting')
    parser.add_argument('infile', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='default - standard input')
    parser.add_argument('outfile', nargs='?',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='default - standard output')
    parser.add_argument('mistakes_amount', nargs='?', type=int, default=3,
                        help='Specifies amount of typos in word(default = 3)')
    subparsers = parser.add_subparsers()
    parser_mispellings = subparsers.add_parser(
        'mispellings', help='Writes mispellings with possible correction')
    parser_mispellings.set_defaults(func=write_mispellings)
    parser_mispellings.add_argument('-coordinate', '-c', nargs='?',
                                    help='Plus writes a coordinate(Line and index)')
    parser_mispellings.add_argument('amount_of_corrections', nargs='?', type=int,
                                    help='Plus corrects first N words')
    parser_mistake_finder = subparsers.add_parser('mistake_finder',
                                                  help='Finds first N mistakes')
    parser_mistake_finder.set_defaults(func=find_mistakes)
    parser_mistake_finder.add_argument('amount_of_mistakes', type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
