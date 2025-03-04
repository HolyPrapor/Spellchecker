#!/usr/bin/env python3

import sys
import argparse
import re
from pathlib import Path
import hashlib

if sys.version_info < (3, 6):
    print('Use python >= 3.6', file=sys.stderr)
    sys.exit(1)

try:
    from SpellCorrector import levenshtein_distance_counter as ldc
except Exception as e:
    print('SpellCorrector not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(2)

try:
    import dictionary_creator as dic_cr
except Exception as e:
    print('Dictionary Creator not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(3)

try:
    from Tests.tempfiles import TempFiles
except Exception as e:
    print('TempFiles module not found: "{}"'.format(e), file=sys.stderr)
    sys.exit(4)

WORD_GETTER = re.compile(r"\w+'?-?\w+")
SPLITTER = re.compile(r"[^\w']")
NUMBER = re.compile(r"[0-9]+")
DASH = re.compile(r"-")
LINE_BREAK_DETECTOR = re.compile(r"(\w+)-$")


class Args:
    pass


def replace_start_with_spaces(string, amount):
    return ' ' * amount + string[amount:]


def is_not_none_or_number_or_dash(string):
    return (string and not NUMBER.search(string)
            and not DASH.match(string))


def detect_line_break(string):
    line_break_word = LINE_BREAK_DETECTOR.search(string)
    if (line_break_word
            and is_not_none_or_number_or_dash(line_break_word.group(1))):
        return line_break_word
    return None


def get_first_word_from_line(string):
    first_word = WORD_GETTER.search(string)
    if first_word and is_not_none_or_number_or_dash(first_word.group(0)):
        return first_word.group(0)
    return None


def write_mistakes(dictionary, args):
    mistakes = mistake_iter(dictionary, args.infile)
    if not args.amount_of_mistakes:
        for mistake in mistakes:
            print_mistake_in_format(mistake, args)
    else:
        for i in range(args.amount_of_mistakes):
            word = next(mistakes, None)
            if word:
                print_mistake_in_format(word, args)


def mispellings_corrector(dictionary, args):
    mispellings = mistake_iter(dictionary, args.infile)
    mistakes_corrected = 0
    for mispelling in mispellings:
        word = mispelling[2]
        if mistakes_corrected < args.amount_of_corrections:
            is_space_missed = try_to_find_missed_space(
                dictionary, word.casefold())
            possible_replacements = []
            if is_space_missed:
                for missed_space in is_space_missed:
                    possible_replacements.append(
                        missed_space[0] + " " + missed_space[1])
            for replacement in ldc.find_possible_replacements(
                    dictionary, word.casefold(), args.typo_amount):
                possible_replacements.append(replacement[0])
            if possible_replacements:
                print_mistake_in_format(
                    mispelling, args, possible_replacements)
            else:
                print_mistake_in_format(mispelling, args, ["???"])
            mistakes_corrected += 1
        else:
            print_mistake_in_format(mispelling, args)


def print_mistake_in_format(mistake, args, correction=None):
    formatted_mistake = ""
    if args.coordinate:
        formatted_mistake += f"{mistake[1]}:{mistake[0]} "
    formatted_mistake += f"{{'word': '{mistake[2]}'"
    if correction:
        formatted_mistake += f", 'correction': {str(correction)}"
    formatted_mistake += "} "
    print(formatted_mistake, file=args.outfile)


def mistake_iter(dictionary, text):
    line_break_word = None
    for (line_counter, line) in enumerate(text):
        line = line.strip()
        if line_break_word:
            first_word = get_first_word_from_line(line)
            if first_word:
                line = replace_start_with_spaces(line, len(first_word))
            if (not first_word or
                    not ldc.is_word_in_dictionary(
                        dictionary, line_break_word.group(1).casefold())):
                yield (line_break_word.start(),
                       line_counter, line_break_word.group(1) + first_word)
        line_break_word = detect_line_break(line)
        if line_break_word:
            line = line[:-(len(line_break_word.group(1)) + 2)]
        for word in WORD_GETTER.finditer(line):
            if not ldc.is_word_in_dictionary(
                    dictionary, word.group(0).casefold()):
                yield (word.start(), line_counter + 1, word.group(0))


def try_to_find_missed_space(dictionary, word):
    word = word.casefold()
    answer = []
    for i in range(1, len(word)):
        first_part = word[:i]
        second_part = word[i:]
        if (ldc.is_word_in_dictionary(dictionary, first_part) and
                ldc.is_word_in_dictionary(dictionary, second_part)):
            answer.append((first_part, second_part))
    return answer


def parse_args():
    """Настройка argparse"""
    parser = argparse.ArgumentParser(
        description='Utility for spellchecking and spellcorrecting')
    parser.set_defaults(coordinate=False,
                        infile=sys.stdin, outfile=sys.stdout,
                        dictionary_file=(
                                Path("Correct Dictionaries/") / 'large.dic'),
                        typo_amount=3)
    parser.add_argument(
        '--infile',
        type=argparse.FileType('r', encoding='utf8'), default=sys.stdin,
        help='default - standard input')
    parser.add_argument(
        '--outfile',
        type=argparse.FileType('w'), default=sys.stdout,
        help='default - standard output')
    parser.add_argument(
        '--dict', dest='dictionary_file',
        help='Specifies dictionary file(default = large.dic)')
    parser.add_argument(
        '--typo', type=int, dest='typo_amount', action='store',
        help='Specifies amount of typos in word(default = 3)')

    subparsers = parser.add_subparsers(dest='Mode')
    subparsers.required = True

    parser_mispellings = subparsers.add_parser(
        'mispellings', help='Writes mispellings with possible correction')
    parser_mispellings.set_defaults(
        func=mispellings_corrector,
        amount_of_corrections=0)
    parser_mispellings.add_argument(
        '--correct', type=int,
        dest='amount_of_corrections',
        action='store',
        help='Plus corrects first N words')
    parser_mispellings.add_argument(
        '--coordinate', '-c', action='store_true',
        help='Plus writes a coordinate(Line and index)')

    parser_mistake_finder = subparsers.add_parser(
        'mistake_finder',
        help='Finds first N mistakes')
    parser_mistake_finder.set_defaults(
        func=write_mistakes)
    parser_mistake_finder.add_argument(
        'amount_of_mistakes', type=int, nargs='?')
    return parser.parse_args()


def is_dictionary(filename):
    dict_hash = md5(filename)
    with TempFiles(1) as files:
        args = Args
        args.first_dict = files[0].name
        args.second_dict = filename
        dic_cr.append(args)
        new_dict_hash = md5(files[0].name)
    return new_dict_hash == dict_hash


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def main():
    args = parse_args()
    if is_dictionary(args.dictionary_file):
        dictionary = ldc.load_dictionary(args.dictionary_file)
    else:
        print("Dictionary is in wrong format")
        sys.exit(5)
    args.func(dictionary, args)


if __name__ == '__main__':
    main()
