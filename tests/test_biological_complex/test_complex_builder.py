#!/usr/bin/env python

"""
Unit tests fror complex_builder module.
"""

from unittest import main, TestCase

from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
from rxnconcompiler.biological_complex.complex_builder import ComplexBuilder
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.rxncon import Rxncon

Ste11 = """Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste11-7>
<Ste11-7>; OR Ste7--Ste11; OR <Ste7-5-5-11>
<Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]"""

Ste11_flatten = "[[or Ste7_[AssocSte11]--Ste11_[AssocSte7]], [and Ste5_[MEKK]--Ste11_[AssocSte5], and Ste5_[MEK]--Ste7_[AssocSte5], and Ste5_[BDSte5]--Ste5_[BDSte5]]]"

class BiologicalComplexBuilderTests(TestCase):
    """
    Unit Tests for ComplexBuilder class.
    """
    def setUp(self):
        """Builds a large 9 moleculs complex."""
        self.comp = BiologicalComplex()
        state_strings = ['A--B', 'A--C', 'A--D', 'B--E', 'B--F', \
                         'E--K', 'E--J', 'D--G', 'D--H']
        state_objects = [get_state(state) for state in state_strings]
        for state in state_objects:
            self.comp.add_state(state)
        self.comp.cid = '1' 

    def test_complex(self):
        """Tests whether complex in the setup is correctly built."""
        self.assertEqual(len(self.comp.molecules), 10)
        mol = self.comp.get_molecules('A')[0]
        self.assertEqual(len(mol.binding_partners), 3)
        mol = self.comp.get_molecules('C')[0]
        self.assertEqual(len(mol.binding_partners), 1)

    def test_boolean_flatten(self):
        rxncon = Rxncon(Ste11)
        builder = ComplexBuilder()
        builder.get_state_sets(rxncon.contingency_pool["<Ste11-7>"])
        self.assertEqual(len(builder.final_states), 2)
        self.assertEqual(len(builder.final_states[0]), 1)
        self.assertEqual(len(builder.final_states[1]), 3)
        self.assertEqual(str(builder.final_states), Ste11_flatten)

    def test_get_branches(self):
        """"""
        self.assertEqual(len(self.comp.get_branches('A')), 6)
        self.assertEqual(len(self.comp.get_top_branches('A')), 3)

    def test_paths(self):
        """"""
        result = '[[K, E, B, A, D, H]]'
        self.assertEqual(str(self.comp.get_paths(Molecule('K'), Molecule('H'))), result)
        result = '[K, E, B, A, D, H]'
        self.assertEqual(str(self.comp.get_shortest_path(Molecule('K'), Molecule('H'))), result)

    def test_add(self):
        comp_sec = BiologicalComplex()
        state_strings = ['A--B', 'A--C', 'A--K', 'K--Z']
        state_objects = [get_state(state) for state in state_strings]
        for state in state_objects:
            comp_sec.add_state(state)
        comp_sec.cid = '2'
        result = 'Complex: A, B, C, D, E, F, G, H, J, K, K, Z'
        self.assertEqual(str(self.comp.complex_addition(comp_sec, Molecule('A'))), result)


if __name__ == '__main__':
    main()
