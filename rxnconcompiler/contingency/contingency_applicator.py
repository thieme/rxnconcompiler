#!/usr/bin/env python

"""
Module contingency_applicator.py
deals wit non-boolean contingencies:
- !  ---> absolutely required
- x  ---> absolutely inhibitory
- k+ ---> positive stimulation
- k- ---> negative stimulation
- 0  ---> no effect
- ?  ---> unknown effect or no effect
Contingencies 0 and ? are ignored.
- ctype input ---> this is a special kind of contingency -
  molecules stay as they are but rate changes.
 
Applies contingencies on:
- molecules
- complexes
- reactions
- reaction containers

In the end coningency application means 
modification of molecule object (gets assitional modification, bond ...).
If contingency type is K+ or K- it also means dupplication of a reaction
and updating the rate for the new one.

How rate is updated for K+/K-:
- 

TODO: How to apply cont like A_P+_B; A--B
"""

import copy
from contingency_factory import ContingencyWrapper
from molecule.molecule import Molecule
from biological_complex.biological_complex import BiologicalComplex


class ContingencyApplicator():
    """
    Applys contingency on 
    - molecules
    - compelxes
    - reactions
    - reaction containers
    """
    def __init__(self, war=None):
        self.war = war

    def apply_on_molecule(self, mol, cont, side = 'L'):
        """
        Applys contingency on molecule.
        Side - indicatecs whether molecule belong to
        left or right substrate complex.
        It is important when we have homodimer states: 
        indicstes which doman is used.
        """
        if cont.state.type == 'Association' and cont.ctype == 'x':
            #mol.binding_sites.append(cont.state)
            mol.add_binding_site(cont.state, side)
        elif cont.state.type == 'Covalent Modification' and cont.ctype == '!':
            mol.add_modification(cont.state)
        elif cont.state.type == 'Covalent Modification' and cont.ctype == 'x':
            mol.add_modification_site(cont.state)
        elif cont.state.type == 'Relocalisation':
            mol.localisation = cont.state
            if cont.ctype == '!':
                cont.state.loc = True


    def add_molecule_to_complex(self, mols, cont, component, compl, reaction):
        """
        mols      - molecules that are present in complex and in contingency 
                    e.g. Complex: A, B, C; Cont: ! A--X  ---> [A]
        cont      - Contingency object, e.g. ! A--X
        component - the other component from contingency - one to be added
                    e.g. X
        compl     - complex
        reaction  - reaction in question
        """
        #print 'add_molecule_to_complex'
        #print mols, cont, component, compl
        # check whether cotingency state in not equal to product state 
        add_partner = True
        for state in mols[0].binding_sites:
            if state == cont.state:
                dom_cont = cont.state.get_component(mols[0].name).domain
                dom_side = state.get_component(mols[0].name).domain  
                if dom_side == dom_cont: 
                    add_partner = False

        # check conflickts between contingency and to_change
        # (state that changes in the reaction)
        for comp_cont in cont.state.components:
            for comp_tochange in reaction.to_change.components:
                if comp_cont.exact_compare(comp_tochange):    
                    add_partner = False

        # check whether domain is not occupied
        new_mols = []
        for mol in mols:
            occupied_doms = mol.get_domains('binding', True)
            if component.domain not in occupied_doms:
                new_mols.append(mol)
        mols = new_mols
        if not mols:
            add_partner = False 
            if self.war:
                self.war.not_applied_contingencies.append(reaction)

        if add_partner:
            mols[0].binding_partners.append(cont.state)
            mol_ob = Molecule(component.name)
            mol_ob.binding_partners.append(cont.state)
            compl.molecules.append(mol_ob) 


    def apply_positive_association(self, reaction, cont):
        """
        it requires either
        - adding a new molecule to a complex
        - or incorporating two substrate complexes into one
        and not just editing existing molecules in a complex.
        It also neads to deal with a situation that there is already one complex.
        """
        component1 = cont.state.components[0]
        component2 = cont.state.components[1]

        # situation when we need to join complexes
        left = reaction.get_substrate_complex('L')
        right = reaction.get_substrate_complex('R')
        left_right = reaction.get_substrate_complex('LR')
        
        if left_right:
            mols1 = left_right.get_molecules(component1.name, component1.cid)
            mols2 = left_right.get_molecules(component2.name, component2.cid)

            if mols1 and mols2:
                # what to do when two molecules are already in?
                # e.g. A.B + C ! A--B
                #print "PROBLEM", mols1, mols2
                pass
            if mols1:
                self.add_molecule_to_complex(mols1, cont, component2, left_right, reaction)

            elif mols2:
                self.add_molecule_to_complex(mols2, cont, component1, left_right, reaction)

        elif left and right:
            # TODO: Refactor make a function to check this condition.
            # A--B, A and B present in substrates
            if ((left.has_molecule(component1.name) and right.has_molecule(component2.name))\
                or (left.has_molecule(component2.name) and right.has_molecule(component1.name)))\
                and not cont.state == reaction.to_change: 
         
                if component1.name in [reaction.left_reactant.name, reaction.right_reactant.name] \
                    and component2.name in [reaction.left_reactant.name, reaction.right_reactant.name]:
                # if A--B, A and B present in substrates but if reaction creates A and B
                # we don't join. We want then A
                    reaction.join_substrate_complexes(cont.state)

                # here one of mols from contingency is present in both complexes
                # but it was added becouse of previously applayed coningency so we dont want to join.
                else:
                    if component1.name == reaction.left_reactant.name \
                        or component2.name == reaction.left_reactant.name:
                        self._add_components_to_complex(left, component1, component2, cont, reaction)
                    else: 
                        self._add_components_to_complex(right, component1, component2, cont, reaction)

        # a molecule needs to be added to complexes 
        # or complexes are already joined:
            else:
                for compl in reaction.substrat_complexes:
                    self._add_components_to_complex(compl, component1, component2, cont, reaction)

                        
    def _add_components_to_complex(self, compl, component1, component2, cont, reaction):
        """
        Helper function.
        Checks which component is already in the complex and adds the second one.
        What to do when both are already present??? (Not decided yet).
        """
        mols1 = compl.get_molecules(component1.name, component1.cid)
        mols2 = compl.get_molecules(component2.name, component2.cid)

        if mols1 and mols2:
            # what to do when two molecules are already in?
            # e.g. A.B + C ! A--B
            #print "PROBLEM", mols1, mols2
            pass

        if mols1:
            self.add_molecule_to_complex(mols1, cont, component2, compl, reaction)

        elif mols2:
            self.add_molecule_to_complex(mols2, cont, component1, compl, reaction)
                

    def apply_on_complex(self, compl, cont):
        """
        Possitive association won't get here.
        """
        if cont.state.type == 'Association': # only negative associations get here.
            side = compl.side
            for component in cont.state.components:
                mols = compl.get_molecules(component.name, component.cid)
                if mols:
                    self.apply_on_molecule(mols[0], cont, side)
        else:
            component = cont.state.components[0]
            mols = compl.get_molecules(component.name, component.cid)
            if mols:
                self.apply_on_molecule(mols[0], cont)        

    def apply_on_reaction(self, reaction, cont):
        """
        Gets reaction and x or ! contingency.
        For ! contingencies with input state creates additional substrate complex.
        For other states applays contingency on substrate complexes.
        """
        for compl in reaction.substrat_complexes:
                self.apply_on_complex(compl, cont)

    def apply_input_on_container(self, container, cont):
        """
        Applys all input contingencies.
        Input contingency is applied by changing reaction rate 
        (adding a local function).

        Rate depend on:
        - ontingency type: difrent functions for !, x and K
        - whether reaction is reversible or irreversible
          (for reversible reaction kr always looks like for K even when its ! or x)

        Different rate function types:
        - k1*k_Input                     ---> function for ! [Input]
        - k1*(1-k_Input)                 ---> function for x [Input]
        - k1_1*(1-k_Input)+k1_2*k_Input  ---> for K+/K- and all reversed reactions  
          (complex must be able to dissociate even when input is not present an more)
        """
        # establish new ids for rates - num1, num2
        highest_subrate = container.highest_subrate  # int
        if highest_subrate == 0:
            num1 = '%s_1' % container.rid
            num2 = '%s_2' % container.rid
        else:
            num1 = '%s_%s' % (container.rid, str(highest_subrate + 1))
            num2 = '%s_%s' % (container.rid, str(highest_subrate + 2))

        if cont.ctype in ['x', '!']:
            for reaction in container:
                if reaction.definition['Reversibility'] == 'reversible':
                    # we will have two rates here (because of reverse rreaction).
                    reaction.rate.update_function(cont, False, num1, num2)
                else:
                    # just multiply old rate by input rate.
                    # We don't need new rate numbers here.
                    # Because it is still one rate.
                    rate_id = reaction.rate.get_ids()[0]
                    reaction.rate.update_function(cont, False, rate_id, None)

        elif 'k' in cont.ctype:
            # here input rate is a switch between two rates.
            for reaction in container:
                reaction.rate.update_function(cont, True, num1, num2)

    def get_rate_ids(self, reaction, container, subrate, keep_old=False):
        """
        When applying K+/K- contingency rates need to be updated.
        This function retuens a list of new ids which 
        will be used for updating.

        e.g. 
        ['1', None]
        ['3_5', '3_6']
        """
        # TODO: Does this function belongs here?
        single_id = lambda container, old_id, subrate: '%s_%s' % (container.rid, str(int(old_id.split('_')[1]) + subrate))
        
        # Trys to keep old id if possible
        if keep_old:
            if subrate == 0:
                return ['%s_1' % container.rid, None]
            else:
                old_ids = reaction.rate.get_ids()
                if len(old_ids) == 1:
                    return [old_ids[0], None]
                else:
                    return old_ids
        else:
            if subrate == 0:
                return ['%s_2' % container.rid, None]
            else:
                old_ids = reaction.rate.get_ids()
                if len(old_ids) == 1:
                    return [single_id(container, old_ids[0], subrate), None]
                else:
                    return [single_id(container, old_ids[0], subrate), single_id(container, old_ids[1], subrate)]

    def apply_on_container(self, container, cont):
        """
        Applys a contingency on a container.
        Top level function. It is called first and direacts tasks to other functions.

        --- If contingency contains Input state:
            apply_input_on_container

        --- If ctype x or ! (no Input):
            apply_on_reaction
            --- If contingency state is Association then:
                apply_positive_association

        --- If ctype is K+ or K- (no Input):
            clone all the reactions in the container 
            for each reaction (now two) applys one ! and one x
            (it is done like in previous step).
            Updates rate:
            reaction.rate.update_name

        Only normal contingencies are applied here.
        """
        # TODO: some ugly stuff here - refactor.
        #       emptying container and adding them again to get consistent ids.
        #       Remove some iterations.
        # Input contingencies are handled by adding function to reaction rate.
        if cont.state.type == 'Input':
            self.apply_input_on_container(container, cont)

        elif cont.ctype in ['x', '!']:
            for reaction in container:
                if cont.state.type == 'Association' and cont.ctype == '!':
                    self.apply_positive_association(reaction, cont)
                else:
                    self.apply_on_reaction(reaction, cont)
          
        elif 'k' in cont.ctype:
            #rate_dict = self.prepare_rates_dict()
            temp = []
            pos_cont = ContingencyWrapper(cont, 'positive').get_contingency()
            neg_cont = ContingencyWrapper(cont, 'negative').get_contingency()
            subrate = container.highest_subrate

            for reaction in container:                
                temp.append(reaction.clone())

            temp2 = []
            #print 'Len:', len(container)
            for reaction in container:
                #print 'Reaction in orig container:', reaction.substrat_complexes[0].molecules[0].modifications, reaction.substrat_complexes[0].molecules[0].modification_sites
                #print 'Mod before cloning', reaction.substrat_complexes[0].molecules[0].modifications
                #print 'Mod site before cloning', reaction.substrat_complexes[0].molecules[0].modification_sites
                reaction = reaction.clone() 
                #print 'Mod after cloning', reaction.substrat_complexes[0].molecules[0].modifications
                #print 'Mod site after cloning', reaction.substrat_complexes[0].molecules[0].modification_sites
                if cont.state.type == 'Association':
                    self.apply_positive_association(reaction, pos_cont)
                else:
                    ############### BUG
                    self.apply_on_reaction(reaction, pos_cont)
                #print 'After applying:', reaction.substrat_complexes[0].molecules[0].modifications, reaction.substrat_complexes[0].molecules[0].modification_sites

                new_rate_ids = self.get_rate_ids(reaction, container, subrate, True)
                reaction.rate.update_name(new_rate_ids[0], new_rate_ids[1])
                temp2.append(reaction)

            #for reaction in temp2:
            #    print 'Reaction in temp2:', reaction.substrat_complexes[0].molecules[0].modifications, reaction.substrat_complexes[0].molecules[0].modification_sites
                
                

            container.empty()
            for reaction in temp2:
                container.add_reaction(reaction)

            for reaction in temp:                
                self.apply_on_reaction(reaction, neg_cont)               
                container.add_reaction(reaction)
                new_rate_ids = self.get_rate_ids(reaction, container, subrate, False)
                reaction.rate.update_name(new_rate_ids[0], new_rate_ids[1])