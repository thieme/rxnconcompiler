#!/usr/bin/env python

"""
Unit tests for rate.py module.
"""

from unittest import main, TestCase

from unittest import TestCase, main
from rxnconcompiler.rulebased import Rxncon, Compiler
from rxnconcompiler.reaction.rate import Rate
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.contingency.contingency import Contingency


class RateTests(TestCase):
    """
    Unit Tests for Rule object.
    """
    def test_basic_rate(self):
        """
        Tests whether rate is correctly created from a reaction.
        """ 
        rxncon = Rxncon('A_ppi_B')
        reaction = rxncon.reaction_pool['A_ppi_B'][0]
        
        # reaction should have automaticly asign rate (ReactionFactory).
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf1', 'kr1'])
        self.assertEqual(reaction.rate._rate_names, ['kf1', 'kr1'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kr1': 1, 'kf1': 1})

        # test creating and seting a rate. 
        rate = Rate(reaction)
        self.assertEqual(rate.get_rates_for_reaction(), ['kf1', 'kr1'])
        self.assertEqual(rate._rate_names, ['kf1', 'kr1'])
        self.assertDictEqual(rate.get_rate_values(), {'kr1': 1, 'kf1': 1})

    def test_get_ids(self):
        """
        Tests whether rate knows its own ids.
        """
        rxncon = Rxncon('A_ppi_B\nA_P+_X')
        reaction = rxncon.reaction_pool['A_ppi_B'][0]
        reaction_p = rxncon.reaction_pool['A_P+_X'][0]

        # test simple case
        self.assertEqual(reaction.rate.get_ids(), ['1'])
        
        # update normal rate with function
        cont = Contingency(None, '!', get_state('[Start]'))
        reaction.rate.update_function(cont, True, '1_1', '1_2')
        self.assertEqual(reaction.rate.get_ids(), ['1_1', '1_2'])

        # test irreversible reaction
        reaction_p.rate.update_function(cont, False, '1_1', '1_2')
        self.assertEqual(reaction_p.rate.get_ids(), ['1_1'])

    def test_k_and_rate(self):
        """
        Tests whether rate is correctly created from a reaction.
        """ 
        '''
        rxncon = Rxncon("""A_ppi_B; ! <bool>
<bool>; AND A--C; AND A--D""")
        reaction = rxncon.reaction_pool['A_ppi_B'][0]
        '''
        comp = Compiler("""A_ppi_B; ! <bool>
<bool>; OR A--C; OR A--D; OR [Start]""")   

    def test_rate_name_update(self):
        """
        Tests whether rate is correctly updated with new number.
        """ 
        rxncon = Rxncon('A_ppi_B')
        reaction = rxncon.reaction_pool['A_ppi_B'][0]

        # test two numbers e.g. 3_5
        reaction.rate.update_name('3_5')
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf3_5', 'kr3_5'])
        self.assertEqual(reaction.rate._rate_names, ['kf3_5', 'kr3_5'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kr3_5': 1, 'kf3_5': 1})

        # test single_number e.g. 131
        reaction.rate.update_name('131')
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf131', 'kr131'])
        self.assertEqual(reaction.rate._rate_names, ['kf131', 'kr131'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kr131': 1, 'kf131': 1})

    def test_rate_function_update(self):
        """
        Tests whether rate is correctly updated with a function.
        """ 
        rxncon = Rxncon('A_ppi_B')
        reaction = rxncon.reaction_pool['A_ppi_B'][0]
        cont = Contingency(None, '!', get_state('[Start]'))
        
        # update normal rate with function
        reaction.rate.update_function(cont, True, '1_1', '1_2')
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf1_2*(1-k_Start)+kf1_1*k_Start', 'kr1_2*(1-k_Start)+kr1_1*k_Start'])
        self.assertEqual(reaction.rate._rate_names, ['kf1_1', 'kr1_1', 'kf1_2', 'kr1_2'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kf1_1': 1, 'kr1_1': 1, 'kf1_2': 1, 'kr1_2': 1, 'k_Start': 0})
        self.assertEqual(reaction.rate._special_rate_names, ['k_Start'])

        # update rate with function with normal value
        reaction.rate.update_name('1_5')
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf1_2*(1-k_Start)+kf1_5*k_Start', 'kr1_2*(1-k_Start)+kr1_5*k_Start'])
        self.assertEqual(reaction.rate._rate_names, ['kf1_5', 'kr1_5', 'kf1_2', 'kr1_2'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kf1_5': 1, 'kr1_5': 1, 'kf1_2': 1, 'kr1_2': 1, 'k_Start': 0})
        self.assertEqual(reaction.rate._special_rate_names, ['k_Start'])

        # update with new function
        reaction.rate.update_function(cont, False, '88_1', '88_2')
        self.assertEqual(reaction.rate.get_rates_for_reaction(), ['kf88_1*k_Start', 'kr88_2*(1-k_Start)+kr88_1*k_Start'])
        self.assertEqual(reaction.rate._rate_names, ['kf88_1', 'kr88_1', 'kr88_2'])
        self.assertDictEqual(reaction.rate.get_rate_values(), {'kf88_1': 1, 'kr88_1': 1, 'kr88_2': 1, 'k_Start': 0})
        self.assertEqual(reaction.rate._special_rate_names, ['k_Start'])


if __name__ == '__main__':
    main()