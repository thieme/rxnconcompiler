#!/usr/bin/env python

"""
RequirementsGeneratorTests
RequirementsFactoryTests
"""

import sys
import os
from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text
from rxnconcompiler.contingency.contingency_factory import ContingencyFactory
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.bngl.requirements import RequirementsGenerator, RequirementsFactory

"""
        
         root
        /  |  \
       /   |   \
  !A--C  !A--D  x<MM>
                /AND\
               /     \
           B-{P}      <MM2>
                     / OR  \
                    /       \
                C-{P}        D-{P}        
"""
RXNCON_INPUT = """A_ppi_B; ! A--C
A_ppi_B; ! A--D
A_ppi_B; x <MM> 
<MM>; AND B-{P} 
<MM>; AND <MM2>
<MM2>; OR C-{P}
<MM2>; OR D-{P}"""


"""
          root
           |
           |
         !<MM>
         /    \
        /  OR  \
       /        \
    <MM2>        <MM3>
    /AND\        / OR\
   /     \      /     \
A-{P}   B-{P}  A--C    A--D
"""

OR_AND_OR = """A_ppi_B; ! <MM>
<MM>; OR <MM2>
<MM>; OR <MM3>
<MM2>; AND A-{P}
<MM2>; AND B-{P}
<MM3>; OR A--C
<MM3>; OR A--D"""

EMPTY_BOOL = """A_ppi_B; ! A--C
A_ppi_B; ! A--D
A_ppi_B; ! <MM> 
<MM>; AND B-{P} 
<MM>; AND <MM2>"""

NO_CONTINGENCIES = """A_ppi_B
A_ppi_C"""

ONLY_EXCLAMATION = """A_ppi_B; ! A-{P}"""

ONLY_X = """A_ppi_B; x B-{P}"""

EXCLAMATION_AND_X = """A_ppi_B; ! A-{P}
A_ppi_B; x B-{P}"""

AND = """A_ppi_B; ! <MM>
<MM>; AND A-{P}
<MM>; AND B-{P}"""

AND_SIMETRIC = """A_ppi_B; ! <MM>
<MM>; AND <MM2>
<MM>; AND <MM3>
<MM2>; AND A-{P}
<MM2>; AND B-{P}
<MM3>; AND A--C
<MM3>; AND A--D"""

AND_ASIMETRIC = """A_ppi_B; ! <MM>
<MM>; AND A-{P}
<MM>; AND <MM2>
<MM2>; AND <MM3>
<MM2>; AND B-{P}
<MM3>; AND A--C
<MM3>; AND A--D"""

OR = """A_ppi_B; ! <MM>
<MM>; OR A-{P}
<MM>; OR B-{P}
<MM>; OR A--C"""

MORE_REACTIONS = """A_ppi_B; ! A-{P}
A_ppi_C; ! A-{P}
A_ppi_D; ! A-{P}
A_ppi_E; ! A-{P}
"""

IGNORED = """A_ppi_B; K+ B-{P}
A_ppi_B; 0 A-{P}
A_ppi_B; ? B--C"""

REQUIREMENTS_TEST = [(RXNCON_INPUT, 2), (EMPTY_BOOL, 1), \
    (NO_CONTINGENCIES, 1), (ONLY_EXCLAMATION, 1), \
    (ONLY_X, 1), (EXCLAMATION_AND_X, 1), (AND, 1), \
    (AND_SIMETRIC, 1), (AND_ASIMETRIC, 1), (OR, 3), (OR_AND_OR, 3),\
    (IGNORED, 1)]

STRING_TEST = [(RXNCON_INPUT, '! A_[AssocC]--C_[AssocA], ! A_[AssocD]--D_[AssocA], x (B_[bd]-{P} and (C_[bd]-{P} or D_[bd]-{P}))'),\
(NO_CONTINGENCIES, ''), \
(ONLY_EXCLAMATION, '! A_[bd]-{P}'),\
(ONLY_X, 'x B_[bd]-{P}'), (EXCLAMATION_AND_X, '! A_[bd]-{P}, x B_[bd]-{P}'),\
(AND, '! (A_[bd]-{P} and B_[bd]-{P})'), (IGNORED, 'k+ B_[bd]-{P}, 0 A_[bd]-{P}, ? B_[AssocC]--C_[AssocB]'),\
(AND_SIMETRIC, '! ((A_[bd]-{P} and B_[bd]-{P}) and (A_[AssocC]--C_[AssocA] and A_[AssocD]--D_[AssocA]))'), \
(AND_ASIMETRIC, '! (A_[bd]-{P} and ((A_[AssocC]--C_[AssocA] and A_[AssocD]--D_[AssocA]) and B_[bd]-{P}))'),\
(OR, '! (A_[bd]-{P} or B_[bd]-{P} or A_[AssocC]--C_[AssocA])'), \
(OR_AND_OR, '! ((A_[bd]-{P} and B_[bd]-{P}) or (A_[AssocC]--C_[AssocA] or A_[AssocD]--D_[AssocA]))')]

class RequirementsGeneratorTests(TestCase):
    """Tests for ReguirementsGenerator class."""

    def get_walker(self, input_str, reaction_str = 'A_ppi_B'):
        """
        Returns walker from given string example and reaction name
        """
        table = parse_text(input_str)

        factory = ContingencyFactory(table)
        pool = factory.parse_contingencies()
        if reaction_str in pool.keys():
            return RequirementsGenerator(pool, reaction_str)
        else:
            empty_root = Contingency(reaction_str)
            return RequirementsGenerator(pool, empty_root)

    def test_str(self):
        """Tests whether RequirementsGenerator produces right string from itself."""
        for input_str, expected_str in STRING_TEST:
            walker = self.get_walker(input_str) 
            self.assertEqual(str(walker), expected_str)  

    def test_requirements(self):
        """Assures whether a proper number of requirement lists is generated."""
        for input_name, num in REQUIREMENTS_TEST:
            walker = self.get_walker(input_name) 
            walker.get_requirements()
            self.assertEqual(len(walker.requirements), num)            
  
    def test_requirements_detail(self):
        """Checks whether proprer requirements are generated."""
        walker = self.get_walker(RXNCON_INPUT) 
        walker.get_requirements()
        self.assertEqual(str(walker.requirements[0]),'[! A_[AssocC]--C_[AssocA], ! A_[AssocD]--D_[AssocA], x B_[bd]-{P}, x C_[bd]-{P}]')
        self.assertEqual(2,len(walker.requirements))
        self.assertEqual(4,len(walker.requirements[0]))
        self.assertEqual(4,len(walker.requirements[1]))

        walker = self.get_walker(OR_AND_OR) 
        walker.get_requirements()
        self.assertEqual(str(walker.requirements), '[[! A_[bd]-{P}, ! B_[bd]-{P}], [! A_[AssocC]--C_[AssocA]], [! A_[AssocD]--D_[AssocA]]]')
        
        walker = self.get_walker(NO_CONTINGENCIES) 
        walker.get_requirements()
        self.assertEqual(walker.requirements, [[]])

        walker = self.get_walker(IGNORED) 
        walker.get_requirements()
        self.assertEqual(walker.requirements, [[]])


class RequirementsFactoryTests(TestCase):
    """Tests for ReguirementsGenerator class."""

    def test_factory(self):
        table = parse_text(MORE_REACTIONS)
        rf = RequirementsFactory(table)
        req_dict = rf.get_requirements_dict()
        self.assertEqual(len(req_dict), 4)


if __name__ == '__main__':
    main()
