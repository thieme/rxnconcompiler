#!/usr/bin/env python

"""
Unit Tests for reaction_factory.py module.
"""

import os
from unittest import main, TestCase

from rxnconcompiler.parser import rxncon_parser
from rxnconcompiler.reaction.reaction_factory import ReactionFactory

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

class ReactionFactoryTests(TestCase):
    """
    Unit Tests for ReactionFactory class.
    """
    def setUp(self):
        """
        Setting data for tests.
        """
        mapk_xls = rxncon_parser.parse_xls(DATA_PATH + "Tiger_et_al_TableS1.xls")
        
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
