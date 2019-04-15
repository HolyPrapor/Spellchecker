#!/usr/bin/env python3

import sys
import argparse
import re

if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(1)

try:
    from SpellCorrector import levenshtein_distance_counter as ldc
except Exception as e:
    print('SpellCorrector not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(2)

word_getter = re.compile(r"\w+'?-?\w+")


def write_mistakes(dictionary, args):
    mistakes = mistake_iter(dictionary, args.infile)
    for i in range(args.amount_of_mistakes):
        word = next(mistakes)
        if try_to_find_line_break(dictionary,
                                  word[0].group(0).casefold()) is not None:
            i -= 1
            continue
        print_mistake_in_format(word, args)


def mispellings_corrector(dictionary, args):
    mispellings = mistake_iter(dictionary, args.infile)
    mistakes_corrected = 0
    for mispelling in mispellings:
        word = mispelling[0].group(0)
        if try_to_find_line_break(dictionary,
                                  word.casefold()) is not None:
            continue
        if mistakes_corrected < args.amount_of_corrections:
            is_space_missed = try_to_find_missed_space(dictionary,
                                                       word.casefold())
            if is_space_missed is not None:
                print_mistake_in_format(
                    mispelling, args,
                    is_space_missed[0] + " " + is_space_missed[1])
                mistakes_corrected += 1
                continue
            possible_replacements = ldc.find_possible_replacements(
                dictionary, word.casefold(), args.typo_amount)
            if len(possible_replacements) > 0:
                print_mistake_in_format(mispelling,
                                        args, possible_replacements[0])
            else:
                print_mistake_in_format(mispelling, args, "???")
            mistakes_corrected += 1
        else:
            print_mistake_in_format(mispelling, args)


def print_mistake_in_format(mistake, args, correction=None):
    formatted_mistake = f"{mistake[0].group(0)}"
    if args.coordinate:
        formatted_mistake += \
            f" at line {mistake[1]} at index {mistake[0].start()}"
    if correction is not None:
        formatted_mistake += f" => {correction}"
    print(formatted_mistake, file=args.outfile)


def mistake_iter(dictionary, text):
    line_counter = 1
    for line in text:
        words = word_getter.finditer(line)
        for word in words:
            if not ldc.is_word_in_dictionary(dictionary,
                                             word.group(0).casefold()):
                yield (word, line_counter)
        line_counter += 1


def try_to_find_line_break(dictionary, word):
    word = word.casefold()
    line_break_index = word.find("-")
    while line_break_index >= 0:
        first_part = word[:line_break_index]
        second_part = word[line_break_index + 1:]
        if ldc.is_word_in_dictionary(dictionary, first_part) \
                and ldc.is_word_in_dictionary(dictionary, second_part):
            return first_part, second_part
        line_break_index = word.find("-", line_break_index + 1)
    return None


def try_to_find_missed_space(dictionary, word):
    word = word.casefold()
    for i in range(1, len(word)):
        first_part = word[:i]
        second_part = word[i:]
        if ldc.is_word_in_dictionary(dictionary, first_part) \
                and ldc.is_word_in_dictionary(dictionary, second_part):
            return first_part, second_part
    return None


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(
        description='Utility for spellchecking and spellcorrecting')
    parser.set_defaults(coordinate=False)
    subparsers = parser.add_subparsers(dest='Mode')
    subparsers.required = True
    parser_mispellings = subparsers.add_parser(
        'mispellings', help='Writes mispellings with possible correction')
    parser_mispellings.set_defaults(
        func=mispellings_corrector,
        amount_of_corrections=0)
    parser_mispellings.add_argument(
        '-correct', type=int,
        dest='amount_of_corrections',
        action='store',
        help='Plus corrects first N words')
    parser_mispellings.add_argument(
        '-coordinate', '-c', action='store_true',
        help='Plus writes a coordinate(Line and index)')
    parser_mistake_finder = subparsers.add_parser(
        'mistake_finder',
        help='Finds first N mistakes')
    parser_mistake_finder.set_defaults(
        func=write_mistakes)
    parser_mistake_finder.add_argument(
        'amount_of_mistakes', type=int)
    parser.set_defaults(
        infile=sys.stdin, outfile=sys.stdout,
        dictionary_file='Correct Dictionaries\\large.dic',
        typo_amount=3)
    parser.add_argument(
        '-infile',
        type=argparse.FileType('r', encoding='utf8'), default=sys.stdin,
        help='default - standard input')
    parser.add_argument(
        '-outfile',
        type=argparse.FileType('w'), default=sys.stdout,
        help='default - standard output')
    parser.add_argument(
        '-dict', dest='dictionary_file',
        help='Specifies dictionary file(default = large.dic)')
    parser.add_argument(
        '-typo', type=int, dest='typo_amount', action='store',
        help='Specifies amount of typos in word(default = 3)')
    return parser.parse_args()


def main():
    args = parse_args()
    dictionary = ldc.load_dictionary(args.dictionary_file)
    args.func(dictionary, args)


if __name__ == '__main__':
    main()
