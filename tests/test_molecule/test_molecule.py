#!/usr/bin/env python

"""
Unit Tests for molecule.py module.
"""

from unittest import main, TestCase

from unittest import TestCase, main
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.contingency.contingency import Contingency

class MoleculeTests(TestCase):
    """
    Unit Tests for Molecule class.
    """
    def test_add_bond(self):
        """
        Tests whether rate is correctly created from a reaction.
        """ 
        # Test whether after adding bond 
        # the same state present in binding_states is removed
        m = Molecule('A')
        state1 = get_state('A_[dom1]--B')
        m.add_binding_site(state1)
        self.assertEqual(len(m.binding_sites), 1)
        m.add_bond(state1)
        self.assertEqual(len(m.binding_partners), 1)
        self.assertEqual(len(m.binding_sites), 0)

        # Test whether after adding bond 
        # different state occupying the same domain in binding_states is removed
        m = Molecule('A')
        state2 = get_state('A_[dom2]--C')
        state3 = get_state('A_[dom2]--D')
        m.add_binding_site(state2)
        self.assertEqual(len(m.binding_sites), 1)
        m.add_bond(state3)
        self.assertEqual(len(m.binding_partners), 1)
        self.assertEqual(len(m.binding_sites), 0)

    def test_add_binding_domain(self):
        """
        Tests adding empty domains especialy in homoreaction.
        """
        m = Molecule('Ste20')
        state1 = get_state('Ste20_[KD]--Ste20_[CRIB]')
        state2 = get_state('Cdc42_[ED]--Ste20_[CRIB]')
        m.add_binding_site(state1)
        self.assertEqual(len(m.binding_sites),1)
        # R indicates that in case of homodimers like te2
        m.add_binding_site(state2, 'R')
        self.assertEqual(len(m.binding_sites),1)
        m.add_binding_site(state2, 'L')
        self.assertEqual(len(m.binding_sites),2)

    def test_contingencies_basic(self):
        """
        Tests geting and adding contingencies.
        """
        # Adding contingencies to molecule.
        mol = Molecule('A')
        conts = [Contingency(None, '!', get_state('A_[T111]-{P}')), \
                Contingency(None, '!', get_state('A_[Y222]-{P}')), \
                Contingency(None, '!', get_state('A--B')), \
                Contingency(None, 'x', get_state('A_[x]--[y]'))]
        for cont in conts:
            mol.add_contingency(cont)
        self.assertEqual(len(mol.modifications), 2)
        self.assertEqual(len(mol.binding_partners), 1)
        self.assertEqual(len(mol.binding_sites), 1)

        # Reading contingencies from molecule.
        read_cont = mol.get_contingencies()
        self.assertEqual(len(read_cont), 4)
        for cont in read_cont:
            self.assertIn(cont, conts)

    def test_contingencies_advanced(self):
        """
        """
        # Case with phosphorilation and deposphorilation.
        mol = Molecule('Ste7')
        conts = [Contingency(None, 'x', get_state('Ste7_[Fus3]-{P}')),\
                Contingency(None, 'x', get_state('Ste7_[ALS359]-{P}')),\
                Contingency(None, '!', get_state('Ste7_[ALS359]-{P}'))]
        for cont in conts:
            mol.add_contingency(cont)
        self.assertIn('Ste7_[Fus3]-{P}', str(mol.modification_sites))
        
        

if __name__ == '__main__':
    main()