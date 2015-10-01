#!/usr/bin/env python

"""
Unit tests fror complex_builder module.
"""

from unittest import main, TestCase

from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
from rxnconcompiler.biological_complex.complex_builder import ComplexBuilder, Tree
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.rxncon import Rxncon


(_ADD, _DELETE, _INSERT) = range(3)

Ste11 = """Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste11-7>
<Ste11-7>; OR Ste7--Ste11; OR <Ste7-5-5-11>
<Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]"""

Ste11_flatten = "[[or Ste7_[AssocSte11]--Ste11_[AssocSte7]], [and Ste5_[MEKK]--Ste11_[AssocSte5], and Ste5_[MEK]--Ste7_[AssocSte5], and Ste5_[BDSte5]--Ste5_[BDSte5]]]"


Cdc24 = '''Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}>
                <Cdc24^{M}>; or <Cdc24^{M/4}>
                <Cdc24^{M/4}>; and Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
                <Cdc24^{M/4}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
                <Cdc24^{M}>; or <Cdc24^{M/F}>
                <Cdc24^{M/F}>; and Cdc24_[AssocFar1]--Far1_[c]
                <Cdc24^{M/F}>; and <Far1^{M}>
                <Far1^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
                <Far1^{M}>; and Far1_[nRING-H2]--Ste4_[AssocFar1]
        '''
# arbitrary numbering in the structured tree
# multiple times a protein with same name in different context
# using default domains
restructured_Tree = """A_ppi_E; ! <comp>
                            <comp>; 5--25 A--B
                            <comp>; 25--7 B--B
                            <comp>; 7--8 B--C
                            <comp>; 25--9 B--D
                            <comp>; 5--10 A--F
                            <comp>; 10--11 F--B
                            <comp>; 11--12 B--G"""
structured_unstructured_Tree = """A_ppi_E; ! <comp>
                                    <comp>; 5--25 A--B
                                    <comp>; 25--7 B--B
                                    <comp>; 7--8 B--C
                                    <comp>; 25--9 B--D
                                    <comp>; 5--10 A--F
                                    <comp>; 10--11 F--B
                                    <comp>; 11--12 B--G
                                    A_ppi_E; ! <comp2>
                                    <comp2>; AND A--B
                                    <comp2>; AND B--C
                                    <comp2>; AND B--B
                                    <comp2>; AND B--G"""
class BiologicalComplexBuilderTests(TestCase):
    """
    Unit Tests for ComplexBuilder class.
    """
    def setUp(self):
        """Builds a large 9 moleculs complex."""
        self.comp = BiologicalComplex()
        state_strings = ['A--B', 'A--C', 'A--D', 'B--E', 'B--F', \
                         'E--K', 'E--J', 'D--G', 'D--H']
        state_objects = [get_state(state) for state in state_strings]
        for state in state_objects:
            self.comp.add_state(state)
        self.comp.cid = '1'

        self.expected_basic_tree = Tree()
        self.expected_basic_tree.add_Node("Cdc24")
        self.expected_basic_tree.add_Node("Far1",parent="Cdc24", parent_cid=1)
        self.expected_basic_tree.add_Node("Ste4", parent="Far1", parent_cid=2)
        self.expected_basic_tree.add_Node("Ste18", parent="St4", parent_cid=3)
        self.expected_basic_tree.add_Node("Ste4", parent="Cdc24", parent_cid=1)
        self.expected_basic_tree.add_Node("Ste18", parent="St4", parent_cid=5)
        self.expected_basic_tree.add_Node("Cdc42")

        self.expected_restructured_tree = Tree()
        self.expected_restructured_tree.add_Node("A", old_cid="5")
        self.expected_restructured_tree.add_Node("B",parent="A", parent_cid=1, old_cid="25")
        self.expected_restructured_tree.add_Node("F",parent="A", parent_cid=1, old_cid="10")
        self.expected_restructured_tree.add_Node("B",parent="B", parent_cid=2, old_cid="7")
        self.expected_restructured_tree.add_Node("D",parent="B", parent_cid=2, old_cid="9")
        self.expected_restructured_tree.add_Node("B",parent="F", parent_cid=3, old_cid="11")
        self.expected_restructured_tree.add_Node("C",parent="B", parent_cid=4, old_cid="8")
        self.expected_restructured_tree.add_Node("G",parent="B", parent_cid=6, old_cid="12")
        self.expected_restructured_tree.add_Node("E")



        self.expected_structued_unstructured_Tree = Tree()
        self.expected_structued_unstructured_Tree.add_Node("A", old_cid="5")
        self.expected_structued_unstructured_Tree.add_Node("B",parent="A", parent_cid=1, old_cid="25")
        self.expected_structued_unstructured_Tree.add_Node("F",parent="A", parent_cid=1, old_cid="10")
        self.expected_structued_unstructured_Tree.add_Node("B",parent="B", parent_cid=2, old_cid="7")
        self.expected_structued_unstructured_Tree.add_Node("D",parent="B", parent_cid=2, old_cid="9")
        self.expected_structued_unstructured_Tree.add_Node("B",parent="F", parent_cid=3, old_cid="11")
        self.expected_structued_unstructured_Tree.add_Node("C",parent="B", parent_cid=4, old_cid="8")
        self.expected_structued_unstructured_Tree.add_Node("G",parent="B", parent_cid=6, old_cid="12")
        # Node for A--B connection is already known
        # add Node B a second time to children of A
        root = self.expected_structued_unstructured_Tree.get_node(cid=1)
        child = self.expected_structued_unstructured_Tree.get_node(name="B", parent_cid=1)
        root.update_children(child.cid, _ADD)

        self.expected_structued_unstructured_Tree.add_Node("C",parent="B", parent_cid=2)
        # Node for B--B connection is already known
        # add Node B a second time to children of B
        root = self.expected_structued_unstructured_Tree.get_node(cid=2)
        child = self.expected_structued_unstructured_Tree.get_node(name="B", parent_cid=2)
        root.update_children(child.cid, _ADD)
        self.expected_structued_unstructured_Tree.add_Node("G",parent="B", parent_cid=2)
        self.expected_structued_unstructured_Tree.add_Node("E")

    def test_complex(self):
        """Tests whether complex in the setup is correctly built."""
        self.assertEqual(len(self.comp.molecules), 10)
        mol = self.comp.get_molecules('A')[0]
        self.assertEqual(len(mol.binding_partners), 3)
        mol = self.comp.get_molecules('C')[0]
        self.assertEqual(len(mol.binding_partners), 1)

    def test_boolean_flatten(self):
        rxncon = Rxncon(Ste11)
        builder = ComplexBuilder()
        builder.get_state_sets(rxncon.contingency_pool["<Ste11-7>"])
        self.assertEqual(len(builder.final_states), 2)
        self.assertEqual(len(builder.final_states[0]), 1)
        self.assertEqual(len(builder.final_states[1]), 3)
        self.assertEqual(str(builder.final_states), Ste11_flatten)

    def test_get_branches(self):
        """"""
        self.assertEqual(len(self.comp.get_branches('A')), 6)
        self.assertEqual(len(self.comp.get_top_branches('A')), 3)

    def test_paths(self):
        """"""
        result = '[[K, E, B, A, D, H]]'
        self.assertEqual(str(self.comp.get_paths(Molecule('K'), Molecule('H'))), result)
        result = '[K, E, B, A, D, H]'
        self.assertEqual(str(self.comp.get_shortest_path(Molecule('K'), Molecule('H'))), result)

    def test_add(self):
        comp_sec = BiologicalComplex()
        state_strings = ['A--B', 'A--C', 'A--K', 'K--Z']
        state_objects = [get_state(state) for state in state_strings]
        for state in state_objects:
            comp_sec.add_state(state)
        comp_sec.cid = '2'
        result = 'Complex: A, B, C, D, E, F, G, H, J, K, K, Z'
        self.assertEqual(str(self.comp.complex_addition(comp_sec, Molecule('A'))), result)

    def test_tree(self):
        """
        check if the tree is build correct
        @return:
        """
        rxncon = Rxncon(Cdc24)
        rxncon_container = rxncon.reaction_pool['Cdc24_[GEF]_GEF_Cdc42_[GnP]']
        builder = ComplexBuilder()
        builder.structure_complex(rxncon.get_complexes(rxncon_container.name), rxncon_container)
        builder_tree = builder.tree
        for i, builder_node in enumerate(builder_tree):
            self.assertEquals(builder_node.name, self.expected_basic_tree[i].name)
            self.assertEquals(builder_node.cid, self.expected_basic_tree[i].cid)
            self.assertEquals(builder_node.children, self.expected_basic_tree[i].children)
            self.assertEquals(builder_node.parent, self.expected_basic_tree[i].parent)

    def test_structuring(self):
        """
        check if the flatten boolean contingencies are properly changed
        @return:
        """
        expected_complex1 = "[1--2 Cdc24_[AssocFar1]--Far1_[c], 3--4 Ste4_[AssocSte18]--Ste18_[AssocSte4], 2--3 Far1_[nRING-H2]--Ste4_[AssocFar1]]"
        expected_complex2 = "[1--5 Cdc24_[AssocSte4]--Ste4_[AssocCdc24], 5--6 Ste4_[AssocSte18]--Ste18_[AssocSte4]]"
        rxncon = Rxncon(Cdc24)
        rxncon_container = rxncon.reaction_pool['Cdc24_[GEF]_GEF_Cdc42_[GnP]']
        builder = ComplexBuilder()
        builder.structure_complex(rxncon.get_complexes(rxncon_container.name), rxncon_container)
        self.assertEquals(str(rxncon.get_complexes(rxncon_container.name)[0][1][0]), expected_complex1)
        self.assertEquals(str(rxncon.get_complexes(rxncon_container.name)[0][1][1]), expected_complex2)

    def test_restructuring(self):
        rxncon = Rxncon(restructured_Tree)
        rxncon_container = rxncon.reaction_pool['A_ppi_E']
        builder = ComplexBuilder()
        builder.structure_complex(rxncon.get_complexes(rxncon_container.name), rxncon_container)
        builder_tree = builder.tree
        for i, builder_node in enumerate(builder_tree):
            self.assertEquals(builder_node.name, self.expected_restructured_tree[i].name)
            self.assertEquals(builder_node.cid, self.expected_restructured_tree[i].cid)
            self.assertEquals(builder_node.old_cid, self.expected_restructured_tree[i].old_cid)
            self.assertEquals(builder_node.children, self.expected_restructured_tree[i].children)
            self.assertEquals(builder_node.parent, self.expected_restructured_tree[i].parent)


    def test_structured_unstructured(self):
        rxncon = Rxncon(structured_unstructured_Tree)
        rxncon_container = rxncon.reaction_pool['A_ppi_E']
        builder = ComplexBuilder()
        builder.structure_complex(rxncon.get_complexes(rxncon_container.name), rxncon_container)
        builder_tree = builder.tree
        for i, builder_node in enumerate(builder_tree):
            self.assertEquals(builder_node.name, self.expected_structued_unstructured_Tree[i].name)
            self.assertEquals(builder_node.cid, self.expected_structued_unstructured_Tree[i].cid)
            self.assertEquals(builder_node.old_cid, self.expected_structued_unstructured_Tree[i].old_cid)
            self.assertEquals(builder_node.children, self.expected_structued_unstructured_Tree[i].children)
            self.assertEquals(builder_node.parent, self.expected_structued_unstructured_Tree[i].parent)
if __name__ == '__main__':
    main()
