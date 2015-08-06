#!/usr/bin/env python

"""
Unit tests for bngl.py module.
"""

from unittest import main, TestCase
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.bngl.bngl import Bngl

class BnglTests(TestCase):
    """
    Tests that based on rxncon objects 
    bngl string can be created.
    """
    def setUp(self):
        # basic reaction.
        rxncon = Rxncon('A_ppi_B')
        rxncon.run_process()
        self.basic = Bngl(rxncon.reaction_pool, rxncon.molecule_pool, rxncon.contingency_pool)
        
    def test_get_src(self):
        """"""
        source = self.basic.get_src()
        self.assertTrue('A(AssocB)' in source)
        self.assertTrue('B(AssocA)' in source)
        self.assertTrue('# Source states:  A_[AssocB]--B_[AssocA] False' in source)
        self.assertTrue('# Product states: A_[AssocB]--B_[AssocA] True' in source)
        self.assertFalse('# Absolute requirements:' in source)
        self.assertFalse('kf1_1' in source)


if __name__ == '__main__':
    main()
