#!/usr/bin/env python

"""
Unit Tests for reaction_factory.py module.
"""

from unittest import main, TestCase
import pickle
import sys
import os,re
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler import rxncon_parser
from rxnconcompiler.reaction_factory import ReactionFactory


class ReactionFactoryTests(TestCase):
    """
    Unit Tests for ReactionFactory class.
    """
    def setUp(self):
        """
        Setting data for tests.
        """
        self.p = ''
        if os.path.exists('test_data/Tiger_et_al_TableS1.xls'):
            self.p = 'test_data/' 
        elif os.path.exists('tests/test_data/Tiger_et_al_TableS1.xls'):
            self.p = 'tests/test_data/' 

        mapk_xls = rxncon_parser.parse_xls(self.p + "Tiger_et_al_TableS1.xls")
        
        self.react_fact = ReactionFactory(mapk_xls)
        self.react_fact.parse_reactions(mapk_xls)
        ipi = rxncon_parser.parse_text('A_ipi_A')
        self.ipi_fact = ReactionFactory(ipi)
        self.ipi_fact.parse_reactions(ipi)
       
    def test_parsing(self):
        """
        Tests whether all reactions are parsed from xls.
        """
        self.assertEqual(len(self.react_fact.reaction_pool), 222)
        self.assertEqual(self.react_fact.reaction_pool['Fus3_[CD]_ppi_Msg5_[n]'].rid, 1)

    def test_ipi_parsing(self):
        """
        Tests parsing of ipi reaction.
        """
        to_change = self.ipi_fact.reaction_pool['A_ipi_A'][0].to_change
        self.assertEqual(str(to_change), 'A_[AssocA1]--[AssocA2]')


if __name__ == '__main__':
    main()
