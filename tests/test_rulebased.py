#!/usr/bin/env python

"""
Unit tests for rulebased.py
"""

import sys
import os
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))

from rxnconcompiler.rulebased import Compiler, Rxncon, Bngl
from rxnconcompiler.parser.rxncon_parser import parse_text

class RxnconTests(TestCase):
    """
    Unit tests for Rxncon class.
    Tests top rxncon objects.              
    """
    def setUp(self):
        """
        Prepares data for tests.
        """
        # basic reaction.
        self.basic = Rxncon('A_ppi_B')  

        # basic reaction with one contingency.
        self.basic_cont = Rxncon('A_ppi_B; ! A--C')  
        
        # boolean contingencies allow to define complexes
        # and include in contingencies molecules that are not a part of reaction.
        self.bool = Rxncon('A_ppi_B; ! <b>\n<b>; AND A--C; AND C--D') 

        # reaction with many contingencies.
        self.cont = Rxncon('A_ppi_B; ! A-{P}; K+ B-{Ub}; x B--G') 

        # reaction with only x (inhibitory) contingncy
        self.cont_x = Rxncon('A_ppi_B; x A-{P}; x B-{Ub}; x B--G')

        # reaction with K contingency
        self.cont_k = Rxncon('A_ppi_B; K+ A--C')

    def test_molecule_pool(self):
        """
        Tests that molecules_pool is created and 
        containe right number of molecules.
        """
        ### Basic reaction.
        self.assertEqual(len(self.basic.molecule_pool), 2)    

        ### Basic reaction with one contingency.
        # molecules from contingencies (only). 
        # are not automatically included in molecules_pool.
        self.assertEqual(len(self.basic_cont.molecule_pool), 2)

    def test_reaction_pool(self):
        """
        Tests that reaction_pool is created 
        and contains ReactionContaiers with Reactions.
        """
        ### Basic reaction.
        # one ReactionContainer present in reaction_pool.
        self.assertEqual(len(self.basic.reaction_pool), 1)
        # one Reaction present in ReactionContainer.
        self.assertEqual(len(self.basic.reaction_pool['A_ppi_B']), 1)

        ### Basic reaction with one contingency.
        # one ReactionContainer present in reaction_pool.
        self.assertEqual(len(self.basic_cont.reaction_pool), 1)
        # one Reaction present in ReactionContainer .
        self.assertEqual(len(self.basic_cont.reaction_pool['A_ppi_B']), 1)

    def test_contingency_pool(self):
        """
        Tests that contingency_pool is created.
        """
        ### Basic reaction.
        # contingency_pool is empty.
        self.assertEqual(len(self.basic.contingency_pool), 0)

        ### Basic reaction with one contingency.
        # number of contingencies in the pool == number of reactions with contingencies 
        # one root contingency present in reaction_pool.
        self.assertEqual(len(self.basic_cont.contingency_pool), 1)
        # the root contingency has one child.
        self.assertEqual(len(self.basic_cont.contingency_pool['A_ppi_B'].children), 1)

        ### Boolean contingency.
        # boolean contingencies can have children (matrioszki)
        # one root contingency
        self.assertEqual(len(self.bool.contingency_pool), 1)
        # the root contingency has one child - bool contingency 
        self.assertEqual(len(self.bool.contingency_pool['A_ppi_B'].children), 1)
        # the boolean contingency has two children
        self.assertEqual(len(self.bool.contingency_pool['A_ppi_B'].children[0].children), 2)

    def test_complex_pool(self):
        """"""
        ### Basic reaction.
        # complex_pool is empty.
        self.assertEqual(len(self.basic.complex_pool), 0)

        ### Basic reaction with one contingency.
        # complex_pool is empty.
        self.assertEqual(len(self.basic_cont.complex_pool), 0)
       
        ### Boolean contingency.
        # one AlternativeComplexes present in the complex_pool.
        self.assertEqual(len(self.bool.complex_pool), 1)
        # one BiologicalComplex present in AlternativeComplexes
        self.assertEqual(len(self.bool.complex_pool['<b>']), 1)
        # three Molecule[a] present in BiologicalComplex. 
        self.assertEqual(len(self.bool.complex_pool['<b>'][0]), 3)

    def test_run_process(self):
        """
        Tests that after runing process 
        (process is 'propagatting' rxncon reactions and contingencies)
        - complexes are applied
        - contingencies are applied
        - product complexes are created
        """
        # TODO: typo change substrat_complexes into substrate_complexes

        ### Basic reaction.
        # Before running reaction there are no substrate and product complexes.
        reaction = self.basic.reaction_pool['A_ppi_B'][0]
        self.assertEqual(len(reaction.substrat_complexes), 0)
        self.assertEqual(len(reaction.product_complexes), 0)
        # in running reaction step substrate and product complexes are created.
        self.basic.run_process()
        reaction = self.basic.reaction_pool['A_ppi_B'][0]
        self.assertEqual(len(reaction.substrat_complexes), 2)
        self.assertEqual(len(reaction.product_complexes), 1)
        # one molecule in substrate contingencies.
        self.assertEqual(len(reaction.substrat_complexes[0]), 1)
        self.assertEqual(len(reaction.substrat_complexes[1]), 1)
        # two molecules in product complexes.
        self.assertEqual(len(reaction.product_complexes[0]), 2)

    def test_warnings(self):
        """
        Checks whether states that are not produced are indicated.
        """
        self.bool.run_process()
        self.assertEqual(len(self.bool.war.not_in_products), 2)
        self.assertEqual(len(self.bool.war.produced_in_more), 0)
        self.cont_x.run_process()
        self.assertEqual(len(self.cont_x.war.not_in_products), 3)
        self.cont_k.run_process()
        self.assertEqual(len(self.cont_k.war.not_in_products), 1)

    def test_add_missing_reactions(self):
        """
        Checks whether if there is a contingency for which a state is not present
        a reaction producing this state is added.
        """
        self.bool.run_process(False, True)
        self.assertTrue(len(self.bool.reaction_pool), 3)
        self.assertEqual(len(self.bool.war.not_in_products), 0)

        self.cont.run_process(False, True)
        self.assertTrue(len(self.cont.reaction_pool), 3)



class CompilerTests(TestCase):
    """
    Unit Tests for Compiler class.
    Tests whether bngl is produced out of 
    dictionary, string, and xls.
    """
    def setUp(self):
        """
        Sets path to test_data or tests/test_data.
        test_data is used when running from tests
        tests/test_data when runing setup.py test
        """
        self.p = ''
        if os.path.exists('test_data/Tiger_et_al_TableS1.xls'):
            self.p = 'test_data/' 
        elif os.path.exists('tests/test_data/Tiger_et_al_TableS1.xls'):
            self.p = 'tests/test_data/' 

    def test_basic(self):
        """Sets data for testing"""
        # bngl string is created from string input (quick).
        from_string = Compiler('A_ppi_B').translate()
        self.assertIn('begin model', from_string)

        # bngl is created from rxncon json dictionary.
        xls_tables = parse_text('A_ppi_B')
        from_dict = Compiler(xls_tables).translate()
        self.assertIn('begin model', from_dict)

        # TODO: add xls
        #from_xls = Compiler('A_ppi_B.xls').translate()
        #self.assertIn('begin model', from_xls)

        # bngls are equal independently from input.
        self.assertTrue(from_string == from_dict)

    def test_mapk_runs(self):
        """Tests that Compiler can process mapk example."""
        from_xls = Compiler(self.p + 'Tiger_et_al_TableS1.xls').translate()
        self.assertIn('begin model', from_xls)


class BnglTests(TestCase):
    """
    Tests that based on rxncon objects 
    bngl string can be created.
    """
    def setUp(self):
        # basic reaction.
        rxncon = Rxncon('A_ppi_B')
        rxncon.run_process()
        self.basic = Bngl(rxncon.reaction_pool, rxncon.molecule_pool, rxncon.contingency_pool)

    def test_get_src(self):
        """"""
        source = self.basic.get_src()
        self.assertTrue('A(AssocB)' in source)
        self.assertTrue('B(AssocA)' in source)
        self.assertTrue('# Source states:  A_[AssocB]--B_[AssocA] False' in source)
        self.assertTrue('# Product states: A_[AssocB]--B_[AssocA] True' in source)
        self.assertFalse('# Absolute requirements:' in source)
        self.assertFalse('kf1_1' in source)



if __name__ == '__main__':
    main()