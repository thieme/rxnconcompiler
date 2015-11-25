#!/usr/bin/env python

"""
-------------------------
Module complex_builder.py
-------------------------
Algorithms for building complexes:
- positive complexes from a booliean contingency
- negative complexes from a positive complex and a root molecule 
- required complexes from a group of positive complexes and a root molecule

Positive complexes - one or more BiologicalComplex
    created from a boolean contingency kept by AlternativeComplexes.
    AND - one complex, OR - more complexes.
    Main contingency type (!, x, K+, K-) does not matter here.
    All compexes in this group can fulfill their biological function.

Root molecule - Molecule that conects the complex to the reaction.
    e.g. for a reaction: A_ppi_B and a complex: X-Y-A-Z it is A.

Negative complexes - one or more BiologicalComplex
    that doesn't have some Moleules (one or more) missing
    in comparison to a single positive complex so it cannot 
    fulfill its biological function.
    To create negative complexes a root molecule is neccesary.
    It allows to built a tree of Molecules so they can be sistematically cat out.
    OR - one complex, AND - more complexes.  
    Main contingency type (!, x, K+, K-) does not matter here.

Required complexes - one or more complexes created based on 
    positive and negative complexes and main contingency type
    (of the boolean contingency) - !, x, K+, K-.
    First required complex will be just positive complex.
    Second will be a sum (complex_addition) 
    of second positive and negative from first.


--------------------------------------------------------------
How contingencies with Input states inside boolean are treated?
--------------------------------------------------------------
- input_conditions parameter is set to a Contingency for liable complexes.
- it is done at the end of the process.
(- later in the flow when applying complexes on reaction it will change reaction rate.) 
"""

import itertools
import copy
import re

from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.util.rxncon_errors import RxnconBooleanError
from complex_tree import ComplexTree

(_ADD, _DELETE, _INSERT) = range(3)

class ComplexBuilder:
    """

    """
    def __init__(self):
        self.states = []
        self.final_states = []

    def flatten_bool(self, bool_cont):
        """
        Builds a flatten list from boolean (containing children) contingency <cont>.
        It can be normal boolean or defined complex
        (which is in fact AND boolean).

        Returns a list of lists of contingencies.

        @param bool_cont:  ContingencyFactory obj
        @return final_states: list of contingencies
        @type final_states: list
        """

        self.get_state_sets(bool_cont) # we want only the list
        return self.final_states

    def check_for_structured_complex(self, complexes, root):
        """
        This function checks if a complex is already structured.
        @return: structured complex
        """
        for complex_tuple in complexes:
            for complex in complex_tuple[1]:
                for cont in complex:
                    if "--" in cont.ctype or re.match("^[1-9]*$", cont.ctype):
                        if self.check_cont_components(cont, root):
                            return complex
                    else:
                        break

        return []

    def structure_complex(self, complexes, reaction_container):
        """
        This function was implemented to structure a certain given complex in regard to the respective reaction.
        The structure can vary with different reactoins
        @param complexes: tuple (contingency, list of list of contingencies)
        @param reaction_container:
        @return:
        """
        self.complexes_test = complexes
        possible_roots = reaction_container.get_reactants()

        self.tree = ComplexTree()

        for root in possible_roots[::-1]: # start with modified first
            if self.tree.get_node(name=root.name) is None:
                self.tree.add_Node(root.name)
                root_node = self.tree.get_node(name=root.name)
                self.structured_complexes = self.check_for_structured_complex(complexes, root_node)
                if self.structured_complexes:
                    self.get_structured_complex(self.structured_complexes, root_node, structure=True)
            #    already = self.tree.get_all_cont()
                for complex_tuple in complexes:
                    for complex in complex_tuple[1]:
                        if complex != self.structured_complexes:
                            self.get_structured_complex(complex, self.tree.get_node(name=root.name))  # TODO: root_node

        self.process_structured_complex()

    def check_cont_components(self, cont, root):
        for component in cont.state.components:
            if component.name == root.name: # first check if the name of the components are the same
                if root.old_cid is None: # if the olc_cid is None then this is the very first root
                    return True
                elif component.cid == root.old_cid: # otherwise the cid of the component should be the same as the old_cid (then they are connected)
                    return True
        return False

    def get_cont_for_root(self, root, inner_list, structure, ):
        root_cont = []
        for cont in inner_list:
                if structure:
                    if self.check_cont_components(cont, root):
                        root_cont.append(cont)
                else:
                    if cont.state.has_component(root):
                        root_cont.append(cont)
        return root_cont

    def initialise_root_old_cid(self, root, root_cont):

        for cont in root_cont:
            for component in cont.state.components:
                if component.name == root.name:
                    if root.old_cid is None:
                        root.old_cid = component.cid
                    elif int(root.old_cid) > int(component.cid):
                        root.old_cid = component.cid

    def get_structured_complex(self, inner_list, root, structure=False):
        """

        """
        stack = [root]
        if not structure:
            for cont in inner_list:
                if "--" in inner_list[0].ctype:
                    structure = True
                    if root.old_cid is not None:
                        self.tree.reset_old_cid()
                    break
        already = []
        while stack:
            stack, already = self._get_complex_layer(inner_list, stack, structure, already)

    def _get_complex_layer(self, inner_list, root_list, structure, already = []):
        """
        Helper function for get_ordered_tree.

        save the path of a certain component
        use the mol structure for saving the id and the path
        """
        def non_structured(new_root, root):
            if not new_root.name in self.tree.children_by_name(root): # check if the node already exists
                self.tree.add_Node(new_root.name, parent=root.name, parent_cid=root.cid)
            else:
                child = self.tree.get_node(name=new_root.name, parent_cid=root.cid)
                root.update_children(child.cid, _ADD)

        def structured(new_root, root, bond):
            if not new_root.name in self.tree.children_by_name(root): # check if the node already exists
                self.tree.add_Node(new_root.name, parent=root.name, parent_cid=root.cid, old_cid=new_root.cid)

            else:
                child = self.tree.get_node(name=new_root.name, parent_cid=root.cid)
                root.update_children(child.cid, _ADD)
                if root_node.old_cid is None:
                    old_root = bond.state.get_partner(bond.state.get_component(new_root.name))
                    if old_root is not None:
                        root_node.old_cid = old_root.cid
                if child.old_cid == None:
                    child.old_cid = new_root.cid
        def get_new_root(bond, root):
            if structure and bond.state.homodimer:
                # in case of a structured complex we want the component of a homodimer which differs from the root
                for comp in bond.state.components:
                    if comp.cid != root.old_cid:
                        return comp
            else:
                # if it is an unstructured complex is does not matter which of both we get, because the name is important only
                return bond.state.get_partner(bond.state.get_component(root.name))

        #already = self.tree.get_all_cont()
        new_roots = []
        for root in root_list:
            root_node = self.tree.get_node(cid=root.cid)
            root_cont = self.get_cont_for_root(root, inner_list, structure)
            # in this case we have to figure out what the correct Molecule is in case of multiple molecules with
            # the same name within a structured complex
            # in this case we take the molecule with the lowest index number as the the root
            if structure and root.old_cid is None:
                self.initialise_root_old_cid(root, root_cont)
                root_cont = self.get_cont_for_root(root, inner_list, structure)

            for bond in root_cont:
                if bond not in already:  # to avoid double contingency recognistion A--B, root: A next root B
                    already.append(bond)
                    if bond.state.type == "Association":

                        new_root = get_new_root(bond, root)

                        if structure:
                            structured(new_root, root_node, bond)
                        else:
                            non_structured(new_root, root_node)
                        root_node.cont.append(bond)
                        new_roots.append(self.tree.get_node(name=new_root.name, parent_cid=root.cid))
                    else:
                        comp = bond.state.components[0]
                        if structure:
                            structured(comp, root_node, bond)
                        else:
                            non_structured(comp, root_node)
                        root_node.cont.append(bond)
                        new_roots = new_roots
        return new_roots, already

    def process_structured_complex(self):
        """
        This function iterates over the constructed tree and adapted the contingencies for a certain parent, children

              A (cid: 1) (cont: and A--B, and A--C)
            /  \
           B   C
        (cid:2)(cid:3)

        [1--2 A--B, 1--3 A--C]

        @return:
        """
        for root in self.tree.get_root_nodes():
            if root.children:
                self.update_tree_contingencies(root.cid)


    def update_tree_contingencies(self, node_cid):
        """
        helper function for process_structured_complex
            sid: is a property of state which shows the orientation/structured relation of the components
                 if structured: 1--2 or something like that
                 if not structured: None
            ctype: shows the contingency type if we have a sid then the type is the same as the sid otherwise it
                   is another contingency
        @param node_cid: cid of a certain node (new root)
        @return:
        """
        if self.tree.contains(node_cid):
            node = self.tree.get_node(cid=node_cid)
            queue = node.children
            if node.new_lvl:

                for i, child_cid in enumerate(queue):
                    child_node = self.tree.get_node(child_cid)
                    root_cont = node.cont[i]
                    # ToDo: what if we have modification then it should be just an integer
                    if len(root_cont.state.components) > 1:
                        if root_cont.state.components[0].name == node.name:
                            sid = "{0}--{1}".format(node.cid ,child_node.cid)
                        else:
                            sid = "{0}--{1}".format(child_node.cid, node.cid)
                    else:
                        #if we have a modification or relocalisation in a structured complex the sid
                        # should show where the modifcation/relocalisation occures
                        sid = str(node.cid)
                    state = get_state(root_cont.state.state_str, sid)
                    # if we have a boolean AND/OR we can change the ctype into --
                    # else we should keep the contingency and just change the cid (complex id)
                    if root_cont.ctype in ["and", "or"] or "--" in root_cont.ctype or re.match("^[1-9]*$", root_cont.ctype):
                        root_cont.ctype = sid
                    root_cont.state = state
                    self.update_tree_contingencies(child_cid)  # recursive call
        else:
            raise NameError("NodeID {0} does not exists!".format(node_cid))

    def get_state_sets(self, bool_cont):
        """
        Traverses through a contingencies list.
        Starts with root contingency that keeps all other contingencies.
        Uses get_states to go one level deeper until there are no more
        contingencies with children. 
        At the end the self.final_states list contain lists with states.
        Each list corresponding to a complex.
        """
        self.states.append([bool_cont])
        while self.states:  # [AND A--C, AND <NOT>]
            state_list = self.states.pop()  # [AND A--C, AND <NOT>]
            self.get_states(state_list)

    def check_bool_type(self, children):
        """
        It is not allowed to mix bool types hence if one child has a specific bool the other children should have the same
        This function is written to test this
        @param children: children of a specific boolean
        @return: True if everything is fine
        @return: False if booleans are mixed


        """
        # TODO: if not implemented bool raise error/warning add it to warnings don't raise and break the program
        reference_child_ctype = children[0].ctype
        for child in children[1:]:
            if (("--" in reference_child_ctype or re.search("^[1-9]*$", reference_child_ctype)) and not ("--" in child.ctype or re.search("^[1-9]*$", child.ctype))):
                raise RxnconBooleanError('Boolean not proper defined mix of {0} and {1}'.format(reference_child_ctype, child.ctype))
            elif (not ("--" in reference_child_ctype or re.search("^[1-9]*$", reference_child_ctype)) and reference_child_ctype != child.ctype):
                raise RxnconBooleanError('Boolean not proper defined mix of {0} and {1}'.format(reference_child_ctype, child.ctype))
        return True

    def get_states(self, node_list):
        """
        Moves contingencies from a given list to
        either self.states (booleans - children) 
        or to self.final_states (leafs - no children)
        """
        to_remove = []
        to_add = []
        to_clone = []
        
        for node in node_list: # [AND <NOT>]
            if node.has_children: # [NOT A--E]
                if len(node.children) > 1:
                    self.check_bool_type(node.children)
                to_remove.append(node)
                child = node.children[0]

                if child.ctype == 'and' or '--' in child.ctype or re.match("^[1-9]*$", child.ctype):
                    to_add.extend(node.children)
                elif child.ctype == 'or':
                    if node.ctype is not None and (node.ctype == "and" or '--' in node.ctype or re.match("^[1-9]*$", node.ctype)):
                        to_clone.append(node.children) # [[AND A--C, AND A--E], [AND A--F, AND A--D]]
                    else:
                        to_clone.extend(node.children) # [AND A--C, AND A--E , AND A--F, AND A--D]
                elif child.ctype == 'not' and (node.ctype!= None and (node.ctype == "and" or '--' in node.ctype or re.match("^[1-9]*$", node.ctype))):
                    for child in node.children:
                        child.ctype = "x"
                        to_add.append(child)
                elif child.ctype == 'not' and node.ctype == "or":
                    for child in node.children:
                        child.ctype = "x"
                        to_clone.append(child)

        for node in to_remove:
            node_list.remove(node)

        if to_add:
            for node in to_add:
                node_list.append(node)  # [<complB>, A--F, A--E] AND A--C -> [AND A--C]
            bool_flag = False
            for node in node_list:
                if node.has_children and len(node.children) > 0:
                    bool_flag = True
            if bool_flag:
                self.states.append(node_list)  # [<complA>, <complB>]
            else:
                self.final_states.append(node_list)

        elif to_clone:

            to_clone_copy = copy.deepcopy(to_clone)
            # remove all lists from to_clone and just keep single ORs
            # lists are saved in another object for later combination
            to_combine = [to_clone.pop(to_clone.index(ele)) for ele in reversed(to_clone_copy) if isinstance(ele,list)]

            # get combinations of this boolean OR level if the previous lvl was an AND
            to_combine = list(itertools.product(*to_combine))  # this returns at least an empty tuple
            if to_combine[0]:
                to_clone += to_combine

            for node in to_clone:
                if isinstance(node, tuple):
                    result = node_list + list(node) # [] + [OR A--C] -> [[OR A--C]] # [AND A--D] + [OR A--C] -> [AND A--D, OR A--C]
                else:
                    result = node_list + [node]
                bool_flag = False
                for node in result:
                    if node.has_children and len(node.children) > 0:
                        bool_flag = True
                if bool_flag:
                    self.states.append(result)
                else:
                    self.final_states.append(result)


if __name__ == "__main__":
    tree = ComplexTree()
    tree.add_Node("A", cid=3)
    tree.add_Node("B", cid=4 , parent="A")
    tree.add_Node("B", parent="B", parent_cid=4)
    tree.add_Node("D", parent="B")
    tree.add_Node("C", parent="B", parent_cid=5)
    #leafs = tree.get_leaf(3)
    tree.show(3)