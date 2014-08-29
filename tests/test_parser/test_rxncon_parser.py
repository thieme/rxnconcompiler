#!/usr/bin/env python

"""
Unit Tests for rxncon_parser.py module.
"""

import os
from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text, parse_xls, parse_rxncon
from util.rxncon_errors import RxnconParserError

import test_data
XLS_DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep
JSON_DATA_PATH = test_data.__path__[0] + os.sep + 'json_files' + os.sep

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
        tables = parse_xls(XLS_DATA_PATH + 'apoptosis_small.xls')
        self.assertEqual(len(tables['reaction_list']), 4)
        self.assertEqual(len(tables['contingency_list']), 6)
        self.assertEqual(tables['reaction_list'][3]['Reaction[Full]'], 'R_CUT_C8')
        self.assertEqual(tables['contingency_list'][3]['Target'], 'FADD_ppi_R')

    def test_apoptosis(self):
        tables = parse_xls(XLS_DATA_PATH + 'apoptosis.xls')

    def test_new_reaction(self):
        """Tests whether xls with new reactions (e.g. lipidation) can be parsed."""
        tables = parse_xls(XLS_DATA_PATH + 'Example_Reactions.xls')

    def test_new_structure(self):
        """Checks whether xls with subcategories in deffinintions can be parsed"""
        tables = parse_xls(XLS_DATA_PATH + 'rxncon_template_subcategory_test.xls')


class RxnconParserTests(TestCase):
    """Tests different kinds of inputs"""
    def setUp(self):
        """
        Read xls.
        """
        self.tables = parse_xls(XLS_DATA_PATH + 'apoptosis_small.xls')
        self.text_input = 'A_[AssocB]_ppi_B_[AssocA]; ! A_[AssocC]--C_[AssocA]'
        self.json_input = JSON_DATA_PATH + 'example.json'

    def test_parse_dict(self):
        new_tables = parse_rxncon(self.tables)
        self.assertEqual(len(new_tables['reaction_list']), 4)
        self.assertEqual(len(new_tables['contingency_list']), 6)
        self.assertEqual(new_tables['reaction_list'][3]['Reaction[Full]'], 'R_CUT_C8')
        self.assertEqual(new_tables['contingency_list'][3]['Target'], 'FADD_ppi_R')

    def test_parse_json(self):
        new_tables = parse_rxncon(self.json_input)
        self.assertEqual(len(new_tables['reaction_list']), 1)
        self.assertEqual(len(new_tables['contingency_list']), 1)




if __name__ == '__main__':
    main()
