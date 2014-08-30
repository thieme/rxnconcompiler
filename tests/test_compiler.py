#!/usr/bin/env python

"""
Unit tests for compiler.py
"""

import os
from unittest import main, TestCase
from rxnconcompiler.parser.rxncon_parser import parse_text
from rxnconcompiler.compiler import Compiler
import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

class CompilerTests(TestCase):
    """
    Unit Tests for Compiler class.
    Tests whether bngl is produced out of 
    dictionary, string, and xls.
    """

    def test_basic(self):
        """Sets data for testing"""
        # bngl string is created from string input (quick).
        from_string = Compiler('A_ppi_B').translate()
        self.assertIn('begin model', from_string)

        # bngl is created from rxncon json dictionary.
        xls_tables = parse_text('A_ppi_B')
        from_dict = Compiler(xls_tables).translate()
        self.assertIn('begin model', from_dict)

        # TODO: add xls
        #from_xls = Compiler('A_ppi_B.xls').translate()
        #self.assertIn('begin model', from_xls)

        # bngls are equal independently from input.
        self.assertTrue(from_string == from_dict)

    def test_mapk_runs(self):
        """Tests that Compiler can process mapk example."""
        from_xls = Compiler(DATA_PATH + 'Tiger_et_al_TableS1.xls').translate()
        self.assertIn('begin model', from_xls)


if __name__ == '__main__':
    main()