#!/usr/bin/env python3

import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import spellcorrector as spl
from Tests.tempfiles import TempFiles
import SpellCorrector.levenshtein_distance_counter as ldc


class Args:
    pass


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


class SpellCorrectorTests(unittest.TestCase):
    def test_default_write_mistakes(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            args = Args
            args.amount_of_mistakes = None
            args.coordinate = None
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args.infile = f1
                    args.outfile = f2
                    spl.write_mistakes(trie, args)
            correct_result = ["{'word': 'wiht'}", "{'word': 'mistakees'}",
                              "{'word': 'Isit'}"]
            assert_file_lines_with_list(self, output.name, correct_result)
            args.amount_of_mistakes = 1
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args.infile = f1
                    args.outfile = f2
                    spl.write_mistakes(trie, args)
            correct_result = ["{'word': 'wiht'}"]
            assert_file_lines_with_list(self, output.name, correct_result)

    def test_write_mistakes_without_mistakes(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text without mistakes', 'Is it a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'without',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            args = Args
            args.amount_of_mistakes = None
            args.coordinate = None
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args.infile = f1
                    args.outfile = f2
                    spl.write_mistakes(trie, args)
            correct_result = []
            assert_file_lines_with_list(self, output.name, correct_result)

    def test_default_mistake_iter(self):
        with TempFiles(2) as files:
            text = files[0]
            dictionary = files[1]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f:
                mistakes = [mistake for mistake in spl.mistake_iter(trie, f)]
            correct_result = [(10, 1, 'wiht'), (15, 1, 'mistakees'),
                              (0, 2, 'Isit')]
            self.assertListEqual(correct_result, mistakes)

    def test_mistake_iter_without_mistakes(self):
        with TempFiles(2) as files:
            text = files[0]
            dictionary = files[1]
            print_lines_to_file(
                ['Test text without mistakes', 'Is it a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'without',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f:
                mistakes = [mistake for mistake in spl.mistake_iter(trie, f)]
            correct_result = []
            self.assertListEqual(correct_result, mistakes)

    def test_mistake_iter_with_zero_length_text(self):
        with TempFiles(2) as files:
            text = files[0]
            dictionary = files[1]
            print_lines_to_file(
                ['test',
                 'text',
                 'without',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f:
                mistakes = [mistake for mistake in spl.mistake_iter(trie, f)]
            correct_result = []
            self.assertListEqual(correct_result, mistakes)

    def test_mistake_iter_with_line_breaks(self):
        with TempFiles(2) as files:
            text = files[0]
            dictionary = files[1]
            print_lines_to_file(
                ['Test text wiht mistak-', 'ees. Isit a mistake? -'],
                text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f:
                mistakes = [mistake for mistake in spl.mistake_iter(trie, f)]
            correct_result = [(10, 1, 'wiht'), (15, 1, 'mistakees'),
                              (5, 2, 'Isit')]
            self.assertListEqual(correct_result, mistakes)

    def test_mistake_iter_with_dashes(self):
        with TempFiles(2) as files:
            text = files[0]
            dictionary = files[1]
            print_lines_to_file(['Test text wi-ht mistak-ees',
                                 'Isit a mistake?'],
                                text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f:
                mistakes = [mistake for mistake in spl.mistake_iter(trie, f)]
            correct_result = [(10, 1, 'wi-ht'), (16, 1, 'mistak-ees'),
                              (0, 2, 'Isit')]
            self.assertListEqual(correct_result, mistakes)

    def test_default_try_to_find_missed_space(self):
        with TempFiles(1) as files:
            dictionary = files[0]
            print_lines_to_file(
                ['test',
                 'text',
                 'without',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
        self.assertEqual([('is', 'it')],
                         spl.try_to_find_missed_space(trie, 'isit'))
        self.assertEqual([('test', 'text')],
                         spl.try_to_find_missed_space(trie, 'testtext'))
        self.assertEqual([], spl.try_to_find_missed_space(trie, 'mistake'))
        self.assertEqual([], spl.try_to_find_missed_space(trie, ''))

    def test_default_print_mistake_in_format(self):
        with TempFiles(1) as files:
            with open(files[0].name, 'w', encoding='utf8') as f:
                args = Args
                args.coordinate = None
                args.outfile = f
                spl.print_mistake_in_format((0, 0, 'msitake'), args)
                spl.print_mistake_in_format((0, 0, 'yep'), args)
            correct_result = ["{'word': 'msitake'}",
                              "{'word': 'yep'}"]
            assert_file_lines_with_list(self, files[0].name, correct_result)

    def test_print_mistake_in_format_with_coordinates(self):
        with TempFiles(1) as files:
            with open(files[0].name, 'w', encoding='utf8') as f:
                args = Args
                args.coordinate = True
                args.outfile = f
                spl.print_mistake_in_format((10, 11, 'msitake'), args)
                spl.print_mistake_in_format((2, 1, 'yep'), args)
            correct_result = ["11:10 {'word': 'msitake'}",
                              "1:2 {'word': 'yep'}"]
            assert_file_lines_with_list(self, files[0].name, correct_result)

    def test_print_mistake_in_format_with_correction(self):
        with TempFiles(1) as files:
            with open(files[0].name, 'w', encoding='utf8') as f:
                args = Args
                args.coordinate = None
                args.outfile = f
                spl.print_mistake_in_format((10, 11, 'msitake'), args,
                                            ['mistake', 'mistakes'])
                spl.print_mistake_in_format((2, 1, 'yep'), args, ['???'])
            correct_result = \
                ["{'word': 'msitake', 'correction': ['mistake', 'mistakes']}",
                 "{'word': 'yep', 'correction': ['???']}"]
            assert_file_lines_with_list(self, files[0].name, correct_result)

    def test_print_mistake_in_format_with_correction_and_coordinates(self):
        with TempFiles(1) as files:
            with open(files[0].name, 'w', encoding='utf8') as f:
                args = Args
                args.coordinate = True
                args.outfile = f
                spl.print_mistake_in_format((10, 11, 'msitake'),
                                            args, ['mistake', 'mistakes'])
                spl.print_mistake_in_format((2, 1, 'yep'), args, ['???'])
            correct_result = \
                ["11:10 {'word': 'msitake',"
                 " 'correction': ['mistake', 'mistakes']}",
                 "1:2 {'word': 'yep', 'correction': ['???']}"]
            assert_file_lines_with_list(self, files[0].name, correct_result)

    def test_default_mispellings_corrector(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args = Args
                    args.infile = f1
                    args.outfile = f2
                    args.coordinate = None
                    args.typo_amount = 2
                    args.amount_of_corrections = 0
                    spl.mispellings_corrector(trie, args)
            correct_answer = ["{'word': 'wiht'}",
                              "{'word': 'mistakees'}",
                              "{'word': 'Isit'}"]
            assert_file_lines_with_list(self, output.name, correct_answer)

    def test_mispellings_corrector_without_mistakes(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text with mistakes', 'Is it a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args = Args
                    args.infile = f1
                    args.outfile = f2
                    args.coordinate = None
                    args.typo_amount = 2
                    args.amount_of_corrections = 0
                    spl.mispellings_corrector(trie, args)
            correct_answer = []
            assert_file_lines_with_list(self, output.name, correct_answer)

    def test_mispellings_corrector_with_coordinates(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args = Args
                    args.infile = f1
                    args.outfile = f2
                    args.coordinate = True
                    args.typo_amount = 2
                    args.amount_of_corrections = 0
                    spl.mispellings_corrector(trie, args)
            correct_answer = ["1:10 {'word': 'wiht'}",
                              "1:15 {'word': 'mistakees'}",
                              "2:0 {'word': 'Isit'}"]
            assert_file_lines_with_list(self, output.name, correct_answer)

    def test_mispellings_corrector_with_corrections(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args = Args
                    args.infile = f1
                    args.outfile = f2
                    args.coordinate = None
                    args.typo_amount = 2
                    args.amount_of_corrections = 100
                    spl.mispellings_corrector(trie, args)
            correct_answer = \
                ["{'word': 'wiht', 'correction': ['with', 'it']}",
                 "{'word': 'mistakees', 'correction': ['mistakes', 'mistake']}",
                 "{'word': 'Isit', 'correction': ['is it', 'is', 'it']}"]
            assert_file_lines_with_list(self, output.name, correct_answer)

    def test_mispellings_corrector_when_amount_of_corrections_less_than_mistakes_amount(self):
        with TempFiles(3) as files:
            text = files[0]
            dictionary = files[1]
            output = files[2]
            print_lines_to_file(
                ['Test text wiht mistakees', 'Isit a mistake?'], text.name)
            print_lines_to_file(
                ['test',
                 'text',
                 'with',
                 'mistakes', 'is', 'it', 'a', 'mistake'], dictionary.name)
            trie = ldc.load_dictionary(dictionary.name)
            with open(text.name, 'r', encoding='utf8') as f1:
                with open(output.name, 'w', encoding='utf8') as f2:
                    args = Args
                    args.infile = f1
                    args.outfile = f2
                    args.coordinate = None
                    args.typo_amount = 2
                    args.amount_of_corrections = 1
                    spl.mispellings_corrector(trie, args)
            correct_answer = ["{'word': 'wiht', 'correction': ['with', 'it']}",
                              "{'word': 'mistakees'}",
                              "{'word': 'Isit'}"]
            assert_file_lines_with_list(self, output.name, correct_answer)

    def test_default_detect_line_break(self):
        self.assertFalse(spl.detect_line_break('Typical string.'))
        self.assertFalse(spl.detect_line_break('String with dash bla-bla'))
        self.assertTrue(spl.detect_line_break('String with li-'))
        self.assertFalse(spl.detect_line_break('ne break'))
        self.assertFalse(spl.detect_line_break('-'))
        self.assertFalse('')

    def test_default_get_first_word_from_line(self):
        self.assertEqual('Typical',
                         spl.get_first_word_from_line('Typical string'))
        self.assertEqual('hey', spl.get_first_word_from_line('hey bro'))
        self.assertIsNone(spl.get_first_word_from_line('sd123'))
        self.assertIsNone(spl.get_first_word_from_line(''))
