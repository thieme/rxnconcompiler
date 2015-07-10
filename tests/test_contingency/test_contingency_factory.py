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
        # the target reaction as well as the bool complex applied to the reaction are stored in the contingency pool
        self.assertEqual(len(self.pool.keys()), 2)
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

        root = self.pool['A_ppi_C']
        bool = self.pool[root.children[0].state.state_str]
        self.assertEqual(bool.count_leafs(), 4)

        root = self.pool['A_ppi_B']
        bool = self.pool[root.children[0].state.state_str]
        self.assertEqual(bool.count_leafs(), 4)

    def test_boolean(self):
        """
        Asseerts that the same boolean contingencie 
        can be used for two reactions.
        """
        table = parse_text(OR_AND_OR)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()
        root = self.pool['A_ppi_B']
        bool = self.pool[root.children[0].state.state_str]
        self.assertEqual(bool.count_leafs(), 4)

class ContingencyApoptosisTests(TestCase):
    """Checks whether proper contingencies pool is generated for apoptosis."""
    def setUp(self):
        apoptosis_xls = parse_xls(DATA_PATH + "apoptosis_final_template.xls")
        factory = ContingencyFactory(apoptosis_xls)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        self.assertEqual(len(self.pool),24)

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
        # 139 reaction + used 8 complexes
        self.assertEqual(len(self.pool),147)

# <Cdc24^{M}>
#   or <Cdc24^{M/4}>,
#       [and Cdc24_[AssocSte4]--Ste4_[AssocCdc24], and Ste4_[AssocSte18]--Ste18_[AssocSte4]] correct
#   or <Cdc24^{M/F}>,
#       [and Cdc24_[AssocFar1]--Far1_[c], and <Far1^{M}>] correct
#       and <Far1^{M}>
#           [and Far1_[nRING-H2]--Ste4_[AssocFar1], and Ste4_[AssocSte18]--Ste18_[AssocSte4]] correct
#   or [START]]correct
# <FIL-signal>
#       [and Cdc42_[AssocMsb2]--Msb2_[CyT], and Msb2_[CyT]--Sho1_[CyT]] correct
# <Pbs2-Nbp2-Ptc1>
#       [and Nbp2_[SH3]--Pbs2_[SIM2], and Nbp2_[n]--Ptc1_[AssocNbp2]] correct
# <SKO/R>
#       [and Sko1_[bZIP]--CRE_[AssocSko1], and Sko1_[n]--Tup1_[AssocSko1], and Cyc8_[TPR1-3]--Tup1_[n]] correct
# <STE11-7>
#       [or Ste7_[AssocSte11]--Ste11_[AssocSte7], or <Ste7-5-5-11>] correct
#           or <Ste7-5-5-11>
#                   [and Ste5_[MEKK]--Ste11_[AssocSte5], and Ste5_[MEK]--Ste7_[AssocSte5], and Ste5_[BDSte5]--Ste5_[BDSte5]] correct
# <Ssk1Ssk2>
#   [and Ssk1_[BDSsk1]--Ssk1_[BDSsk1], and Ssk1_[RR]--Ssk2_[BDSsk1]] correct
# <Ste11^{M/50}>
#       [and Opy2_[BDSte50]--Ste50_[RA], and Ste11_[SAM]--Ste50_[SAM]]
# <Ste11^{M}>
#       [or Sho1_[CyT]--Ste11_[BDSho1], or <Ste11^{M/5}>]
#       or <Ste11^{M/5}>
#           [and Ste5_[MEKK]--Ste11_[AssocSte5], and <Ste5^{M}>]
#                   and <Ste5^{M}> [and Ste4_[BDSte5]--Ste5_[nRING-H2], and Ste4_[AssocSte18]--Ste18_[AssocSte4]]








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
        Checks whether right contingencie type is assigned right based 
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
    Checks whether complexes are parsed corectly.
    (boolean contingencies with defined geometry)
    """
    def setUp(self):
        table = parse_text(COMPLEX)
        factory = ContingencyFactory(table)
        self.pool = factory.parse_contingencies()

    def test_parsing(self):
        """Tests whether contingencies with defined geometry are parsed."""
        # reaction and boolean contingencies directly applied to a reaction are stored in the contingency pool
        self.assertEqual(len(self.pool.keys()), 2)
        self.assertIn('A_ppi_X', self.pool.keys())
        self.assertEqual(len(self.pool['A_ppi_X'].children),3)

    def test_complex(self):
        """Tests whether all contingencies go to the complex."""
        root = self.pool['A_ppi_X']
        self.assertEqual(len(root.children), 3)
        # one change is that the structure of the boolean contingencies are not longer saved within the reactions they are applied on
        # but on their own the advantage is that we have to define them only ones and can apply them contingency dependent
        bool = self.pool[root.children[2].state.state_str]
        self.assertEqual(len(bool.children), 5)


if __name__ == '__main__':
    main()