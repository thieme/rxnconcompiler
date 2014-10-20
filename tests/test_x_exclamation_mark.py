from rxnconcompiler.rxncon import Rxncon
from unittest import main, TestCase

from unittest import main, TestCase
from rxnconcompiler.bngl.bngl import Bngl
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.parser.rxncon_parser import parse_rxncon


# MR 19.10.2014
# Name of this test sounds to me like 
# acceptance test - testing the end product - bngl.
# If you look for some inspiration for asserts you can go other
# acceptance tests.
# Perhaps it would also help to have unit tests - 
# just testting whether new functions work.
#
# You can also use oposite case 
# A_ppi_B; x A-{P}
# X_P+_A

class x_exclamation_mark_Tests(TestCase):
    """
    Unit tests for Rxncon class.
    Tests top rxncon objects.
    """
    def setUp(self):
        """
        Prepares data for tests.
        """
        # basic reaction with one contingency.
        input_data = "/home/thiemese/projects/rxncon/rxncon-unix/web2py/applications/yeastmap/modules/rxncon/test/test_data/Tiger_et_al_TableS1.xls"
        self.xls_tables = parse_rxncon(input_data)
        self.basic_cont = Rxncon('Z_P+_A_[Z] \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A_[Z]')
        #rxncon = Rxncon('Z_P+_A_[Z] \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A_[Z]')
        rxncon = Rxncon(input_data)
        rxncon.run_process()
        self.bngl_src = Bngl(rxncon.reaction_pool, rxncon.molecule_pool, rxncon.contingency_pool)
        #print bngl_src.get_src()



    def test_change(self):
        """
        Tests that molecules_pool is created and
        containe right number of molecules.
        """
        print "self.basic_cont: ", self.basic_cont
        print "bngl_src: ", self.bngl_src.get_src()



# class x_exclamation_mark_Tests(TestCase):
#     """
#     Unit test for the new logic implementation of x and !
#     """

#     def setUP(self):

#         """
#         Prepares data for tests.
#         """
#         print "HIER"
#         self.basic_cont = Rxncon('A_ppi_B; ! A--C')
#         self.basic = Rxncon('A_ppi_B')

#     def test_change(self):
#         print "DA"
#         print self.basic
#         self.basic_cont.find_conflict()




if __name__ == '__main__':
    main()