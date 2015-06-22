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
            if input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex
                compl.input_conditions = [Contingency(None, '!', input_cont.state)]
                compl.is_positive = True
                required_complexes.add_complex(compl)
            elif input_cont.ctype == 'and':
                compl = result[0][0] # single positive complex
                compl.input_conditions = [Contingency(None, '!', input_cont.state)]  

        elif bool_ctype == "x":
            if input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex     
                compl.input_conditions = [Contingency(None, 'x', input_cont.state)]
                compl.is_positive = False          
            elif input_cont.ctype == 'and':
                compl = result[0][0]  # single positive complex
                compl.input_conditions = [Contingency(None, 'x', input_cont.state)]
                compl.is_positive = False
                required_complexes.add_complex(compl)
                #required_complexes[0].input_condition = Contingency(None, '!', input_cont.state)  # single positive complex

        else:  # k+/k- (which means ! and x) 
            if input_cont.ctype == 'or':
                compl = result[1][0]  # single negative complex
            elif input_cont.ctype == 'and':
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
        #print "###all_single_complexes: ", all_single_complexes
        #for tupl in all_single_complexes:
        #    for mol in tupl[0].molecules:
                #print "mol.inspect: ", mol.inspect() 

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
        
    def create_basic_complexes_from_boolean(self, alter_comp):
        """
        This function generates biological complexes from a flatten list of booleans (self.final_states)
        @param alter_comp: AlternativeComplex obj
        @return complexes: list of BiologicalComplex obj
        @type complexes: list
        @return alter_comp: AlternativeComplex obj
        """

        complexes = []
        # if state appears more than 1 warning
        # if contra sign kill complex and make stronger warning 
        for state_group in self.final_states:
            comp = BiologicalComplex()
            self.stack = state_group
            while self.stack:
                state = self.stack.pop()
                if state.state.type == 'Input':
                    # negative input
                    # multiple inputs
                    alter_comp.input_condition = state
                elif state.state.type == "Covalent Modification":
                    comp.add_state_mod(complexes, state)
                # TODO: loc ...
                elif state.state.type == "loc":
                    pass
                elif state.state.type == "Association":
                    result = comp.add_state(state) # A--B
                    if result:
                        self.stack = result + self.stack
                else:
                    # todo: make a clear error if the reaction is not defined
                    assert "reaction not defined"
            if comp.molecules:
                # each self.stack results in one comp
                complexes.append(comp)
                #[A, D, C, B]
        return complexes, alter_comp

    def build_positive_complexes_from_boolean(self, bool_cont):
        """
        Builds positive complexes from boolean (containing children) contingency <cont>.
        It can be normal boolean or defined complex
        (which is in fact AND boolean).

        #WARNING: so far boolean can have only interaction and modification states

        Returns AlternativeComplexes object.
        Information about Input states is stored in AlternativeComplex.input_condition.

        @param bool_cont:  ContingencyFactory obj
        @return alter_complexes: list of AlternativeComplex obj
        @type alter_complexes: list
        """
        alter_complexes = []
        self.get_state_sets(bool_cont)

        alter_complexes.append(copy.deepcopy(self.final_states)
        alter_comp = AlternativeComplexes(str(bool_cont.state))
        alter_comp.ctype = bool_cont.ctype  # set the ctype later its the same as positive_complexes.ctype
        complexes, alter_comp = self.create_basic_complexes_from_boolean(alter_comp)
        complexes = sorted(complexes, key=lambda comp: len(comp))
        for cid, comp in enumerate(complexes):# [ACDB, AC]
            comp.cid = str(cid + 1)
            alter_comp.add_complex(comp)
        alter_complexes.append(alter_comp)

        return alter_complexes

    def check_state_connected_to_stack(self, state, state_stack):
        for ele in state_stack:
            if state.state.has_component(ele.state.components[0]):
                return True
            elif len(ele.state.components) > 1 and state.state.has_component(ele.state.components[1]):
                return True
        return False

    def check_if_input(self, stack):
        """
        This function checks if the state_group consists only of input
        if one of the elements is not an input False is returned
        """
        for ele in stack:
            if ele.state.type != 'Input':
                return False
        return True

    def check_state_connection(self):
        # we do this later
        """
        This function checks the connectivity of the different state_groups (the connectivity of the state_group elements is not yet checked)
        The state_groups are assigned to lists one list for each molecule in the reaction.
        Example:

                        A_ppi_B; ! <comp>
                        <comp>; or A-{P}
                        <comp>; or B-{P}
                        <comp>; or <compA>
                        <compA>; and A--C
                        <compA>; and A--D
                        <comp>; or <compB>
                        <compB>; and B--E
                        <compB>; and B--F

        final_states:  [[or A_[bd]-{P}], [or B_[bd]-{P}], [and B_[AssocE]--E_[AssocB], and B_[AssocF]--F_[AssocB]], [and A_[AssocC]--C_[AssocA], and A_[AssocD]--D_[AssocA]]]

        Step 1: iterate over final_states (containing all state_groups defined)
        Step 2: if its the first state_groupe generate a list in stacks containing the state_group
                Round1: stacks = [[[or A_[bd]-{P}]]]
        Step 3: check next state_group
                Round2: state_group = [or B_[bd]-{P}] _> [[[or A_[bd]-{P}]],[[or B_[bd]-{P}], ]]
                Round3: state_group = [and B_[AssocE]--E_[AssocB], and B_[AssocF]--F_[AssocB]]
                Round4: state_group = [and A_[AssocC]--C_[AssocA], and A_[AssocD]--D_[AssocA]]
            Step 3.1.: if one of the states in state_group overlaps with one already known in one of the lists of stacks than append
                       the state_group to the respective list
                Round3: stacks = [[[or A_[bd]-{P}]],[[or B_[bd]-{P}], [and B_[AssocE]--E_[AssocB], and B_[AssocF]--F_[AssocB]]]]
                Round4: stacks = [[[or A_[bd]-{P}],[and A_[AssocC]--C_[AssocA], and A_[AssocD]--D_[AssocA]]],[[or B_[bd]-{P}], [and B_[AssocE]--E_[AssocB], and B_[AssocF]--F_[AssocB]]]]
            Step 3.2.: if not create a new list stacks containing the state_group
                Round2: stacks = [[[or A_[bd]-{P}]],[[or B_[bd]-{P}]]]
            proceed with Step 3
        The result is a list containing two lists.
        One for A: [[or A_[bd]-{P}],[and A_[AssocC]--C_[AssocA], and A_[AssocD]--D_[AssocA]]]
        One for B: [[or B_[bd]-{P}], [and B_[AssocE]--E_[AssocB], and B_[AssocF]--F_[AssocB]]]

        Inputs connected with an OR are saved during the process and added to the respective lists afterwords.

        A_ppi_B <comp>
        <comp>; OR <A>
        <comp>; OR <B>
        <A>; AND A-{P}
        <A>; AND <NOTB>
        <NOTB>; NOT B-{P}
        <B>; AND B-{P}
        <B>; AND <NOTA>
        <NOTA>; NOT A-{P}
        #

        final_states = [[AND A-{P}, ANDNOT B-{P}], [AND B-{P}, ANDNOT A-{P}]]

        """
        stacks = []
        input_stacks = []
        for state_group in self.final_states:  # Step 1
            self.stack = state_group
            new_stack = True
            for state in  self.stack:  # Step 3
                found_connection = False

                if stacks:
                    for i, stack in enumerate(stacks):  # part of Step 3: iterate over stacks to get the single lists
                        for j, state_stack in enumerate(stack):  # part of Step 3: iterate over the elements of the single lists
                            # Step 3.1 if we have a new state_group we have to check if a list with overlapping Molecules exists
                            if new_stack and self.check_state_connected_to_stack(state, state_stack):  # if the is an overlap append the state_group to the respective list
                                stacks[i].append(self.stack)
                                found_connection = True
                                new_stack = False
                                break
                            # if not the first element has an overlap than might be that one of the following has one
                            elif not new_stack and self.check_state_connected_to_stack(state, state_stack):  
                                stacks[i].append(self.stack)
                                found_connection = True
                                break
     
                        if found_connection:
                            break
                    # Step 3.2 if there was no overlap in the existing lists we have an other group and append a new list to stacks
                    if not found_connection:  
                        if not self.check_if_input(self.stack):  # we have to distinguish between normal states and inputs like [START]
                            # if the state_group is not a single input or a collection of and connected inputs we open a new list
                            # this is also done if one of the elements in state_group is not an input
                            stacks.append([self.stack])  
                        else:
                            input_stacks.append(self.stack)  # otherwise we save this state_group separately and apply it later to all the lists
                        new_stack = False
                        break
                    else:
                        break
                else:  # Step 2 
                    if not self.check_if_input(self.stack):
                        stacks.append([self.stack])
                    else:
                        input_stacks.append(self.stack)
                    break
        # here we apply the inputs to the respective lists
        while input_stacks:
            input_stack = input_stacks.pop()
            for stack in stacks:
                stack.append(input_stack)

        return stacks

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
                to_remove.append(node)
                # we don't mix bool types hence if one child has a specific bool the other children have the same
                # todo: check if all children have the same bool type
                # todo: if not implemented bool raise error/warning
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
                        child.ctype = "andnot"
                        to_add.append(child)
                elif child.ctype == 'not' and node.ctype == "or":
                    for child in node.children:
                        child.ctype = "ornot"
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

            #for nodes in to_clone:
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

    def build_negative_complexes(self, compl, root_molecule):
        """
        @type complex:  BiologicalComplex
        @param complex: complex to negate.

        @type root_molecule:  string
        @param root_molecule: name of reaction component - 
                              the molecule that always needs to be there.

        #TODO: What if we have two root molecules
        """
        # todo: we have to negate the negation at this point
        ordered_states = self.get_states_from_complex(compl, root_molecule)
        if len(ordered_states[0]):
            ordered_states = ordered_states[0]  # positive states with bond and/or mod
        else:
            ordered_states = ordered_states[1]  # states with negative bond and/or mod (sites)
        alter_comp = AlternativeComplexes('')
        counter = len(ordered_states) -1
        # todo: write a function for positive states (those which have not a defined site)
        # todo: write a function for negative states (those which have a site defined)
        while counter: 
            comp = BiologicalComplex()
            comp.is_positive = False
            for state in ordered_states[:counter]:
                comp.add_state(state)
            last_state = ordered_states[counter]
            mols = comp.get_molecules(last_state.components[0].name)
            if len(last_state.components) > 1:
                mols += comp.get_molecules(last_state.components[1].name)
                mols[0].set_site(last_state) # todo: here we have to add a bond not a site if we want to negate a bond
                
            alter_comp.add_complex(comp)
            counter -=1

        comp = BiologicalComplex()
        comp.is_positive = False
        mol = Molecule(root_molecule.name)
        mol.set_site(ordered_states[0]) # todo: here we have to add a bond not a site
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
        result = [[],[]]
        stack = [root_molecule]
        while stack:
            states_mols = self._get_complex_layer(compl, stack, result)
            result[0] += states_mols[0]  # result_pos
            result[1] += states_mols[1]   # result_neg
            stack = states_mols[2]   # new root
        return result

    def _get_complex_layer(self, compl, root_list, already=None):
        """
        Helper function for get_states_from_complex.
        """
        if not already:
            already = []
        result_pos = []
        result_neg = []
        new_roots = []
        for root_molecule in root_list:
            mol = compl.get_molecules(root_molecule.name)[0]
            for bond in mol.binding_partners:
                if bond not in already[0]:
                    result_pos.append(bond)
                    new_root = bond.get_partner(mol.get_component())
                    new_roots.append(new_root)
            for mod in mol.modifications:
                if mod not in already[0]:
                    result_pos.append(mod)
                    #new_root = mod.get_partner(mol.get_component())
                    #new_roots = []
            # todo: we could have binding-sites negating binding sites means to establish a bond
            for site in mol.binding_sites:
                if site not in already[1]:
                    result_neg.append(site)
                    # don't set a new root because we are looking on a site, that means that the partner is not bound hence there is no connection
                    #new_root = site.get_partner(mol.get_component())
                    #new_roots.append(new_root)
            # todo: we could have modification-sites negating mod sites means to establish a mod
            for mod_site in mol.modification_sites:
                if mod_site not in already[1]:
                    result_neg.append(mod_site)
        return result_pos, result_neg, new_roots
