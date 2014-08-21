#!/usr/bin/env python

"""
Acceptance tests for generated bngl.
Checks whether it can be run in BioNetGen

Requires: PERL_PATH and BIONETGEN_PATH
BNG_PATH should be set and exported in ~/.bashrc

Test data is imported from rxncon.test.test_data.xxx
All available data sets are in DATA_SETS dictionary.
Comment or uncomment lines in DATA_SETS
to decide which data sets to run.

Tests also daa from xls files.

How to use the tests:
most of them run very long and need to by
manualy stopped. Best is to run one at the time.
(this is why they are commented out).
"""

import sys
import os
import re
import subprocess
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))

from unittest import TestCase, main
from utils_for_tests import filter_reactions, filter_exclude_reactions
from rxnconcompiler.rulebased import Compiler, Rxncon
from test_data.rules_basic_data import DATA as BASIC
from test_data.rules_mapk_data import DATA as MAPK
from test_data.rules_input_data import DATA as INPUT
from test_data.rules_geometry_data import DATA as GEOMETRY
from test_data.rules_difficult_data import DATA as DIFFICULT
from test_data.rules_pheromon_data import DATA as PHEROMON

# To run more tests uncomment the data sets.
DATA_SETS = {
    # name: [data_set1, data_set2, ...]
    #'Basic Data Set': BASIC,
    'MAPK Data Set': MAPK,
    #'Input (e.g. Start) Data Set': INPUT,
    #'Complex Geometry Data Set': GEOMETRY,
    #'Difficault Cases Data Set': DIFFICULT,
    #'Pheromon Pathway Data Set': PHEROMON
}


PERL_PATH = '/usr/bin/perl'
BIONETGEN_PATH = os.environ['BNG_PATH'] + 'BNG2.pl'


class BioNetGenTests(TestCase):
    """
    Tests whether bngl generated through rxncon 
    can be run in BioNetGen.
    """
    def setUp(self):
        """
        Prepares reaction set to test.
        Filters reactions based on given tags.
        e.g. tags = ['p+', 'bool', '2']
        """
        tags = []  # when empty all reactions are included.
 
        self.data_sets = {}
        for data_set_name in DATA_SETS.keys():
            self.data_sets[data_set_name] = []
            for single_set in DATA_SETS[data_set_name]:
                reactions = filter_reactions(tags, single_set)
                self.data_sets[data_set_name].append(reactions)

    def assertBnglRuns(self, bngl):
        """
        Asserts that bngl code can be run in BioNetGen.
        Sometimes it run to long end it need to be stopped
        (to long mean - pass).
        """
        f = open('temp.bngl', 'w')
        f.write(bngl)
        f.close()

        import time
        p = subprocess.Popen([PERL_PATH, BIONETGEN_PATH, os.getcwd() + os.sep + 'temp.bngl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        print stderr
        #self.assertTrue(os.path.exists('temp.net'))
        self.assertTrue("Finished processing file" in stdout)
        self.assertFalse(stderr)
    
        '''
    def test_bngl_code(self):
        """
        Collects data (rxncon reactions and cont) from mapk test data.
        takes everything into on estring. 
        Produces bngl code and run it in BioNetGen.
        """ 
        for data_set_name in self.data_sets.keys():
            print 'Testing: %s...' % data_set_name
            for single_set in self.data_sets[data_set_name]:
                all_reactions = '' # '\n'.join(self.reactions)
                for reaction in single_set:
                    all_reactions += reaction + '\n'
                if all_reactions:
                    bngl = Compiler(all_reactions).translate(False, True, True, True)
                    f = open('mapk_data3.bngl', 'w')
                    f.write(bngl)
                    self.assertBnglRuns(bngl)
        '''
        '''
    def test_bngl_code_from_quick(self):
        """
        Takes mapk xls file and produces quick string out of it.
        Then produces bngl code from the quick string
        and run it in BioNetGen.
        """ 
        quick_data = str(Rxncon("test_data" + os.sep + "Tiger_et_al_TableS1.xls"))
        bngl = Compiler(quick_data).translate(False, True, True, True)
        self.assertBnglRuns(bngl)
        '''
        '''
    def test_simple_example_xls(self):
        """
        Tests rxncon_simple_example.xls. 
        """ 
        bngl = Compiler("test_data" + os.sep + "rxncon_simple_example.xls").translate()
        self.assertBnglRuns(bngl)
        '''
        '''
    def test_nimp_xls(self):
        """
        Tests NIMP reaction in BioNetGen
        """
        bngl = Compiler("test_data" + os.sep + "nimp_test.xls").translate()
        self.assertBnglRuns(bngl)
        '''
        '''
    def test_mapk_xls(self):
        """
        Tests mapk reaction in BioNetGen
        """
        bngl = Compiler("test_data" + os.sep + "Tiger_et_al_TableS1.xls").translate(False, True, True, True)
        self.assertBnglRuns(bngl)
        '''
    def tearDown(self):
        """
        Removes temp.bngl and temp.net after testing.
        """
        if os.path.exists('temp.bngl'): 
            os.remove('temp.bngl')
        if os.path.exists('temp.net'): 
            os.remove('temp.net')
        

if __name__ == '__main__':
    main()
