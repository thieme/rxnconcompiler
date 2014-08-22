#!/usr/bin/env python

"""
Unit tets for contingency.py module.

Classes:
- ContingencyTests:        basic tests

- BooleanContingencyTests: tests for boolean contingencies

- ComplexContingencyTests: tests for complexes 
                           (boolean contingencies with deffined geometry)
"""

import sys
import os
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler.contingency import Contingency
from rxnconcompiler.state import get_state


class ContingencyTests(TestCase):
    """
    Basic Unit Tests for Contingency class.
    """
    def test_init(self):
        """Tests creating a contingency."""
        contingency = Contingency('A_ppi_B', '!', 'A--D')
        self.assertEqual(contingency.target_reaction, 'A_ppi_B')
        self.assertEqual(contingency.ctype, '!')
        self.assertEqual(contingency.state, 'A--D')

    def test_get_copy(self):
        """Tests whether a new object is created."""
        cont = Contingency('A_ppi_B', '!', 'A--D')
        cont_copy = cont.clone()
        cont_copy.ctype = 'x'
        self.assertEqual(cont.ctype, '!')
        self.assertEqual(cont_copy.ctype, 'x')
        cont_copy = cont.clone('k+')  
        self.assertEqual(cont.ctype, '!')
        self.assertEqual(cont_copy.ctype, 'k+')

    def test_count_children(self):
        """Tests counting contingency children."""
        cont = Contingency('A_ppi_B', '!', 'A--D')
        result = cont.count_leafs()
        self.assertEqual(result, 0)


class BooleanContingencyTests(TestCase):
    """
    Unit Tests for Contingency class.
    Tests boolean contingencies 
    (contingencies that have children).
    """
    def setUp(self):
        """Creating data for tests."""
        self.boolean = Contingency('A_ppi_B', 'K+', get_state('<MM>'))
        cont1 = Contingency('<MM>', 'AND', get_state('B-{P}'))
        boolean2 = Contingency('<MM>', 'AND', get_state('<MM2>'))
        cont2 = Contingency('<MM2>', 'OR', get_state('C-{P}'))
        cont3 = Contingency('<MM2>', 'OR', get_state('D-{P}'))
        boolean2.add_child(cont2)
        boolean2.add_child(cont3)
        self.boolean.add_child(cont1)
        self.boolean.add_child(boolean2)

    def test_init(self):
        """Tests creating a boolean contingency."""
        self.assertEqual(self.boolean.target_reaction, 'A_ppi_B')
        self.assertEqual(self.boolean.ctype, 'k+')
        self.assertEqual(self.boolean.state, get_state('<MM>'))

    def test_add_child(self):
        """Tests ading children to contingency"""
        self.assertEqual(len(self.boolean.children), 2)

    def test_is_parent(self):
        """Tests whether contingency can say whether it is a parent of anouther one."""
        self.assertTrue(self.boolean.is_parent(self.boolean.children[0]))

    def test_get_copy(self):
        """Tets cloning boolean contingency."""
        bool_copy = self.boolean.clone()
        bool_copy.ctype = '!'
        self.assertEqual(self.boolean.ctype, 'k+')
        self.assertEqual(bool_copy.ctype, '!')
        bool_copy = self.boolean.clone('x')
        self.assertEqual(self.boolean.ctype, 'k+')
        self.assertEqual(bool_copy.ctype, 'x')
        self.assertEqual(len(bool_copy.children), len(self.boolean.children))
        self.assertEqual(bool_copy.children[0].inherited_ctype, bool_copy.ctype)
        self.assertEqual(self.boolean.children[0].inherited_ctype, self.boolean.ctype)

    def test_count_children(self):
        """Tets counting children."""
        result = self.boolean.clone()
        self.assertEqual(result.count_leafs(), 3)

class ComplexContingencyTests(TestCase):
    """
    Unit Tests for Contingency class.
    Tests boolean contingencies with defined geometry. 
    """
    def setUp(self):
        self.complex = Contingency('A_ppi_X', '!', '<C1>')
        self.child1 = Contingency('<C1>', '1--2', 'A--B')
        self.child2 = Contingency('<C1>', '1--3', 'A--C')
        self.child3 = Contingency('<C1>', '1--4', 'A--D')
        self.child4 = Contingency('<C1>', '2--5', 'B--E')
        self.child5 = Contingency('<C1>', '2--6', 'B--F')
        self.complex.add_child(self.child4)
        self.complex.add_child(self.child5)
        self.complex.add_child(self.child1)
        self.complex.add_child(self.child2)
        self.complex.add_child(self.child3)

    def test_add_child(self):
        """Checks proper number of children."""
        self.assertEqual(len(self.complex.children), 5)
        self.assertEqual(len(self.complex.get_children()), 5)
        self.assertEqual(self.complex.count_leafs(), 5)


if __name__ == '__main__':
    main()
