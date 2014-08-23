#!/usr/bin/env python

"""
Unit Tets for util.py module.
"""

from unittest import main, TestCase
import sys
import os
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler.util.util import create_all_combinations

class UtilTests(TestCase):
    """
    Tests for generic functions from utils.
    """
    def test_create_all_combinations(self):
        """Tests for all combinations generator."""
        output = list(create_all_combinations([1,2,3]))
        expected = [[3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
        output.sort()
        expected.sort()
        self.assertEqual(output, expected)
        

if __name__ == '__main__':
    main()