#!/usr/bin/env python3

import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from dictionary_creator import *


class TestTest(unittest.TestCase):
    def test_default_merge(self):
        pass

    def test_merge_with_zero_length_dict(self):
        pass

    def test_default_append(self):
        pass

    def test_append_with_zero_length_dict(self):
        pass

    def test_default_create(self):
        pass

    def test_create_with_zero_length_text(self):
        pass

    def test_default_get_words_from_dict(self):
        pass

    def test_default_get_words_from_text(self):
        pass

    def test_get_words_from_text_with_encoding(self):
        pass

    def test_get_words_from_text_with_no_text(self):
        pass

    def test_get_words_from_text_with_numbers(self):
        pass

    def test_default_is_not_none_or_number(self):
        pass

    def test_is_not_none_or_number_without_string(self):
        pass
