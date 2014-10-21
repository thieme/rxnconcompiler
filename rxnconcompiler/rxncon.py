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
        self.conflict_found = False
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
        
    def solve_conflicts(self, reaction_containter, required_cont_reaction_container, NEW_STATE, product_contingencyTarget_reaction):
        # MR: add documentation.
        # MR: it is long, you can try to divide it into smaller functions.
        for reaction in reaction_containter:  # iterate over all reactions we want to change

            reaction_clone = reaction.clone()  # clone the reaction (get the second reaction) step 5.1
        #     # create contingencies for applying on the reaction we want to change
        #     # have to initialize a contingency 5.2
            cont_x = Contingency(target_reaction=product_contingencyTarget_reaction,ctype="x",state=NEW_STATE)
            cont_exclamation = Contingency(target_reaction=product_contingencyTarget_reaction,ctype="!",state=NEW_STATE)

            # step 5.2
            ## 5.2.1
            # apply x contingency on right right of substrate 
            for comp in reaction.substrat_complexes: # iterate over the different substrate complexes
                if reaction.right_reactant in comp.molecules: # find the right reactant complex
                    ContingencyApplicator().apply_on_complex(comp,cont_x) # apply new contingency to this complex
            ## 5.2.2
            # apply x contingency on right complex of product 
            for comp in reaction.product_complexes:
                if reaction.right_reactant in comp.molecules:
                    ContingencyApplicator().apply_on_complex(comp,cont_x)

            #5.3 change cloned reaction
            #5.3.1 change cloned reaction substrate side
            for i, component in enumerate(reaction_clone.substrat_complexes):
                    if reaction_clone.right_reactant in component.molecules: # find the right reactant complex in molecules of component
                        mol_index = component.molecules.index(reaction_clone.right_reactant)  # get the index of the molecule in the molecule List
                        mol = component.molecules[mol_index] # get the molecule
                        # check in NEW_STATE if we have to add additional molecules
                        for reaction2 in required_cont_reaction_container:
                            for add_comp in reaction2.product_complexes:
                                for add_mol in add_comp.molecules:
                                    if mol.name != add_mol.name:
                                        # replace the component by it's complex so instead of A(P) we get A(P,AssocB!1).B(AssocA!1) on substrate side
                                        reaction_clone.substrat_complexes[i] = add_comp 
                        ContingencyApplicator().apply_on_complex(component, cont_exclamation)

            #5.3.2 change cloned reaction product side
            to_add = []
            for component in reaction_clone.product_complexes:  # iterating over the components of product complex
                if reaction_clone.right_reactant in component.molecules:  # if the component molecule list contains the right handed reactant
                    mol_index = component.molecules.index(reaction_clone.right_reactant)  # get the index of the molecule in the molecule List
                    mol = component.molecules[mol_index] # get the molecule
                    # check in NEW_STATE if we have to add additional molecules
                    for reaction2 in required_cont_reaction_container:
                        for add_comp in reaction2.substrat_complexes:
                            if mol.name != add_comp.molecules[0].name:
                                # append the molecule directly to the product complex list to generate a separated molecule 
                                # we get X + A(Z~U,AssocB) + B(AssocA) on the product side
                                #reaction_clone.product_complexes.append(add_comp) #
                                to_add.append(add_comp)
                    ContingencyApplicator().apply_on_complex(component,cont_x)
            reaction_clone.product_complexes.extend(to_add)
        reaction_containter.add_reaction(reaction_clone)
        self.reaction_pool[reaction_containter.name] = reaction_containter
        

    def find_conflicts(self):
        """
        check if there are conflicts between generated states and required contingencies
        MR: Would be nice to have some example in documentation.
        """
        # MR:
        # Be careful with function responsibility:
        # for me it is misleading that function called find_conflicts 
        # also solve them.
        # Be careful with function responsibility:
        # I would call both functions in the run_process - find and solve and have some self.conflicts
        # (I see WCM influence here ;-D)
        # Perhaps it will be easier to start some ConflictSolver,
        # as you manipulate data at the end of run_process anyway? 

        from rxnconcompiler.molecule.state import get_state
        import re
        print "self.reaction_pool: ", self.reaction_pool
        #print "self.contingency_pool.get_required_contingencies(): ", self.contingency_pool.get_required_contingencies()
        for product_contingency in self.reaction_pool.get_product_contingencies():  # step 1 get product contingencies if the reaction we have to change
            #if str(product_contingency)[0] == "x": # check for absolute inhibitory reactions
            # the change should only be applied if the dependence reaction is reversible like ppi, ipi ...
            if self.reaction_pool[product_contingency.target_reaction][0].definition['Reversibility'] == 'reversible':
                for required_cont in self.contingency_pool.get_required_contingencies():  # step 2 get required contingency, for possible conflicts
                    # MR: this line is a long one :-)
                    #     perhaps it would be a good idea to have a function is_conflict() 
                    #     which would do this job.
                    if (str(required_cont.state)) == str(product_contingency.state) and (str(required_cont.ctype) != str(product_contingency.ctype) and str(required_cont.ctype) not in ["and", "or", "0"]) and (required_cont.state,product_contingency.state) not in self.solved_conflicts:  # step 3 check for conflicts
                        print str(required_cont.ctype)
                        self.conflict_found = True
                        #step 4 
                        ## get reaction from reaction_pool
                        ## get reaction to which contingency belongs
                        # explanation  ^(?!_)\[([^]]+)\] search for any string containing [ ] but not for those with an _ in front
                        # this leads to a search for only [ ] string so domains and sub-domains are excluded
                        if re.search('^(?!_)\[(.*?)\]',required_cont.target_reaction) or re.search('<(.*?)>', required_cont.target_reaction):
                            #print "product_contingency.target_reaction: ", product_contingency.target_reaction
                            ##print "required_cont.target_reaction: ", required_cont.target_reaction
                            #print "Conflict: ", "required_cont: ", required_cont, " ",  "product_contingency: ", product_contingency
                            pass
                            #self.solved_conflicts.append((required_cont.state,product_contingency.state))
                        else:
                            print "product_contingency.target_reaction: ", product_contingency.target_reaction
                            print "required_cont.target_reaction: ", required_cont.target_reaction
                            print "Conflict: ", "required_cont: ", required_cont, " ",  "product_contingency: ", product_contingency
                            reaction_containter = self.reaction_pool[product_contingency.target_reaction]  # get reaction object of reaction we want to change
                            required_cont_reaction_container = self.reaction_pool[required_cont.target_reaction]  # get reaction object of conflict reaction
                            # MR: big letters are usually used for global variables,
                            #     perhaps something more descriptive like conflict_state
                            NEW_STATE = required_cont_reaction_container.sp_state  # get the state of the conflict reaction

                            self.solve_conflicts(reaction_containter, required_cont_reaction_container, NEW_STATE, product_contingency.target_reaction)
                            self.solved_conflicts.append((required_cont.state,product_contingency.state))
        #if self.conflict_found:
         #   self.conflict_found = False
         #   self.find_conflicts()

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
            for reaction in react_container:
                reaction.run_reaction()
        self.find_conflicts()


if __name__ == '__main__':
    main()


