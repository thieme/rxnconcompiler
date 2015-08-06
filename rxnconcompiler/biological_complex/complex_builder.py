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

from biological_complex import BiologicalComplex, \
        AlternativeComplexes
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.util.util import product

class ComplexBuilder:
    """
    Colection of algorithms creating groups of complexes.
    (BiologicalComplex objects keept by AlternativeComplexes).
    """
    def __init__(self):
        self.states = []
        self.final_states = []

    def helper_required_complexes(self, all_single_complexes, root):
        """
        Gets all positive and negative complexes as a list of tuples:
        [(PositiveComplex: (NegativeComplex, NegativeComplex, ...)), ...)]

        Goes through Positive : (neg1, neg2, neg3 ...) pairs.
        1 iteration:
          required gets positive1
          negative1 = negative1
        2 iteration:
          requires gets positive2 + each negative1
          (there are so many new positive complexes as there were negative
          + means that complexes are added and create tugether one complex) 
          negative change ???
        3 iteration:
          requires gets positive3 + each negative2
          negative change ???
          ...

        Returns required complexes (AlternativeComplexes object) 
        and list of negative complexes from the last iteration.
        """

        required_complexes= AlternativeComplexes('')
        negative = []
        for comp in all_single_complexes:
            if negative == []:
                required_complexes.add_complex(comp[0])
                negative = comp[1]
            else:
                for neg in negative:
                    required_complexes.add_complex(neg.complex_addition(comp[0], root))
                # What is this
                negative = [first_comp.complex_addition(sec_comp, root) for first_comp, sec_comp in product(negative, comp[1])]
        return required_complexes, negative

    def apply_input_contingency(self, bool_ctype, input_cont, required_complexes, result):
        """
        Sets input_conditions parameter 
        for complexes in a ready required complexes
        (it ia a Contingency).

        It does it based on main contingency (!, x, K+, K-) 
        and type of boolean (AND, OR).
        """
        if bool_ctype == "!":
            if  input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex
                compl.input_conditions = [Contingency(None, '!', input_cont.state)]
                compl.is_positive = True
                required_complexes.add_complex(compl)
            elif  input_cont.ctype == 'and':
                compl = result[0][0] # single positive complex
                compl.input_conditions = [Contingency(None, '!', input_cont.state)]  

        elif bool_ctype == "x":
            if  input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex     
                compl.input_conditions = [Contingency(None, 'x', input_cont.state)]
                compl.is_positive = False          
            elif  input_cont.ctype == 'and':
                compl = result[0][0]  # single positive complex
                compl.input_conditions = [Contingency(None, 'x', input_cont.state)]
                compl.is_positive = False
                required_complexes.add_complex(compl)
                #required_complexes[0].input_condition = Contingency(None, '!', input_cont.state)  # single positive complex

        else: # k+/k- (which means ! and x) 
            if  input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex
            elif  input_cont.ctype == 'and':
                compl = result[0][0]  # single positive complex
            compl.input_conditions = [Contingency(None, '!', input_cont.state), Contingency(None, 'x', input_cont.state)]
            compl.is_positive = 'both'

    def build_required_complexes(self, positive_complexes, root):
        """
        Builds all required complexes for one boolean contingeny.

        @type root:  Molecule object
        @param root: a molecule from a reaction for which complex will be applied.
        """
        # Build all posibilities
        all_single_complexes = []
        for comp in positive_complexes:
            negative = self.build_negative_complexes(comp, root)
            all_single_complexes.append((comp, negative))
        result = self.helper_required_complexes(all_single_complexes, root)

        # Chooses required complexes from all possibilities (result)
        # based on main contingencies type (x, !, K+, K-).
        if positive_complexes.ctype == "!": 
            # C1; not C1, C2; not C1, not C2, C3 ...
            required_complexes = result[0]
            if positive_complexes.input_condition:
                self.apply_input_contingency('!', \
                    positive_complexes.input_condition, required_complexes, result)

        elif positive_complexes.ctype == "x":
            # not C1, not C2, not C3 ...
            required_complexes= AlternativeComplexes('')
            for neg_comp in result[1]:
                required_complexes.add_complex(neg_comp)
            if positive_complexes.input_condition:
                self.apply_input_contingency('x', \
                    positive_complexes.input_condition, required_complexes, result)

        elif 'k' in positive_complexes.ctype:
            # ! and x 
            required_complexes = result[0]
            for neg_comp in result[1]:
                required_complexes.add_complex(neg_comp)
            if positive_complexes.input_condition:
                self.apply_input_contingency(positive_complexes.ctype, \
                    positive_complexes.input_condition, required_complexes, result)

        return required_complexes

    def build_positive_complexes_from_boolean(self, bool_cont):
        """
        Builds positive complexes from boolean (containing children) contingency <cont>.
        It can be normal boolean or defined complex
        (which is in fact AND boolean).

        #WARNING: so far boolean can have only interaction states.

        Returns AlternativeComplexes object.
        Information about Input states is stored in AlternativeComplex.input_condition.
        """
        alter_comp = AlternativeComplexes(str(bool_cont.state))
        alter_comp.ctype = bool_cont.ctype

        complexes = []
        self.get_state_sets(bool_cont)
        for state_group in self.final_states:
            comp = BiologicalComplex()
            if self.check_conection(state_group):
                self.stack = state_group
                while self.stack:
                    state = self.stack.pop()
                    if state.state.type == 'Input':
                        alter_comp.input_condition = state
                    else:
                        result = comp.add_state(state.state)
                        if result:
                            self.stack = result + self.stack
            if comp.molecules:
                complexes.append(comp)

        complexes = sorted(complexes, key=lambda comp: len(comp))
        for cid, comp in enumerate(complexes):
            comp.cid = str(cid + 1)
            alter_comp.add_complex(comp)

        return alter_comp

    def check_conection(self, states):
        """Asures that all molecules within given group of states are conected."""
        return True

    def get_state_sets(self, bool_cont):
        """
        Traverses through a contingenies list.
        Starts with root contingency that keeps all other contingencies.
        Uses get_states to go one level deeper until there are no more
        contingencies with children. 
        At the end the self.final_states list contain lists with states.
        Each list coresponding to a complex.
        """
        self.states.append([bool_cont])
        while self.states:
            state_list = self.states.pop()
            self.get_states(state_list)

    def get_states(self, node_list):
        """
        Moves contingencies from a given list to
        either self.states (booleans - children) 
        or to self.final_states (leafs - no children)
        """
        to_remove = []
        to_add = []
        to_clone = []
        
        for node in node_list:
            if node.has_children:
                to_remove.append(node)
                for child in node.children:
                    if child.ctype == 'and' or '--' in child.ctype:
                        to_add.append(child)
                    if child.ctype == 'or':
                        to_clone.append(child)

        for node in to_remove:
            node_list.remove(node)

        if to_add:
            for node in to_add:
                node_list.append(node)
            bool_flag = False
            for node in node_list:
                if node.has_children and len(node.children) > 0:
                    bool_flag = True
            if bool_flag:
                self.states.append(node_list)
            else:
                self.final_states.append(node_list)

        elif to_clone:
            for node in to_clone:
                result = node_list + [node]
                bool_flag = False
                for node in result:
                    if node.has_children and len(node.children) > 0:
                        bool_flag = True
                if bool_flag:
                    self.states.append(result)
                else:
                    self.final_states.append(result)

    def build_negative_complexes(self, compl, root_molecule):
        """
        @type complex:  BiologicalComplex
        @param complex: complex to negate.

        @type root_molecule:  string
        @param root_molecule: name of reaction component - 
                              the molecule that alvays needs to be there.

        #TODO: What if we have two root molecules
        """
        ordered_states = self.get_states_from_complex(compl, root_molecule)
        alter_comp = AlternativeComplexes('')
        counter = len(ordered_states) -1
        while counter: 
            comp = BiologicalComplex()
            comp.is_positive = False
            for state in ordered_states[:counter]:
                comp.add_state(state)
            last_state = ordered_states[counter]
            mols = comp.get_molecules(last_state.components[0].name)
            mols += comp.get_molecules(last_state.components[1].name)
            mols[0].add_binding_site(last_state)
            alter_comp.add_complex(comp)
            counter -=1

        comp = BiologicalComplex()
        comp.is_positive = False
        mol = Molecule(root_molecule.name)
        mol.add_binding_site(ordered_states[0])
        comp.molecules.append(mol)
        alter_comp.add_complex(comp)
        return alter_comp

    
    def get_states_from_complex(self, compl, root_molecule):
        """
        Given single BiologicalComplex returns a list of 
        interaction states that 'create' the complex.
        List is ordered according to the layers starting 
        from states that include given root_molecule.

                 A
               / | \
              /  |  \
             /   |   \
            B    C    D
           / \       / \
          /   \     /   \
         F     E    G    H
              / \
             /   \
            K     J

        Returns: 
        [ A--B, A--C, A--D,
          B--F, B--E, D--G, D--H,
          E--K, E--J ]
        Order within the layers is not important.
        """
        result = []
        stack = [root_molecule]
        while stack:
            states_mols = self._get_complex_layer(compl, stack, result)
            result += states_mols[0]
            stack = states_mols[1]
        return result

    def _get_complex_layer(self, compl, root_list, already=None):
        """
        Helper function for get_states_from_complex.
        """
        if not already:
            already = []
        result = []
        new_roots = []
        for root_molecule in root_list:
            mol = compl.get_molecules(root_molecule.name)[0]
            for bond in mol.binding_partners:
                if bond not in already:
                    result.append(bond)
                    new_root = bond.get_partner(mol.get_component())
                    new_roots.append(new_root)
        return result, new_roots
