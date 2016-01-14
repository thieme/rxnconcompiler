from unittest import TestCase, main
from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.sbml.SBML_2_4 import SBMLBuilder
from libsbml import *

class sbml_test(TestCase):
    def test_build_model(self):

        # basic test for reversible protein protein interaction reaction
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

        species = toy1sbml.model.getListOfSpecies()
        a = species.get("s_m1")
        b = species.get("s_m2")
        ab = species.get("s_m3_m4")
        self.assertIsInstance(a, Species)
        self.assertEqual(a.getName(), "a")
        self.assertIsInstance(b, Species)
        self.assertEqual(b.getName(), "b")
        self.assertIsInstance(ab, Species)
        self.assertEqual(ab.getName(), "a-b")

        reactions = toy1sbml.model.getListOfReactions()
        r1 = reactions.get("r1")
        self.assertIsInstance(r1, Reaction)
        self.assertEqual(r1.getName(), "a_ppi_b")
        law = r1.getKineticLaw()
        self.assertIsInstance(law, KineticLaw)
        self.assertEqual(law.getFormula(), "kf1 * s_m1 * s_m2 - kr1 * s_m3_m4")

        # basic test for irreversible phosphorylation reaction