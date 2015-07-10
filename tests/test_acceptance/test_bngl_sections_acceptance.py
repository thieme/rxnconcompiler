#!/usr/bin/env python

"""
Acceptance tests for bngl file.
Tests molecules and species section
"""

import os
import re
import subprocess
from unittest import main, TestCase

from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.compiler import Compiler

import test_data
DATA_PATH = test_data.__path__[0] + os.sep + 'xls_files' + os.sep


class MoleculesTests(TestCase):
    """
    Tests whether molecule section in bngl code is correct.
    """
    def setUp(self):
        """
        set test data
        """
        simple = Compiler(DATA_PATH + "rxncon_simple_example.xls").translate()
        #nimp = Compiler("test_data" + os.sep + "nimp_test.xls").translate()
        
        molecule_pattern = 'begin molecule types.*?end molecule types'
        mp = re.compile(molecule_pattern, re.DOTALL)
        self.mol_simple = re.findall(mp, simple)[0]
        #self.mol_nimp = re.findall(mp, nimp)[0]


    def test_simple_example(self):
        """
        Test whether molecule section produced from simple example is correct.
        """ 
        mols = self.mol_simple.split('\n')[1:-1]
        self.assertEqual(len(mols), 6)
        self.assertEqual(mols[0], 'Hog1(T174~U~P,Y176~U~P)')
        self.assertEqual(mols[2], 'Pbs2(S514~U~P,T518~U~P,AssocSho1)')

    def test_Sho1_Ste11_case(self):
        """
        Test whether molecule section produced from simple example is correct.
        """ 
        test_data = '''Sho1_ppi_Ste11; x Ste5_[MEKK]--Ste11; k+ Hkr1--Sho1; k+ Msb2--Sho1; k+ Msb2_[CyT]--Sho1_[CyT]; ! <Ste11^{M/50}>
                        <Ste11^{M/50}>; and Opy2_[BDSte50]--Ste50_[RA]
                        <Ste11^{M/50}>; and Ste11_[SAM]--Ste50_[SAM]'''

        bngl = Compiler(test_data).translate(True, True, True, True)
        molecule_pattern = 'begin molecule types.*?end molecule types'
        mp = re.compile(molecule_pattern, re.DOTALL)
        
        mols_text = re.findall(mp, bngl)[0]
        mols = mols_text.split('\n')[1:-1]
        self.assertEqual(len(mols), 7)
        for mol in mols:
            if mol.startswith('Ste11'):
                self.assertIn('AssocSte5', mol)

    def test_mapk_case(self):
        """
        Test whether molecule section produced from simple example is correct.
        """ 
        quick_data = str(Rxncon(DATA_PATH + "Tiger_et_al_TableS1.xls"))
        bngl = Compiler(quick_data).translate(add_translation=False, add_missing_reactions=True, add_complexes=True, add_contingencies=True)

        molecule_pattern = 'begin molecule types.*?end molecule types'
        mp = re.compile(molecule_pattern, re.DOTALL)
        
        mols_text = re.findall(mp, bngl)[0]
        mols = mols_text.split('\n')[1:-1]
        for mol in mols:
            if mol.startswith('Ste7'):
                self.assertIn('Fus3', mol)


if __name__ == '__main__':
    main()