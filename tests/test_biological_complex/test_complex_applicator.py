#!/usr/bin/env python

"""
Unit Tests for complex_applicator.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.rulebased import Rxncon
from rxnconcompiler.biological_complex.complex_applicator import ComplexApplicator

REACTIONS = """ProtA_[a]_ipi_ProtA_[b]"""

class ComplexApplicatorTests(TestCase):
    """
    UnitTests for ComplexApplicator class.
    """

    def setUp(self):
        """"""
        rxncon = Rxncon(REACTIONS)
        self.ipi_container = rxncon.reaction_pool["ProtA_[a]_ipi_ProtA_[b]"]

    def test_no_complexes_ipi(self):
        """
        If there are no complexes given should add complexes
        with single molecule.
        For ipi should be one LR comoplex.
        """
        self.assertEqual(self.ipi_container[0].substrat_complexes, [])
        ComplexApplicator(self.ipi_container, None).apply_complexes()
        self.assertEqual(len(self.ipi_container[0].substrat_complexes), 1)
        self.assertEqual(self.ipi_container[0].substrat_complexes[0].side, 'LR')

        

if __name__ == '__main__':
    main()
