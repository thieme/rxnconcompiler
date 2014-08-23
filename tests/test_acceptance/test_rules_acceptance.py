#!/usr/bin/env python

"""
Acceptance Tests for translation from rxncon to bngl.
Checks whether obtained rules are correct.
Tests all data given in DATA_SETS.
Single data set is a dict (e.g. /test_data/rules_basic_data.py).
"""

import sys
import os
import re
import subprocess
from unittest import main, TestCase
sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))

from unittest import TestCase, main
from utils_for_tests import filter_reactions
from rxnconcompiler.rulebased import Compiler
from test_data.rules_basic_data import DATA as BASIC
from test_data.rules_mapk_data import DATA as MAPK
from test_data.rules_input_data import DATA as INPUT
from test_data.rules_geometry_data import DATA as GEOMETRY
from test_data.rules_difficult_data import DATA as DIFFICULT
from test_data.rules_pheromon_data import DATA as PHEROMON

# To run more tests uncomment the data sets.
DATA_SETS = {
    # name: [data_set1, data_set2, ...]
    'Basic Data Set': BASIC,
    'MAPK Data Set': MAPK,
    #'Input (e.g. Start) Data Set': INPUT,
    #'Complex Geometry Data Set': GEOMETRY,
    'Difficault Cases Data Set': DIFFICULT,
    #'Pheromon Pathway Data Set': PHEROMON

}


class RuleAcceptanceTests(TestCase):
    """
    Tests rule-output for each single reaction + contingencies input.
    Each reaction (with contingencies) is run as separate input.
    BNGL obtained for reaction is run in BioNetGen
    Only rules string is tested.
    """
    def setUp(self):
        """
        Prepares reaction set to test.
        Filters reactions based on given tags.
        e.g. tags = ['ppi']
        """
        tags = []  # when empty all reactions are included.

        self.data_sets = {}
        for data_set_name in DATA_SETS.keys():
            self.data_sets[data_set_name] = []
            for single_set in DATA_SETS[data_set_name]:
                self.data_sets[data_set_name].append(filter_reactions(tags, single_set))

    def assertRule(self, reaction, rule, bngl):
        """
        Checks whether single rule can be found in given bngl.
        If not prints message.
        Returns 1 for pass and 0 for fail.
        """
        try:
            self.assertIn(rule, bngl)
            return 1

        except AssertionError:
            print 
            print '=' * 70
            print 'FAIL: ', reaction
            print '-' * 70 
            print 'Rule: ', rule  
            print 'Not found in:'
            react_name = re.sub('[\[,\],\(,\)]','',reaction.split(';')[0])
            react_name = react_name.replace('-','\-').replace('+','\+').split('_')               
            react_name += [x.lower() for x in react_name]
            rule_pattern = '#[%s,\s]+###.*?' % (','.join(react_name))
            rule_pattern += 'end reaction'
            rp = re.compile(rule_pattern, re.DOTALL)
            result = re.findall(rp, bngl)
            for res in result:
                for l in res.split('\n'):
                    if not l.startswith('#') and not l.startswith('end'):
                        print l
            return 0

    def assertSystemAsReactions(self, data_dict, system_name="Test set"):
        """
        Tests reactions forom a single rxncon system (data set).
        One system == one dictionary from test_data 

        Gets each rxncon reaction (+ its contingencies) separately 
        and produces bngl for it. 
        Checks whether produced rule / rules are correct. 
        Tests all reactions one by one.
        """
        n_reactions = 0
        n_rules = 0
        for reaction in data_dict:
            #print reaction
            bngl = Compiler(reaction).translate()
            reaction_passed = True
            for rule in data_dict[reaction]['Rules']:
                result = self.assertRule(reaction, rule, bngl) # 1 or 0
                n_rules += result
                if result == 0:
                    reaction_passed = False
            if reaction_passed:
                n_reactions += 1

        print
        print 'Run %i reactions (%s):' % (len(data_dict), system_name)
        print '%i reactions and %i rules OK.' % (n_reactions, n_rules) 

        self.assertEqual(n_reactions, len(data_dict))


    def test_all_single_rules(self):
        """
        Tests all data sets by testing each reaction separately.
        Single reaction is an input and output rule / rules is tested.
        Summary at the andis separate for each dataset.
        """
        for data_set_name in self.data_sets.keys():
            for single_set in self.data_sets[data_set_name]:
                self.assertSystemAsReactions(single_set, data_set_name)


if __name__ == '__main__':
    main()