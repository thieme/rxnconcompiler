from unittest import TestCase, main
from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.sbml.SBML_2_4 import SBMLBuilder
from libsbml import *


class SbmlTest(TestCase):

    def test_build_model(self):

        # basic test for reversible protein protein interaction reaction
        simple_ppi = """
        a_ppi_b
        """
        rxncon_ppi = Rxncon(simple_ppi)
        rxncon_ppi.run_process()
        reducedPD_ppi = ReducedProcessDescription(rxncon_ppi.reaction_pool)
        reducedPD_ppi.build_reaction_Tree()
        sb = SBMLBuilder()

        toy1sbml = sb.build_model(reducedPD_ppi.tree)
        self.assertEqual(toy1sbml.getLevel(), 2)
        self.assertEqual(toy1sbml.getVersion(), 4)
        self.assertEqual(toy1sbml.model.getNumSpecies(), 3)
        self.assertEqual(toy1sbml.model.getNumReactions(), 1)

        species = toy1sbml.model.getListOfSpecies()
        a = species.get("s1")
        b = species.get("s2")
        ab = species.get("s3")
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
        self.assertEqual(law.getFormula(), "kf1 * s1 * s2 - kr1 * s3")


        # basic test for irreversible phosphorylation reaction
        simple_phos = """
        a_p+_b
        """

        rxncon_phos = Rxncon(simple_phos)
        rxncon_phos.run_process()
        reducedPD_phos = ReducedProcessDescription(rxncon_phos.reaction_pool)
        reducedPD_phos.build_reaction_Tree()
        sb2 = SBMLBuilder()
        toy2sbml =  sb2.build_model(reducedPD_phos.tree)


        self.assertEqual(toy2sbml.getLevel(), 2)
        self.assertEqual(toy2sbml.getVersion(), 4)
        self.assertEqual(toy2sbml.model.getNumSpecies(), 3)
        self.assertEqual(toy2sbml.model.getNumReactions(), 1)

        species = toy2sbml.model.getListOfSpecies()
        a = species.get("s1")
        b = species.get("s2")
        ab = species.get("s3")
        self.assertIsInstance(a, Species)
        self.assertEqual(a.getName(), "a")
        self.assertIsInstance(b, Species)
        self.assertEqual(b.getName(), "b")
        self.assertIsInstance(ab, Species)
        self.assertEqual(ab.getName(), "b(a~P)")

        reactions = toy2sbml.model.getListOfReactions()
        r1 = reactions.get("r1")
        self.assertIsInstance(r1, Reaction)
        self.assertEqual(r1.getName(), "a_p+_b")
        law = r1.getKineticLaw()
        self.assertIsInstance(law, KineticLaw)
        self.assertEqual(law.getFormula(), "k1 * s1 * s2")


        # test for reversible ppi and irreversible p+ in one model
        toy3 = """
        a_p+_b_[x]
        c_p+_b_[x]
        d_ppi_e
        """
        rxncon_toy3 = Rxncon(toy3)
        rxncon_toy3.run_process()
        reducedPD_toy3 = ReducedProcessDescription(rxncon_toy3.reaction_pool)
        reducedPD_toy3.build_reaction_Tree()
        sb3 = SBMLBuilder()
        toy3sbml = sb3.build_model(reducedPD_toy3.tree)
        sb3.save_SBML(toy3sbml, os.path.expanduser("~/Desktop/parserOutput/unittest_toy3.xml"))

        self.assertEqual(toy3sbml.getLevel(), 2)
        self.assertEqual(toy3sbml.getVersion(), 4)
        self.assertEqual(toy3sbml.model.getNumSpecies(), 7)
        self.assertEqual(toy3sbml.model.getNumReactions(), 2)

        species = toy3sbml.model.getListOfSpecies()
        a = species.get("s1")
        b = species.get("s2")
        c = species.get("s4")
        d = species.get("s5")
        e = species.get("s6")
        bp = species.get("s3")
        de = species.get("s7")
        self.assertIsInstance(a, Species)
        self.assertEqual(a.getName(), "a")
        self.assertIsInstance(b, Species)
        self.assertEqual(b.getName(), "b")
        self.assertIsInstance(c, Species)
        self.assertEqual(c.getName(), "c")
        self.assertIsInstance(d, Species)
        self.assertEqual(d.getName(), "d")
        self.assertIsInstance(e, Species)
        self.assertEqual(e.getName(), "e")
        self.assertIsInstance(bp, Species)
        self.assertEqual(bp.getName(), "b(x~P)")
        self.assertIsInstance(de, Species)
        self.assertEqual(de.getName(), "d-e")

        reactions = toy3sbml.model.getListOfReactions()

        r1 = reactions.get("r1")
        self.assertIsInstance(r1, Reaction)
        self.assertEqual(r1.getName(), "a_p+_b_[x];c_p+_b_[x]")
        law = r1.getKineticLaw()
        self.assertIsInstance(law, KineticLaw)
        self.assertEqual(law.getFormula(), "k1 * s1 * s2 + k2 * s2 * s4")

        r3 = reactions.get("r3")
        self.assertIsInstance(r3, Reaction)
        self.assertEqual(r3.getName(), "d_ppi_e")
        law = r3.getKineticLaw()
        self.assertIsInstance(law, KineticLaw)
        self.assertEqual(law.getFormula(), "kf3 * s5 * s6 - kr3 * s7")


        # libsmbl test for errors in the SBML Document

        errors1 = toy1sbml.getNumErrors()
        self.assertEquals(errors1, 0)

        errors2 = toy2sbml.getNumErrors()
        self.assertEquals(errors2, 0)

        errors3 = toy3sbml.getNumErrors()
        self.assertEquals(errors3, 0)