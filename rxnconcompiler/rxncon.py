#!/usr/bin/env python

#KR: code review 2013/12/29
# goals:
# 1. general comments on architecture (OOP and other)
# 2. question of complexes/negated complexes
# 3. everything else I see.
#    (since you have been refactoring a while I'll be more nitpicking)

# TODO: define role of 'super' complexes in the process.
# TODO: define role of domains in the process 

"""
Module rulebased.py translates rxncon input to BNGL

Process steps:
1.   Data parsing.
==================
1.a. Parsing rxncon input into a dictionary 
     that reflects th xls input tables.
     Dictionary contains:
     - reaction_list 
     - contingency_list
     - reaction_definitions
1.b. Parsing data from dictionary into rxnon objects.
     The result is: 
     - ReactionPool containing ReactionContainer objects, 
       each with single Reaction object.
     - ContingencyPool containing root contingency 
       for all reactions with contingencies
     - MoleculesPool containg Molecule objects 
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
     All remaining single Molecul objects are 
     exchanged with complex containing single molecule.
4.   Applying other (non-comlex) contingencies.
===============================================
5.   Running reactions to obtain product complexes.
=======================
6.   Translating reactions into BNGL string.
============================================
6.a. Prepare RulePoll out of RecationPool 
     (same strucrure with RuleContainer and Rule objects) 
6.b. Create strings for all sections using BnglTranslator, and BnglOutput



Classes:
- Compiler:      Input: txt/xls/dict. Output: bngl string.
                 Uses parser, rxncon reactions propagation, 
                 translation of reactions into rules.

- RxnconWarnings: collects all problems in rxncon reactions propagation.

- Rxncon:        Input: rxncon dict. Output: rxncon objects. 
                 out of initial reactions and contingencies produces reactions 
                 similar to bngl rules.

- Bngl:          Input: rxncon objects. Output: bngl string. # redundant

- BioNetGen:     Input: rxncon dict. Output: bngl string.

- main:          defines CLI - Commend Line Interface.
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


class Rxncon:
    """
    Manage the process that leads from the tabular data representation 
    to the object oriented representation of reactions and contingencies.
    The process and objects are bngl-oriented.
    #KR: better 'The process and objects were designed to allow...'
    E.g. they were design to allow flexible and unambiguous 
    translation to bngl string in later stage.

    The end product is a pool of ReactionContainer objects.
    Single ReactionContainer object coresponds to a RuleContainer object.
    Single ReactionContainer has all data neccessary for translation into bngl.

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
                       (captures all posible alternative reactions
                       depending on conditions in which reaction can happen). 
        ContingencyPool - dictionary of all contingencies.
                          rxncon_reaction_str: root contingency 
                          (which contains all contingencies assign to this reaction).
        ComplexPool - dict of all complexes (defined as children-containing contingencies with '<>').
                      '<name>': AlternativeComplexes (which contains BiologicalComplex objects).
        """
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
        Prepares a list of complexes aplicable to a give reaction.

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

        add_translation: when Trues add reanslation reaction for each protein # not available yet.
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

            # single contingency is applied for all reactions. If K+/K- reactions are dubbled.
            self.update_reactions()
            for reaction in react_container:
                reaction.run_reaction()



if __name__ == '__main__':
    main()


