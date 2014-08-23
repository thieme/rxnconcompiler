#!/usr/bin/env python

"""
Unit Tests for biological_complex.py module.
"""

import sys
import os
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))

from rxnconcompiler.rulebased import Rxncon
from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex, AlternativeComplexes
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.molecule.molecule import Molecule

Ste11 = """Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste11-7>
<Ste11-7>; OR Ste7--Ste11; OR <Ste7-5-5-11>
<Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]"""


class BiologicalComplexTests(TestCase):
    """
    Unit Tests for BiologicalComplex Class.
    """
    def setUp(self):
        """Prepares data for tests."""
        rxncon = Rxncon(Ste11)
        rxncon.run_process()
        rections = rxncon.reaction_pool['Ste11_[KD]_P+_Ste7_[(ALS359)]']
        self.compl1 = rections[0].product_complexes[0]
        self.compl2 = rections[1].product_complexes[0]

        self.comp = BiologicalComplex()
        state_strings = ['A--B', 'A--C', 'A--D', 'B--E', 'B--F', \
                         'E--K', 'E--J', 'D--G', 'D--H']
        state_objects = [get_state(state) for state in state_strings]
        for state in state_objects:
            self.comp.add_state(state)
        self.comp.cid = '1' 
        
    def test_get_contingencies(self):
        """"""
        cont = self.compl1.get_contingencies()
        expected = '[! Ste7_[ALS359]-{P}, ! Ste7_[AssocSte11]--Ste11_[AssocSte7]]'
        self.assertEqual(expected, str(cont))

    def test_remove_molecule(self):
        """"""
        self.assertEqual(len(self.comp), 10)
        mol = self.comp.get_molecules('D')[0]
        self.assertEqual(len(mol.binding_partners), 3)
        mol = Molecule('H')
        self.comp.remove_molecule(mol)
        mol = self.comp.get_molecules('D')[0]
        self.assertEqual(len(mol.binding_partners), 2)
        self.assertEqual(len(self.comp), 9)

    def test_get_bonds(self):
        """"""
        # Artificial test:
        compl = BiologicalComplex()
        compl.molecules.append(Molecule('A'))
        compl.molecules.append(Molecule('A'))
        compl.molecules.append(Molecule('B'))
        compl.molecules.append(Molecule('B'))
        state = get_state('A--B')
        for mol in compl.molecules:
            mol.add_bond(state)
        bonds = compl.get_bonds()
        self.assertIn(1, bonds.values())
        self.assertIn(2, bonds.values())

        # Real life test:
        compl = BiologicalComplex()
        ste51 = Molecule('Ste5')
        ste52 = Molecule('Ste5')
        ste41 = Molecule('Ste4')
        ste42 = Molecule('Ste4')
        state1 = get_state('Ste4_[BDSte5]--Ste5_[nRING-H2]')
        state2 = get_state('Ste5_[BDSte5]--Ste5_[BDSte5]')
        ste51.add_bond(state1)
        ste51.add_bond(state2)
        ste52.add_bond(state1)
        ste52.add_bond(state2)
        ste41.add_bond(state1)
        ste42.add_bond(state1)
        compl.molecules = [ste41, ste42, ste51, ste52]
        bonds = compl.get_bonds()
        b1 = bonds[(ste41, state1)]
        b2 = bonds[(ste42, state1)]
        self.assertNotEqual(b1, b2)
        self.assertIn(1, bonds.values())
        self.assertIn(2, bonds.values())
        self.assertIn(3, bonds.values())


class AlternativeComplexesTests(TestCase):
    """
    Unit Tests for AlternativeComplexes Class.
    """
    def setUp(self):
        """Prepares data for tests."""
        rxncon = Rxncon(Ste11)
        rxncon.run_process()
        rections = rxncon.reaction_pool['Ste11_[KD]_P+_Ste7_[(ALS359)]']
        compl1 = rections[0].product_complexes[0]
        compl2 = rections[1].product_complexes[0]
        self.alt_comp = AlternativeComplexes('test')
        self.alt_comp.add_complex(compl1)
        self.alt_comp.add_complex(compl2)

    def test_empty(self):
        """
        Tests whether AlternaticeComplexes can be emptied. 
        """
        self.assertEqual(len(self.alt_comp), 2)
        self.alt_comp.empty()
        self.assertEqual(len(self.alt_comp), 0)

    def test_clone(self):
        """
        Tests whether new BiologicalComplex objects are 
        created while cloning AlternaticeComplexes. 
        """
        compl0_mol0_id = self.alt_comp[0].molecules[0]._id
        new = self.alt_comp.clone()
        new_compl0_mol0_id = new[0].molecules[0]._id
        #print compl0_mol0_id, new_compl0_mol0_id
        self.assertNotEqual(compl0_mol0_id, new_compl0_mol0_id)

if __name__ == '__main__':
    main()
