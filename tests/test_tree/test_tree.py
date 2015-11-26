from unittest import main, TestCase
from rxnconcompiler.tree import Tree
import copy
(_ROOT, _DEPTH, _WIDTH) = range(3)

class TestTree(TestCase):
    """"""

    def setUp(self):
        """Constructor for TestTree"""
        self.tree = Tree()
        self.tree.add_Node(name="Harry", id=1)  # root node
        self.tree.add_Node(name="Jane", id=2, parent="Harry", parent_id=1)
        self.tree.add_Node(name="Bill", id=3, parent="Harry", parent_id=1)
        self.tree.add_Node(name="Joe", id=4, parent="Jane", parent_id=2)
        self.tree.add_Node(name="Diane", id=5, parent="Jane",parent_id=2)
        self.tree.add_Node(name="George", id=6,parent="Diane",parent_id=5)
        self.tree.add_Node(name="Mary", id=7, parent="Diane", parent_id=5)
        self.tree.add_Node(name="Jill", id=8, parent="George", parent_id=6)
        self.tree.add_Node(name="Carol", id=9, parent="Jill", parent_id=8)
        self.tree.add_Node(name="Grace", id=10,parent="Bill", parent_id=3)
        self.tree.add_Node(name="Mark", id=11, parent="Harry", parent_id=1)

    def test_add_Node(self):
        tree = Tree()
        tree.add_Node(name="Harry", id=1)  # root node
        self.assertEqual(len(tree.nodes), 1)
        self.assertEqual(tree.nodes[0].name, "Harry")
        self.assertEqual(tree.nodes[0].id, 1)

    def test_test_children(self):
        tree = Tree()
        tree.add_Node(name="Harry", id=1)  # root node
        tree.add_Node(name="Jane", id=2, parent="Harry", parent_id=1)

        self.assertEqual(len(tree.nodes[0].children), 1)
        self.assertEqual(tree.nodes[0].children[0].id, 2)
        self.assertEqual(tree.nodes[0].children[0].name, "Jane")

    def test_tree(self):
        """
                  Harry
                /   |   \
            Jane   Bill Mark
            /   \    |
        Joe   Diane Grace
              /   \
           Georg  Mary
             |
            Jill
             |
            Carol

        @return:
        """

        tree = copy.deepcopy(self.tree)

        #harry
        self.assertEqual(len(tree.nodes[0].children), 3)
        self.assertEqual(tree.nodes[0].children[0].id, 2)
        self.assertEqual(tree.nodes[0].children[0].name, "Jane")
        self.assertEqual(tree.nodes[0].children[1].id, 3)
        self.assertEqual(tree.nodes[0].children[1].name, "Bill")
        self.assertEqual(tree.nodes[0].children[2].id, 11)
        self.assertEqual(tree.nodes[0].children[2].name, "Mark")

        self.assertEqual(len(tree.nodes[1].children), 2)
        self.assertEqual(tree.nodes[1].children[0].id, 4)
        self.assertEqual(tree.nodes[1].children[0].name, "Joe")
        self.assertEqual(tree.nodes[1].children[1].id, 5)
        self.assertEqual(tree.nodes[1].children[1].name, "Diane")

        self.assertEqual(len(tree.nodes[2].children), 1)
        self.assertEqual(tree.nodes[2].children[0].id, 10)
        self.assertEqual(tree.nodes[2].children[0].name, "Grace")


        self.assertEqual(len(tree.nodes[4].children), 2)
        self.assertEqual(tree.nodes[4].children[0].id, 6)
        self.assertEqual(tree.nodes[4].children[0].name, "George")
        self.assertEqual(tree.nodes[4].children[1].id, 7)
        self.assertEqual(tree.nodes[4].children[1].name, "Mary")

        self.assertEqual(len(tree.nodes[5].children), 1)
        self.assertEqual(tree.nodes[5].children[0].id, 8)
        self.assertEqual(tree.nodes[5].children[0].name, "Jill")

        self.assertEqual(len(tree.nodes[7].children), 1)
        self.assertEqual(tree.nodes[7].children[0].id, 9)
        self.assertEqual(tree.nodes[7].children[0].name, "Carol")

    def test_show(self):
        tree = copy.deepcopy(self.tree)
        expected = [",Harry [1] parent: (None, None)",
                    "-, Jane [2] parent: ('Harry', 1)",
                    "--, Joe [4] parent: ('Jane', 2)",
                    "--, Diane [5] parent: ('Jane', 2)",
                    "---, George [6] parent: ('Diane', 5)",
                    "----, Jill [8] parent: ('George', 6)",
                    "-----, Carol [9] parent: ('Jill', 8)",
                    "---, Mary [7] parent: ('Diane', 5)",
                    "-, Bill [3] parent: ('Harry', 1)",
                    "--, Grace [10] parent: ('Bill', 3)",
                    "-, Mark [11] parent: ('Harry', 1)"]
        tree.show(1,tree_print=False)
        #self.assertEqual(tree.show_tree, expected)

    def test_node_remove(self):
        tree = copy.deepcopy(self.tree)

        tree.remove_Node(id=1)

        self.assertEqual(len(tree.nodes), 10)

        self.assertEqual(tree.nodes[7].id, 2)
        self.assertEqual(tree.nodes[7].name, "Jane")
        self.assertEqual(tree.nodes[7].parent, (None,None))

        self.assertEqual(tree.nodes[8].id, 3)
        self.assertEqual(tree.nodes[8].name, "Bill")
        self.assertEqual(tree.nodes[8].parent, (None,None))

        self.assertEqual(tree.nodes[9].id, 11)
        self.assertEqual(tree.nodes[9].name, "Mark")
        self.assertEqual(tree.nodes[9].parent, (None,None))

        self.assertEqual(len(tree.nodes[7].children), 2)

        self.assertEqual(tree.nodes[7].children[0].id, 4)
        self.assertEqual(tree.nodes[7].children[0].name, "Joe")
        self.assertEqual(tree.nodes[7].children[1].id, 5)
        self.assertEqual(tree.nodes[7].children[1].name, "Diane")

        self.assertEqual(len(tree.nodes[8].children), 1)
        self.assertEqual(tree.nodes[8].children[0].id, 10)
        self.assertEqual(tree.nodes[8].children[0].name, "Grace")


        self.assertEqual(len(tree.nodes[1].children), 2)
        self.assertEqual(tree.nodes[1].children[0].id, 6)
        self.assertEqual(tree.nodes[1].children[0].name, "George")
        self.assertEqual(tree.nodes[1].children[1].id, 7)
        self.assertEqual(tree.nodes[1].children[1].name, "Mary")

        self.assertEqual(len(tree.nodes[2].children), 1)
        self.assertEqual(tree.nodes[2].children[0].id, 8)
        self.assertEqual(tree.nodes[2].children[0].name, "Jill")

        self.assertEqual(len(tree.nodes[4].children), 1)
        self.assertEqual(tree.nodes[4].children[0].id, 9)
        self.assertEqual(tree.nodes[4].children[0].name, "Carol")

    def test_expand_depth(self):

        tree = copy.deepcopy(self.tree)

        expected = ['Harry', 'Jane', 'Joe', 'Diane', 'George', 'Jill', 'Carol', 'Mary', 'Bill', 'Grace', 'Mark']
        expand_list = []
        for node in tree.expand_tree(1, mode=_DEPTH):
            expand_list.append(node.name)
        self.assertEqual(expand_list, expected)

    def test_expand_width(self):

        tree = copy.deepcopy(self.tree)

        expected = ['Harry', 'Jane', 'Bill', 'Mark', 'Joe', 'Diane', 'Grace', 'George', 'Mary', 'Jill', 'Carol']
        expand_list = []

        for node in tree.expand_tree(1, mode=_WIDTH):
            expand_list.append(node.name)
        self.assertEqual(expand_list, expected)
