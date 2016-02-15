import copy

from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.tree import Tree, Node, Children
from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
import re

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)
class EdgeReaction():
    def __init__(self, rtype, reversibility):
        self.rtype = rtype
        self.reversibility = reversibility
    def __repr__(self):
        return str(self)
    def __str__(self):
        return "({},{})".format(self.rtype, self.reversibility)

class ReducedPDChildren(Children):
    def __init__(self, name, id):
        Children.__init__(self, name, id)


class ReducedPDEdge():
    def __init__(self, parent_id, node_id, reaction):
        self.__edge = []
        self.reaction = [reaction]
        # a combination of parent and children if there is no parent the first number will be set to 0
        self.id = (parent_id,node_id)

    @property
    def edge(self):
        return self.__edge

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{0}-{1}".format(self.id, self.reaction)

class ReducedPDNode(Node):
    def __init__(self, complex, positive_cont, id, new_lvl=True):
        self.name = ""
        self.get_name(complex.molecules)
        Node.__init__(self, self.name, id, new_lvl=new_lvl)
        self.node_object = complex
        self.positive_cont = positive_cont
        self.parent = []

    @property
    def node_object(self):
        return self.__node_object

    @node_object.setter
    def node_object(self, value):
        if isinstance(value, BiologicalComplex):
            self.__node_object = value

    def update_children(self, name, id, mode=_ADD):
        if mode == _ADD:
            self.children.append(ReducedPDChildren(name, id))
        if mode == _DELETE:
            for i,child in enumerate(self.children):
                if id == child.id and name == child.name:
                    del self.children[i]
        if mode == _INSERT:
            pass

    def get_loc_domain(self, domains, used_domains, mol):
        # 1. Localisation domain
        loc_str = ''

        if mol.localisation:
            loc_str += '~%s' % (mol.localisation.modifier)
        if mol.alternative_localisations:
            for loc in sorted(mol.alternative_localisations):
                loc_str += '~%s' % loc
        if loc_str:
            dom = mol.localisation.components[0].domain
            domains.append('%s%s' % (dom, loc_str))
            used_domains.append(dom)
        return domains, used_domains

    def get_mod_domain(self, domains, used_domains, mol):
        # 2. Covalent modification domains
        mod_domains = []
        for modif in mol.modifications:
            if modif.components[0].domain not in used_domains:
                used_domains.append(modif.components[0].domain)
                mod_domains.append('%s~%s' % (modif.components[0].domain, modif.modifier))

        mod_domains.sort()
        domains += mod_domains

        return domains, used_domains

    def get_molecule_str(self, mol):
        """
        Returns molecule string.
        String contains:
        - all possible localisations
        - all all modification sites with both True and False modifiers
        """

        domains = []
        used_domains = []

        domains, used_domains = self.get_loc_domain(domains, used_domains, mol)
        domains, used_domains = self.get_mod_domain(domains, used_domains, mol)

        if domains:
            result = "%s(%s)" %(mol.name, ','.join(domains))
        #else:
        #    result = mol.name
            return re.sub('[-/]', '', result)

    def format_name(self, mol, first=False):
        modifications = self.get_molecule_str(mol)
        #modifications = ",".join(mol.modifications)
        if modifications:
            if first:
                self.name+= modifications
            else:
                self.name+="-%s"%(modifications)
        else:
            if first:
                self.name+=mol.name
            else:
                self.name+="-%s"%mol.name

    def get_name(self, molecules):
        """
        creates names they should look like Ste5-Ste5-St7_{P,Ub}-Ste11
        modification are only shown if they are present
        @param molecules: list of Molecule objects
        @return:
        """
        for i, mol in enumerate(molecules):
            if i == 0:
                self.format_name(mol, first=True)
            else:
                self.format_name(mol)


class ReducedPDTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.last_node = ""
        self.edges = []

    def set_parent(self, node, parent_list):
        """
        set the parent to a respective node
        @param node:
        @param parent_list:
        @return:
        """
        if parent_list is None:
            node.parent.append((None, None))
            return node
        for parent_id in parent_list:
            parent_node = self.get_node(parent_id)
            self.add_parent(parent_node, node)
        return node

    def set_edge(self, node, parent_list, reaction):
        if parent_list is None:
            pass # if partents list are None we have the roots there are no edges
        else:
            for parent_id in parent_list:
                self.add_edge(node=node, parent_id=parent_id, reaction=reaction)

    def add_edge(self, node, parent_id, reaction):
        edge = ReducedPDEdge(parent_id=parent_id, node_id=node.id, reaction=reaction)
        #if edge.id in self.edges:

        self.edges.append(edge)

    def get_edge(self, parent_id, child_id):
        for edge in self.edges:
            if edge.id == (parent_id, child_id):
                return edge

    def remove_edge(self):
        pass

    def add_Node(self, complex, id=None, parent_list=None, parent_id=None, reaction=None, reversibility=None):
        """
        add a node in a tree
        """
        if id is None:
            id = self.get_highest_id()
            id += 1


        # get list of properties
        positive_cont = []
        for mol in complex.molecules:
            positive_cont.extend([str(binding_partner) for binding_partner in mol.binding_partners])
            positive_cont.extend([str(modification) for modification in mol.modifications])
        positive_cont = set(positive_cont)
        node = ReducedPDNode(complex=complex, positive_cont=positive_cont, id=id)
        edge_reaction = EdgeReaction(reaction.rtype,reaction.definition["Reversibility"])
        if self.has_node(node.name):
            node = self.nodes[self.get_index(node.name)]
            self.last_node = node.name
            if parent_list is not None:
                for parent_id in parent_list:
                    parent_node = self.get_node(parent_id)
                    parent_tuple = (parent_node.name, parent_node.id)
                    node_tuple = (node.name, node.id)
                    if parent_tuple not in node.parent and node_tuple[1] not in parent_list:
                            self.add_parent(parent_node, node)
                            self.add_edge(node=node, parent_id=parent_tuple[1], reaction=reaction)
                    if parent_tuple in node.parent and node_tuple[1] not in parent_list:
                        edge = self.get_edge(parent_tuple[1], node_tuple[1])
                        if edge is not None and reaction not in edge.reaction:
                            edge_reaction = EdgeReaction(reaction.rtype, reaction.substrat_complexes.molecules, reaction.product_complexes.molecules, reaction.definition["reversibility"])
                            edge.reaction.append(edge_reaction)
            return
        elif not self.has_node(node.name) and len(node.node_object.molecules) > 1 and not parent_list:

            parent_list = []
            mols_needed = copy.deepcopy(node.node_object.molecules)
            # find node with most common properties
            tree_node_sharing_most_properties = []
            max = 0
            for tree_node in self.nodes:
                sharing_properties = tree_node.positive_cont.intersection(node.positive_cont)
                if len(sharing_properties) > max:
                    tree_node_sharing_most_properties = tree_node
                    max = len(sharing_properties)

            assert tree_node_sharing_most_properties
            parent_list.append(tree_node_sharing_most_properties.id)

            states_left = node.positive_cont.difference(tree_node_sharing_most_properties.positive_cont)
            mols_left = []
            mols_used = []
            while len(mols_needed) > 0:
                mol = mols_needed.pop()
                if mol not in tree_node_sharing_most_properties.node_object.molecules:
                    mols_left.append(mol)
                else:
                    mols_used.append(mol)

            if len(mols_left) == 1:
                edge_reaction = EdgeReaction("2.1.1.1", "reversible")
                parent_list.append(self.get_index(mols_left[0].name))

        self.nodes.append(node)
        self.last_node = node.name
        self.set_parent(node=node, parent_list=parent_list)
        self.set_edge(node=node, parent_list=parent_list, reaction=edge_reaction)


    def add_parent(self, parent, node):
        """
        update function if node is known but a parent missing
        @param parent_id: int
        @param node: ReducedPDNode obj
        @return:
        """
        parent_tuple = (parent.name, parent.id)
        self.update_children(parent_tuple, node.name, node.id, _ADD)
        node.parent.append((parent.name, parent.id))

        #node.parent.append(parent_tuple)
        #self.update_children(parent_tuple[0],node.name, node.id, _ADD, parent_tuple[1])

    def show(self, position, level=_ROOT):
        """
        basic visualisation of the tree for testing and developing
        """
        if self.contains(position):
            node = self.get_node(id=position)
            queue = node.children
            print("\t" * level, "{0} [{1}] parent: {2}".format(node.name, node.id, node.parent))
            if node.new_lvl:
                level += 1
                for element in queue:
                    self.show(element, level)  # recursive call
        else:
            raise NameError("Node {0} does not exists!".format(position))


class ReducedProcessDescription(object):

    """"""

    def __init__(self,reaction_pool):
        """Constructor for ReducedProcessDescription"""
        self.tree = ReducedPDTree()
        self.reaction_pool = reaction_pool

    def build_reaction_Tree(self):
        for rxn_container in self.reaction_pool:
            for rxn in rxn_container:
                parents = []
                for substrate_complex in rxn.substrat_complexes:
                    self.tree.add_Node(complex=substrate_complex, reaction=rxn )
                    parents.append(self.tree.nodes[self.tree.get_index(self.tree.last_node)].id)
                for product_complex in rxn.product_complexes:
                    self.tree.add_Node(complex=product_complex, parent_list=parents, reaction=rxn)

if __name__ == "__main__":
    TOY1 = """
    Ste11_ppi_Ste7
    Ste11_[KD]_P+_Ste7_[(ALS359)]; ! Ste11--Ste7
    """
    TOY2 = """
    a_p+_b
    a_p+_c
    """
    TOY3 = """
    a_p+_b_[x]
    c_p+_b_[x]
    """
    TOY4 = """Ste5_ppi_Ste11
    Ste5_ppi_Ste7
    Ste5_ppi_Ste5
    Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <b>
    <b>; AND Ste5--Ste11
    <b>; AND Ste5--Ste7
    <b>; AND Ste5--Ste5"""

    TOY5 = """
    A_ppi_C
    C_ppi_E
    A_p+_B_[x]; ! <comp>
    <comp>; AND A--C
    <comp>; AND C--E
    """
    TOY6 = """
    A_ppi_B
    B_ppi_C
    C_ppi_E
    E_p+_C; ! C--E
    A_p+_E; ! <comp>
    <comp>; AND <Ccomp>
    <comp>; AND <Acomp>
    <Ccomp>; AND C--E
    <Ccomp>; AND C-{P}
    <Acomp>; AND A--B
    <Acomp>; AND B--C
    """

    rxncon = Rxncon(TOY6)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    # TOY2 = """Ste5_ppi_Ste11
    # Ste5_ppi_Ste7
    # Ste5_ppi_Ste5
    # Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <b>
    # <b>; AND Ste5--Ste11
    # <b>; AND Ste5--Ste7
    # <b>; AND Ste5--Ste5"""
    #


    # TOY5 = """
    # Ste5_ppi_Ste11
    # Ste5_ppi_Ste7; ! Ste5--Ste11
    # Ste5_ppi_Fus3
    # Fus3_ppi_Ste7; ! Ste5--Fus3
    # Fus3_ppi_Ste7; ! Ste5--Ste7
    # """
    #
    # TOY6 = """
    # Ste5_ppi_Ste11
    # Ste5_ppi_Ste7
    # Ste5_ppi_Fus3
    # Fus3_ppi_Ste7; ! Ste5--Fus3
    # Fus3_ppi_Ste7; ! Ste5--Ste7
    # Ste7_P+_Fus3; ! <ComplexC>
    # <ComplexC>; AND Fus3--Ste7
    # <ComplexC>; AND Ste5--Ste11
    # <ComplexC>; AND Ste5--Ste7
    # """
