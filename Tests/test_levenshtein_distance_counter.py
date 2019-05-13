#!/usr/bin/env python3

import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import SpellCorrector.levenshtein_distance_counter as ldc
from Tests.tempfiles import TempFiles


class LevenshteinDistanceTests(unittest.TestCase):
    def test_default_insert_word(self):
        some_string = 'test'
        trie = ldc.Trie()
        trie.insert_word(some_string)
        current_node = trie.root
        for letter in some_string:
            self.assertTrue(letter in current_node.children)
            current_node = current_node.children[letter]
        some_string = 'apple'
        trie.insert_word(some_string)
        current_node = trie.root
        for letter in some_string:
            self.assertTrue(letter in current_node.children)
            current_node = current_node.children[letter]

    def test_insert_word_when_word_is_already_inserted(self):
        some_string = 'test'
        trie = ldc.Trie()
        trie.insert_word(some_string)
        current_node = trie.root
        for letter in some_string:
            self.assertTrue(letter in current_node.children)
            current_node = current_node.children[letter]
        trie.insert_word(some_string)
        current_node = trie.root
        for letter in some_string:
            self.assertTrue(letter in current_node.children)
            current_node = current_node.children[letter]
        self.assertTrue(current_node.word)

    def test_default_is_word_in_dictionary(self):
        word = 'hello'
        trie = ldc.Trie()
        trie.insert_word(word)
        self.assertTrue(ldc.is_word_in_dictionary(trie, word))
        self.assertFalse(ldc.is_word_in_dictionary(trie, 'hi'))
        self.assertFalse(ldc.is_word_in_dictionary(trie, 'hell'))

    def test_default_find_possible_replacements(self):
        word = 'hellp'
        trie = ldc.Trie()
        trie.insert_word('hello')
        replacements = ldc.find_possible_replacements(trie, word, 1)
        self.assertTrue(('hello', 1) in replacements)
        self.assertEqual(1, len(replacements))
        trie.insert_word('hell')
        replacements = ldc.find_possible_replacements(trie, word, 1)
        self.assertTrue(('hell', 1) in replacements)
        self.assertEqual(2, len(replacements))

    def test_find_possible_replacements_without_replacements(self):
        word = 'hellp'
        trie = ldc.Trie()
        trie.insert_word('hello')
        replacements = ldc.find_possible_replacements(trie, word, 0)
        self.assertEqual(0, len(replacements))
        word = 'apple'
        replacements = ldc.find_possible_replacements(trie, word, 2)
        self.assertEqual(0, len(replacements))

    def test_find_possible_replacements_with_empty_string(self):
        trie = ldc.Trie()
        trie.insert_word('hello')
        trie.insert_word('help')
        trie.insert_word('a')
        replacements = ldc.find_possible_replacements(trie, '', 1)
        self.assertTrue(('a', 1) in replacements)
        self.assertEqual(1, len(replacements))

    def test_default_load_dictionary(self):
        with TempFiles(1) as files:
            tmp = files[0]
            with open(tmp.name, 'w') as f:
                print('apple', file=f)
                print('help', file=f)
            trie = ldc.load_dictionary(f.name)
        self.assertTrue(ldc.is_word_in_dictionary(trie, 'apple'))
        self.assertTrue(ldc.is_word_in_dictionary(trie, 'help'))
        self.assertFalse(ldc.is_word_in_dictionary(trie, 'hello'))

    def test_load_dictionary_without_words(self):
        with TempFiles(1) as files:
            tmp = files[0]
            trie = ldc.load_dictionary(tmp.name)
        self.assertFalse(ldc.is_word_in_dictionary(trie, 'apple'))
        self.assertFalse(ldc.is_word_in_dictionary(trie, 'help'))
