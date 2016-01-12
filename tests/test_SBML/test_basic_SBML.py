from unittest import TestCase, main
from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.sbml.SBML_2_4 import SBMLBuilder

class sbml_test(TestCase):
    def test_build_model(self):
        simple = """
        a_ppi_b
        """
        rxncon = Rxncon(simple)
        rxncon.run_process()
        reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
        reducedPD.build_reaction_Tree()
        sb = SBMLBuilder()

        toy1sbml =  sb.build_model(reducedPD.tree)
        self.assertEqual(toy1sbml.getLevel(), 2)
        self.assertEqual(toy1sbml.getVersion(), 4)
        self.assertEqual(toy1sbml.model.getNumSpecies(), 3)
        self.assertEqual(toy1sbml.model.getNumReactions(), 1)
        #species = toy1sbml.getListOfSpecies
