#!/usr/bin/env python

"""
Unit Tests rxnconCompiler_interface.py module.
"""

import os
from unittest import main, TestCase

import rxnconcompiler.rxnconCompiler_interface as interface

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep

class RxnconCompilerInterfaceTests(TestCase):
    """
    Unit Tests for rxnconCompiler interface.
    """
    def setUp(self):
        """
        Parses xls_tables. 
        """
        self.tiger_path = DATA_PATH + 'Tiger_et_al_TableS1.xls' 
        self.xls_tables = interface.parse(self.tiger_path)

    def tearDown(self):
        """
        Removes files.
        """
        if os.path.exists('test.json'):
            os.remove('test.json')
        if os.path.exists('test.rxncon'):
            os.remove('test.rxncon')

    def test_get_bngl(self):
        """
        Tests that BNGL code is produced.
        """
        self.assertIn('begin model', interface.get_bngl(self.xls_tables))
        self.assertIn('begin model', interface.get_bngl(self.tiger_path))

    def test_filter_reactions(self):
        """
        Tests whether it is possible to filter reaction in the rxncon json dictionary.
        """
        self.assertEqual(1, len(interface.filter_reactions(self.xls_tables, ['1'])['reaction_list']))
        self.assertEqual(1, len(interface.filter_reactions(self.tiger_path, ['1'])['reaction_list']))

    def test_get_bngl_reactions(self):
        """
        Tests that only rules section is produced.
        """
        self.assertTrue(interface.get_bngl_reactions(self.xls_tables)[1].startswith('begin reaction rules'))
        self.assertTrue(interface.get_bngl_reactions(self.tiger_path)[1].startswith('begin reaction rules'))

    def test_get_rxncon(self):
        """
        Tests string is returnes.
        """
        self.assertEqual(interface.get_rxncon('A_ppi_B').strip(), 'A_ppi_B')

    def test_get_rxncon_file(self):
        """
        Tests file is written.
        """
        interface.get_rxncon('A_ppi_B', 'test.rxncon')
        self.assertTrue(os.path.exists('test.rxncon'))
        f = open('test.rxncon')
        self.assertEqual(f.read(), 'A_ppi_B\n')

    def test_get_json_reactions(self):
        """
        Tests correct string is written.
        """
        json_output = interface.get_json_reactions('A_ppi_B', 'test.json')
        words = ['A--B', 'ComponentA', 'A_ppi_B', 'ProductState', 'Reaction']
        for word in words:
            self.assertIn(word, json_output)
        self.assertTrue(os.path.exists('test.json'))      
        f = open('test.json')
        content = f.read()
        for word in words:
            self.assertIn(word, content)

    def test_get_json_contingencies(self):
        """
        Tests correct string is returned.
        """
        json_output = interface.get_json_contingencies('A_ppi_B', 'test.json')
        self.assertIn('"contingency_list": []', json_output)
        json_output = interface.get_json_contingencies('A_ppi_B; ! A--C', 'test.json')
        words = ["Contingency", "!", "Modifier", "A--C", "Target", "A_ppi_B"]
        for word in words:
            self.assertIn(word, json_output)
        self.assertTrue(os.path.exists('test.json'))      
        f = open('test.json')
        content = f.read()
        for word in words:
            self.assertIn(word, content)

    def test_get_json_definitions(self):
        """
        Tests correct json string is returned.
        """
        json_output = interface.get_json_definitions('A_ppi_B', 'test.json')
        words = ["Directionality", "Modifier or Boundary"]
        for word in words:
            self.assertIn(word, json_output)
        self.assertTrue(os.path.exists('test.json'))      
        f = open('test.json')
        content = f.read()
        for word in words:
            self.assertIn(word, content)

    def test_get_json(self):
        """"""
        json_output = interface.get_json('A_ppi_B; ! A--C', 'test.json')
        words = ["Directionality", "Modifier", "reaction_list", \
                 "reaction_definition", "contingency_list", "Target"]
        for word in words:
            self.assertIn(word, json_output)        
        self.assertTrue(os.path.exists('test.json'))      
        f = open('test.json')
        content = f.read()
        for word in words:
            self.assertIn(word, content)


if __name__ == '__main__': 
    main()
