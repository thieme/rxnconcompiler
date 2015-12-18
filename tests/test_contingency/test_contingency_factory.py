#!/usr/bin/env python

"""
Unit Tests for contingency_factory.py module

Classes:
- ContingencyFactoryTests: tests generation of contingency pool for basic exampls
- ContingencyApoptosisTests: tests generation of contingency pool for apoptosis
- ContingencyMAPKTests: tests generation of contingency pool for MAPK
- ContingencyWrapperTests: test creting flat contingencies with 
                           just 'positive' or 'negative' sign. 
- ComplexTests: tests generation of contingency pool for boolean contingencies 
                with deffined gemetry
"""

import sys
import os
from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text, parse_xls
from rxnconcompiler.contingency.contingency_factory import ContingencyFactory, ContingencyWrapper
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.molecule.state import get_state

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

RXNCON_INPUT = """A_ppi_B; ! A--C
A_ppi_B; ! A--D
A_ppi_B; K+ <MM> 
<MM>; AND B-{P} 
<MM>; AND <MM2>
<MM2>; OR C-{P}
<MM2>; OR D-{P}"""

TWO_REACTIONS = """A_ppi_B; K+ <MM>
A_ppi_C; K+ <MM>
<MM>; OR <MM2>
<MM>; OR <MM3>
<MM2>; AND A-{P}
<MM2>; AND B-{P}
<MM3>; OR A--C
<MM3>; OR A--D
"""

COMPLEX = """A_ppi_X; ! A-{P}
A_ppi_X; ! B-{P}
A_ppi_X; ! <C1>
<C1>; 1--2 A--B
<C1>; 1--3 A--C
<C1>; 1--4 A--D
<C1>; 2--5 B--E
<C1>; 2--6 B--F"""

OR_AND_OR = """A_ppi_B; ! <MM>
<MM>; OR <MM2>
<MM>; OR <MM3>
<MM2>; AND A-{P}
<MM2>; AND B-{P}
<MM3>; OR A--C
<MM3>; OR A--D"""


class ContingencyFactoryTests(TestCase):
    """Checks whether proper contingencies pool is generated for simple example."""
    def setUp(self):
        table = parse_text(RXNCON_INPUT)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        self.assertEqual(len(self.pool.keys()), 1)
        self.assertIn('A_ppi_B', self.pool.keys())
        self.assertEqual(len(self.pool['A_ppi_B'].children),3)

    def test_contingencies(self):
        created = self.pool['A_ppi_B'].children[0] 
        expected = Contingency('A_ppi_B', '!', get_state('A--C'))
        self.assertEqual(created, expected)

    def test_two_reactions(self):
        """
        Asserts that the same boolean contingency 
        can be used for two reactions.
        """
        table = parse_text(TWO_REACTIONS)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()
        self.assertEqual(self.pool['A_ppi_C'].count_leafs(), 4)
        self.assertEqual(self.pool['A_ppi_B'].count_leafs(), 4)

    def test_boolean(self):
        """
        Asserts that the same boolean contingency 
        can be used for two reactions.
        """
        table = parse_text(OR_AND_OR)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()
        self.assertEqual(self.pool['A_ppi_B'].count_leafs(), 4)

class ContingencyApoptosisTests(TestCase):
    """Checks whether proper contingencies pool is generated for apoptosis."""
    def setUp(self):
        apoptosis_xls = parse_xls(DATA_PATH + "apoptosis_final_template.xls")
        factory = ContingencyFactory(apoptosis_xls)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        self.assertEqual(len(self.pool), 24)

    def test_contingencies(self):
        cont = Contingency('TRAIL_i_R', 'x', get_state('FADD--R'))
        self.assertEqual(len(self.pool['TRAIL_i_R'].children),1)
        self.assertEqual(self.pool['TRAIL_i_R'].children[0], cont)


class ContingencyMAPKTests(TestCase):
    """Checks whether proper contingencies pool is generated for MAPK."""
    def setUp(self):
        apoptosis_xls = parse_xls(DATA_PATH + "Tiger_et_al_TableS1.xls")
        factory = ContingencyFactory(apoptosis_xls)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        self.assertEqual(len(self.pool), 139)

class ContingencyWrapperTests(TestCase):
    """
    Unit Tests for ContingencyWrapper.
    """
    def setUp(self):
        self.contingency = Contingency('A_ppi_B', '!', 'A--D')
        self.wrapped_pos = ContingencyWrapper(self.contingency, 'positive')
        self.wrapped_neg = ContingencyWrapper(self.contingency, 'negative')

    def test_str(self):
        expected = 'positive ! A--D'
        self.assertEqual(str(self.wrapped_pos), expected)
        expected = 'negative ! A--D'
        self.assertEqual(str(self.wrapped_neg), expected)

    def test_get_contingency(self):
        new = self.wrapped_pos.get_contingency()
        self.assertEqual(new, self.contingency)

    def test_new_sign(self):
        """
        Checks whether right contingency type is assigned right based 
        on old contingency type and mode (positive or negative).
        """
        # K+: positive: !, negative: x
        cont = Contingency('A_ppi_B', 'K+', 'A--D')
        pos = ContingencyWrapper(self.contingency, 'positive').get_contingency()
        neg = ContingencyWrapper(self.contingency, 'negative').get_contingency()
        # K-: positive: !, negative: x
        cont = Contingency('A_ppi_B', 'K-', 'A--D')
        pos = ContingencyWrapper(self.contingency, 'positive').get_contingency()
        neg = ContingencyWrapper(self.contingency, 'negative').get_contingency()


class ComplexTests(TestCase):
    """
    Checks whether complexes are parsed correctly.
    (boolean contingencies with defined geometry)
    """
    def setUp(self):
        table = parse_text(COMPLEX)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        """Tests whether contingencies with defined geometry are parsed."""
        self.assertEqual(len(self.pool.keys()), 1)
        self.assertIn('A_ppi_X', self.pool.keys())
        self.assertEqual(len(self.pool['A_ppi_X'].children), 3)

    def test_complex(self):
        """Tests whether all contingencies go to the complex."""
        root = self.pool['A_ppi_X']
        self.assertEqual(len(root.children), 3)
        self.assertEqual(len(root.children[2].children), 5)


if __name__ == '__main__':
    main()