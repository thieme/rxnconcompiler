#!/usr/bin/env python

"""
Unit Tests for reaction_container.py module.
"""

from unittest import main, TestCase
import pickle
import sys
import os,re
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler.rulebased import Rxncon

REACTIONS = """PolII_TRSC_Gene 
Ribo_TRSL_A
Proteasome_DEG_Protein
Kinase_P+_Target
A_ppi_B
A_ppi_C; K+ <bool> 
<bool>; AND A--D; AND A--E; AND [Start]
"""

class ReactionContainerTests(TestCase):
    """
    Tests for reaction parsing.
    """
    def setUp(self):
        """
        Prepares ReactionContainer objects through Rxncon.
        """
        rxn = Rxncon(REACTIONS)
        rxn.run_process()

        self.interaction = rxn.reaction_pool['A_ppi_B']
        self.translation = rxn.reaction_pool['Ribo_TRSL_A']
        self.transcription = rxn.reaction_pool['PolII_TRSC_Gene']
        self.degradation = rxn.reaction_pool['Proteasome_DEG_Protein']
        self.phosphorylation = rxn.reaction_pool['Kinase_P+_Target']
        self.bool = rxn.reaction_pool['A_ppi_C']

    def test_get_modifier(self):
        """
        Get modifier should return either list of somplexes or empty list.
        Depends on reaction type.
        """
        self.assertEqual(self.interaction.get_modifier(), [])
        self.assertEqual(str(self.translation.get_modifier()), '[Complex: Ribo, Complex: AmRNA]')
        self.assertEqual(str(self.transcription.get_modifier()), '[Complex: PolII]')
        self.assertEqual(str(self.degradation.get_modifier()), '[Complex: Proteasome]')
        self.assertEqual(str(self.phosphorylation.get_modifier()), '[Complex: Kinase]')

    def test_highest_subrate(self):
        """
        Test whether corect int value is found.
        """
        self.assertEqual(self.bool.highest_subrate, 2)
        self.assertEqual(self.interaction.highest_subrate, 0)

    def test_empty_container(self):
        """
        Test whether container is realy empty.
        """
        self.assertEqual(len(self.bool), 3)
        self.bool.empty()
        self.assertEqual(len(self.bool), 0)


if __name__ == '__main__':
    main()
