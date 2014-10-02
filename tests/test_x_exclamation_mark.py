from rxnconcompiler.rxncon import Rxncon
from unittest import main, TestCase

from unittest import main, TestCase
from rxnconcompiler.bngl.bngl import Bngl
from rxnconcompiler.rxncon import Rxncon


class x_exclamation_mark_Tests(TestCase):
    """
    Unit tests for Rxncon class.
    Tests top rxncon objects.
    """
    def setUp(self):
        """
        Prepares data for tests.
        """
        # basic reaction.
        print "HIER"
#        self.basic = Rxncon('A_ppi_B')

        # basic reaction with one contingency.
        self.basic_cont = Rxncon('Z_P+_A \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A')
        rxncon = Rxncon('Z_P+_A \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A')
        rxncon.run_process()
        bngl_src = Bngl(rxncon.reaction_pool, rxncon.molecule_pool, rxncon.contingency_pool)
        print bngl_src.get_src()



    def test_change(self):
        """
        Tests that molecules_pool is created and
        containe right number of molecules.
        """
        print self.basic_cont



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