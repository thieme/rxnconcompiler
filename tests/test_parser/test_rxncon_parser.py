#!/usr/bin/env python

"""
Unit Tests for rxncon_parser.py module.
"""

import os
from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text, parse_xls, parse_rxncon
from rxnconcompiler.util.rxncon_errors import RxnconParserError
from rxnconcompiler.parser.check_parsing import ContingenciesManipulation

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

class RxnconParserConingencyManipulationTests(TestCase):
    def setUp(self):
        complete_overlap_test = """ Z_p+_A
                                        Y_p+_A_[d]
                                        W_p+_A_[d/s]
                                        V_p+_A_[d/s(r)]
                                        H_p+_A_[d/(r)]
                                        G_p+_A_[(r)]
                                        A_ppi_C; ! A-{P}
                                        A_ppi_D; ! A_[d]-{P}
                                        A_ppi_E; ! A_[d/s]-{P}
                                        A_ppi_F; ! A_[d/s(r)]-{P}
                                        A_ppi_I; ! A_[d/(r)]-{P}
                                        A_ppi_J; ! A_[(r)]-{P}"""

        default_mod_test = """Z_p+_A
                                   W_p+_A
                                   A_ppi_C; ! A-{P}
                                """
        delete = """A_ppi_B; ! A-{P}
                         A_ppi_E; ! A--B
                         C_p+_D; ! A--C
                      """
        self.complete_overlap_xls_table = parse_text(complete_overlap_test)
        self.complete_overlap_minipulator  = ContingenciesManipulation(self.complete_overlap_xls_table)
        self.complete_overlap_minipulator.LumpedContingencyModifier()

    def test_domain_complete_overlap_general(self):
        self.assertEqual(self.complete_overlap_xls_table['reaction_list'], self.complete_overlap_minipulator.parsed_reactions) # this should not change here
        self.assertEqual(self.complete_overlap_xls_table['reaction_definition'], self.complete_overlap_minipulator.parsed_definition) # this should not change here
        self.assertEqual(len(self.complete_overlap_minipulator.parsed_contingencies), 21)

    def test_complete_overlap_domain_contingency(self):

        expected = [{'Contingency': 'OR', 'Modifier': u'A_[Z]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 7},
                     {'Contingency': 'OR', 'Modifier': u'A_[d]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 8},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 9},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s(r)]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 10},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/(r)]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 11},
                     {'Contingency': 'OR', 'Modifier': u'A_[(r)]-{P}', 'Target': '<AutomaticGeneratedComplex1>', 'ContingencyID': 12},
                     {'Contingency': 'OR', 'Modifier': u'A_[d]-{P}', 'Target': '<AutomaticGeneratedComplex2>', 'ContingencyID': 13},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s]-{P}', 'Target': '<AutomaticGeneratedComplex2>', 'ContingencyID': 14},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s(r)]-{P}', 'Target': '<AutomaticGeneratedComplex2>', 'ContingencyID': 15},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/(r)]-{P}', 'Target': '<AutomaticGeneratedComplex2>', 'ContingencyID': 16},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s]-{P}', 'Target': '<AutomaticGeneratedComplex3>', 'ContingencyID': 17},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s(r)]-{P}', 'Target': '<AutomaticGeneratedComplex3>', 'ContingencyID': 18},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/s(r)]-{P}', 'Target': '<AutomaticGeneratedComplex4>', 'ContingencyID': 19},
                     {'Contingency': 'OR', 'Modifier': u'A_[d/(r)]-{P}', 'Target': '<AutomaticGeneratedComplex4>', 'ContingencyID': 20},
                     {'Contingency': 'OR', 'Modifier': u'A_[(r)]-{P}', 'Target': '<AutomaticGeneratedComplex4>', 'ContingencyID': 21}]
        for cont in expected:
            self.assertIn(cont,self.complete_overlap_minipulator.parsed_contingencies)

    def test_complete_overlapping_domain_detailed(self):


        expected = {'A-{P}': {'modifiers': [u'A_[Z]-{P}', u'A_[d]-{P}', u'A_[d/s]-{P}', u'A_[d/s(r)]-{P}', u'A_[d/(r)]-{P}', u'A_[(r)]-{P}'], 'name': '<AutomaticGeneratedComplex1>'},
                    'A_[(r)]-{P}': {'modifiers': [u'A_[d/s(r)]-{P}', u'A_[d/(r)]-{P}', u'A_[(r)]-{P}'], 'name': '<AutomaticGeneratedComplex4>'},
                    'A_[d/(r)]-{P}': {'modifiers': [u'A_[d/s(r)]-{P}', u'A_[d/(r)]-{P}', u'A_[(r)]-{P}'], 'name': '<AutomaticGeneratedComplex4>'},
                    'A_[d/s(r)]-{P}': {'modifiers': [u'A_[d/s(r)]-{P}', u'A_[d/(r)]-{P}', u'A_[(r)]-{P}'], 'name': '<AutomaticGeneratedComplex4>'},
                    'A_[d/s]-{P}': {'modifiers': [u'A_[d/s]-{P}', u'A_[d/s(r)]-{P}'], 'name': '<AutomaticGeneratedComplex3>'},
                    'A_[d]-{P}': {'modifiers': [u'A_[d]-{P}', u'A_[d/s]-{P}', u'A_[d/s(r)]-{P}', u'A_[d/(r)]-{P}'], 'name': '<AutomaticGeneratedComplex2>'}}

        self.assertEqual(expected, self.complete_overlap_minipulator.new_contingencies)

    def test_deleting_nondefined_modifier_contingencies(self):
        pass

    def test_default_modification_domain(self):
        pass


if __name__ == '__main__':
    main()
