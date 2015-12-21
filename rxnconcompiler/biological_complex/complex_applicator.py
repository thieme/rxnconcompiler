#!/usr/bin/env python

"""
Module complex_applicator.py

Adds complexes to reaction:
- applys boolean complexes
- build complex from single molecules from reactants 
  (if there is no boolean contingency to apply)

Befor: reaction.substrate_complexes is empty.
After: reaction.substrate_complexes contain one or two complexes.

Input: ReactionContainer object, complexes (AC or [AC, AC] or []).
       AC - AlternativeComplexes (created by ComplexBuilder).
       1 boolean contingency == 1 AC object
Effect: all reactions in ReactionConteiner have updated substrat_complexes    


How the complexes can be applied:
1 Reaction            ---> 0, 1, or 2 BiologicalComplex
1 ReactionContainer   ---> 0, 1, or 2 AlternativeComplexes
1 AlternativeComplexes ---> 1 or more BiologicalComplex

if AlternativeComplexes > 1 BiologicalComplex
---> ReactionContainer has more than 1 Reaction (more rules)
"""

import copy
import itertools
import re

from biological_complex import BiologicalComplex
from complex_builder import ComplexBuilder
from rxnconcompiler.util.util import product
from rxnconcompiler.contingency.contingency_applicator import ContingencyApplicator


class Association(list):
    def __init__(self, complex, relation, k = False):
        list.__init__(self)
        self.__pos = False
        self.__neg = False
        self.__both = False
        self._k = k

        if relation != None:
            self.__set_complex(complex, relation)
    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value
    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        self.__pos = value

    @property
    def neg(self):
        return self.__neg

    @neg.setter
    def neg(self, value):
        self.__neg = value

    @property
    def both(self):
        return self.__both

    @both.setter
    def both(self, value):
        self.__both = value

    def set_complex_type(self, sign):
        if sign == "!":
            self.pos = True
        elif sign == "x":
            self.neg = True
        elif sign == "!x":
            self.both = True

    def get_complex_type(self):
        if self.pos:
            return "!"
        elif self.neg:
            return "x"
        elif self.both:
            return "!x"

    def get_relation_by_sign(self, sign):
        if self.pos and sign == "!":
            return "!"
        elif self.neg and sign == "x":
            return "x"
        elif (self.pos and sign == "x") or (self.neg and sign == "!") or sign == "!x":
            return "!x"

    def get_relation(self, other):

        if other.pos and self.pos:
            return "!"
        elif other.neg and self.neg:
            return "x"
        elif (other.pos and self.neg) or (other.neg and self.pos) or other.both or self.both:
            return "!x"

    def __set_complex(self, complex, relation):
        self.extend(complex)
        self.set_complex_type(relation)

    def add_complex(self, complex):
        self.append(complex)

    def merge_complex(self, complex):
        self.extend(complex)

    def get_all_k(self):
        k_complexes = [complex for complex in self if complex.k]
        return k_complexes

    def get_all_non_k(self):
        complexes = [complex for complex in self if not complex.k]
        return complexes

class ComplexApplicator:
    """
    Interface between AlternativeComplex objects and ReactionContainer object.
    """
    def __init__(self, reaction_container, complexes, war=None):
        """"""
        self.reaction_container = reaction_container
        self.complexes = complexes
        self.possible_roots = reaction_container.get_reactants()
        self.war = war

    def change_contingency_relation(self, inner_list, cont_sign):
        """
        This function changes the contingency to a respective contingency sign like ! or x
        if the contingency sign is x and the current contingency does not contain and AND, OR, NOT it will
        change the contingency sign to the opposite
        @param inner_list:
        @param cont_sign:
        @return:
        """
        for cont in inner_list:
            if cont.ctype in ["and", "or", "not"] or "--" in cont.ctype or re.match("^[1-9]*$", cont.ctype):
                cont.ctype = cont_sign
            elif cont_sign == "x": # we only have to change the cont sign in opposite if the very first cont is negative
                self.change_contingency_opposite(cont)

    def change_contingency_opposite(self, cont):
        """
        This function changes the contingency to the opposite sign
        @param cont: contingency
        @return: changed contingency
        """
        if cont.ctype == "!":
            cont.ctype = "x"
        elif cont.ctype == "x":
            cont.ctype = "!"
        return cont

    def apply_complexes(self):
        """
        This function prepares the defined complexes and builds all non-overlapping rules and applied them to the reaction_container

        This function calls
            positive_application if the complex is defined with !
            negative_application if the complex is defined with x

            builds the combination of those lists if we have different boolean complexes applied to the same reaction
            builds all non-overlapping rules
            applies the rules to the reaction_container

        @return:
        """

        association = Association([], None)

        self.k_plus = False
        for complex in self.complexes:

            if complex[0] == "!":
                #self.association.append(self.positive_application(copy.deepcopy(complex)))
                pos_comp = Association(self.positive_application(copy.deepcopy(complex)), "!")
                association.add_complex(pos_comp)
            elif complex[0] == "x":
                #self.association.append(self.negative_application(copy.deepcopy(complex)))
                neg_comp = Association(self.negative_application(copy.deepcopy(complex)), "x")
                association.add_complex(neg_comp)
            elif complex[0] in ["k+","k-"]:
                self.k_plus = True

                pos_comp = Association(self.positive_application(copy.deepcopy(complex)), "!", k = True)
                association.add_complex(pos_comp)
                neg_comp = Association(self.negative_application(copy.deepcopy(complex)), "x", k = True)
                association.add_complex(neg_comp)

        if self.k_plus:
            complex_combination_list = self.k_plus_combination(association)
        else:
            #complex_combination_list = self.complex_combination()
            complex_combination_list = self.combine(0, association)

        rules = self.building_rules(complex_combination_list)

        self.apply_rules(rules)

    def combine(self, complex_idx_start, association_complexes):
        """
        This function builds all combinations of the applied boolean contingencies.

        For example for a definition like
                        A_ppi_B; ! <bool>
                           <bool>; AND A--D; AND A--E
                        A_ppi_B; x <bool2>
                           <bool2>; AND B--F; AND B--G
                        A_ppi_B; x <bool3>
                           <bool3>; AND B--H; AND B--I
        we need to concider a tree like:


                          0          [! A--D; ! A--E]
                                            |
                                            |
                          1      [[! B--F; x B--G],[x B--F]]
                                            |
                                            |
                          2      [[! B--H; x B--I],[x B--H]]]

        for each list (e.g. [! B--H; x B--I]) within a list (e.g. [[! B--H; x B--I],[x B--H]])

        this resulting in 4 combination possibilities.

        [! A--D; ! A--E; ! B--F; x B--G; ! B--H; x B--I]
        [! A--D; ! A--E; ! B--F; x B--G; x B--H]
        [! A--D; ! A--E; x B--F; ! B--H; x B--I]
        [! A--D; ! A--E; x B--F; x B--H]

        @param complex_idx_start:
        @return:
        """
        self.association_complexes = association_complexes
        self.new_list = Association([], None)
        if len(self.association_complexes) == 1:
            self.new_list.extend(self.association_complexes[0])
            complexes = sorted(self.new_list, key=lambda comp: len(comp))
            return complexes

        complex_idx_end = complex_idx_start+1
        if self.association_complexes[0].k:
            complex_idx_end = complex_idx_start + 2  # element at index is not returned
        stack = self.association_complexes[complex_idx_start:complex_idx_end]
        for complex_collection in stack:
            if complex_collection.k:
                complex_idx_start = 2
                complex_idx_end = 4
            else:
                complex_idx_start = complex_idx_end
                complex_idx_end = complex_idx_start + 1

            for inner_list in complex_collection:
                new_complex = Association([], complex_collection.get_complex_type())
                new_complex.add_complex(inner_list)
                if complex_collection.k:
                    new_complex.k = True
                    new_complex[-1].k = True
                combined_complexes, further_processing = self.__combine_helper(complex_idx_start, complex_idx_end, new_complex, complex_collection.get_complex_type(), init=True)
                if not further_processing:
                    self.new_list.merge_complex(combined_complexes)
        complexes = sorted(self.new_list, key=lambda comp: len(comp))
        return complexes

    def __combine_helper(self, complex_idx_start,complex_idx_end, current_list, relation, init=False):
        """
        helper function for combine()
        This is a recusive function creating all possible combinations.

        @param complex_idx_start: is the start index within the collected lists of contingencies defined
                                  within the boolean and proceeded according the boolean contingency

        @param current_list: is the actual list
        @param relation: defines if the current list is possitive ("!") negative ("x") or both ("!" as well as "x")
        @param init: defines if we add a new possible complex or not
        @return: returns a list of combinations and the information if we went deeper than the 1 level in the tree
        """

        not_set = True
        complex_idx_start = complex_idx_start
        complex_idx_end = complex_idx_end
        new_complex = copy.deepcopy(current_list)
        if current_list.k and len(self.association_complexes[complex_idx_start:]) - complex_idx_end + 2 > 0:
            further_processing = True  # true if we can go one level deeper
            complex = self.association_complexes[complex_idx_start:complex_idx_end]
        elif current_list.k:
            further_processing = False # false if we reached the end
            complex = self.association_complexes[complex_idx_start:]
        elif len(self.association_complexes[complex_idx_start:]) > 1:
            further_processing = True  # true if we can go one level deeper
            complex = self.association_complexes[complex_idx_start:complex_idx_end]
        else:
            further_processing = False # false if we reached the end
            complex = self.association_complexes[complex_idx_start:]

        for i, outer_list in enumerate(complex):

            if outer_list.k and not_set:
                shift = 2
                complex_idx_start = complex_idx_start + shift
                complex_idx_end = complex_idx_start + shift
                not_set = False
            elif not outer_list.k and not_set:
                shift = 1
                complex_idx_start = complex_idx_start + shift
                complex_idx_end = complex_idx_start + shift
                not_set = False

            for inner_list in outer_list:
                sign = outer_list.get_relation_by_sign(relation)
                if not init:
                    new_complex.add_complex(Association(copy.deepcopy(current_list[-1]), sign))
                new_complex[-1].merge_complex(copy.deepcopy(inner_list))
                init = False
                if further_processing: # if it's not the last element
                    combined_complexes, further = self.__combine_helper(complex_idx_start, complex_idx_end, new_complex, sign, init=True)
                    self.new_list.merge_complex(combined_complexes)
                    init = True
                    new_complex = Association([], relation)
                    if current_list.k:
                        new_complex.k = True
                    new_complex.merge_complex(copy.deepcopy(current_list))
        return new_complex, further_processing


    def k_plus_combination(self, association):
        """
                                       b
                                    /     \
                                   !       x
                                   |       |
                                   b1      b1
                                  /  \    /  \
                                 !    x   !   x
                                 |    |   |   |
                                b2    b2  b2  b2
                                /\    /\  /\   /\
                               !  x  !  x ! x  ! x
        @return:
        """
        complexes = Association([], None)

        k_complexes = association.get_all_k()
        normal_complexes = association.get_all_non_k()
        if len(k_complexes) == 2:
            for outer_list in k_complexes:
                complexes.merge_complex(outer_list)
        else:
            complexes.merge_complex(self.combine(0, k_complexes))

        if normal_complexes:
            new_complexes = Association([], None)
            combined_complexes = self.combine(0, normal_complexes)
            for k_complexe in complexes:
                for i, normal_complexes in enumerate(combined_complexes):
                    k_complexe_copy = copy.deepcopy(k_complexe)
                    new_complexes.add_complex(k_complexe_copy)
                    new_complexes[-1].merge_complex(normal_complexes)

            complexes = sorted(new_complexes, key=lambda comp: len(comp))

        return complexes

    def k_plus_application(self, complex):
        """
        Not used yet
        @param complex:
        @return:
        """
        # positive association
        self.positive_application(complex)
        # negative association
        k_plus_complexes = []
        for inner_list in complex[1]:
            counter = len(inner_list) -1
            #k_plus_complexes = []
            while counter:
                k_plus_complexes.append([])
                for cont in inner_list[:counter]:
                    k_plus_complexes[-1].append(cont)
                last_cont = inner_list[counter]
                k_plus_complexes[-1].append(self.change_contingency_opposite(copy.deepcopy(last_cont)))
                counter -=1
            k_plus_complexes.append([])

            k_plus_complexes[-1].append(self.change_contingency_opposite(copy.deepcopy(inner_list[0])))
        self.association[-1].extend(k_plus_complexes)
        pass

    def positive_application(self, complex):
        """
        changed the contingencies within a complex to ! as long as there is no x
        @param complex:
        @return:
        """
        pos_complex = []
        for inner_list in complex[1]:
            self.change_contingency_relation(inner_list, "!")
            inner_list = Association(inner_list, "!")
            pos_complex.append(inner_list)
        return pos_complex

    def build_negative_ordered_trees(self, complex):

        negative_complex_tree = Association([], None)
        for root in self.possible_roots: # an inner_list can contain more than one root
            for inner_list in complex:
                for cont in inner_list:
                    if cont.state.has_component(root):
                        negative_tree = self.build_tree_combinations_from_list(inner_list, root)
                        for tree in negative_tree:
                            if tree not in negative_complex_tree:
                                negative_complex_tree.add_complex(tree)
                        break
        return negative_complex_tree

    def build_tree_combinations_from_list(self, inner_list, root):
        """
        This function builds all negative trees based on a collection of ordered contingencies (see also get_ordered_tree())

        @param inner_list:
        @param root:
        @return:
        """
        cont_tree, state_tree = self.get_ordered_tree(inner_list, root)
        negative_complex_tree = Association([], None)


        counter = len(cont_tree) -1
        while counter:
            negative_complex_tree.add_complex(Association([], "x"))
            for cont in cont_tree[:counter]:
                negative_complex_tree[-1].append(cont)
            last_cont = cont_tree[counter]
            negative_complex_tree[-1].append(self.change_contingency_opposite(copy.deepcopy(last_cont)))
            counter -=1
        negative_complex_tree.add_complex(Association([], "x"))

        negative_complex_tree[-1].append(self.change_contingency_opposite(copy.deepcopy(cont_tree[0])))
        return negative_complex_tree

    def get_ordered_tree(self, inner_list, root):
        """
        This function generates an ordered tree based on a contingency collection and a root

        generates a list of interaction states and the respective contingencies that 'create' the complex.
        List is ordered according to the layers starting from contingencies that include given root_molecule.

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

        @param inner_list: contingency collection
        @param root: root of the tree (at the beginning its a reactant
        @return:
        """
        result = [[],[]]
        stack = [root]
        while stack:
            states_mols = self._get_complex_layer(inner_list, stack, result)
            result[0] += states_mols[0][0]
            result[1] += states_mols[0][1]
            stack = states_mols[1]   # new roots
        state_tree = result[0]
        cont_tree = result[1]
        return cont_tree, state_tree

    def _get_complex_layer(self, inner_list, root_list, already=None):
        """
        Helper function for get_ordered_tree.
        """
        new_roots = []
        result = [[],[]]
        for root in root_list:
            root_cont = []
            for cont in inner_list:
                if cont.state.has_component(root):
                    root_cont.append(cont)
            for bond in root_cont:
                if bond not in already[1]:
                    result[0].append(bond.state)
                    bond.ctype = "!"
                    result[1].append(bond)
                    if bond.state.type == "Association":
                        new_root = bond.state.get_partner(bond.state.get_component(root.name))
                        new_roots.append(new_root)
                    else:
                        new_roots = new_roots
        return result, new_roots

    def negative_application(self,complex):
        """
        changes the contingency from ! to x and vice versa and saves the changed complex in association list
        @param complex:
        @return:
        """

        negative_complex_tree = self.build_negative_ordered_trees(complex[1])
        tmp = []
        for inner_list in itertools.product(*copy.deepcopy(complex[1])):

            tmp_list = copy.deepcopy(inner_list)
            self.change_contingency_relation(tmp_list, "x")
            tmp_list = self.check_connectivity(tmp_list, negative_complex_tree)
            if tmp_list != [] and tmp_list not in tmp:
                tmp.append(Association(tmp_list, "x"))
        return tmp

    def check_connectivity(self, inner_list, complex_tree):
        """
        This function compares each inner_list with all possible trees and checks if the contingencies within a list
        are fully connected.

        @param inner_list: list of contingencies connected by AND
        @param complex_tree: trees generated by get_ordered_tree() contains all possible full trees of the boolean description
        @return: adapted inner_list with all missing connections to the root or an empty list if at least one contingency
                is not part of the same tree as the others
        """
        """
        @param inner_list:
        @param complex_tree:
        @return:
        """
        inner_list = list(inner_list)
        inner_list_copy = copy.deepcopy(inner_list)
        correct_tree = []
        for i, cont in enumerate(inner_list_copy):
            for tree in complex_tree:
                cont_tracking = []
                if cont == tree[-1]:
                    correct_tree.append(True)
                    cont_idx = tree.index(cont)
                    if cont_idx not in cont_tracking:
                        cont_tracking.append(cont_idx)
                        cont_tracking.sort()
                        missing = self.check_for_missing_cont(cont_tracking)
                        for missing_cont_idx in missing:
                            if tree[missing_cont_idx] not in inner_list:
                                inner_list.insert(missing_cont_idx,tree[missing_cont_idx])
                                if missing_cont_idx != 0: # we already add 0 to cont_tracking in check_for_missing_cont
                                    cont_tracking.append(missing_cont_idx)
                    break

        if len(correct_tree) == len(inner_list_copy): # if we found for all contingencies a tree
                return inner_list  # if we don't break all cont of the inner_list were found in this tree we can return

        # at this point we don't found a tree containing all contingencies therefor we have to check if all
        # contingencies are conntected to the root directly
        validation_list = []
        for root in self.possible_roots:
            for cont in inner_list:
                if cont.state.has_component(root):
                    validation_list.append(cont)
        if len(validation_list) == len(inner_list):
            return inner_list  # if all cont are containing a root molecule the list is valid
        else:
            return [] # if at least one cont don't contain a root molceule the list is invalid

    def check_for_missing_cont(self, cont_tracking):
        """
        This function added the index of possible missing connections.
        @param cont_tracking: list of index of contingencies within a certain tree
        @return:
        """
        missing = []

        if cont_tracking[0] != 0:
            # if we don't saw see root_cont until now we insert it
            # if we are in the wrong tree we will see this later and replace inner_list with it's original
            cont_tracking.insert(0,0)
            missing.append(0)

        for rank in xrange(0, len(cont_tracking)-1):
            if cont_tracking[rank+1] - cont_tracking[rank] >= 2:
                missing.extend(range(cont_tracking[rank]+1, cont_tracking[rank+1]))

        return missing
    def sort_rules_by_cid(self, rule):
        #rule_dict = dict(((comp), cont) for cont.state.components in rule )
        rule_dict = {}
        input_cont = []
        for cont in rule:
            #for component in cont.state.components:
            if cont.state.type == "Input":
                input_cont.append(cont)
                continue
            components = cont.state.components
            if len(components) > 1 and int(components[0].cid) <  int(components[1].cid):
                rule_dict[(int(components[0].cid), int(components[1].cid))] = cont
            elif len(components) > 1 and int(components[0].cid) >  int(components[1].cid):
                rule_dict[(int(components[1].cid), int(components[0].cid))] = cont
            else:
                rule_dict[(int(components[0].cid), components[0].domain)] = cont
        cid_tuble = rule_dict.keys()
        cid_tuble.sort()  # keys in a dict are not sorted
        new_rule_order = []
        for cid in cid_tuble:
            new_rule_order.append(rule_dict[cid])
        new_rule_order.extend(input_cont)
        return new_rule_order

    def apply_rule(self, rule, reaction, cap):
        """
        This function applies a single rule at the reaction_container
        @param rule: collection of contingencies
        @param reaction: reaction of reaction_conainer
        @param cap: ContingencyApplicator() object
        @return: if inputs like [START] are found they will be returned as list
        """

        # ((left.has_molecule(component1.name) and right.has_molecule(component2.name))
        #         or (left.has_molecule(component2.name) and right.has_molecule(component1.name))
        #         or (left.has_molecule(component1.name, component1.cid) and right.has_molecule(component2.name))
        #         or (left.has_molecule(component1.name) and right.has_molecule(component2.name, component2.cid))
        #         or (left.has_molecule(component2.name, component2.cid) and right.has_molecule(component1.name))
        #         or (left.has_molecule(component2.name) and right.has_molecule(component1.name, component1.cid))

        apply_later = []
        input_cont = []
        rule = self.sort_rules_by_cid(rule)
        for cont in rule: # split rules
            left = reaction.left_reactant
            right = reaction.right_reactant
            if cont.state.has_component(left) or cont.state.has_component(right):
                #self.apply_cont(reaction, cont, cap)
                cap.apply_simple_cont_on_reaction(reaction, cont)
            else:
                cont_applied =False
                for comp in reaction.substrat_complexes:
                    if len(cont.state.components) > 1:
                        if comp.has_molecule(cont.state.components[0].name, cont.state.components[0].cid) or comp.has_molecule(cont.state.components[1].name, cont.state.components[1].cid):
                            cap.apply_simple_cont_on_reaction(reaction, cont)
                            cont_applied = True
                    elif comp.has_molecule(cont.state.components[0].name, cont.state.components[0].cid):
                        cap.apply_simple_cont_on_reaction(reaction, cont)
                        cont_applied = True


                if not cont_applied and cont.state.type == "Input":
                    input_cont.append(cont)
                elif not cont_applied:
                    apply_later.append(cont)

        for cont in apply_later:
            if cont.state.type == "Input":
                input_cont.append(cont)
            else:
                cap.apply_simple_cont_on_reaction(reaction, cont)

        return input_cont

    def apply_rules(self, complex_rules):
        """
        The non-overlapping rules prepared in building_rules() will be applied here to the respective reaction_container
        @param complex_rules: non-overlapping rules
        @return:
        """
        cap = ContingencyApplicator(self.war)
        reaction_container_clone = self.reaction_container[0].clone()
        first_rule = True
        self.counter = 1

        for rule in complex_rules:
            if first_rule:
                first_rule = False
                reaction = copy.deepcopy(reaction_container_clone)

                self.set_basic_substrate_complex(reaction)
                input_list = self.apply_rule(rule, reaction, cap)

                self.update_reaction_rate(reaction, rule, input_list)
                self.reaction_container[0] = reaction

            else:
                reaction = copy.deepcopy(reaction_container_clone)

                self.set_basic_substrate_complex(reaction)
                input_list = self.apply_rule(rule, reaction, cap)

                self.update_reaction_rate(reaction, rule, input_list)
                self.reaction_container.add_reaction(reaction)


    def update_reaction_rate(self, reaction, rule, input_list):
        """
        When there are alternative complexes to apply
        new reactions will be created (copies of basic one)
        and added to a ReactionContainer. In some cases they will
        all have the same rate, in some cases it needs to be changed.
        This function updates reaction rate.

        Rate has single digit when only positive
        or negative complexes are present.
        When both:
        - X_1 for positive
        - X_2 for negative

        Additionally it updates rates with functions
        if input conditions are present in complex.

        Arguments:
        - reaction (has already basic rate)
        - compl (may have input condition)
        - both_types if True means that X will be exchanged with X_1 or X_2.

        @param reaction: reaction of the current reaction_container
        @param rule: collection of contingencies
        @param input_list: collection of inputs like [START]
        @return:
        """
        if self.k_plus:
            if rule.pos:
                reaction.rate.update_name('%s_1' % reaction.main_id)
            else:
                reaction.rate.update_name('%s_2' % reaction.main_id)
        if input_list:
            is_switch = False
            if self.k_plus:
                is_switch = True
            reaction.rate.update_function(input_list[0], is_switch,
                                          '%s_1' % reaction.main_id, '%s_2' % reaction.main_id)

    def check_root(self, root, complex):
        """
        checks if the root is part of the current complex (complex_copy)
        @param root:
        @param complex:
        @return: bool True if the root is part of the complex else False
        """
        for cont in complex:
            if cont.state.has_component(root):
                return True
        return False

    def conflict_check(self, ref_cont, complex_copy):
        """
        This function checks if there are conflicts between a collection of contingencies and a reference contingency
        @param ref_cont: reference contingency
        @param complex_copy: collection of contingencies
        @return: False if the ref_cont is not member of complex_copy
        @return: True if the ref_cont is member of complex_copy and there is a conflict
        @return: None if the ref_cont is member of complex_copy and there is no conflict
        """
        found = False
        for cont in complex_copy:
            #if ref_cont.state.state_str == cont.state.state_str and ref_cont.target_reaction == cont.target_reaction:
            if ref_cont.state.state_str == cont.state.state_str:
                #for comp in ref_cont.state.components:
                if len(ref_cont.state.components) > 1:
                    if cont.state.has_component(ref_cont.state.components[0]) and cont.state.has_component(ref_cont.state.components[1]):
                        found = True

                elif cont.state.has_component(ref_cont.state.components[0]):
                    found = True

                if found:
                    if ref_cont.ctype != cont.ctype:
                        return True
                    else:
                        return None
        return False


    def adapt_complex(self, rules, complex_copy, root):
        """
        if rules is not empty the current complex (complex_copy) is checked versus all the rules if there is an overlap with one rule
        this will be eliminated and the complex_copy will be modified. all further checks will be done with the modified complex_copy
        @param rules: all non-overlapping rules until this step
        @param complex_copy: current complex
        @param root: current root
        @return complex_copy: modified current complex
        @return not_in_complex: list of contingencies not in the current complex and not containing the root
        """
        not_in_complex = []
        for rule in rules:

            not_in = []
            verify = []
            for ref_cont in rule:
                check = self.conflict_check(ref_cont, complex_copy)
                if not check and check is not None:
                    verify.append(ref_cont)
                elif check and check is not None:
                    verify = []
                    break

            if verify:
                for ref_ele in verify:
                    if ref_ele.state.has_component(root):
                        complex_copy.append(self.change_contingency_opposite(copy.deepcopy(ref_ele)))
                    #elif not ref_ele.state.has_component(root) and ref_ele not in not_in:
                    else:
                        already_known_states = [known_ele.state.state_str for known in not_in_complex for known_ele in known]
                        if ref_ele.state.state_str not in already_known_states:
                            not_in.append(copy.deepcopy(ref_ele))

            if not_in != [] and not_in not in not_in_complex:
                not_in_complex.append(not_in)
        return complex_copy, not_in_complex

    def verify_rules(self, rules, complex_copy, not_in_complex, complex_tree):
        """
        if there are contingencies in one of the rules which have not the root molecule and are not part of the current complex.
        we add these contingencies to the current complex in different combinations to get all non overlapping rules.
        e.g. not_in_complex = [[! B--B1, ! B--B2]] both contingencies are in one rule but not in the complex and don't have the root as molecule
        two rules will be generated one with x B--B1 and one with ! B--B1 x B--B2
        in the case of [[! B--B1], [! B--B2]]
        both contingencies will be added to the same rule as negation x B--B1 x B--B2
        
        @param rules: all generated rules until this step
        @param complex_copy: current complex
        @param not_in_complex: contingencies not in the current complex and don't have the root as molecule
        @return rules: modified rules
        """
        next = False
        #self.check_combinatorial_conflict(complex_copy, not_in_complex, complex_tree)

        for not_in in not_in_complex:
            for not_in_cont in not_in:
                self.change_contingency_opposite(not_in_cont)
                for tree in complex_tree:
                    if not_in_cont == tree[-1]:
                        if len(tree) == 1:
                            if not next:
                                complex_copy = copy.deepcopy(complex_copy)
                                #complex_copy, tree = self.check_combinatorial_conflict(complex_copy, not_in_cont, tree)
                                complex_copy.extend(tree)
                                rules.append(copy.deepcopy(complex_copy))
                                next = True
                            elif next:
                                rules[-1].append(copy.deepcopy(not_in[0]))
                        else:
                            # important for conntected states
                            if complex_copy not in rules:
                                rules.append(complex_copy)
                            #complex_copy, tree = self.check_combinatorial_conflict(complex_copy, not_in_cont, tree)
                            new_complex_copy = copy.deepcopy(complex_copy)
                            for complex_cont in copy.deepcopy(new_complex_copy):
                                check = self.conflict_check(complex_cont, tree)
                                if check or check == None:
                                    new_complex_copy.remove(complex_cont)
                            new_complex_copy.extend(tree)
                            if new_complex_copy not in rules:
                                rules.append(new_complex_copy)

        return rules

    def building_rules(self, complex_combination_list):
        """
        This function builds all non-overlapping rules
        @param complex_combination_list: list of contingency combinations generated in complex_combination()
        @return rules: all non-overlapping rules
        """

        complex_tree = []
        for complex in self.complexes:
            negative_complex_tree = self.build_negative_ordered_trees(complex[1])
            complex_tree.extend(negative_complex_tree)

        rules = []
        known_complexes = []
        for root in self.possible_roots:
            new_root = True
            for complex in complex_combination_list:
                complex_copy = copy.deepcopy(complex)
                root_found = self.check_root(root, complex_copy)
                if root_found and new_root and str(complex_copy) not in known_complexes:
                    known_complexes.append(str(complex))
                    complex_copy, not_in_complex = self.adapt_complex(rules, complex_copy, root)
                    if not_in_complex:
                        rules = self.verify_rules(rules, complex_copy, not_in_complex, complex_tree)
                    else:
                        rules.append(complex_copy)
                    new_root = False
                elif root_found and str(complex_copy) not in known_complexes:
                    known_complexes.append(str(complex))
                    complex_copy, not_in_complex = self.adapt_complex(rules, complex_copy, root)
                    if not_in_complex != []:
                        rules = self.verify_rules(rules, complex_copy, not_in_complex, complex_tree)
                    else:
                        rules.append(complex_copy)

        return rules

    def set_basic_substrate_complex(self, reaction):
        """
        This function initialises the substrate complex of the reaction
         @param reaction: reaction of the current reaction_compiler
        """

        if reaction.left_reactant._id == reaction.right_reactant._id:
            self.molecule2complex(reaction.left_reactant, reaction, 'LR')
        else:
            if reaction.left_reactant:
                self.molecule2complex(reaction.left_reactant, reaction, 'L')
            if reaction.right_reactant:
                self.molecule2complex(reaction.right_reactant, reaction, 'R')

    def set_reaction_id(self, reaction):
        if len(self.reaction_container) > 1: 
            reaction.rid = "%i_%i" %(self.reaction_container.rid, self.counter)  
            self.counter += 1
        return reaction

    def add_substrate_complexes(self, reaction, complexes):
        """
        """
        if type(complexes) != list:
            complexes = [complexes]
        if len(complexes) > 2: #sth with product went wrong
            raise TypeError('Cannot apply more than two complexes on a reaction.')

        lmol = reaction.left_reactant
        rmol = reaction.right_reactant
        lmol_is_complex = False
        rmol_is_complex = False

        for compl in complexes:
            clmol = compl.get_molecules(lmol.name, lmol.mid)
            crmol = compl.get_molecules(rmol.name, rmol.mid)
            if clmol:
                clmol[0].is_reactant = True
            if crmol:
                crmol[0].is_reactant = True

            if clmol and crmol:
                if lmol_is_complex or rmol_is_complex:
                    raise TypeError('Reactant is already a complex cannot add another complex.')
                crmol[0] = crmol[0] + rmol
                clmol[0] = clmol[0] + lmol
                compl.side = 'LR'
                reaction.substrat_complexes.append(compl)
                lmol_is_complex = True
                rmol_is_complex = True

            elif clmol:
                if lmol_is_complex:
                    raise TypeError('Reactant is already a complex cannot add another complex.')
                clmol[0] = clmol[0] + lmol
                compl.side = 'L'
                reaction.substrat_complexes.append(compl)
                lmol_is_complex = True

            elif crmol:
                if rmol_is_complex:
                    raise TypeError('Reactant is already a complex cannot add another complex.')
                crmol[0] = crmol[0] + rmol
                compl.side = 'R'
                reaction.substrat_complexes.append(compl)
                rmol_is_complex = True

        if not lmol_is_complex:
            self.molecule2complex(lmol, reaction, 'L')

        if not rmol_is_complex:
            self.molecule2complex(rmol, reaction, 'R')

    def molecule2complex(self, mol, reaction, side=None):
        """
        Creates BiologicalComplex with single Molecule inside.
        Adds this complex to reaction.substrat_complexes.

        Input:
        - mol:      Molecule object
        - reaction: Reaction object
        - side:     L, R, LR indicates on which side of reaction should be the complex.
        """
        compl = BiologicalComplex()
        compl.side = side
        compl.molecules.append(mol)
        reaction.substrat_complexes.append(compl)