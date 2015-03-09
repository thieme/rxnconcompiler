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
from biological_complex import BiologicalComplex
from complex_builder import ComplexBuilder
from rxnconcompiler.util.util import product
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.contingency.contingency_applicator import ContingencyApplicator


class ComplexApplicator:
    """
    Interface between AlternativeComplex objects and ReactionContainer object.
    """
    def __init__(self, reaction_container, complexes):
        """"""
        #print complexes
        self.reaction_container = reaction_container        
        self.builder = ComplexBuilder()

        if not complexes:
            self.complexes = []
            self.not_connected_states = {}
        else:
            self.not_connected_states = complexes.not_connected_states
            #if len(complexes) > 2: #more than two booleans
            #    raise TypeError('Cannot apply more than two boolean contingencies on a reaction.')
            self.complexes = self.prepare_complexes_to_apply(complexes)
        
        #def check_complexes(self)

    def _prepare_alter_complex(self, alter_complex):
        """
        Gets single AlternativeComplexes object and 
        Input: all positive complexes.
        Output: all required complexes (combinations of positive and negative complexes).

        Complexes can contain a complex with no molecules and just an input state.
        """
        # TODO: EMPTY COMPLEXES??? WHY???
        to_remove = [comp for comp in alter_complex if (comp.molecules == [] and not comp.input_conditions)]
        for comp in to_remove:
            alter_complex.remove(comp)
        #############################################
        root = self.get_root_molecules(alter_complex.get_first_non_empty())[0]
        #print 'Root', root
        com = self.builder.build_required_complexes(alter_complex, root)
        return com
       
    def prepare_complexes_to_apply(self, input_complexes):
        """
        @type input_complexes:  list of AlternativeComplexes
        @param input_complexes: one or two AlternativeComplexes objects as a list.
                                Alternative Complexes object keeps all complexes 
                                from one boolean contingency. Maximaly two boolean 
                                contingency can be applied on a reaction.
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

    def both_complex_types_present(self):
        """
        BiologicalComplex.is_positive can have three values:
        - True
        - False
        - 'both' (when k+/k- input condition)

        Returns False when either only 
        positive complexes are present or only negative.

        Returns True when positive and negative complexes 
        are present or complexes that are both positive and negtiv at the time (K).

        It also returns True when reaction is reversible 
        and complex contains input condition.
        (then we need two rates anyway for reversible reaction).
        """
        pos = False
        neg = False

        for reaction, compl in zip(self.reaction_container, self.complexes):
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
        When there are alternative complexes to applay 
        new reactions will be created (copies of basic one) 
        and added to a ReactionContainer. In some cases they will 
        all have the same rate, in some cases it needs to be changed.
        This function updates reaction rate.

        Rate has single digit when only positive 
        or negative complexes are present.
        When both:
        - X_1 for positive 
        - X_2 for negative

        Additionaly it updates rates with functions 
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

    def set_not_connected_states(self, missing_condition, raw_reaction, cap, already):
        for current_not_connected_state in self.not_connected_states[missing_condition]['not_connected']:
            #print "current_not_connected_state: ", current_not_connected_state
            # we have to add a reaction for each combination. Therefore we copy an unmodified reaction
            reaction = copy.deepcopy(raw_reaction)
            self.set_basic_substrate_complex(reaction)  # set the basic molecules of the unmodified reaction

            cont1 = Contingency(target_reaction=self.reaction_container.name, ctype="!", state=missing_condition)
            cont2 = Contingency(target_reaction=self.reaction_container.name, ctype="x", state=current_not_connected_state)
            cap.apply_on_reaction(reaction, cont2)  # apply the not connected state contingency for this iteration step
        #    reaction_copy = copy.deepcopy(reaction)  # take a copy of this modified reaction for later extension of the different combination of other states
            cap.apply_on_reaction(reaction, cont1)  # apply the missing condition
            
            #self.reaction_container.add_reaction(reaction) # this results in a reaction with a first simple combination of the missing condition and the not connected states
            # have a look at all states which are not connected to the missing condition to get all the combinations of missing condition and not connected states
            # for other_not_connected_state in self.not_connected_states[missing_condition]['not_connected']:  
            #     if other_not_connected_state != current_not_connected_state:
            #         reaction_combi = copy.deepcopy(reaction_copy)
            #         # as long as we have not connected states left add a x contingency
            #         if other_not_connected_state not in already and current_not_connected_state not in already:
            #             #cont1 = Contingency(target_reaction=self.reaction_container.name, ctype="!", state=missing_condition)
            #             cont3 = Contingency(target_reaction=self.reaction_container.name, ctype="x", state=other_not_connected_state)

            #             already.append(other_not_connected_state)
            #             cap.apply_on_reaction(reaction_combi, cont1)
            #             cap.apply_on_reaction(reaction_combi, cont3)
            #             self.reaction_container.add_reaction(reaction_combi)
                    
        return already

    def apply_complexes(self):
        """
        """
        raw_reaction = self.reaction_container[0].clone()
        while self.complexes and len(self.reaction_container) != len(self.complexes) and len(self.complexes) > 0:
            new_reaction = self.reaction_container[0].clone()
            self.reaction_container.add_reaction(new_reaction)

        counter = 1
        pos_and_neg_compl = self.both_complex_types_present()

        for reaction, compl in zip(self.reaction_container, self.complexes):
            if len(self.reaction_container) > 1: 
                reaction.rid = "%i_%i" %(self.reaction_container.rid, counter)  
                counter +=1
            self.add_substrate_complexes(reaction, compl)
            self.update_reaction_rate(reaction, compl, pos_and_neg_compl)

        if self.complexes == []:
            reaction = self.reaction_container[0]
            self.set_basic_substrate_complex(reaction)
            # if reaction.left_reactant._id == reaction.right_reactant._id:
            #     self.molecule2complex(reaction.left_reactant, reaction, 'LR')
            # else:
            #     if reaction.left_reactant:
            #         self.molecule2complex(reaction.left_reactant, reaction, 'L')
            #     if reaction.right_reactant:
            #         self.molecule2complex(reaction.right_reactant, reaction, 'R')

        cap = ContingencyApplicator()

        #print "self.not_connected_states: ", self.not_connected_states
        already = []
        # ToDo: refactor
        for missing_condition in self.not_connected_states:
            print "missing_condition: ", missing_condition
            #print "missing_condition: ", missing_condition
            #already = self.set_not_connected_states(missing_condition, raw_reaction, cap, already)
            reaction = copy.deepcopy(raw_reaction)
            reaction_neg = copy.deepcopy(raw_reaction)
            self.set_basic_substrate_complex(reaction)  # set the basic molecules of the unmodified reaction
            self.set_basic_substrate_complex(reaction_neg)  # set the basic molecules of the unmodified reaction
            ### duplication
            if missing_condition.type == "Association":
                    for comp in reaction.substrat_complexes:
                        if comp.has_molecule(missing_condition.components[0].name): 
                            comp.add_state(missing_condition)
                        elif comp.has_molecule(missing_condition.components[1].name):
                            comp.add_state(missing_condition)

            cont1 = Contingency(target_reaction=self.reaction_container.name, ctype="!", state=missing_condition)
            cont1_neg = Contingency(target_reaction=self.reaction_container.name, ctype="x", state=missing_condition)
            cap.apply_on_reaction(reaction, cont1)  # apply the missing condition
            cap.apply_on_reaction(reaction_neg, cont1_neg)
            #print "hier"
            for current_not_connected_state in self.not_connected_states[missing_condition]['not_connected']:
                print "current_not_connected_state: ", current_not_connected_state
                # we have to add a reaction for each combination. Therefore we copy an unmodified reaction
                
                cont2 = Contingency(target_reaction=self.reaction_container.name, ctype="x", state=current_not_connected_state)
                cap.apply_on_reaction(reaction, cont2)  # apply the not connected state contingency for this iteration step
                cap.apply_on_reaction(reaction_neg, cont2)

            self.reaction_container.add_reaction(reaction)

            for current_connected_state in self.not_connected_states[missing_condition]['connected']:
                print "current_connected_state: ", current_connected_state
                reaction_neg_last = copy.deepcopy(reaction_neg)
                ## I have to add a modification or a binding partner at this position for the respective molecule
                ### duplication
                if current_connected_state.type == "Association":
                    for comp in reaction_neg_last.substrat_complexes:
                        if comp.has_molecule(current_connected_state.components[0].name): 
                            comp.add_state(current_connected_state)

                        elif comp.has_molecule(current_connected_state.components[1].name):
                            comp.add_state(current_connected_state)

                cont = Contingency(target_reaction=self.reaction_container.name, ctype="!", state=current_connected_state)
                cap.apply_on_reaction(reaction_neg_last, cont)
                self.reaction_container.add_reaction(reaction_neg_last)
                cont_neg = Contingency(target_reaction=self.reaction_container.name, ctype="x", state=current_connected_state)
                cap.apply_on_reaction(reaction_neg, cont_neg)
                reaction_neg = copy.deepcopy(reaction_neg)
            #    reaction_copy = copy.deepcopy(reaction)  # take a copy of this modified reaction for later extension of the different combination of other states


    def get_root_molecules(self, compl):
        """"""
        root = []
        lmol = self.reaction_container[0].left_reactant
        rmol = self.reaction_container[0].right_reactant
        root += compl.get_molecules(lmol.name, lmol.mid)
        root += compl.get_molecules(rmol.name, rmol.mid)
        return root

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