from unittest import TestCase, main

from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.SBGN.PD import ReducedProcessDescription

class BasicTreeTest(TestCase):
    """
    for testing the basic tree of the PD.py
    """
    def setUp(self):

        self.example_complex_modification = """
                Ste11_ppi_Ste7
                Ste11_[KD]_P+_Ste7_[(ALS359)]; ! Ste11--Ste7
                """

        self.example_same_kinase_diff_targets = """
                A_p+_B
                A_p+_C
                """
        self.example_diff_kinase_same_target = """
            A_p+_B_[x]
            C_p+_B_[x]
            """

    def test_complex_modification(self):

        rxncon = Rxncon(self.example_complex_modification)
        rxncon.run_process()
        PD = ReducedProcessDescription(rxncon.reaction_pool)
        PD.build_reaction_Tree()
        self.assertEqual(len(PD.tree.nodes),4)
        self.assertEqual(len(PD.tree.nodes[0].children), 1)
        self.assertEqual(PD.tree.nodes[0].children[0], 3)
        self.assertEqual(PD.tree.nodes[0].id, 1)
        self.assertEqual(PD.tree.nodes[0].name, "Ste11")
        self.assertEqual(PD.tree.nodes[0].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[0].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[1].children), 1)
        self.assertEqual(PD.tree.nodes[1].children[0], 3)
        self.assertEqual(PD.tree.nodes[1].id, 2)
        self.assertEqual(PD.tree.nodes[1].name, "Ste7")
        self.assertEqual(PD.tree.nodes[1].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[1].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[2].children), 1)
        self.assertEqual(PD.tree.nodes[2].children[0], 4)
        self.assertEqual(PD.tree.nodes[2].id, 3)
        self.assertEqual(PD.tree.nodes[2].name, "Ste11-Ste7")
        self.assertEqual(PD.tree.nodes[2].parent, [("Ste11",1),("Ste7",2)])
        self.assertIsInstance(PD.tree.nodes[2].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[3].children), 0)
        self.assertEqual(PD.tree.nodes[3].id, 4)
        self.assertEqual(PD.tree.nodes[3].name, "Ste11-Ste7(ALS359~P)")
        self.assertEqual(PD.tree.nodes[3].parent, [("Ste11-Ste7",3)])
        self.assertIsInstance(PD.tree.nodes[3].node_object, BiologicalComplex)

    def test_same_kinase_diff_target(self):

        rxncon = Rxncon(self.example_same_kinase_diff_targets)
        rxncon.run_process()
        PD = ReducedProcessDescription(rxncon.reaction_pool)
        PD.build_reaction_Tree()

        self.assertEqual(len(PD.tree.nodes),5)
        self.assertEqual(len(PD.tree.nodes[0].children), 2)
        self.assertEqual(PD.tree.nodes[0].children, [3,5])
        self.assertEqual(PD.tree.nodes[0].id, 1)
        self.assertEqual(PD.tree.nodes[0].name, "A")
        self.assertEqual(PD.tree.nodes[0].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[0].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[1].children), 1)
        self.assertEqual(PD.tree.nodes[1].children, [3])
        self.assertEqual(PD.tree.nodes[1].id, 2)
        self.assertEqual(PD.tree.nodes[1].name, "B")
        self.assertEqual(PD.tree.nodes[1].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[1].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[2].children), 0)
        self.assertEqual(PD.tree.nodes[2].id, 3)
        self.assertEqual(PD.tree.nodes[2].name, "B(A~P)")
        self.assertEqual(PD.tree.nodes[2].parent, [("A",1),("B",2)])
        self.assertIsInstance(PD.tree.nodes[2].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[3].children), 1)
        self.assertEqual(PD.tree.nodes[3].children, [5])
        self.assertEqual(PD.tree.nodes[3].id, 4)
        self.assertEqual(PD.tree.nodes[3].name, "C")
        self.assertEqual(PD.tree.nodes[3].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[3].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[4].children), 0)
        self.assertEqual(PD.tree.nodes[4].id, 5)
        self.assertEqual(PD.tree.nodes[4].name, "C(A~P)")
        self.assertEqual(PD.tree.nodes[4].parent, [("A",1), ("C", 4)])
        self.assertIsInstance(PD.tree.nodes[4].node_object, BiologicalComplex)

    def test_diff_kinase_same_target(self):

        rxncon = Rxncon(self.example_diff_kinase_same_target)
        rxncon.run_process()
        PD = ReducedProcessDescription(rxncon.reaction_pool)
        PD.build_reaction_Tree()

        self.assertEqual(len(PD.tree.nodes),4)
        self.assertEqual(len(PD.tree.nodes[0].children), 1)
        self.assertEqual(PD.tree.nodes[0].children, [3])
        self.assertEqual(PD.tree.nodes[0].id, 1)
        self.assertEqual(PD.tree.nodes[0].name, "A")
        self.assertEqual(PD.tree.nodes[0].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[0].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[1].children), 1)
        self.assertEqual(PD.tree.nodes[1].children, [3])
        self.assertEqual(PD.tree.nodes[1].id, 2)
        self.assertEqual(PD.tree.nodes[1].name, "B")
        self.assertEqual(PD.tree.nodes[1].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[1].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[2].children), 0)
        self.assertEqual(PD.tree.nodes[2].id, 3)
        self.assertEqual(PD.tree.nodes[2].name, "B(x~P)")
        self.assertEqual(PD.tree.nodes[2].parent, [("A",1),("B",2),("C",4)])
        self.assertIsInstance(PD.tree.nodes[2].node_object, BiologicalComplex)

        self.assertEqual(len(PD.tree.nodes[3].children), 1)
        self.assertEqual(PD.tree.nodes[3].children, [3])
        self.assertEqual(PD.tree.nodes[3].id, 4)
        self.assertEqual(PD.tree.nodes[3].name, "C")
        self.assertEqual(PD.tree.nodes[3].parent, [(None,None)])
        self.assertIsInstance(PD.tree.nodes[3].node_object, BiologicalComplex)