#!/usr/bin/env python

"""
Unit Tests for complex_applicator.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.biological_complex.complex_applicator import ComplexApplicator

REACTIONS = """ProtA_[a]_ipi_ProtA_[b]"""

class ComplexApplicatorTests(TestCase):
    """
    UnitTests for ComplexApplicator class.
    """

    def setUp(self):
        """"""
        self.rxncon = Rxncon(REACTIONS)
        #rxncon.run_process()
        self.ipi_container = self.rxncon.reaction_pool["ProtA_[a]_ipi_ProtA_[b]"]

        self.rxncon_bool = Rxncon("""A_p+_B; ! <bool>
                        <bool>; AND A--B; AND A--C; AND A--D; AND B--E
                        <bool>; AND B--F; AND E--K; AND E--J; AND D--G; AND D--H""")
        self.bool_container = self.rxncon_bool.reaction_pool["A_p+_B"]

    def test_no_complexes_ipi(self):
        """
        If there are no complexes given should add complexes
        with single molecule.
        For ipi should be one LR comoplex.
        """
        self.assertEqual(self.ipi_container[0].substrat_complexes, [])
        self.rxncon.apply_contingencies(self.ipi_container,[])
        #ComplexApplicator(self.ipi_container, None).apply_complexes()
        self.assertEqual(len(self.ipi_container[0].substrat_complexes), 1)
        self.assertEqual(self.ipi_container[0].substrat_complexes[0].side, 'LR')

    def test_get_states_from_complex(self):
        """"""

        complex = self.rxncon_bool.get_complexes("A_p+_B")
        applicator = ComplexApplicator(self.bool_container, [])
        pos_bool = applicator.positive_application(complex[0])
        applicator.get_ordered_tree(pos_bool[0], self.bool_container[0].left_reactant)

        level1 = ['A_[AssocB]--B_[AssocA]', 'A_[AssocC]--C_[AssocA]', 'A_[AssocD]--D_[AssocA]']
        level2 = ['B_[AssocE]--E_[AssocB]', 'B_[AssocF]--F_[AssocB]', 'D_[AssocG]--G_[AssocD]', 'D_[AssocH]--H_[AssocD]']
        level3 = ['E_[AssocK]--K_[AssocE]', 'E_[AssocJ]--J_[AssocE]']
        for state in applicator.state_tree[:3]:
            self.assertTrue(str(state) in level1)
        for state in applicator.state_tree[3:7]:
            self.assertTrue(str(state) in level2)
        for state in applicator.state_tree[7:]:
            self.assertTrue(str(state) in level3)

    def test_build_tree_combinations_from_list(self):
        """"""
        complex = self.rxncon_bool.get_complexes("A_p+_B")
        applicator = ComplexApplicator(self.bool_container, [])
        pos_bool = applicator.positive_application(complex[0])
        negative_ordered_tree = applicator.build_negative_ordered_trees(pos_bool)
        self.assertTrue(len(negative_ordered_tree), 18)
        self.assertEqual(negative_ordered_tree[-1][0].state.state_str, 'A--B')
        self.assertEqual(negative_ordered_tree[8][0].state.state_str, 'A--B')


if __name__ == '__main__':
    main()
