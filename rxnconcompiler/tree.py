(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Children():
    """"""

    def __init__(self, name, id):
        """Constructor for Children"""
        self.id = id
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, int):
            if self.id == other:
                return True
            else:
                return False

        if isinstance(other, str):
            if self.name == other:
                return True
            else:
                return False
        if self.id == other.id and self.name == other.name:
            return True
        else:
            return False

class Node:
    """

    """
    def __init__(self, name, id, new_lvl=True, ID=True):
        if ID:
            self.id = id
        self.name = name
        self.new_lvl = new_lvl
        self.__children = []
        self.parent = (None, None) # (name, id)
        self.__cont = []

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def cont(self):
        return self.__cont

    @property
    def children(self):
        return self.__children

    def update_children(self, name, id, mode=_ADD):
        if mode == _ADD:
            self.children.append(Children(name, id))
        if mode == _DELETE:
            for i,child in enumerate(self.children):
                if id == child.id and name == child.name:
                    del self.children[i]
        if mode == _INSERT:
            pass
            #self.children = [Children(id)]


class Tree(object):
    def __init__(self):
        self.nodes = []
        self.show_tree = []

    def get_highest_id(self):
        max_id = -1
        for node in self.nodes:
            if node.id > max_id:
                max_id = node.id
        return max_id

    def add_Node(self, name, id=None, parent=(None,None), parent_id=None):
        """
        add a node in a tree
        """
        #if not self.contains(identifier):
        if id is None:
            id = self.get_highest_id()
            id += 1
        node = Node(name=name, id= id)
        self.nodes.append(node)
        parent_node = self.update_children(parent, node.name, node.id, _ADD)
        #if parent[0] is None and parent[1] is None:
        if parent[0] is None:
            node.parent = parent
        else:
            node.parent = (parent_node.name, parent_node.id)

        return node

    def set_parent(self, node, children, levelup=False):
        """
        change the parent of one or more children
        """
        for child in children:
            child_node = self.get_node(id=child.id)
            # we have two instances to manipulate
            # 1) the list of nodes in the tree
            # 2) the update_children information
            # To update the nodes list we have to remove the node change the information and put it back
            # to update the treeTracker we have also to remove the old entry and replace it with the new one to make sure that everything is in correct position
            old_node_idx =  self.get_index(child_node.name)
            old_node = self.nodes.pop(old_node_idx)  # remove the node by its index from nodes list
            self.update_children(child_node.parent, child_node.name, child_node.id, _DELETE)  # remove the respective entry in treeTracker

            if levelup:
                old_node.parent = node.parent  # change the parent of the old node
            else:
                old_node.parent = node.id  # change the parent of the old node
            self.nodes.append(old_node)  # put the node back in the nodes list
            self.update_children(old_node.parent, old_node.name, old_node.id, _ADD)  # add the node again in the treeTracker

    def remove_Node(self, id):
        """
        remove a node from the tree
        """
        if self.contains(id):
            node = self.get_node(id=id)
            children = self.get_children(node.id)
            self.set_parent(node, children, levelup=True)
            self.update_children(node.parent, node.name, node.id, _DELETE)
            node_idx = self.get_index(node.name)
            #self.nodes.remove(node)
            del self.nodes[node_idx]
        else:
            raise("Node {0} not known!".format(id))
            #print "Node {0} not known!".format(id)

    def expand_tree(self, position, mode=_DEPTH):
        # Python generator. Based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        node = self.get_node(id=position)
        yield node
        queue = node.children
        while queue:
            node = self.get_node(id=queue[0].id)
            yield node
            expansion = node.children
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first

    def is_branch(self, position):
        return self[position].children

    def update_children(self, parent, name, id, mode):
        #if parent[0] is None and parent[1] is None:
        if parent[0] is None:
            return
        else:
            if parent[0] is None:
                parent_idx = self.get_index(parent[1])
                self[parent_idx].update_children(name, id, mode)
                return self[parent_idx]
            else:
                parent = self.get_node(parent[1])
                parent.update_children(name, id, mode)
                return parent

    def get_index(self, name):
        """
        get the index of identifier
        """
        for i, node in enumerate(self.nodes):
            if node.name == name:
                return i

    def has_node(self, name):
        if self.get_index(name) is not None:
            return True
        else:
            return False

    def show(self, position, level=_ROOT, tree_print=True):
        """
        basic visualisation of the tree for testing and developing
        """
        if self.contains(position):
            node = self.get_node(id=position)
            queue = node.children
            output = "-" * level
            output += ",{0} [{1}] parent: {2}\n".format(node.name, node.id, node.parent)
            if tree_print:
                print(output)
            self.show_tree.append(output)
            if node.new_lvl:
                level += 1
                for element in queue:
                    self.show(element.id, level, tree_print)  # recursive call
        else:
            raise NameError("Node {0} does not exists!".format(position))

    def get_leaf(self, position):
        """
        get the leafes of a node
        gets identifier type str
        return list of identifier type str
        """
        leafes = [node for node in self.expand_tree(position) if self.get_children(node.id) == []]
        return leafes

    def get_root_nodes(self):
        root_nodes = [node for node in self.nodes if node.parent == (None, None)]
        return root_nodes

    def get_parent(self, id):
        """
        get the parent of a specific node
        """
        for node in self.nodes:
            if node.id == id:
                return node.parent

    def get_children(self, id):
        """
        get all children of a specific node
        """
        children = [node for node in self.nodes if node.parent[1] == id]
        return children

    def get_node(self, id=None, name=None, parent_id=None):
        for node in self.nodes:
            if id is not None and node.id == id:
                return node
            elif (name != None and parent_id is not None) and (node.name == name and node.parent[1] == parent_id):
                return node
            elif name is not None and parent_id is None and node.name == name: # we have a root node
                return node

    def __getitem__(self, idx):
        return self.nodes[idx]

    def contains(self, id):
        """
        test if a node already exists
        """
        for node in self.nodes:
            if node.id == id:
                return True

    def list_of_node_names(self):
        names = [node.name for node in self.nodes]
        return names

    def children_by_name(self, node):
        result = []
        for child in node.children:
            child_node = self.get_node(child.id)
            result.append(child_node.name)
        return result

    def get_all_cont(self):
        result = []
        for node in self.nodes:
            result.extend(node.cont)
        return result

if __name__ == "__main__":
    tree = Tree()
    #, parent=(None,None), parent_id=None
    tree.add_Node(name="Harry", id=1)  # root node
    tree.add_Node(name="Jane", id=2, parent=("Harry",1))
    tree.add_Node(name="Bill", id=3, parent=("Harry",1))
    tree.add_Node(name="Joe", id=4, parent=("Jane",2))
    tree.add_Node(name="Diane", id=5, parent=("Jane",2))
    tree.add_Node(name="George", id=6,parent=("Diane",5))
    tree.add_Node(name="Mary", id=7, parent=("Diane", 5))
    tree.add_Node(name="Jill", id=8, parent=("George", 6))
    tree.add_Node(name="Carol", id=9, parent=("Jill", 8))
    tree.add_Node(name="Grace", id=10,parent=("Bill", 3))
    tree.add_Node(name="Mark", id=11, parent=("Harry", 1))
    pass
    # print("="*80)
    #tree.show(1)
    # print("="*80)
    #tree.remove_Node(id=1)
    pass

    #tree.show(2)
    # print("="*80)
    # tree.show("bill")
    # print("="*80)
    list = []
    for node in tree.expand_tree(1, mode=_WIDTH):
        list.append(node.name)
    print list
    # print("="*80)
    #
    #print tree.get_leaf(1)

