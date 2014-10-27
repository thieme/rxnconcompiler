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
import re

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
        #self.find_conflicts_on_mol()
        self.complex_pool = ComplexPool()
        self.create_complexes()
        self.update_contingencies()

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
        # Add apropriate reaction_factory
        pass

    def is_conflict(self,product_contingency, required_cont):
        #self.conflict_found = False
        if re.search('^(?!_)\[(.*?)\]',required_cont.target_reaction) or re.search('<(.*?)>', required_cont.target_reaction):
            return False
        elif str(required_cont.state) == str(product_contingency.state):
            if str(required_cont.ctype) != str(product_contingency.ctype):
                if str(required_cont.ctype) not in ["and", "or", "0"]:
                    if self.reaction_pool[required_cont.target_reaction][0].definition['Reversibility'] == 'reversible':
                        #self.conflict_found = True
                        return True # self.conflict_found
        return False # self.conflict_found
        

    def find_conflicts_on_mol(self, react_container):
        import re
               # MR:
        # Be careful with function responsibility:
        # for me it is misleading that function called find_conflicts 
        # also solve them.
        # Be careful with function responsibility:
        # I would call both functions in the run_process - find and solve and have some self.conflicts
        # (I see WCM influence here ;-D)
        # Perhaps it will be easier to start some ConflictSolver,
        # as you manipulate data at the end of run_process anyway? 

        product_contingency = react_container.product_contingency
        conflict_state = ""
        self.conflict_found = False
        #print "product_contingency: ", product_contingency
        for required_cont in self.contingency_pool.get_required_contingencies():  # step 2 get required contingency, for possible conflicts
        # the change should only be applied if the dependence reaction is reversible like ppi, ipi ...
            #print required_cont.target_reaction
            #print self.reaction_pool.keys()
            #print "required_cont: ", required_cont
            self.is_conflict(product_contingency, required_cont)
            #print self.conflict_found
            if self.is_conflict(product_contingency, required_cont):#self.conflict_found: #and self.reaction_pool[required_cont.target_reaction][0].definition['Reversibility'] == 'reversible':
                    self.conflict_found = True

                #print self.conflict_found
                #if self.conflict_found:
                        # explanation  ^(?!_)\[([^]]+)\] search for any string containing [ ] but not for those with an _ in front
                        # this leads to a search for only [ ] string so domains and sub-domains are excluded
                    if re.search('^(?!_)\[(.*?)\]',required_cont.target_reaction) or re.search('<(.*?)>', required_cont.target_reaction):
                        pass
                    else:
                        #step 4 
                        ## get reaction from reaction_pool
                        ## get reaction to which contingency belongs

                        required_cont_reaction_container = self.reaction_pool[required_cont.target_reaction]  # get reaction object of conflict reaction
                        
                        
                        #print "required_cont_reaction_container.sp_state: ", required_cont_reaction_container.sp_state
                        conflict_state = required_cont_reaction_container.sp_state  # get the state of the conflict reaction
                        print "##############"
                        #print "required_cont_reaction_container.sp_state: ", required_cont_reaction_container.sp_state
                        print "product_complexes: ", product_contingency.target_reaction
                        print "product_contingency.target_reaction: ", product_contingency.target_reaction
                        print "conflict_state: ", conflict_state
                        #print "required_cont.target_reaction: ", required_cont.target_reaction
                        print "conflict product_contingency: ", product_contingency, " required_cont: ", required_cont
                        cont_k = Contingency(target_reaction=product_contingency.target_reaction,ctype="k+",state=conflict_state)
                        print "cont_k: ", cont_k
                        cap = ContingencyApplicator()
                        # apply a k+ contingency to our product contingency target reaction
                        # step 5.1, 5.2, 5.3
                        #this approach also solves problems with adapting the reaction rates
                        cap.apply_on_container(react_container, cont_k)

                        self.apply_contingencies(react_container)
                        #changed_react_container = True #.append(react_container)

        return react_container, conflict_state

    def get_molecules_on_state(self, comp, conflict_state):
        result = []
        for mol in comp.molecules:
            if mol.has_state(conflict_state):
                result.append(mol)
        return result

    def solve_conlict(self, react_container, conflict_state):
        """
        change the conflicted reactions

        The reactions are already cloned by applying k+ contingency on the container
        now we have to change the product complex because we have

            Z + A(Z~U,AssocB!1).B(AssocA!1) -> Z + A(Z~P,AssocB!1).B(AssocA!1)    k1_1

            Z + A(Z~U,AssocB) -> Z + A(Z~P,AssocB)    k1_2

        and want 

            Z + A(Z~U,AssocB!1).B(AssocA!1) -> Z + A(Z~P,AssocB!1) + B(AssocA!1)    k1_1

            Z + A(Z~U,AssocB) -> Z + A(Z~P,AssocB)    k1_2
        """
        from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
        from rxnconcompiler.molecule.molecule import Molecule

        product_contingency = react_container.product_contingency

        #cont = Contingency('C_p+_B_[C]', 'K+', get_state('A--B'))
        cont_x = Contingency(product_contingency.target_reaction, 'x', conflict_state)
        cont_exc = Contingency(product_contingency.target_reaction, '!', conflict_state)

        cap = ContingencyApplicator()

        conflict_state_component_names = [component.name for component in conflict_state.components]
        
        
        for reaction in react_container:
            #cont_reaction_list = [ (str(cont_reaction).split()[0],str(cont_reaction).split()[1]) for cont_reaction in reaction.get_contingencies()]
            cont_reaction_dict = {}
            for cont_reaction in reaction.get_contingencies():
                cont_reaction_dict[str(cont_reaction).split()[1]] = str(cont_reaction).split()[0]

            #print "cont_reaction_list: ", cont_reaction_list
            # print "<<<<<<<<<"
            # print "dir(reaction): ", dir(reaction)
            # print "<<<<<<<<<"
            # print "reaction: ", reaction
            # print "reaction.conditions: ", reaction.conditions
            # print "reaction.definition: ", reaction.definition
            # print "reaction.get_contingencies: ", reaction.get_contingencies()
            # print "reaction.get_domain: ", reaction.get_domain()
            # print "reaction.get_modifier: ", reaction.get_modifier() 
            # print "reaction.get_product_contingency", reaction.get_product_contingency()
            # print "reaction.get_source_contingency",reaction.get_source_contingency()
            # print "reaction.get_sp_state: ", reaction.get_sp_state()
            # #print "reaction.get_specific_contingencies: ", reaction.get_specific_contingencies()
            # #print "reaction.get_substrate_complex: ",reaction.get_substrate_complex()
            # print "reaction.inspect: ", reaction.inspect()
            # print "reaction.left_reactant: ", reaction.left_reactant
            # print "reaction.main_id: ",  reaction.main_id
            # print "reaction.name: ", reaction.name
            # print "reaction.product_complexes: ", reaction.product_complexes
            # print "reaction.rate: ", reaction.rate
            # print "reaction.rid", reaction.rid
            # print "reaction.right_reactant: ", reaction.right_reactant
            # print "reaction.rtype: ", reaction.rtype
            # print "reaction.substrat_complexes", reaction.substrat_complexes
            print "reaction.to_change: ", reaction.to_change
            new_complex = []
            for i, comp in enumerate(reaction.product_complexes):
               #             A                   [A,B]                    len([A])              len([A,B]) if conflict_state True
                conflicted_mol = []
                if str(conflict_state) in cont_reaction_dict and cont_reaction_dict[str(conflict_state)] == "!":
                    print "conflict_state: ", conflict_state
                    print "comp: ", comp
                    print "comp: ", dir(comp)
                    print "comp.molecules: ", comp.molecules
                    print "cont_reaction_list: ", cont_reaction_dict
                    print "reaction.right_reactant: ", reaction.right_reactant

                    print "dir(reaction.right_reactant): ", dir(reaction.right_reactant)
                    print "reaction.right_reactant.has_bond: ", reaction.right_reactant.has_bond(conflict_state)
                    print "reaction.right_reactant.has_state: ", reaction.right_reactant.has_state(conflict_state)
                    print "reaction.left_reactant: ", reaction.left_reactant
                    print "reaction.left_reactant.has_bond: ", reaction.left_reactant.has_bond(conflict_state)
                    print "reaction.left_reactant.has_state: ", reaction.left_reactant.has_state(conflict_state)
                   
                    #print conflict_state.get_molecules_on_state_condition(name=reaction.right_reactant.name)
                    conflicted_mol = self.get_molecules_on_state(comp,conflict_state)
                    
                    if conflicted_mol:
                        for mol in conflicted_mol:
                            new = BiologicalComplex()
                            new.side = 'LR'
                            mol.remove_bond(conflict_state)
                            new.molecules.append(mol)
                            new_complex.append(new)
                    else:
                        new_complex.append(comp)
                #if reaction.right_reactant in comp.molecules and #len(comp.molecules) == len(conflict_state_component_names):
                    #print "##############"
                    #print "required_cont_reaction_container.sp_state: ", required_cont_reaction_container.sp_state
                    #print "product_contingency.target_reaction: ", product_contingency.target_reaction
                    #print "conflict_state: ", conflict_state
                    #print "required_cont.target_reaction: ", required_cont.target_reaction
                    #print "conflict product_contingency: ", product_contingency, " required_cont: ", required_cont
                    
                    #mol_index = comp.molecules.index(reaction.right_reactant)  # get the index of the molecule in the molecule List


                    #mol = comp.molecules[mol_index]

                    # new = BiologicalComplex()
                    # new.side = 'LR'
                    # mol.remove_bond(conflict_state)
                    # new.molecules.append(mol)

                    # new_complex.append(new)
                    # if len(comp.molecules) > 1:
                    #     new = BiologicalComplex()
                    #     new.side = 'LR'
                    #     for molecule in comp.molecules:
                    #         if mol.name != molecule.name and molecule.name in conflict_state_component_names:
                    #             if molecule.has_bond(conflict_state):
                    #                 molecule.remove_bond(conflict_state)
                    #             new.molecules.append(molecule)

                    #     new_complex.append(new)
                else:
                    new_complex.append(comp)
            if new_complex:
                print "new_complex: ", new_complex
                reaction.product_complexes = new_complex

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
        #print 'Contingencies', self.contingency_pool['Ste11_[KD]_P+_Ste7_[AL(T363)]'].children[1].children
        self.war.calculate_missing_states(self.reaction_pool, self.contingency_pool)
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
            if add_contingencies:
                self.apply_contingencies(react_container)

            # single contingency is applied for all reactions. If K+/K- reactions are doubled.
            self.update_reactions()

            react_container, conflict_state = self.find_conflicts_on_mol(react_container)

            for reaction in react_container:
                reaction.run_reaction()

            if self.conflict_found:
                self.solve_conlict(react_container, conflict_state)
                #pass
        #self.find_conflicts()


if __name__ == '__main__':
    main()


