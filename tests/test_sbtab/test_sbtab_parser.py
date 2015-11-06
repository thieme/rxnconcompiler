__author__ = 'Mathias Wajnberg'

'''
Skript tests checking function of directories and parsing of sbtab files.
Parsing of rxncon files is not tested here, as this is done elsewhere by Basti.
Done parsing tests:
    - xls files
        - new rxncon and standard SBtab (Tiger files)
    - csv
        - tiger files minimized version
'''

from unittest import TestCase, main
import os
from rxnconcompiler.parser.parsing_controller import DirCheck
import rxnconcompiler.rxncon as rxncon
import test_data

SBTAB_FILES = os.path.join(test_data.__path__[0], "sbtab_files")

class DirCheckTest(TestCase):

    def test_rxncon_detection(self):
        path=os.path.join(SBTAB_FILES,"rxncon_old/Tiger_et_al_TableS1.xls")
        d= DirCheck(path)
        d.check_directory_type()

        self.assertEqual(d.rxncon_detected,1)
        self.assertEqual(d.rxncon_sbtab_detected,0)
        self.assertFalse(d.other_detected)
        self.assertFalse(d.sbtab_detected)

        print "#################",__name__, 'successful.##################'


    def test_rxncon_sbtab_detection(self):
        path=os.path.join(SBTAB_FILES,"rxncon_new/rxncon_template_2_0.xls")
        d= DirCheck(path)
        d.check_directory_type()

        self.assertEqual(d.rxncon_detected,0)
        self.assertEqual(d.rxncon_sbtab_detected,1)
        self.assertFalse(d.other_detected)
        self.assertTrue(d.sbtab_detected)

        print "#################",__name__, 'successful.##################'

    def test_sbtab_detection(self):
        path=os.path.join(SBTAB_FILES,"sbtab")
        d= DirCheck(path)
        d.check_directory_type()

        self.assertEqual(d.rxncon_detected,0)
        self.assertEqual(d.rxncon_sbtab_detected,0)
        self.assertFalse(d.other_detected)
        self.assertTrue(d.sbtab_detected)

        print "#################",__name__, 'successful.##################'

    def test_other_detection(self):
        path=SBTAB_FILES
        d= DirCheck(path)
        d.check_directory_type()

        self.assertTrue(d.other_detected)

        print "#################",__name__, 'successful.##################'

class ParserTest(TestCase):

    def xls_tables_keys_test(self, xls_tables):
        # test keys of each of the three lists
        # gets called in other funcitons
        cont_exp_keys=['Contingency','ContingencyID','Modifier','Target']
        def_exp_keys= ['Category','Comment', 'Directionality','ModifierBoundary','ProductState[Component]','Reaction:Name','ReactionType:ID','ReactionType:Name','Reversibility','SourceState[Component]' ,'UID:Reaction' ,'coProduct(s)','coSubstrate(s)']
        rxns_exp_keys=['ComponentA[DSR]','ComponentA[Domain]','ComponentA[Name]','ComponentA[Residue]','ComponentA[Subdomain]','ComponentB[DSR]','ComponentB[Domain]','ComponentB[Name]','ComponentB[Residue]','ComponentB[Subdomain]','ProductState','ReactionID','ReactionType:ID','Reaction[Full]','SourceState','UID:Reaction']
        for dictionary in xls_tables["contingency_list"]:
            self.assertEqual(dictionary.keys().sort(), cont_exp_keys.sort())
        for dictionary in xls_tables["reaction_definition"]:
            self.assertEqual(dictionary.keys().sort(), def_exp_keys.sort())
        for dictionary in xls_tables["reaction_list"]:
            self.assertEqual(dictionary.keys().sort(), rxns_exp_keys.sort())


    def test_rxncon_sbtab_parsing_xls(self):
        path=os.path.join(SBTAB_FILES,"rxncon_new/rxncon_template_2_0.xls")
        d= DirCheck(path)
        xls_tables=d.controller()
        expected= ['reaction_definition', 'contingency_list', 'reaction_list']
        for key in xls_tables.keys():
            self.assertTrue(key in expected)

        # test if length of list of dictionries is correct
        self.assertEqual(len(xls_tables["reaction_definition"]), 32)
        self.assertEqual(len(xls_tables["contingency_list"]), 2)
        self.assertEqual(len(xls_tables["reaction_list"]), 23)

        self.xls_tables_keys_test(xls_tables)

    def test_sbtab_parsing_csv(self):
        #works
        path=os.path.join(SBTAB_FILES,"sbtab/tiger_files_csv_cut") #csv
        d= DirCheck(path)
        xls_tables=d.controller()

        self.assertEqual(len(xls_tables["reaction_definition"]), 43)
        self.assertEqual(len(xls_tables["contingency_list"]), 10)
        self.assertEqual(len(xls_tables["reaction_list"]), 6)

        self.xls_tables_keys_test(xls_tables)

        print "#################",__name__, 'successful.##################'

    def test_sbtab_parsing_xls(self):
        #works
        path=os.path.join(SBTAB_FILES,"sbtab/tiger_files_xls") #xls
        d= DirCheck(path)
        xls_tables=d.controller()

        self.assertEqual(len(xls_tables["reaction_definition"]), 43)
        self.assertEqual(len(xls_tables["contingency_list"]), 313)
        self.assertEqual(len(xls_tables["reaction_list"]), 222)

        self.xls_tables_keys_test(xls_tables)

        print "#################",__name__, 'successful.##################'


class DataManipulationTest(TestCase):

    def test_bngl_output(self):
        '''
        Function opens mini example networks in the all formats, that has been parsed by hand. This generates
        4 rxncon objects from which bngl output gets generated. Then, this output gets compared.
        '''
        paths=[os.path.join(SBTAB_FILES,"sbtab/tiger_files_csv_cut"), #sbtab_csv
              os.path.join(SBTAB_FILES,"sbtab/tiger_files_xls_cut"), #sbtab_xls
              os.path.join(SBTAB_FILES,"rxncon_old/tiger_files_old_rxncon_cut.xls") , # rxncon old
              os.path.join(SBTAB_FILES,"rxncon_new/tiger_files_new_rxncon_cut.xls") # rxncon new
              ]
              # rxncon new

        for path in paths:
            d = DirCheck(path)
            xls_tables=d.controller()

            r= rxncon.Rxncon(xls_tables)

        print "#################",__name__, 'successful.##################'

if __name__ == '__main__':
    main()