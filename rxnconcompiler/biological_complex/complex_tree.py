from rxnconcompiler.tree import Tree, Node, Children
(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class ComplexChildren(Children):
    """"""

    def __init__(self, name, cid, reaction=None, reversibility=None):
        """Constructor for Children"""
        Children.__init__(name, cid)
        self.cid = cid

    def __repr__(self):
        return self.name

class ComplexNode(Node):
    """"""

    def __init__(self, name, cid, old_cid=None, new_lvl=True):
        """Constructor for ComplexNode"""
        #super(ComplexNode, self).__init__(name, cid, new_lvl=new_lvl)
        Node.__init__(self, name, cid, new_lvl=new_lvl)
        self.cid = self.id
        self.old_cid = old_cid

    @property
    def old_cid(self):
        return self.__old_cid

    @old_cid.setter
    def old_cid(self, value):
        self.__old_cid = value

    @property
    def cid(self):
        return self.__cid

    @cid.setter
    def cid(self, value):
        self.__cid = value


class ComplexTree(Tree):
    def __init__(self):
        Tree.__init__(self)

    def get_highest_cid(self):
        max_cid = 0
        for node in self.nodes:
            if node.cid > max_cid:
                max_cid = node.cid
        return max_cid

    def add_Node(self, name, cid=None, old_cid=None, parent=(None,None), parent_cid=None):
        """
        add a node in a tree
        """
        if cid is None:
            cid = self.get_highest_cid()
            cid += 1
        node = ComplexNode(name=name, cid=cid, old_cid=old_cid)
        self.nodes.append(node)
        parent_node = self.update_children(parent, node.name, node.cid, _ADD, parent_cid)
        if parent[0] is None:
            node.parent = (None, None)
        else:
            node.parent = (parent_node.name, parent_node.cid)

        return node

    def show(self, position, level=_ROOT):
        """
        basic visualisation of the tree for testing and developing
        """
        if self.contains(position):
            node = self.get_node(cid=position)
            queue = node.children
            print("\t" * level, "{0} [{1}] parent: {2}".format(node.name, node.cid, node.parent))
            if node.new_lvl:
                level += 1
                for element in queue:
                    self.show(element, level)  # recursive call
        else:
            raise NameError("Node {0} does not exists!".format(position))

    def get_parent(self, cid):
        """
        get the parent of a specific node
        """
        for node in self.nodes:
            if node.cid == cid:
                return node.parent

    def get_node(self, cid=None, name=None, parent_cid=None):
        for node in self.nodes:
            if cid is not None and node.cid == cid:
                return node
            elif (name != None and parent_cid is not None) and (node.name == name and node.parent[1] == parent_cid):
                return node
            elif name is not None and parent_cid is None and node.name == name: # we have a root node
                return node

    def contains(self, cid):
        """
        test if a node already exists
        """
        for node in self.nodes:
            if node.cid == cid:
                return True

    def children_by_old_cid(self, node):
        result = []
        for child in node.children:
            child_node = self.get_node(cid=child.cid)
            result.append(child_node.old_cid)
        return result

    def reset_old_cid(self):
        for node in self.nodes:
            if node.old_cid is not None:
                node.old_cid = None