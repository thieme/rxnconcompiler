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
from biological_complex import BiologicalComplex, AlternativeComplexes
from complex_builder import ComplexBuilder
from rxnconcompiler.util.util import product
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.contingency.contingency_applicator import ContingencyApplicator
from rxnconcompiler.molecule.molecule import Molecule


class ComplexApplicator:
    """
    Interface between AlternativeComplex objects and ReactionContainer object.
    """
    def __init__(self, reaction_container, complexes):
        """"""
        self.reaction_container = reaction_container
        self.complexes = complexes

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
            if cont.ctype in ["and", "or", "not"] or "--" in cont.ctype:
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
        self.association = []
        for complex in self.complexes:

            if complex[0] == "!":
                self.positive_application(copy.deepcopy(complex))
            elif complex[0] == "x":
                self.negative_application(copy.deepcopy(complex))
            elif complex[0] in ["k+","k-"]:
                self.positive_application(copy.deepcopy(complex))
                self.negative_application(copy.deepcopy(complex))

        complex_combination_list = self.complex_combination()
        rules = self.building_rules(complex_combination_list)

        self.apply_rules(self.reaction_container, rules)

    def positive_application(self, complex):
        """
        changed the contingencies within a complex to ! as long as there is no x
        @param complex:
        @return:
        """
        for inner_list in complex[1]:
            self.change_contingency_relation(inner_list, "!")
        self.association.append(complex[1])

    def negative_application(self,complex):
        """
        changes the contingency from ! to x and vice versa and saves the changed complex in association list
        @param complex:
        @return:
        """
        tmp = []
        for inner_list in itertools.product(*copy.deepcopy(complex[1])):
            tmp_list = copy.deepcopy(inner_list)
            self.change_contingency_relation(tmp_list, "x")
            tmp.append(list(tmp_list))
        self.association.append(tmp)

    def complex_combination(self):
        """
        This function builds the complex combinations if we have more than one boolean complex which
        should be applied to a certain reaction
        @return: combination of the input
        """
        new_list = []
        already_seen = []
        #combination = True
        if len(self.association) == 1:
            new_list.extend(self.association[0])
            #new_list[0] = False
            complexes = sorted(new_list, key=lambda comp: len(comp))
            return complexes
        for outer_list in self.association:
            if outer_list not in already_seen:
                already_seen.append(outer_list)
            for outer_list2 in self.association:
                if outer_list2 not in already_seen:
                    already_seen.append(outer_list2)
                    for inner_list in outer_list:
                        for inner_list2 in outer_list2:
                            new_list.append(copy.deepcopy(inner_list))
                            new_list[-1].extend(inner_list2)
        complexes = sorted(new_list, key=lambda comp: len(comp))
        return complexes

    def apply_rules(self, reaction_container, complex_rules):
        """
        The non-overlapping rules prepared in building_rules() will be applied here to the respective reaction_container
        @param reaction_container: rxncon object containing the reaction information and the substrate complex
        @param complex_rules: non-overlapping rules
        @return:
        """
        cap = ContingencyApplicator()
        reaction_container_clone = reaction_container[0].clone()
        first_rule = True
        for rule in complex_rules:
            apply_later = []
            if first_rule:
                first_rule = False
                reaction = copy.deepcopy(reaction_container_clone)
                self.set_basic_substrate_complex(reaction)
                for cont in rule:
                    if cont.state.has_component(self.reaction_container[0].left_reactant) or cont.state.has_component(self.reaction_container[0].right_reactant):
                        if cont.state.type == 'Association' and cont.ctype == '!':
                            cap.apply_positive_association(reaction, cont)
                        elif cont.state.type == "Intraprotein" and cont.ctype == '!':
                            cap.apply_positive_intraprotein(reaction, cont)
                        else:
                            cap.apply_on_reaction(reaction, cont)
                    else:
                        apply_later.append(cont)

                for cont in apply_later:
                    if cont.state.type == 'Association' and cont.ctype == '!':
                        cap.apply_positive_association(reaction, cont)
                    elif cont.state.type == "Intraprotein" and cont.ctype == '!':
                        cap.apply_positive_intraprotein(reaction, cont)
                    else:
                        cap.apply_on_reaction(reaction, cont)
                reaction_container[0] = reaction
            else:
                reaction = copy.deepcopy(reaction_container_clone)
                self.set_basic_substrate_complex(reaction)
                for cont in rule:
                    if cont.state.has_component(self.reaction_container[0].left_reactant) or cont.state.has_component(self.reaction_container[0].right_reactant):
                        if cont.state.type == 'Association' and cont.ctype == '!':
                            cap.apply_positive_association(reaction, cont)
                        elif cont.state.type == "Intraprotein" and cont.ctype == '!':
                            cap.apply_positive_intraprotein(reaction, cont)
                        else:
                            cap.apply_on_reaction(reaction, cont)
                    else:
                        apply_later.append(cont)
                for cont in apply_later:
                    if cont.state.type == 'Association' and cont.ctype == '!':
                        cap.apply_positive_association(reaction, cont)
                    elif cont.state.type == "Intraprotein" and cont.ctype == '!':
                        cap.apply_positive_intraprotein(reaction, cont)
                    else:
                        cap.apply_on_reaction(reaction, cont)

                reaction_container.add_reaction(reaction)

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

    def conflict_check(self, ref_cont, complex_sign, complex_state):
        """
        @param ref_cont:
        @param complex_sign:
        @param complex_state:
        @return: True if a conflict exists else False
        """
        if ref_cont.state.state_str in complex_state:  # check if ref_cont is a member of complex
            idx_cont = complex_state.index(ref_cont.state.state_str)
            if ref_cont.ctype != complex_sign[idx_cont]:  # if ref_cont is a member of the complex check if the sign is different
                return True
        else:
            return False

    def adapt_complex(self, rules, complex_copy, root):
        """
        if rules is not empty the current complex (complex_copy) is checked versus all the rules if there is an overlap with one rule
        this will be eleminated and the complex_copy will be modified. all further checks will be done with the modified complex_copy
        @param rules: all non-overlapping rules until this step
        @param complex_copy: current complex
        @param root: current root
        @return complex_copy: modified current complex
        @return not_in_complex: list of contingencies not in the current complex and not containing the root
        """

        not_in_complex = []
        for rule in rules:
            sign = []
            state = []
            for cont in complex_copy:
                sign.append(cont.ctype)
                state.append(cont.state.state_str)
            not_in = []
            verify = []
            for ref_cont in rule:
                check = self.conflict_check(ref_cont, sign, state)
                if not check and check != None:
                    verify.append(ref_cont)
                elif check and check != None:
                    verify = []
                    break

            if verify:
                for ref_ele in verify:
                    if ref_ele.state.has_component(root):
                        complex_copy.append(self.change_contingency_opposite(copy.deepcopy(ref_ele)))
                    elif not ref_ele.state.has_component(root) and ref_ele not in not_in:
                        already_known_states = [known_ele.state.state_str for known in not_in_complex for known_ele in known]
                        if ref_ele.state.state_str not in already_known_states:
                            not_in.append(ref_ele)

            if not_in != [] and not_in not in not_in_complex:
                not_in_complex.append(not_in)
        return complex_copy, not_in_complex

    def verify_rules(self, rules, complex_copy, not_in_complex):
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
        for not_in in not_in_complex:
            if len(not_in) > 1:
                next = False
                new_complex_copy = copy.deepcopy(complex_copy)
                for i, cont in enumerate(not_in):
                    if i == 0:
                        if self.change_contingency_opposite(copy.deepcopy(cont)) not in complex_copy or cont not in complex_copy:
                            complex_copy.append(self.change_contingency_opposite(copy.deepcopy(cont)))
                            rules.append(complex_copy)
                    else:
                        new_complex_copy.extend(not_in[:i])
                        new_complex_copy.append(self.change_contingency_opposite(copy.deepcopy(cont)))
                        rules.append(new_complex_copy)
            else:
                if not next:
                    complex_copy.append(self.change_contingency_opposite(copy.deepcopy(not_in[0])))
                    rules.append(complex_copy)
                    next = True
                elif next:
                    rules[-1].append(self.change_contingency_opposite(copy.deepcopy(not_in[0])))

        return rules


    def building_rules(self, complex_combination_list):
        """
        This function builds all non-overlapping rules
        @param complex_combination_list: list of contingency combinations generated in complex_combination()
        @return rules: all non-overlapping rules
        """

        possible_roots = [self.reaction_container[0].left_reactant, self.reaction_container[0].right_reactant]
        rules = []
        known_complexes = []
        for root in possible_roots:
            new_root = True
            for complex in complex_combination_list:
                complex_copy = copy.deepcopy(complex)
                root_found = self.check_root(root, complex_copy)
                if root_found and new_root and str(complex_copy) not in known_complexes:
                    known_complexes.append(str(complex))
                    complex_copy, not_in_complex = self.adapt_complex(rules, complex_copy, root)
                    if not_in_complex != []:
                        rules = self.verify_rules(rules, complex_copy, not_in_complex)
                    else:
                        rules.append(complex_copy)
                    new_root = False
                elif root_found and str(complex_copy) not in known_complexes:
                    known_complexes.append(str(complex))
                    complex_copy, not_in_complex = self.adapt_complex(rules, complex_copy, root)
                    if not_in_complex != []:
                        rules = self.verify_rules(rules, complex_copy, not_in_complex)
                    else:
                        rules.append(complex_copy)

        return rules

    def _prepare_alter_complex(self, alter_complex):
        """
        Gets single AlternativeComplexes object and 
        Input: all positive complexes.
        Output: all required complexes (combinations of positive and negative complexes).

        Complexes can contain a complex with no molecules and just an input state.
        """
        # TODO: EMPTY COMPLEXES??? WHY???
        # remove not connected complexes to one of the reaction molecules
        # special cases are TRSL or other reactions with cofactors
        to_remove = [comp for comp in alter_complex if (comp.molecules == [] and not comp.input_conditions)]
        for comp in to_remove:
            alter_complex.remove(comp)

        # TODO: we are in context of reactions -> know all roots and special things like mRNA need and so on
        #  For each root:
        #    find all connected states
        #       add states to root
        #       remove state from list
        #   apply com = self.builder.build_required_complexes(alter_complex, root)
        #############################################
        # AB
        # [A,B] [C, D]
        # A       C
        possible_roots = [self.reaction_container[0].left_reactant, self.reaction_container[0].right_reactant]


        for root in possible_roots:
            alter_complex_of_root = AlternativeComplexes(alter_complex.name)
            alter_complex_of_root.ctype = alter_complex.ctype
            alter_complex_of_root.input_condition = alter_complex.input_condition
            for comp in alter_complex: # [Complex: A,C, Complex: A,D, Complex: B,E Complex G,F]
                if comp.has_molecule(root.name):  # we only consider those complexes which are directly connected to one of the roots
                    alter_complex_of_root.append(comp)
            if alter_complex_of_root:
                com = self.builder.build_required_complexes(alter_complex_of_root, root)

        #root = self.get_root_molecules(alter_complex.get_first_non_empty())[0]
        #print 'Root', root
        #com = self.builder.build_required_complexes(alter_complex, root)
        return com
       
    def prepare_complexes_to_apply(self, input_complexes):
        """
        @type input_complexes:  list of AlternativeComplexes
        @param input_complexes: one or two AlternativeComplexes objects as a list.
                                Alternative Complexes object keeps all complexes 
                                from one boolean contingency. Maximal two boolean
                                contingency can be applied on a reaction. why???? one can define arbitrary number of boolean contingencies to a reaction
        """
        if 'AlternativeComplexes' in str(input_complexes.__class__):
            # one boolean contingency
            input_complexes = input_complexes.clone()
            return self._prepare_alter_complex(input_complexes)
        else:
            # two boolean contingencies
            alter = []
            for alter_complex in input_complexes:
                if 'AlternativeComplexes' in str(alter_complex.__class__):
                    alter_complex = alter_complex.clone()
                elif type(alter_complex) == list:
                    alter_complex = [x.clone() for x in alter_complex]
                alter.append(self._prepare_alter_complex(alter_complex))
                return list(product(alter))

    def both_complex_types_present(self, com):
        """
        BiologicalComplex.is_positive can have three values:
        - True
        - False
        - 'both' (when k+/k- input condition)

        Returns False when either only 
        positive complexes are present or only negative.

        Returns True when positive and negative complexes 
        are present or complexes that are both positive and negative at the time (K).

        It also returns True when reaction is reversible 
        and complex contains input condition.
        (then we need two rates anyway for reversible reaction).
        """
        pos = False
        neg = False

        #for reaction, compl in zip(self.reaction_container, self.complexes):
        for reaction, compl in zip(self.reaction_container, com):
            if reaction.definition['Reversibility'] == 'reversible' and compl.input_conditions:
                return True
            elif compl.is_positive == 'both':
                return True
            elif compl.is_positive:
                pos = True
            elif not compl.is_positive:
                neg = True
        
        if pos and neg: 
            return True 
        return False

    def update_reaction_rate(self, reaction, compl, both_types=False):
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
        """
        if both_types:
            if compl.is_positive:
                reaction.rate.update_name('%s_1' % reaction.main_id) 
            else:
                reaction.rate.update_name('%s_2' % reaction.main_id)
        if compl.input_conditions:
            is_switch = False
            if compl.is_positive == 'both':
                is_switch = True
            reaction.rate.update_function(compl.input_conditions[0], is_switch, \
                '%s_1' % reaction.main_id, '%s_2' % reaction.main_id)

    def set_basic_substrate_complex(self, reaction):
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

    def change_non_complex_molecule(self, reactant):
        for stackes in self.final_separated_states:
            for stack in stackes:
                for ele in stack:
                    #if ele.ctype == "or":
                    mol1 = Molecule(ele.state.components[0].name)
                    if mol1 == reactant:
                        reactant.set_site(ele.state)
                    elif len(ele.state.components) > 1:
                        mol2 = Molecule(ele.state.components[1].name)
                        if mol2 == reactant:
                            reactant.set_site(ele.state)

    def get_or_conditions_of_other_reactant(self, reaction, comp):

        reaction_left_reactant = reaction.left_reactant
        reaction_right_reactant = reaction.right_reactant
        if not comp.has_molecule(reaction_left_reactant.name):
            self.change_non_complex_molecule(reaction_left_reactant)
        elif not comp.has_molecule(reaction_right_reactant.name):
            self.change_non_complex_molecule(reaction_right_reactant)

    # def apply_complexes(self):
    #     """
    #     applies the complexes as well as the alternative complexes
    #     """
    #
    #     com_number = 0
    #     reaction_container_clone = self.reaction_container[0].clone()
    #     self.counter = 1
    #     second_reactant = False
    #     print "self.complexes: ", self.complexes
    #     #self.complexes = [[self.complexes[0][0],self.complexes[0][2]]]
    #     #print "self.complexes: ", self.complexes
    #     for com in self.complexes:
    #         reaction_container_tmp = []
    #
    #         while com and len(self.reaction_container[com_number:]) != len(com) and len(com) > 0:
    #             new_reaction = copy.deepcopy(reaction_container_clone)
    #             self.reaction_container.add_reaction(new_reaction)
    #
    #         pos_and_neg_compl = self.both_complex_types_present(com)
    #         for reaction, compl in zip(self.reaction_container[com_number:], com):
    #             reaction = self.set_reaction_id(reaction)
    #             self.add_substrate_complexes(reaction, compl)
    #             if second_reactant:
    #                 self.get_or_conditions_of_other_reactant(reaction, compl)
    #             self.update_reaction_rate(reaction, compl, pos_and_neg_compl)
    #         com_number = len(com)
    #         second_reactant = True
    #
    #     if self.complexes == []:
    #             reaction = self.reaction_container[0]
    #             self.set_basic_substrate_complex(reaction)

    def get_root_molecules(self, compl):
        """"""
        root = []
        lmol = self.reaction_container[0].left_reactant # [A]
        rmol = self.reaction_container[0].right_reactant # 
        root += compl.get_molecules(lmol.name, lmol.mid)
        root += compl.get_molecules(rmol.name, rmol.mid)
        return root # [A,B]

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