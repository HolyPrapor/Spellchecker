#!/usr/bin/env python3

import unittest
import os
import sys
from enum import Enum

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import dictionary_creator as dic_cr
from Tests.tempfiles import TempFiles


class Args:
    pass


class ArgsTypes(Enum):
    MERGE = 1
    APPEND = 2
    CREATE = 3


def print_lines_to_file(lines, filename):
    with open(filename, 'w', encoding='utf8') as f:
        for line in lines:
            print(line, file=f)


def assert_file_lines_with_list(self, filename, correct_result):
    with open(filename, 'r') as f:
        num_lines = sum(1 for line in f)
        f.seek(0)
        self.assertEqual(len(correct_result), num_lines)
        for index, result in enumerate(f):
            self.assertEqual(correct_result[index], result.rstrip())


def prepare_args(args_type, files):
    args = Args
    if args_type == ArgsTypes.MERGE:
        args.first_dict = files[0].name
        args.second_dict = files[1].name
        args.output_file = files[2].name
    elif args_type == ArgsTypes.APPEND:
        args.first_dict = files[0].name
        args.second_dict = files[1].name
    elif args_type == ArgsTypes.CREATE:
        args.text = files[0].name
        args.output_file = files[1].name
    return args


class DictionaryCreatorTests(unittest.TestCase):
    def test_default_merge(self):
        with TempFiles(3) as files:
            first_dict = files[0]
            print_lines_to_file(['apple', 'hello'], first_dict.name)
            second_dict = files[1]
            print_lines_to_file(['bobby'], second_dict.name)
            third_dict = files[2]
            args = prepare_args(ArgsTypes.MERGE, files)
            dic_cr.merge(args)
            correct_result = ['apple', 'bobby', 'hello']
            assert_file_lines_with_list(self, third_dict.name, correct_result)

    def test_merge_with_zero_length_dict(self):
        with TempFiles(3) as files:
            first_dict = files[0]
            print_lines_to_file(['apple', 'hello'], first_dict.name)
            third_dict = files[2]
            args = prepare_args(ArgsTypes.MERGE, files)
            dic_cr.merge(args)
            correct_result = ['apple', 'hello']
            assert_file_lines_with_list(self, third_dict.name, correct_result)

    def test_default_append(self):
        with TempFiles(2) as files:
            first_dict = files[0]
            print_lines_to_file(['apple', 'hello'], first_dict.name)
            second_dict = files[1]
            print_lines_to_file(['bobby'], second_dict.name)
            args = prepare_args(ArgsTypes.APPEND, files)
            dic_cr.append(args)
            correct_result = ['apple', 'bobby', 'hello']
            assert_file_lines_with_list(self, first_dict.name, correct_result)

    def test_append_with_zero_length_dict(self):
        with TempFiles(2) as files:
            first_dict = files[0]
            second_dict = files[1]
            print_lines_to_file(['bobby'], second_dict.name)
            args = prepare_args(ArgsTypes.APPEND, files)
            dic_cr.append(args)
            correct_result = ['bobby']
            assert_file_lines_with_list(self, first_dict.name, correct_result)

    def test_default_create(self):
        with TempFiles(2) as files:
            text = files[0]
            print_lines_to_file(
                ["This is test text.", 'I like python!'], text.name)
            output = files[1]
            args = prepare_args(ArgsTypes.CREATE, files)
            args.encoding = 'utf8'
            dic_cr.create(args)
            correct_result = sorted(['this', 'is', 'test', 'text', 'i',
                                     'like', 'python'])
            assert_file_lines_with_list(self, output.name, correct_result)

    def test_create_with_zero_length_text(self):
        with TempFiles(2) as files:
            output = files[1]
            args = prepare_args(ArgsTypes.CREATE, files)
            args.encoding = 'utf8'
            dic_cr.create(args)
            correct_result = []
            assert_file_lines_with_list(self, output.name, correct_result)

    def test_default_get_words_from_dict(self):
        with TempFiles(1) as files:
            print_lines_to_file(['apple', 'bobby', 'hello'], files[0].name)
            correct_result = {'apple', 'bobby', 'hello'}
            with open(files[0].name, 'r') as f:
                result = dic_cr.get_words_from_dict(f)
            self.assertSetEqual(correct_result, result)

    def test_default_get_words_from_text(self):
        with TempFiles(1) as files:
            print_lines_to_file(['Hi baby', 'How are', 'you?'], files[0].name)
            correct_result = {'hi', 'baby', 'how', 'are', 'you'}
            with open(files[0].name, 'r') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_get_words_from_text_with_encoding(self):
        with TempFiles(1) as files:
            with open(files[0].name, 'w', encoding='cp1251') as f:
                print('Привет', file=f)
                print('как', file=f)
                print('дела?', file=f)
            correct_result = {'привет', 'как', 'дела'}
            with open(files[0].name, 'r', encoding='cp1251') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_get_words_from_text_with_no_text(self):
        with TempFiles(1) as files:
            correct_result = set()
            with open(files[0].name, 'r') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_get_words_from_text_with_numbers(self):
        with TempFiles(1) as files:
            print_lines_to_file(
                ['Прив8ет', 'как', 'дела?', '8 9123 8-800-555-35-35'],
                files[0].name)
            correct_result = {'как', 'дела'}
            with open(files[0].name, 'r', encoding='utf8') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_default_is_not_none_or_number_or_dash(self):
        self.assertTrue(dic_cr.is_not_none_or_number_or_dash('TestString'))
        self.assertFalse(dic_cr.is_not_none_or_number_or_dash(''))
        self.assertFalse(dic_cr.is_not_none_or_number_or_dash('1512'))
        self.assertFalse(dic_cr.is_not_none_or_number_or_dash('15twitter.com'))
        self.assertTrue(dic_cr.is_not_none_or_number_or_dash(
            'WhatDoYouThinkAboutMyTests'))
        self.assertFalse(dic_cr.is_not_none_or_number_or_dash('-'))

    def test_default_add(self):
        with TempFiles(1) as files:
            dictionary = files[0]
            print_lines_to_file(['apple', 'hello'], dictionary.name)
            args = Args
            args.dict = dictionary.name
            args.word = 'mango'
            dic_cr.add(args)
            correct_result = sorted(['apple', 'mango', 'hello'])
            assert_file_lines_with_list(self, dictionary.name, correct_result)

    def test_add_with_wrong_word(self):
        with TempFiles(1) as files:
            dictionary = files[0]
            print_lines_to_file(['apple', 'hello'], dictionary.name)
            args = Args
            args.dict = dictionary.name
            args.word = 'lsakdf====--://'
            dic_cr.add(args)
            correct_result = ['apple', 'hello']
            assert_file_lines_with_list(self, dictionary.name, correct_result)

    def test_default_get_words_from_text_with_line_breaks(self):
        with TempFiles(1) as files:
            text = files[0]
            print_lines_to_file(
                ['Hey Boys how are you do-', 'ing today?'], text.name)
            correct_result = {'hey', 'boys', 'how', 'are', 'you', 'doing',
                              'today'}
            with open(files[0].name, 'r', encoding='utf8') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_get_words_from_text_with_dashes(self):
        with TempFiles(1) as files:
            text = files[0]
            print_lines_to_file(['Hey Boys bla-bla how are you do-',
                                 'ing today? I fee-',
                                 'l yourself very good. Hey -'],
                                text.name)
            correct_result = {'bla-bla', 'hey', 'boys', 'how', 'are',
                              'you', 'doing', 'today', 'i',
                              'feel', 'yourself', 'very', 'good'}
            with open(files[0].name, 'r', encoding='utf8') as f:
                result = dic_cr.get_words_from_text(f)
            self.assertSetEqual(correct_result, result)

    def test_default_detect_line_break(self):
        self.assertFalse(dic_cr.detect_line_break('Typical string.'))
        self.assertFalse(dic_cr.detect_line_break('String with dash bla-bla'))
        self.assertTrue(dic_cr.detect_line_break('String with li-'))
        self.assertFalse(dic_cr.detect_line_break('ne break'))
        self.assertFalse(dic_cr.detect_line_break('-'))
        self.assertFalse('')

    def test_default_get_first_word_from_line(self):
        self.assertEqual('Typical', dic_cr.get_first_word_from_line(
            'Typical string'))
        self.assertEqual('hey', dic_cr.get_first_word_from_line('hey bro'))
        self.assertIsNone(dic_cr.get_first_word_from_line('sd123'))
        self.assertIsNone(dic_cr.get_first_word_from_line(''))
