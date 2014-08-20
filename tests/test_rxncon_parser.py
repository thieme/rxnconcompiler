#!/usr/bin/env python

"""
Unit Tests for rxncon_parser.py module.
"""

from unittest import main, TestCase
import os
import sys
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler.rxncon_parser import parse_text, parse_xls
from rxnconcompiler.rxncon_errors import RxnconParserError

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
        tables = parse_xls('test_data/apoptosis_small.xls')
        self.assertEqual(len(tables['reaction_list']), 4)
        self.assertEqual(len(tables['contingency_list']), 6)
        self.assertEqual(tables['reaction_list'][3]['Reaction[Full]'], 'R_CUT_C8')
        self.assertEqual(tables['contingency_list'][3]['Target'], 'FADD_ppi_R')

    def test_apoptosis(self):
        tables = parse_xls('test_data/apoptosis.xls')

    def test_new_reaction(self):
        """Tests whether xls with new reactions (e.g. lipidation) can be parsed."""
        tables = parse_xls('test_data/Example_Reactions.xls')
        #print tables['reaction_list']

    def test_new_structure(self):
        """Checks whether xls with subcategories in deffinintions can be parsed"""
        tables = parse_xls('test_data/rxncon_template_subcategory_test.xls')
        #print tables['reaction_definition']


if __name__ == '__main__':
    main()
