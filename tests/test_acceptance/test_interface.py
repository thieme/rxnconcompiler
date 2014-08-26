#!/usr/bin/env python

"""
Unit Tests rxnconCompiler_interface.py module.
"""

import os
from unittest import main, TestCase
import sys

import rxnconcompiler.rxnconCompiler_interface as interface

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

class RxnconCompilerInterfaceTests(TestCase):
    """
    Unit Tests for rxnconCompiler interface.
    """
    def setUp(self):
        """
        Parses xls_tables. 
        """
        self.tiger_path = DATA_PATH + 'Tiger_et_al_TableS1.xls' 
        self.xls_tables = interface.parse(self.tiger_path)

    def test_get_src(self):
        """
        Tests that BNGL code is produced.
        """
        self.assertIn('begin model', interface.get_src(self.xls_tables))
        self.assertIn('begin model', interface.get_src(self.tiger_path))

    def test_filter_reactions(self):
        """
        Tests whether it is possible to filter reaction in the rxncon json dictionary.
        """
        self.assertEqual(1, len(interface.filter_reactions(self.xls_tables, ['1'])['reaction_list']))
        self.assertEqual(1, len(interface.filter_reactions(self.tiger_path, ['1'])['reaction_list']))

    def test_get_reactions(self):
        """
        Tests that only rules section is produced.
        """
        self.assertTrue(interface.get_reactions(self.xls_tables)[1].startswith('begin reaction rules'))
        self.assertTrue(interface.get_reactions(self.tiger_path)[1].startswith('begin reaction rules'))




if __name__ == '__main__': 
    main()
