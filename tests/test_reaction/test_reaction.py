#!/usr/bin/env python

"""
Unit Tests for module reaction.py.
"""

from unittest import main, TestCase

from rxnconcompiler.rxncon import Rxncon

REACTIONS = """PolII_TRSC_Gene 
Ribo_TRSL_A
Proteasome_DEG_Protein
Kinase_P+_Target
A_ppi_B
X_ipi_X"""

class ReactionTests(TestCase):
    """
    Unit Tests for Reaction class and its children classes.
    """
    def setUp(self):
        """
        Prepares reaction objects through Rxncon.
        """
        rxn = Rxncon(REACTIONS)
        rxn.run_process()

        self.interaction = rxn.reaction_pool['A_ppi_B'][0]
        self.translation = rxn.reaction_pool['Ribo_TRSL_A'][0]
        self.transcription = rxn.reaction_pool['PolII_TRSC_Gene'][0]
        self.degradation = rxn.reaction_pool['Proteasome_DEG_Protein'][0]
        self.phosphorylation = rxn.reaction_pool['Kinase_P+_Target'][0]
        self.intraprotein = rxn.reaction_pool['X_ipi_X'][0]

    def test_get_modifier(self):
        """
        Get modifier should return either list of somplexes or empty list.
        Depends on reaction type.
        """
        self.assertEqual(self.interaction.get_modifier(), [])
        self.assertEqual(self.intraprotein.get_modifier(), [])
        self.assertEqual(str(self.translation.get_modifier()), '[Complex: Ribo, Complex: AmRNA]')
        self.assertEqual(str(self.transcription.get_modifier()), '[Complex: PolII]')
        self.assertEqual(str(self.degradation.get_modifier()), '[Complex: Proteasome]')
        self.assertEqual(str(self.phosphorylation.get_modifier()), '[Complex: Kinase]')

    def test_run_reactions_ppi_with_bool(self):
        """
        Test whether bonds are created after running reaction.
        """
        inp = """A_ppi_B; K+ <bool> 
<bool>; AND A--C; AND A--D; AND A--E"""
        rxn = Rxncon(inp)
        rxn.run_process()
        reaction = rxn.reaction_pool['A_ppi_B'][3]
        for mol in reaction.product_complexes[0].molecules:
            self.assertEqual(mol.binding_sites, [])

    def test_intraprotein_reaction(self):
        """
        Test whether product_complexes are created correctly.
        Intraprotein is a subtype of Association.
        """
        pc = self.intraprotein.product_complexes
        self.assertEqual(len(pc), 1)
        self.assertEqual(str(pc), '[Complex: X]')
        self.assertEqual(pc[0].molecules[0].binding_sites, [])
        self.assertEqual(str(pc[0].molecules[0].binding_partners), '[X_[AssocX1]--[AssocX2]]')



if __name__ == '__main__':
    main()
