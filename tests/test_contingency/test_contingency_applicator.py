#!/usr/bin/env python

"""
Unit tets for contingency classes:
ContingencyFactory
"""

from unittest import main, TestCase
from rxnconcompiler.rulebased import Rxncon
from rxnconcompiler.contingency.contingency_applicator import ContingencyApplicator
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.biological_complex.complex_applicator import ComplexApplicator


class ContingencyApplicatorTests(TestCase):
    """Checks whether proper contingencies pool is generated for simple example."""
    def setUp(self):
        rxn = Rxncon('A_ppi_B')
        self.rcont = rxn.reaction_pool['A_ppi_B']  # reaction container

    def test_kminus(self):
        """Tests whether k- is properly applied."""
        cont = Contingency('A_ppi_B', 'K+', get_state('A_[T666]-{P}'))
        cont2 = Contingency('A_ppi_B', 'K+', get_state('A_[T777]-{P}'))
        ComplexApplicator(self.rcont, []).apply_complexes() 
        cap = ContingencyApplicator()
        cap.apply_on_container(self.rcont, cont)
        # Applying first contingency:
        for react in self.rcont:
            mod = react.substrat_complexes[0].molecules[0].modifications
            mod_sites = react.substrat_complexes[0].molecules[0].modification_sites
            self.assertTrue(cont.state in mod + mod_sites)
        # Applying second contingencies:
        cap.apply_on_container(self.rcont, cont2)
        for react in self.rcont:
            mod = react.substrat_complexes[0].molecules[0].modifications
            mod_sites = react.substrat_complexes[0].molecules[0].modification_sites
            self.assertTrue(cont.state in mod + mod_sites)
            self.assertTrue(str(cont.state) in [str(st) for st in (mod + mod_sites)])

    def test_applying_on_homo(self):
        """"""
        reactions = Rxncon('Ste20_[KD]_ppi_Ste20_[CRIB]').reaction_pool['Ste20_[KD]_ppi_Ste20_[CRIB]']
        ComplexApplicator(reactions, []).apply_complexes() 
        reaction = reactions[0]
        lmol = reaction.substrat_complexes[0].molecules[0]
        rmol = reaction.substrat_complexes[1].molecules[0]
        cont = Contingency('Ste20_[KD]_ppi_Ste20_[CRIB]', 'x', get_state('Cdc42_[ED]--Ste20_[CRIB]'))
        cap = ContingencyApplicator()
        cap.apply_on_molecule(lmol, cont, 'L')
        cap.apply_on_molecule(rmol, cont, 'R')
        self.assertEqual(len(lmol.binding_sites), 2)
        self.assertEqual(len(rmol.binding_sites), 1)


if __name__ == '__main__':
    main()
