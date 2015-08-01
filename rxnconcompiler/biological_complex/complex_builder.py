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
from zeitgeist.datamodel import child

from biological_complex import BiologicalComplex, \
        AlternativeComplexes
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.util.util import product
import itertools
import copy

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
            if not "--" in reference_child_ctype and reference_child_ctype != child.ctype:
                raise Exception('Boolean not properly defined mix of {0} and {1}'.format(reference_child_ctype, child.ctype))
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

                if child.ctype == 'and' or '--' in child.ctype:
                    to_add.extend(node.children)
                elif child.ctype == 'or':
                    if node.ctype == "and":
                        # todo: check not --
                        to_clone.append(node.children) # [[AND A--C, AND A--E], [AND A--F, AND A--D]]
                    else:
                        to_clone.extend(node.children) # [AND A--C, AND A--E , AND A--F, AND A--D]
                elif child.ctype == 'not' and node.ctype == "and":
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
