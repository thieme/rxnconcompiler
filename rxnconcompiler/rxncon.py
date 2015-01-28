#!/usr/bin/env python

# MR: code review 2014/10/19
# goal: comment on rxncon.py
# Tests: 115; F:1; E:6
#
# General comments:
# - you got inside the existing code really quickly - great!
# - I like your function names.
# - Thanks for fixing typos!
# - Rxncon starts to be long - you can think whether you see any logical
#   divisions e.g. parsing xls into objects and advanced operations,
#   or all 'updates'.
#   Perhaps it would be good to keep here only top level operations -
#   go through this class and if something is to detailed
#   (both your and my code) - find a better place for that).
#   (see also comment in find_conflicts).


#KR: code review 2013/12/29
# goals:
# 1. general comments on architecture (OOP and other)
# 2. question of complexes/negated complexes
# 3. everything else I see.
#    (since you have been refactoring a while I'll be more nitpicking)

# TODO: define role of 'super' complexes in the process.
# TODO: define role of domains in the process 

"""
Module rxncon.py creates rxncon objects.

Process steps:
1.   Data parsing.
==================
1.a. Parsing rxncon input into a dictionary 
     that reflects th xls input tables.
     Dictionary contains:
     - reaction_list 
     - contingency_list
     - reaction_definitions
1.b. Parsing data from dictionary into rxncon objects.
     The result is: 
     - ReactionPool containing ReactionContainer objects, 
       each with single Reaction object.
     - ContingencyPool containing root contingency 
       for all reactions with contingencies
     - MoleculesPool containing Molecule objects 
       representing all substrates.
2.   Creating complexes from boolean or complex contingencies.
==============================================================
     One complex may have alternative built (AlternativeComplexes).   
3.   Using complexes in reactions.
==================================
     When boolean or complex contingency are applicable to a reaction 
     its substrates are exchange with complexes.
     When there are alternative complexes available reaction is cloned
     so the ReactionContainer contain in the end 
     all alternatives when reaction can run
     as single Reaction objects.
     All remaining single Molecule objects are 
     exchanged with complex containing single molecule.
4.   Applying other (non-complex) contingencies.
===============================================
5.   Running reactions to obtain product complexes.
=======================
6.   Translating reactions into BNGL string.
============================================
6.a. Prepare RulePoll out of RecationPool 
     (same structure with RuleContainer and Rule objects) 
6.b. Create strings for all sections using BnglTranslator, and BnglOutput



Classes:
- Rxncon:        Input: rxncon dict. Output: rxncon objects.
                 out of initial reactions and contingencies produces reactions
                 similar to bngl rules.

"""

from util.warnings import RxnconWarnings
from molecule.domain_factory import DomainFactory
from biological_complex.biological_complex import ComplexPool
from biological_complex.complex_applicator import ComplexApplicator
from biological_complex.complex_builder import ComplexBuilder
from contingency.contingency_applicator import ContingencyApplicator
from contingency.contingency_factory import ContingencyFactory
from reaction.reaction_factory import ReactionFactory
from parser.rxncon_parser import parse_rxncon
from contingency.contingency import Contingency
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
from rxnconcompiler.molecule.molecule import Molecule
import re
import copy


class ConflictSolver:
    """
    """
    def __init__(self, reaction_pool, contingency_pool):
        self.contingency_pool = contingency_pool
        self.reaction_pool = reaction_pool

    def is_conflict(self, product_contingency, required_cont):
        if re.search('^(?!_)\[(.*?)\]', required_cont.target_reaction) or re.search('<(.*?)>', required_cont.target_reaction):
            return False
        elif str(required_cont.state) == str(product_contingency.state):
            if str(required_cont.ctype) != str(product_contingency.ctype):
                if str(required_cont.ctype) not in ["and", "or", "0"]:
                    if self.reaction_pool[required_cont.target_reaction][0].definition['Reversibility'] == 'reversible':
                        return True
        return False

    def get_molecules_on_state(self, comp, conflicted_state):
        """
        find all molecules involved in the conflicted_state
        return a list of these molecules
        """
        result = [mol for mol in comp.molecules if mol.has_state(conflicted_state)]
        return result

    def create_complexes(self):
        """
        Uses ComplexBuilder to create ComplexPool.
        """
        bools = self.contingency_pool.get_top_booleans()
        for bool_cont in bools:
            builder = ComplexBuilder()
            alter_comp = builder.build_positive_complexes_from_boolean(bool_cont)
            self.complex_pool[str(bool_cont.state)] = alter_comp

    def delet_redundant_reactions(self, rcont):
        """
        in find_conflicts_recursive we are applying k+ for each state we found in a chain. 
        This result in redundant reactions, which has to be deleted. This is done here.
        """

        common_cont = rcont.get_common_contingencies()

        already_applied = []

        remove_reaction = []
        for i, reaction in enumerate(rcont):
            if reaction.get_contingencies() in already_applied:
                remove_reaction.append(i)
            else:
                already_applied.append(reaction.get_contingencies())
                reaction.run_reaction()
        
        for i in reversed(remove_reaction):
            del rcont[i]
        return rcont

    def get_conflict_chain_save(self, conflicted_state, chain=[]):
        """
        find a possible chain of conflicts which are resulting from an initial conflict state.
        
        @param conflicted_state: A--B
        @type conflicted_state: string
        @param chain: List of all follow up states which are conflicted.
        @type chain: list
        @return chain: A list of all follow up conflicts resulting from the initial conflicting state
        """
        
        chain.append(conflicted_state)  # the conflict we have found is at least the conflict we have to deal with.
        for required_cont in self.contingency_pool.get_required_contingencies():

            if required_cont.target_reaction in self.reaction_pool and self.reaction_pool[required_cont.target_reaction].sp_state.type == "Association":
                if required_cont.ctype == "!" and required_cont.state == conflicted_state:  # find states which are dependent on this conflicting state

                    conflicted_state = self.reaction_pool[required_cont.target_reaction].sp_state  # get the state of the reaction which is conflicted
                    self.get_conflict_chain(conflicted_state, chain)  # this state is a new conflicting state and is used for the next iteration.
        #print chain
        return chain  # return a chain of all follow up conflicts

    def _get_contingency_reaction_dict(self):
        info_dict = {}
        for required_cont in self.contingency_pool.get_required_contingencies():
            if self.reaction_pool[required_cont.target_reaction].sp_state.type == "Association" and required_cont.ctype == "!":
                if required_cont.state not in info_dict:

                    info_dict[required_cont.state] = [self.reaction_pool[required_cont.target_reaction].sp_state]
                else:
                    info_dict[required_cont.state].append(self.reaction_pool[required_cont.target_reaction].sp_state)
        return info_dict

    def get_conflict_chain_save(self, conflicted_state, chain=[]):
        """
        find a possible chain of conflicts which are resulting from an initial conflict state.
        
        @param conflicted_state: A--B
        @type conflicted_state: string
        @param chain: List of all follow up states which are conflicted.
        @type chain: list
        @return chain: A list of all follow up conflicts resulting from the initial conflicting state
        """
        self._get_contingency_reaction_dict()
        #chain[conflicted_state] = {}  # the conflict we have found is at least the conflict we have to deal with.
        for required_cont in self.contingency_pool.get_required_contingencies():

            if required_cont.target_reaction in self.reaction_pool and self.reaction_pool[required_cont.target_reaction].sp_state.type == "Association":
                if required_cont.ctype == "!" and required_cont.state == conflicted_state:  # find states which are dependent on this conflicting state

                    #chain[conflicted_state][]
                    conflicted_state = self.reaction_pool[required_cont.target_reaction].sp_state  # get the state of the reaction which is conflicted
                    self.get_conflict_chain(conflicted_state, chain)  # this state is a new conflicting state and is used for the next iteration.
        #print chain
        return chain  # return a chain of all follow up conflicts
        
    def _add_chain(self, chain):
        if chain not in self.chain_collection:
            self.chain_collection.append(chain)

    def _merge_chains(self):
        new_chain = []
        for chain in self.chain_collection:
            new_chain.extend(chain)
        new_chain = list(set(new_chain))

        return new_chain

    def search_conflicte_chains(self, conflicted_state, chain=[]):

        copy_mapping_info_dict = copy.deepcopy(self.mapping_info_dict)

        chain, found_more_elements = self.get_conflict_chain(conflicted_state, copy_mapping_info_dict, [conflicted_state], set())  # get all follow up conflicts/consequences of the first conflict
        self._add_chain(chain)

        if found_more_elements:
            for element in found_more_elements: 
                index = self.chain_collection[-1].index(element)
                if index == 0:
                    chain = [self.chain_collection[-1][0]]
                else:
                    chain = self.chain_collection[-1][0:index]
                found_more_elements = found_more_elements - set([element])
                chain, found_more_elements = self.get_conflict_chain(chain[-1], copy_mapping_info_dict, chain, found_more_elements)

        self._add_chain(chain)
        chain = self._merge_chains()

        return chain

    def get_conflict_chain(self, conflicted_state, copy_mapping_info_dict, chain=[], found_more_elements=set()):
        """
        find a possible chain of conflicts which are resulting from an initial conflict state.
        
        @param conflicted_state: A--B
        @type conflicted_state: string
        @param chain: List of all follow up states which are conflicted.
        @type chain: list
        @return chain: A list of all follow up conflicts resulting from the initial conflicting state
        """
        
        if conflicted_state in copy_mapping_info_dict:

            if copy_mapping_info_dict[conflicted_state] != []:
                chain.append(copy_mapping_info_dict[conflicted_state].pop())
                if copy_mapping_info_dict[conflicted_state] != []:
                    found_more_elements.add(conflicted_state)
                self.get_conflict_chain(chain[-1], copy_mapping_info_dict, chain, found_more_elements)

        return chain, found_more_elements
        #return chain  # return a chain of all follow up conflicts

    def find_conflicts_recursive(self, product_contingency, conflicted_state, react_container):
        """
        find all follow up conflicts, which result from the initial conflict. Apply a k+ contingency for each. 
        """
        self.chain_collection = []
        self.mapping_info_dict = self._get_contingency_reaction_dict()
        chain = self.search_conflicte_chains(conflicted_state)

        cap = ContingencyApplicator()
        for element in chain:  # apply k+ contingency for all the conflicted states
            cont_k = Contingency(target_reaction=product_contingency.target_reaction,ctype="k+",state=element)
            cap.apply_on_container(react_container, cont_k)
            self.conflicted_states.append(element)

        return react_container

    def find_conflicts_on_mol(self, react_container):
        """
        find all conflicts a specific reaction/reaction_container is involved in
        apply a k+ contingency on this reaction (state=conflicted_state)
        return the reaction container and all states which are conflicted by this reaction 
        """
        import re

        product_contingency = react_container.product_contingency
        conflicted_state = ""
        self.conflicted_states = []
        self.conflict_found = False
        #self.conflict_recursion = True

        for required_cont in self.contingency_pool.get_required_contingencies():  # step 2 get required contingency, for possible conflicts
            #  the change should only be applied if the dependence reaction is reversible like ppi, ipi ...

            self.is_conflict(product_contingency, required_cont)
            if self.is_conflict(product_contingency, required_cont):  # self.conflict_found: #and self.reaction_pool[required_cont.target_reaction][0].definition['Reversibility'] == 'reversible':
                    self.conflict_found = True
                    required_cont_reaction_container = self.reaction_pool[required_cont.target_reaction]  # get reaction object of conflict reaction

                    conflicted_state = required_cont_reaction_container.sp_state  # get the state of the conflict reaction
                    #print "conflicted_state: ", conflicted_state
                    #if self.conflict_recursion:
                    react_container = self.find_conflicts_recursive(product_contingency, conflicted_state, react_container)
                    #else:
                        

                       #  print "##############"
                       #  print "product_contingency.target_reaction: ", product_contingency.target_reaction
                       #  print "required_cont.target_reaction: ", required_cont.target_reaction
                       # #print dir(required_cont.target_reaction)
                       #  print "conflicted_state: ", conflicted_state
                       #  print "conflict product_contingency: ", product_contingency, " required_cont: ", required_cont
                    #print conflicted_state
                    #cont_k = Contingency(target_reaction=product_contingency.target_reaction,ctype="k+",state=conflicted_state)

                        #cont_k = Contingency(target_reaction=product_contingency.target_reaction,ctype="k+",state=conflicted_state)
                    #cap = ContingencyApplicator()

                        # apply a k+ contingency to our product contingency target reaction
                        # step 5.1, 5.2, 5.3
                        # this approach also solves problems with adapting the reaction rates
                    #print "HIER"
                    #cap.apply_on_container(react_container, cont_k)

                    #self.conflicted_states.append(conflicted_state)


        return react_container

    def change_reversibility(self, reaction):
        """
        changes the reversibility of a reaction. This is needed if we change a reaction because of a conflict with an other reaction. This changes are not reversible.
        """
        if reaction.definition['Reversibility'] == 'reversible':
            reaction.reversibility = 'irreversible'
            reaction.rate.set_basic_rates(reaction)
        return reaction

    def reorder_molecules(self, new_complex, comp, found_no_complex, already_in_complex):
        """
        This function is to reorder the molecules, meaning to bring molecules together in a complex if they belong together.
        This function is repeated recursively as long as there is a molecule we cannot assign.
        """
        tmp_complex = copy.deepcopy(new_complex)
        for i, new_comp in enumerate(tmp_complex):  # iterate over the components of the new product_complexes
            for single_new_comp_mol in new_comp.molecules:  # iterate over the molecules of the single component.
                if single_new_comp_mol.binding_partners:  # There could be more than one molecule in the complex so we have to check the binding partners for each single molecule
                    for mol in comp.molecules:  # check all the molecules which are in the original product complex
                        if mol._id not in already_in_complex:  # check if a molecule is already bound a complex
                            for binding_partners in single_new_comp_mol.binding_partners:  # iterate over the binding partners of the molecule of the complex we are looking at
                                if binding_partners.has_component(mol):  # check if the molecule of the original complex is part of this complex.
                                    new_complex[i].molecules.append(mol)  # if yeas add the molecule to this complex
                                    already_in_complex.append(mol._id)  # mark this protein to be known
                                    if mol._id in found_no_complex:  # if we found in a previous round no complex for this molecule it will be listed in found_no_complex.
                                        found_no_complex = found_no_complex.difference(set([mol._id]))  # remove the id from this list
                                    break  # we found an complex were this molecule can be added so we can make a break
                            else:
                                found_no_complex.add(mol._id)  # if we don't have a break in the for loop we will end up here, because we did not found a complex we can assign the respective molecule.
        if found_no_complex:  # as long as there are a molecule we can not assign repeat the procedure
            self.reorder_molecules(new_complex, comp, found_no_complex, already_in_complex)
        return new_complex  # if all molecules are assigned leave this function

    def reassign_complexes(self, conflicted_mol, conflicted_state, comp, reaction, new_complex):
        """
        if there are conflicted molecules create for each of them a separated complex
        """
        already_in_complex = []  # to list all molecules we already assigned to a complex
        to_change_in_reaction = reaction.to_change  # what should be changed in this reaction, this is important if we have symmetrical interactions which are conflicted
        for mol in conflicted_mol:  # iterate over all molecules which are directly involved in the conflict

            if mol._id not in already_in_complex:  # check if we saw this molecule before

                new = BiologicalComplex()  # initialise a new complex
                new.side = 'LR'  # set the side
                mol.remove_bond(conflicted_state)  # remove the bond of the conflicting state. This leads to a loose of the bond and should result in a disconnection later
                new.molecules.append(mol)  # add the molecule to the new established complex
                already_in_complex.append(mol._id)  # add the molecule to the known molecules
                for comp_mol in comp.molecules:  # iterate of all the other molecules in the original product complex
                    if comp_mol._id != mol._id and comp_mol._id not in already_in_complex:  # the molecule of the original product complex should not be the same as the conflicting molecule and not known.
                        if len(to_change_in_reaction.components) == 2 and ((to_change_in_reaction.components[0].name == comp_mol.name and to_change_in_reaction.components[1].name == mol.name) or (to_change_in_reaction.components[1].name == comp_mol.name and to_change_in_reaction.components[0].name == mol.name)):
                            if set(new.molecules[0].binding_partners) & set(comp_mol.binding_partners):  # check if there are overlapping binding partners
                                    reaction = self.change_reversibility(reaction)  # if we change a reaction in this way we have to change the type to irreversible
                                    comp_mol.remove_bond(conflicted_state)  # remove the bond of the conflicting state. This leads to a loose of the bond and should result in a disconnection later
                                    new.molecules.append(comp_mol)  # add the molecule to the new product complex
                                    already_in_complex.append(comp_mol._id)  # add the molecule to the known molecules
                                    break  # if we find a binding partner we don't have to look further

                new_complex.append(new)  # extend the product complexes
        return new_complex, already_in_complex

    def solve_conlict(self, react_container):
        """
        change the reactions responsible for the conflict 

        The reactions are already cloned by applying k+ contingency on the container
        now we have to change the product complex because we have

            Z + A(Z~U,AssocB!1).B(AssocA!1) -> Z + A(Z~P,AssocB!1).B(AssocA!1)    k1_1

            Z + A(Z~U,AssocB) -> Z + A(Z~P,AssocB)    k1_2

        and want 

            Z + A(Z~U,AssocB!1).B(AssocA!1) -> Z + A(Z~P,AssocB!1) + B(AssocA!1)    k1_1

            Z + A(Z~U,AssocB) -> Z + A(Z~P,AssocB)    k1_2
        """

        product_contingency = react_container.product_contingency
        reversible = False

        for conflicted_state in self.conflicted_states:
            for reaction in react_container:
                cont_reaction_dict = {}
                for cont_reaction in reaction.get_contingencies():
                    cont_reaction_dict[str(cont_reaction).split()[1]] = str(cont_reaction).split()[0]  # later we need to distinguish when which reaction combination of the k+ was applied
                new_complex = []

                for i, comp in enumerate(reaction.product_complexes):

                    conflicted_mol = []
                    # check if the conflict state was applied on this complex and if this was a ! contingency

                    if str(conflicted_state) in cont_reaction_dict and cont_reaction_dict[str(conflicted_state)] == "!":

                        conflicted_mol = self.get_molecules_on_state(comp, conflicted_state)

                        if conflicted_mol:
                            new_complex, already_in_complex = self.reassign_complexes(conflicted_mol, conflicted_state, comp, reaction, new_complex)

                            if len(conflicted_mol) != len(comp.molecules):  # find binding partners which are left
                                reaction = self.change_reversibility(reaction)

                                found_no_complex = set([])
                                new_complex = self.reorder_molecules(new_complex, comp, found_no_complex, already_in_complex)

                        else:
                            new_complex.append(comp)
                    else:
                        new_complex.append(comp)
                if new_complex:
                    reaction.product_complexes = new_complex


class Rxncon:
    """
    Manage the process that leads from the tabular data representation
    to the object oriented representation of reactions and contingencies.
    The process and objects are bngl-oriented.
    #KR: better 'The process and objects were designed to allow...'
    E.g. they were design to allow flexible and unambiguous
    translation to bngl string in later stage.

    The end product is a pool of ReactionContainer objects.
    Single ReactionContainer object corresponds to a RuleContainer object.
    Single ReactionContainer has all data necessary for translation into bngl.

    @type xls_tables:  dictionary
    @param xls_tables: rxncon input data
    """
    def __init__(self, xls_tables):
        """
        Constructor creates basic objects with explicitly given information:
        - MoleculePool created by Reaction Factory
        - ReactionPool created by Reaction Factory
        - ContingencyPool created by ContingencyFactory
        - ComplexPool created here using ComplexBuilder
        Data is supplemented by domain info for ppis with no domain specified by the user.

        MoleculePool - list of all right and left reactants from all reactions.
        ReactionPool - dict of all reactions.
                       rxncon reaction str: ReactionContiner object
                       (captures all possible alternative reactions
                       depending on conditions in which reaction can happen).
        ContingencyPool - dictionary of all contingencies.
                          rxncon_reaction_str: root contingency
                          (which contains all contingencies assign to this reaction).
        ComplexPool - dict of all complexes (defined as children-containing contingencies with '<>').
                      '<name>': AlternativeComplexes (which contains BiologicalComplex objects).
        """
        self.solved_conflicts = []
        self.war = RxnconWarnings()
        self.df = DomainFactory()
        self.xls_tables = parse_rxncon(xls_tables)
        reaction_factory = ReactionFactory(self.xls_tables)
        self.molecule_pool = reaction_factory.molecule_pool
        self.reaction_pool = reaction_factory.reaction_pool
        contingency_factory = ContingencyFactory(self.xls_tables)
        self.contingency_pool = contingency_factory.parse_contingencies()
        
        self.complex_pool = ComplexPool()
        self.create_complexes()

        self.update_contingencies()
        self.solve_conflict = ConflictSolver(self.reaction_pool, self.contingency_pool)

    def __repr__(self):
        """
        Rxncon object is represented as rxncon string 
        (quick format).
        """
        #KR: this is cool! I see both MR's handwriting here.
        result = ''
        react_keys = [(self.reaction_pool[reaction].rid, reaction) for reaction in self.reaction_pool.keys()]
        for reaction in sorted(react_keys):
            result += reaction[1]
            if self.contingency_pool.has_key(reaction[1]):
                cont_root = self.contingency_pool[reaction[1]]
                all_cont = cont_root.get_children()
                for cont in all_cont:
                    later = []
                    if cont.ctype in ['or', 'and'] or '--' in cont.ctype:
                        later.append(cont)
                    else:
                        result += '; %s' % str(cont)
                    for cont in later:
                        result += '\n%s; %s %s' % (cont.target_reaction, cont.ctype, str(cont.state))
            result = result.strip() + '\n'
        return result

    def create_complexes(self):
        """
        Uses ComplexBuilder to create ComplexPool.
        """
        bools = self.contingency_pool.get_top_booleans()
       #print "bools: ", bools
        for bool_cont in bools:
            builder = ComplexBuilder()
            alter_comp = builder.build_positive_complexes_from_boolean(bool_cont)
            self.complex_pool[str(bool_cont.state)] = alter_comp

    def get_requirements_dict(self):
        """
        """
        req_dict = {}
        for rname in self.reaction_pool.keys():
            req_dict[rname] = []
            for reaction in self.reaction_pool[rname]:
                req_dict[rname].append(reaction.get_contingencies())
        return req_dict

    def get_complexes(self, reaction_name):
        """
        Prepares a list of complexes applicable to a give reaction.

        @type  reaction_name: string
        @param reaction_name: reaction string e.g. A_ppi_B_[bd_A].

        @rtype:  list of AlternativeComplexes object
        @return: all complexes defined by boolean contingencies
                 applicable to a given reaction.
        """
      #  print "self.contingency_pool: ", self.contingency_pool
        #print "self.contingency_pool[reaction_name]: ", self.contingency_pool[reaction_name]
        if not self.contingency_pool.has_key(reaction_name):
            return []
        cont_root = self.contingency_pool[reaction_name]

        for cont in cont_root.children:
            if cont.state.type == 'Boolean':
                if self.complex_pool.has_key(str(cont.state)):
                    return self.complex_pool[str(cont.state)]

    def apply_contingencies(self, container):
        """
        Applys non-boolean contingencies.
        0, ? are ignored
        """
        contingencies = []
        if self.contingency_pool.has_key(container.name):
            for cont in self.contingency_pool[container.name].children:
                if cont.children == []:
                    contingencies.append(cont)
        cap = ContingencyApplicator(self.war)
        for cont in contingencies:            
            cap.apply_on_container(container, cont)

    def update_contingencies(self):
        """
        Function that changes domain name in contingencies
        with modification state (when domain is not provide by the user).
        Domain indicates which enzyme creates the state.
        State must match one of the states produced in the reactions.
        """
        # TODO: make ContingencyUpdator class out of it.
        # TODO: separate functions for different updates.

        modifications = self.contingency_pool.get_modification_contingencies()
        if modifications:

            for cont in modifications:
                if cont.state.has_bd_domain():
                    available = self.reaction_pool.find_modification_product(cont.state)
                    available = sorted(available, key=lambda state: state.components[0].name)
                    default_domain_present = False
                    for state in available:
                        if state.has_bd_domain():
                            default_domain_present = True
                    if not default_domain_present:
                        if len(available) > 1: 
                            self.war.produced_in_more[cont] = available
                            cont.state = available[0]
                        elif len(available) == 1:
                            cont.state = state
                        else:
                            self.war.not_in_products.append(cont)
        # TODO: refine this function. Add warnings.
        relocalisations = self.contingency_pool.get_relocalisation_contingencies()
        for cont in relocalisations:
            if not cont.state.not_modifier:
                available = self.reaction_pool.find_relocalisation_product(cont.state)
                if available:
                    if available[0].modifier == cont.state.modifier:
                        cont.state.not_modifier = available[0].not_modifier
                    else:
                        cont.state.not_modifier = available[0].modifier

    def update_reactions(self):
        """
        TODO: To be implemented.
        translation - get empty domains
        x, ! - get additional reaction / modify existing ones.
        """
        pass

    def get_input_dict(self):
        """"""
        pass

    def add_missing_reactions(self, states_list):
        """
        Creates pool of reaction that produce states required in the system
        and adds them to the systems reaction pool (self.reaction_pool).
        """
        reaction_factory = ReactionFactory(states_list)
        missing_molecule_pool = reaction_factory.molecule_pool
        missing_reaction_pool = reaction_factory.reaction_pool
        self.reaction_pool.update_pool(missing_reaction_pool)
        self.molecule_pool += missing_molecule_pool
        self.war.not_in_products = []

    def add_translation(self):
        """
        Adds translation reaction for each protein to reaction_pool.
        """
        # Add appropriate reaction_factory
        pass

    def run_process(self, add_translation=False, add_missing_reactions=False, add_complexes=True, add_contingencies=True):
        """
        Transforms table into objects.
        Groups the information that belong together.
        Adds implicit information.

        add_translation: when Trues add translation reaction for each protein # not available yet.
        add_missing_reactions: when True looks for required states that are not produced and adds proper reactions.
        add_complexes: when True applys boolean contingencies.
        add_contingencies: when True applys non-boolean contingencies.
        """
        #print self.contingency_pool.get_mutual_exclusive_contingencies()
        #self.contingency_pool.print_mutual_exclusive_contingencies()

        # print 'Contingencies', self.contingency_pool['Ste11_[KD]_P+_Ste7_[AL(T363)]'].children[1].children
        self.war.calculate_missing_states(self.reaction_pool, self.contingency_pool)
        #self.war.get_mutual_exclusive_reactions(self.reaction_pool)
        if add_missing_reactions:
            self.add_missing_reactions(list(self.war.not_in_products))
        if add_translation:
            self.add_translation()

        for react_container in self.reaction_pool:

            # initially container has one reaction
            # (changes after running the process because of OR and K+/K-)
            complexes = []
            if add_complexes:
                complexes = self.get_complexes(react_container.name)

            ComplexApplicator(react_container, complexes).apply_complexes()

            # after applying complexes we may have more reactions in a single container.
            react_container = self.solve_conflict.find_conflicts_on_mol(react_container)
            if add_contingencies or self.solve_conflict.conflict_found:
                self.apply_contingencies(react_container)

            # single contingency is applied for all reactions. If K+/K- reactions are doubled.
            self.update_reactions()

            react_container = self.solve_conflict.delet_redundant_reactions(react_container)
            #for reaction in react_container:
                #print dir(reaction)
            #    reaction.run_reaction()

            if self.solve_conflict.conflict_found:
                self.solve_conflict.solve_conlict(react_container)


if __name__ == '__main__':
    main()
