#!/usr/bin/env python

"""
Module reaction_factory.py 
produces Reaction objects and puts them in ReactionPool

Class ReactionFactory   - generates ReactionPool and MoleculePool 
                          out of reactions list from xls_table.
                        
"""

from reaction import Reaction, Modification, Interaction, \
                     SyntDeg, Relocalisation
from reaction_container import ReactionContainer, ReactionPool
from rate import Rate 
from definitions.definitions import ReactionDefinitions
from definitions.default_definition import DEFAULT_DEFINITION
from molecule.molecule import Molecule, MoleculePool
from molecule.state import get_state


ENZYME = 'Enzyme'  # universal name for proteins that perform covalent modification reactions.
TRANSPORTER = 'Transporter'  # universal name for proteins that are on the left side of relocalisation reaction. 

class ReactionFactoryFromDict:
    """
    Builds ReactionPool and MoleculePool from the xls_tables dict. 
    """
    def __init__(self, xls_tables):
        self.definitions = ReactionDefinitions(xls_tables)
        self.reaction_pool = ReactionPool()
        self.molecule_pool = MoleculePool()
        self.parse_reactions(xls_tables)

    def parse_reactions(self, xls_tables):
        """
        Go through all rows in xls_tables['reaction_list']
        and cretes single ReactionContainer object or each row.
        Adds ReactionContainer to ReactionPool.
        Adds left and right reactant to  MoleculePool.
        """
        for row_id, row in enumerate(xls_tables['reaction_list']):
            container = ReactionContainer()
            container.name = row['Reaction[Full]']
            container.rid = row_id + 1
            container.rtype = row['ReactionType']

            reaction = self.get_reaction_object(row) 
            reaction.rid = row_id + 1
            reaction.rate = Rate(reaction)

            container.add_reaction(reaction)
            self.reaction_pool[container.name] = container
            self.molecule_pool.append(reaction.left_reactant)
            self.molecule_pool.append(reaction.right_reactant)
           
    def add_reactants(self, reaction, row):
        """
        Adds left and right reactant as Molecule objects. 
        For ipi there is only single object as left and right reactant.
        """
        if reaction.rtype == 'ipi':
            mol = Molecule(row['ComponentA[Name]'])
            mol.is_reactant = True
            reaction.left_reactant = mol
            reaction.right_reactant = mol

        else:
            reaction.left_reactant = Molecule(row['ComponentA[Name]'])
            reaction.left_reactant.is_reactant = True
            reaction.right_reactant = Molecule(row['ComponentB[Name]'])
            reaction.right_reactant.is_reactant = True

    def get_preliminary_reaction(self, row):
        """ 
        Gets info common for all reactions into reaction object.

        @type row:  dict
        @param row: row from xls_tables['reaction_list']
        @rtype: specific Reaction object
        """
        r_type = row['ReactionType'].lower()

        categories_dict = self.definitions.categories_dict
        if r_type in categories_dict['Covalent Modification']:
            reaction = Modification()
        elif r_type in categories_dict['Association']:
            reaction = Interaction()
        elif r_type in categories_dict['Synthesis/Degradation']:
            reaction = SyntDeg()
        elif r_type in categories_dict['Relocalisation']:
            reaction = Relocalisation()
        

        reaction.rtype = r_type
        reaction.name = row['Reaction[Full]']
        if self.definitions.has_key(r_type):
            reaction.definition = self.definitions[r_type]
        else: 
            raise TypeError('No reactio type %s.') % r_type

        self.add_reactants(reaction,row)
        return reaction

    def get_reaction_object(self, row):
        """
        Takes a row and returns reaction object.
        """
        r_type = row['ReactionType'].lower()
        categories_dict = self.definitions.categories_dict
        reaction = self.get_preliminary_reaction(row)

        if r_type in categories_dict['Covalent Modification']:
            state = get_state(row, reaction, 'Covalent Modification')
            if r_type == 'pt': # if subtype == Trnas
                reaction.right_reactant.add_modification_site(state)
                reaction.left_reactant.add_modification(state)
            elif '-' in r_type or r_type in ['gap']:
                reaction.right_reactant.add_modification(state)
            else:
                reaction.right_reactant.add_modification_site(state)
            reaction.to_change = state

        elif r_type in categories_dict['Association']:
            # ipi is destinctive state: it is A_[a]--[b]
            # where both domains are in the same protein.
            if r_type == 'ipi':
                state = get_state(row, reaction, 'Intraprotein')
                reaction.left_reactant.add_binding_site(state)
                reaction.to_change = state
            else:
                state = get_state(row, reaction, 'Association')
                #if reaction.rtype == 'Association':
                #    print state
                reaction.left_reactant.add_binding_site(state)
                reaction.right_reactant.add_binding_site(state)
                reaction.to_change = state

        elif r_type in categories_dict['Synthesis/Degradation']:
            pass

        elif r_type in categories_dict['Relocalisation']:
            state = get_state(row, reaction, 'Relocalisation')
            reaction.to_change = state
            reaction.right_reactant.localisation = state
        else:
            reaction = Reaction()

        reaction.definition = self.definitions[r_type]
        return reaction


class ReactionFactoryFromList:
    """Builds ReactionPool and MoleculePool from a list of states."""
    def __init__(self, states_list):
        self.definitions = ReactionDefinitions({'reaction_definition': DEFAULT_DEFINITION})
        self.reaction_pool = ReactionPool()
        self.molecule_pool = MoleculePool()
        self.parse_reactions(states_list)

    def get_reaction_type(self, state):
        """
        Returns string that describes reaction type.
        E.g. 'ppi', 'p+'
        """
        if state.type == 'Association':
            return 'ppi'
        elif state.type == 'Intraprotein':
            return 'ipi'
        elif state.type == 'Covalent Modification':
            # TODO: find out more elegant way
            if state.modifier == 'Ub':
                return 'ub+'
            elif state.modifier == 'Truncated':
                return 'cut'
            else:
                return 'p+'
        elif state.type == 'Relocalisation':
            return 'mimp' # TODO: this won't be working add function for that.

    def get_reaction_str(self, state):
        """
        Creates reaction string e.g. A_[n]_ppi_B_[c] from state.
        """
        rtype = self.get_reaction_type(state)
        if state.type == 'Association':
            return '%s_%s_%s' % (str(state.components[0]), rtype, str(state.components[1]))
        elif state.type == 'Intraprotein':
            return '%s_%s_[%s]' % (str(state.components[0]), rtype, state.components[0].second_domain)
        elif state.type == 'Covalent Modification':
            return '%s_%s_%s' % (ENZYME, rtype, str(state.components[0]))
        elif state.type == 'Relocalisation':
            return '%s_%s_%s' % (TRANSPORTER, rtype, str(state.components[0]))


    def add_reactants(self, reaction, state):
        """
        Adds left and right reactant as Molecule objects. 
        For ipi there is only single object as left and right reactant.
        """
        if state.type == 'Association':
            reaction.left_reactant = Molecule(state.components[0].name)
            reaction.left_reactant.is_reactant = True
            reaction.right_reactant = Molecule(state.components[1].name)
            reaction.right_reactant.is_reactant = True

        elif state.type == 'Intraprotein':
            mol = Molecule(state.components[0].name)
            mol.is_reactant = True
            reaction.left_reactant = mol
            reaction.right_reactant = mol

        elif state.type == 'Covalent Modification':
            reaction.left_reactant = Molecule(ENZYME)
            reaction.left_reactant.is_reactant = True
            reaction.right_reactant = Molecule(state.components[0].name)
            reaction.right_reactant.is_reactant = True
           
        elif state.type == 'Relocalisation':
            reaction.left_reactant = Molecule(TRANSPORTER)
            reaction.left_reactant.is_reactant = True
            reaction.right_reactant = Molecule(state.components[0].name)
            reaction.right_reactant.is_reactant = True

    def get_preliminary_reaction(self, state):
        """ 
        Gets info common for all reactions into reaction object.
        """
        if state.type == 'Association':
            reaction = Interaction()
        elif state.type == 'Intraprotein':
            reaction = Interaction()
        elif state.type == 'Covalent Modification':
            reaction = Modification()
        elif state.type == 'Relocalisation':
            reaction = Relocalisation()
        reaction.rtype = self.get_reaction_type(state)
        reaction.name = self.get_reaction_str(state)
        if self.definitions.has_key(reaction.rtype):
            reaction.definition = self.definitions[reaction.rtype]
        else: 
            raise TypeError('No reactio type %s.') % reaction.rtype
        self.add_reactants(reaction, state)
        return reaction

    def get_reaction_object(self, state):
        """
        Takes a row and returns reaction object.
        """
        r_type = self.get_reaction_type(state).lower()
        #categories_dict = self.definitions.categories_dict
        reaction = self.get_preliminary_reaction(state)
        if state.type == 'Association':
            reaction.left_reactant.add_binding_site(state)
            reaction.right_reactant.add_binding_site(state)
        elif state.type == 'Intraprotein':
            reaction.left_reactant.add_binding_site(state)
        elif state.type == 'Covalent Modification':
            reaction.right_reactant.add_modification_site(state)
        elif state.type == 'Relocalisation':
            reaction.right_reactant.localisation = state
        reaction.to_change = state
        reaction.definition = self.definitions[r_type]
        return reaction

    def parse_reactions(self, states_list):
        """
        Go through all states in states_list
        and cretes single ReactionContainer object for each state.
        Adds ReactionContainer to ReactionPool.
        Adds left and right reactant to  MoleculePool.
        """
        for state_id, state in enumerate(states_list):
            container = ReactionContainer()
            container.name = self.get_reaction_str(state)
            container.rid = state_id + 1
            container.rtype = self.get_reaction_type(state)

            reaction = self.get_reaction_object(state) 
            reaction.rid = state_id + 1
            reaction.rate = Rate(reaction)

            container.add_reaction(reaction)
            self.reaction_pool[container.name] = container
            self.molecule_pool.append(reaction.left_reactant)
            self.molecule_pool.append(reaction.right_reactant)


class ReactionFactory:
    """
    Builds ReactionPool and MoleculePool.
    Uses either ReactionFactoryFromDict or ReactionFactoryFromList 
    ReactionFactoryFromDict - classical parsing of input .
    ReactionFactoryFromList - for creating ractions for missing states.
    """   
    def __init__(self, imp):
        """
        Imput: xls_tables (dict) or list of states.
        """
        self.parse_reactions(imp)

    def parse_reactions(self, imp):
        """
        Checks type of input and uses right factory.
        """
        if type(imp) == dict:
            rf = ReactionFactoryFromDict(imp)
        elif type(imp) == list:
            rf = ReactionFactoryFromList(imp)
        self.definitions = rf.definitions
        self.reaction_pool = rf.reaction_pool
        self.molecule_pool = rf.molecule_pool