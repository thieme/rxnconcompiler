#!/usr/bin/env python

"""
Class Component    - cleaps information about name, domain and id.
Class State        - represents states.
Class StateFactory - produces State object out of sa tring. 
"""

import re
import copy
from domain_factory import DomainFactory

class Component:
    """
    Component object keeps informations about name, domain and id.
    It is used in State. 
    """
    def __init__(self, name, domain=None, cid=None):
        self.name = name.strip()
        self.domain = domain
        if self.domain:
            self.domain = self.domain.strip()
        self.cid = cid
        self.second_domain = None  # for ipi states

    def __repr__(self):
        #return str((self.name , self.domain, self.cid))
        if self.second_domain:
            return '%s_[%s]_[%s]' % (self.name, self.domain, self.second_domain)
        elif self.domain:
            return '%s_[%s]' % (self.name, self.domain)
        return self.name 

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if self.cid and other.cid and self.cid != other.cid:
            return False
        return True

    def __cmp__(self, other):
        if self.name < other.name:  # compare name value (should be unique)
            return -1
        elif self.name > other.name:
            return 1
        elif self.name == other.name and self.cid and other.cid:
            if self.cid < other.cid:
                return -1
            elif self.cid > other.cid:
                return 1
        else: return 0        

    def exact_compare(self, other):
        """
        Checks not only name (__cmp__) but also domain.
        """
        if not self == other:
            return False
        if self.domain != other.domain: 
            return False
        if self.second_domain != other.second_domain:
            return False
        return True

class State:
    """
    State object keeps information about state of 0, 1 or 2 components.
    E.g. 
    - two components might interact 
    - one component might be covalently modified
    - it can be also input or name of a boolean

    Types of states: 
    - Null
    - Boolean
    - Association
    - Intraprotein  # intraprotein association  
    - Covalent Modification
    - Relocalisation
    - Input
    - Polymer
    - Component
    """
    def __init__(self):
        self.components = []
        self.state_str = ''
        self.type = None #: string that keeps information about state type

        self.sid = None #: valid only for association
        self.modifier = None #: valid only for covalent modification e.g. Ub, P and Relocalisation.
        self.not_modifier = None #: valid only for covalent modification (always U) and Relocalisation (substrate localisation).
        self.loc = False # only for localisation, distinguishes between products and substrates.
        self.homodimer = False # only for asocciation, when A--A
       
    def __repr__(self):
        if self.type == 'Intraprotein':
            return '%s_[%s]--[%s]' % (self.components[0].name, \
                self.components[0].domain, self.components[0].second_domain)
        if self.type == 'Association':
            return '%s--%s' % (str(self.components[0]), str(self.components[1]))
        if self.type in ['Covalent Modification', 'Relocalisation']:
            return '%s-{%s}' % (str(self.components[0]), self.modifier)
        return self.state_str

    def __eq__(self, other):
        """
        Compares states only in respect to component names.
        To include domains in comparison use hash function.
        """
        if self.components:
            if sorted(self.components, key=lambda comp: comp.name) == sorted(other.components, key=lambda comp: comp.name):
                return True
            else:
                return False
        else:
            if self.state_str == other.state_str:
                return True
            else:
                return False

    def __hash__(self):
        """
        Enables using states as keys in a dictionary
        and having sets of states.
        """
        #return (str(self) + str(self.sid)).__hash__()
        return (str(self)).__hash__()

    def has_component(self, component):
        """
        Checks wchether stat contains a component.
        @type component:  Component
        @param component: component to check.
        @rtype:  True / False
        """
        if component in self.components:
            return True
        return False

    def get_component(self, name, side = 'L'):
        """
        Returns component when given a name.
        If state is Assosiation and homodimer
        returns component based on side:
        L - left component
        R - right component
        """
        if self.homodimer:
            if side == 'L':
                return self.components[0]
            elif side == 'R':
                return self.components[1]
        for comp in self.components:
            if comp.name == name:
                return comp

    def get_partner(self, component):
        """
        Valid only for association states.
        Given a component returns second one.
        """
        if not self.type == 'Association':
            return None
        if component == self.components[0]:
            return self.components[1]
        elif component == self.components[1]:
            return self.components[0]
        else: 
            return None

    def clone(self):
        """
        Creates new identical instance of State.
        """
        new = State()
        new.components = copy.deepcopy(self.components)
        new.state_str = self.state_str
        new.type = self.type
        new.sid = copy.deepcopy(self.sid)
        new.modifier = self.modifier
        new.not_modifier = self.not_modifier
        return new

    def has_bd_domain(self):
        """
        Checks whether 'bd' is a name of any domain in the state.
        """
        for component in self.components:
            if component.domain == 'bd':
                return True
        return False


class StateFactory:
    """
    StateFactory object producess State object based on a string.
    """
    def __init__(self):
        self.loc = ['Cytoplasm', 'Nucleus', \
        'Vacuole', 'Mitochondria', 'Endosome', 'Extracellular']
        self.df = DomainFactory()

    def get_dash_dash_state_from_string(self, state, state_str, state_id=None, loc_not_modifier=None):
        """
        Complete Association or Intraprotein state from str.
        Returns State object.
        """
        comp = state_str.split('--') 
        compA_name = comp[0].split('_')[0]
        compA_domain = self.df.get_association_domain_from_str(state_str, 'A') 
        compB_name = comp[1].split('_')[0]
        compB_domain = self.df.get_association_domain_from_str(state_str, 'B')
        if compB_name.startswith('['):
            state.type = 'Intraprotein' # A_[a]--[b]
            comp_object = Component(compA_name, compA_domain)
            comp_object.second_domain = re.sub('[\[\]]', '', compB_name)
            state.components = [comp_object]
        else:
            state.type = 'Association' # A--B
            if state_id:
                idA = state_id.split('--')[0]
                idB = state_id.split('--')[1]
            else:
                idA = None
                idB = None
            compA_object = Component(compA_name, compA_domain, idA)
            compB_object = Component(compB_name, compB_domain, idB)
            state.components = [compA_object, compB_object]
            if compA_name == compB_name:
                state.homodimer = True
        return state

    def get_dash_state_from_string(self, state, state_str, state_id=None, loc_not_modifier=None):
        """
        Complete Modification or Relocalisation state from str.
        Returns State object.
        """
        comp_name_dom = state_str.split('-{')[0].split('_')
        comp_dom = self.df.get_modification_domain_from_str(state_str)
        comp = Component(comp_name_dom[0], comp_dom)
        state.components.append(comp)   
        modifier = state_str.split('-{')[1].replace('}','')
        compartments = [compartment.lower() for compartment in self.loc]
        if modifier.lower() in compartments:
            state.type = 'Relocalisation'
            state.components[0].domain = self.df.get_localisation_domain()
            state.modifier = modifier
            state.not_modifier = loc_not_modifier
        else:
            state.type = 'Covalent Modification'
            state.modifier = state_str.split('-{')[1].replace('}','') # e.g. P, Ub, truncated
            state.not_modifier = 'U' # for Unmodified
        return state

    def get_state_from_string(self, state_str, state_id=None, loc_not_modifier=None):
        """
        Produces State object from given string.
        When given id (e.g. 1--2) assigns ids to interacting components.
        """
        if type(state_str) != str and type(state_str) != unicode:
            raise TypeError('get_states argument must be a string.')

        state = State()
        state.state_str = state_str
        state.sid = state_id
        if state_str == '': # Empty state
            state.type = 'Null'
        elif state_str.startswith('<'):
            state.type = 'Boolean' 
        elif '--' in state_str: # Association | Intraprotein
            state = self.get_dash_dash_state_from_string(state, state_str, state_id, loc_not_modifier)
        elif '-' in state_str: # Covalent Modification | Relocalisation
            state = self.get_dash_state_from_string(state, state_str, state_id, loc_not_modifier)
        elif '*' in state_str: # Polymerisation
            state.components = [Component(state_str.split('*')[0])]
            state.type = 'Polymer'
        elif state_str.startswith('['): #Input
            state.type = 'Input'
            state.components = [Component(state_str.replace('[','').replace(']',''))]
        else: # single component
            state.components = [Component(state_str)]
            state.type = 'Component'
        return state

    def get_state_from_reaction(self, row, reaction, category):
        """
        Returns state object.
        Input: row from xls_tables (dict), reaction object, state type (str).
        """
        state = State()
        state.type = category

        if category == 'Covalent Modification':
            state.modifier = reaction.definition['Modifier or Boundary'] # e.g. P, Ub, truncated
            state.not_modifier = 'U' # for Unmodified
            comp_name = row['ComponentB[Name]'].split('_')[0]
            comp_dom = self.df.get_modification_domain_from_dict(row, reaction)
            comp = Component(comp_name, comp_dom)
            state.components.append(comp)
            state.state_str = '%s_[%s]-{%s}' % (comp_name, comp_dom, state.modifier)

        elif category == 'Intraprotein': 
            l_dsr = self.df.get_intraprotein_domain_from_dict(row, 'A')
            r_dsr = self.df.get_intraprotein_domain_from_dict(row, 'B')
            state_str = '%s_[%s]--[%s]' %(row['ComponentA[Name]'], \
                l_dsr, r_dsr)
            state = self.get_state_from_string(state_str)

        elif category == 'Association': 
            l_dsr = self.df.get_association_domain_from_dict(row, 'A')
            r_dsr = self.df.get_association_domain_from_dict(row, 'B')        
            state_str = '%s_[%s]--%s_[%s]' %(row['ComponentA[Name]'], \
                l_dsr, row['ComponentB[Name]'], r_dsr) 
            state = self.get_state_from_string(state_str)
        
        elif category == 'Relocalisation':
            comp_name = row['ComponentB[Name]'].split('_')[0]
            dom = self.df.get_localisation_domain()
            state.components.append(Component(comp_name, dom))
            if row.has_key('ProductState[Modification]'): 
                state.modifier = re.sub('[-{}]', '', row['ProductState[Modification]'])
                state.not_modifier = re.sub('[-{}]', '', row['SourceState[Modification]'])
            elif row.has_key('ProductState'):
                state.modifier = row['ProductState'].split('-{')[-1].replace('}','')
                state.not_modifier = row['SourceState'].split('-{')[-1].replace('}','')
            state.state_str = '%s_[%s]-{%s}' % (comp_name, dom, state.modifier)
        return state


    def get_state(self, first_arg=None, sec_arg=None, third_arg=None):
        """
        Switch between two functions:
        - get_state_from_reaction
        - get_state_from_string
        depends on arguments.
        """
        if type(first_arg) == dict:
            return self.get_state_from_reaction(first_arg, sec_arg, third_arg)
        elif type(first_arg) in [str, unicode]:
            return self.get_state_from_string(first_arg, sec_arg, third_arg)


get_state = StateFactory().get_state
