#!/usr/bin/env python

"""
Unit Tests for rxncon_parser.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text, parse_xls
from rxnconcompiler.util.rxncon_errors import RxnconParserError

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

class RxnconTextParserTests(TestCase):

    def test_parse_text(self):
        """Tests creation of table dict"""
        tables = parse_text('A_ppi_A')
        self.assertEqual(tables['reaction_list'][0]['Reaction[Full]'], 'A_ppi_A')
        self.assertEqual(tables['contingency_list'], [])

    def test_parse_two_reactions_with_contingency(self):
        """Tests creation of table dict"""
        tables = parse_text('A_ppi_B\nA_ppi_C; ! A--B ')
        self.assertEqual(tables['reaction_list'][0]['ProductState'], 'A--B')

    def test_parse_error(self):
        """Tests creation of table dict"""
        self.assertRaises(RxnconParserError, parse_text, 'A_ppi_B ; C_ppi_D')

    def test_parse_product_state(self):
        """"""
        tables = parse_text('''A_[D]_ppi_A_[D]''')
        self.assertEqual(tables['reaction_list'][0]['ProductState'], 'A_[D]--A_[D]')


class RxnconXlsParserTests(TestCase):

    def test_parse_xls(self):
        tables = parse_xls(DATA_PATH + 'apoptosis_small.xls')
        self.assertEqual(len(tables['reaction_list']), 4)
        self.assertEqual(len(tables['contingency_list']), 6)
        self.assertEqual(tables['reaction_list'][3]['Reaction[Full]'], 'R_CUT_C8')
        self.assertEqual(tables['contingency_list'][3]['Target'], 'FADD_ppi_R')

    def test_apoptosis(self):
        tables = parse_xls(DATA_PATH + 'apoptosis.xls')

    def test_new_reaction(self):
        """Tests whether xls with new reactions (e.g. lipidation) can be parsed."""
        tables = parse_xls(DATA_PATH + 'Example_Reactions.xls')

    def test_new_structure(self):
        """Checks whether xls with subcategories in deffinintions can be parsed"""
        tables = parse_xls(DATA_PATH + 'rxncon_template_subcategory_test.xls')


if __name__ == '__main__':
    main()
