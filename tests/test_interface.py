#!/usr/bin/env python

"""
Unit Tests rxnconCompiler_interface.py module.
"""

import os
from unittest import main, TestCase
from rxnconcompiler import interface

import test_data
XLS_DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep
JSON_DATA_PATH = test_data.__path__[0] + os.sep + 'json_files' + os.sep
IPATH = os.sep.join([test_data.__path__[0], '..', '..', 'rxnconcompiler'])

class InterfaceTests(TestCase):
    """
    Unit Tests for rxnconcompiler interface.
    """
    def setUp(self):
        """
        Parses xls_tables. 
        """
        self.tiger_path = XLS_DATA_PATH + 'Tiger_et_al_TableS1.xls' 
        self.json_example = JSON_DATA_PATH + 'example.json'
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

    def test_json_to_json(self):
        """read-write-read test"""
        tables = interface.parse(self.tiger_path)
        interface.get_json(tables, 'test.json')
        new_tables = interface.parse('test.json')
        self.assertEqual(tables, new_tables)


class CliTests(TestCase):
    """
    Unit Tests for rxnconcompiler CLI.
    """
    def setUp(self):
        """
        Parses xls_tables. 
        """
        self.cpath = os.getcwd()
        os.chdir(IPATH)

        self.tiger_path = XLS_DATA_PATH + 'Tiger_et_al_TableS1.xls' 
        self.json_example = JSON_DATA_PATH + 'example.json'
        #self.xls_tables = interface.parse(self.tiger_path)

    def tearDown(self):
        """
        Removes files.
        """
        if os.path.exists('test.json'):
            os.remove('test.json')
        if os.path.exists('test.rxncon'):
            os.remove('test.rxncon')
        if os.path.exists('rxnconcompiler.output'):
            os.remove('rxnconcompiler.output')
        os.chdir(self.cpath)

    def test_basic(self):
        """
        Tests yhe most simple command:
        python interface.py 'A_ppi_B; ! A--C' 
        """
        os.system("python interface.py 'A_ppi_B'")
        self.assertTrue(os.path.exists('rxnconcompiler.output'))
        f = open('rxnconcompiler.output') 
        cont = f.read()
        self.assertIn('A(AssocB) + B(AssocA) <-> A(AssocB!1).B(AssocA!1)', cont) 

    def test_json2bngl(self):
        """
        Tests json can be read.
        """
        com = "python interface.py %s -o 'test.json'" % self.json_example
        os.system(com)
        self.assertTrue(os.path.exists('test.json'))
        f = open('test.json') 
        cont = f.read()
        self.assertIn('A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <->', cont) 

    def test_json2rxncon(self):
        """
        Tests json can be translated into rxncon quick text.
        """
        com = "python interface.py %s -o 'test.rxncon' --rxncon" % self.json_example
        os.system(com)
        self.assertTrue(os.path.exists('test.rxncon'))
        f = open('test.rxncon') 
        cont = f.read()
        self.assertIn('A_ppi_B; ! A_[AssocC]--C_[AssocA]', cont)

    def test_tiger2rxncon(self):
        """
        Tests MAPK network can be translated into rxncon through CLI.
        """
        com = "python interface.py %s -o 'test.rxncon' --rxncon" % self.tiger_path
        os.system(com)
        self.assertTrue(os.path.exists('test.rxncon'))
        f = open('test.rxncon') 
        cont = f.read()
        self.assertIn('Fus3_[CD]_ppi_Msg5_[n]', cont)

    def test_tiger2json(self):
        """
        Tests MAPK network can be translated into json through CLI.
        """
        com = "python interface.py %s -o 'test.json' --json" % self.tiger_path
        os.system(com)
        self.assertTrue(os.path.exists('test.json'))
        f = open('test.json') 
        cont = f.read()
        self.assertIn('Fus3_[CD]_ppi_Msg5_[n]', cont)
        self.assertIn('reaction_list', cont)

    def test_tiger2bngl(self):
        """
        Tests MAPK network can be translated into bngl through CLI.
        """
        com = "python interface.py %s" % self.tiger_path
        os.system(com)
        self.assertTrue(os.path.exists('rxnconcompiler.output'))
        f = open('rxnconcompiler.output') 
        cont = f.read()
        self.assertIn('Ste11 p+ Pbs2', cont)  

if __name__ == '__main__': 
    main()
