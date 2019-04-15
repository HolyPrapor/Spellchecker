#!/usr/bin/env python3

import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from spellcorrector import *


class TestTest(unittest.TestCase):
    def test_default_write_mistakes(self):
        pass

    def test_write_mistakes_without_mistakes(self):
        pass

    def test_default_mistake_iter(self):
        pass

    def test_mistake_iter_without_mistakes(self):
        pass

    def test_mistake_iter_with_zero_length_text(self):
        pass

    def test_default_try_to_find_line_break(self):
        pass

    def test_try_to_find_line_break_without_line_break(self):
        pass

    def test_default_try_to_find_missed_space(self):
        pass

    def test_try_to_find_missed_space_without_missed_space(self):
        pass

    def test_try_to_find_missed_space_with_empty_string(self):
        pass

    def test_default_print_mistake_in_format(self):
        pass

    def test_print_mistake_in_format_with_coordinates(self):
        pass

    def test_print_mistake_in_format_with_correction(self):
        pass

    def test_print_mistake_in_format_with_correction_and_coordinates(self):
        pass

    def test_print_mistake_in_format_with_empty_string(self):
        pass

    def test_default_mispellings_corrector(self):
        pass

    def test_mispellings_corrector_without_mistakes(self):
        pass

    def test_mispellings_corrector_with_coordinates(self):
        pass

    def test_mispellings_corrector_with_corrections(self):
        pass

    def test_mispellings_corrector_when_amount_of_corrections_less_than_mistakes_amount(self):
        pass
