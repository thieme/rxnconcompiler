#!/usr/bin/env python

"""
Unit Tets for state.py module.
"""

import sys
import os
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
from rxnconcompiler.state import get_state, State, Component

class StateFactoryTests(TestCase):
	"""Unit Tests for StateFactory class."""

	def test_creation(self):
		"""Tests whether states are created."""
		# Association
		state = get_state("C--D") 
		self.assertEqual(str(state), "C_[AssocD]--D_[AssocC]")
		state = get_state("D--C")
		self.assertEqual(str(state), "D_[AssocC]--C_[AssocD]")
		# Intraprotein
		state = get_state("C_[a]--[b]") 
		self.assertEqual(str(state), "C_[a]--[b]")
		self.assertEqual(state.type, "Intraprotein")
		# Covalent Modfication
		state = get_state("A-{P}")
		self.assertEqual(str(state), "A_[bd]-{P}")
		state = get_state("A-{truncated}")
		self.assertEqual(str(state), "A_[bd]-{truncated}")
		# Localisation
		state = get_state("A-{mitochondria}")
		self.assertEqual(str(state), "A_[loc]-{mitochondria}")
		# Synthesis (single)
		state = get_state("A")
		self.assertEqual(str(state), "A")
		# Polymerisation
		state = get_state("A*4")
		self.assertEqual(str(state), "A*4")
		# Null
		state = get_state("")
		self.assertEqual(str(state), "")

	def test_wrong_input(self):
		"""Assurs that for wrong input states are not created."""
		pass
		#self.assertRaises(TypeError, get_state, 123)
		#self.assertRaises(TypeError, get_state, ['A--B'])

	def test_modification(self):
		""""""
		state = get_state("Fus3_[(T180)]-{P}")
		self.assertEqual(str(state), 'Fus3_[T180]-{P}')
		self.assertEqual(state.components[0].name, 'Fus3')
		self.assertEqual(state.components[0].domain, 'T180')


class StateTests(TestCase):
	"""UnitTests for State class"""  

	def test_state_id(self):
		"""
		Tests assignig id to components of state.
		Only for Associations.
		"""
		state = get_state("D--C", "1--2")
		self.assertEqual(str(state.components), '[D_[AssocC], C_[AssocD]]')
		self.assertEqual(state.components[0].name, 'D')
		self.assertEqual(state.components[0].cid, '1')
		self.assertEqual(state.components[1].name, 'C')
		self.assertEqual(state.components[1].cid, '2')


if __name__ == '__main__':
	main()
