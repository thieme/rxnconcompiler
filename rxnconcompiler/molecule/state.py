#!/usr/bin/env python

"""
Class State        - represents states.
Class StateFactory - produces State object out of sa tring. 
"""

import re
import copy
from domain_factory import DomainFactory
from component import Component

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
        self.__components = []
        self.__state_str = ''
        self.__type = None #: string that keeps information about state type

        self.__sid = None #: valid only for association
        self.__modifier = None #: valid only for covalent modification e.g. Ub, P and Relocalisation.
        self.__not_modifier = None #: valid only for covalent modification (always U) and Relocalisation (substrate localisation).
        self.__loc = False # only for localisation, distinguishes between products and substrates.
        self.__homodimer = False # only for asocciation, when A--A
        self.__domain = None

    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, value):
        self.__domain = value
    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, components):
        assert isinstance(components, list)
        self.__components = components

    @property
    def state_str(self):
        return self.__state_str

    @state_str.setter
    def state_str(self, state_str):
        assert isinstance(state_str, str)
        self.__state_str = state_str

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def sid(self):
        return self.__sid

    @sid.setter
    def sid(self, sid):
        self.__sid = sid

    @property
    def modifier(self):
        return self.__modifier

    @modifier.setter
    def modifier(self, modifier):
        self.__modifier = modifier

    @property
    def not_modifier(self):
        return self.__not_modifier

    @not_modifier.setter
    def not_modifier(self, not_modifier):
        self.__not_modifier = not_modifier

    @property
    def loc(self):
        return self.__loc

    @loc.setter
    def loc(self, loc):
        assert isinstance(loc, bool)
        self.__loc = loc

    @property
    def homodimer(self):
        return self.__homodimer

    @homodimer.setter
    def homodimer(self, homodimer):
        assert isinstance(homodimer, bool)
        self.__homodimer = homodimer

    def __repr__(self):
        str(self)

    def __str__(self):
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
        #if self.components:
        #    if sorted(self.components, key=lambda comp: comp.name) == sorted(other.components, key=lambda comp: comp.name):
        #        return True
        #    else:
        #        return False
        #else:
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
        self.loc = ['Cytoplasm', 'Nucleus',
                    'Vacuole', 'Mitochondria', 'Endosome', 'Extracellular']
        self.df = DomainFactory()

    def get_dash_dash_state_from_string(self, state, state_str, domain, state_id=None, loc_not_modifier=None):
        """
        Complete Association or Intraprotein state from str.
        Returns State object.
        """
        comp = state_str.split('--') 
        compA_name = comp[0].split('_')[0]
        compB_name = comp[1].split('_')[0]

        if domain != None:
            compA_domain = self.df.get_association_domain_from_str(state_str, 'A', domain[0])
            compB_domain = self.df.get_association_domain_from_str(state_str, 'B', domain[1])
        else:
            compA_domain = self.df.get_association_domain_from_str(state_str, 'A')
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
        if state_id:
            comp = Component(comp_name_dom[0], comp_dom, state_id)
        else:
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

    def get_state_from_string(self, state_str, state_id=None, loc_not_modifier=None, domain=None):
        """
        Produces State object from given string.
        When given id (e.g. 1--2) assigns ids to interacting components.
        """
        if type(state_str) != str and type(state_str) != unicode:
            raise TypeError('get_states argument must be a string.')

        state = State()
        state.state_str = state_str
        state.sid = state_id
        #state.domain = domain
        if state_str == '': # Empty state
            state.type = 'Null'
        elif state_str.startswith('<'):
            state.type = 'Boolean' 
        elif '--' in state_str: # Association | Intraprotein
            state = self.get_dash_dash_state_from_string(state, state_str, domain, state_id, loc_not_modifier)
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

    def set_dom_str(self, comp_dom):
        if comp_dom[1] or comp_dom[2]:
            comp_dom = "{0}/{1}{2}".format(comp_dom[0],comp_dom[1],comp_dom[2])
            #state.state_str = '%s_[%s]-{%s}' % (comp_name, comp_dom, state.modifier)
        else:
            comp_dom = comp_dom[0]
        #    state.state_str = '%s_[%s]-{%s}' % (comp_name, comp_dom[0], state.modifier)
        return comp_dom

    def get_state_from_reaction(self, row, reaction, category):
        """
        Returns state object.
        Input: row from xls_tables (dict), reaction object, state type (str).
        """
        state = State()
        state.type = category

        if category == 'Covalent Modification':
            if 'ModifierBoundary' in reaction.definition:
                state.modifier = reaction.definition['ModifierBoundary'] # e.g. P, Ub, truncated
            else:
                state.modifier = reaction.definition['Modifier or Boundary']
            state.not_modifier = 'U' # for Unmodified
            comp_name = row['ComponentB[Name]'].split('_')[0]
            comp_dom = self.df.get_modification_domain_from_dict(row)
            comp = Component(comp_name, comp_dom)
            state.components.append(comp)
            #self.set_state_str_modification(state, comp_name, comp_dom)
            state.state_str = '%s_[%s]-{%s}' % (comp_name, comp_dom.name, state.modifier)

        elif category == 'PT':
            # this is a special case
            # PT has two states that change in the reaction 
            # here the source_state is returned
            if 'ModifierBoundary' in reaction.definition:
                state.modifier = reaction.definition['ModifierBoundary'] # e.g. P, Ub, truncated
            else:
                state.modifier = reaction.definition['Modifier or Boundary'] # e.g. P, Ub, truncated
            state.not_modifier = 'U' # for Unmodified
            comp_name = row['ComponentA[Name]'].split('_')[0]
            comp_dom = self.df.get_modification_domain_from_dict(row, 'A')
            comp = Component(comp_name, comp_dom)
            state.components.append(comp)
            state.state_str = '%s_[%s]-{%s}' % (comp_name, comp_dom.name, state.modifier)

        elif category == 'Intraprotein': 
            l_dsr = self.df.get_intraprotein_domain_from_dict(row, 'A')
            r_dsr = self.df.get_intraprotein_domain_from_dict(row, 'B')
            state_str = '%s_[%s]--[%s]' %(row['ComponentA[Name]'],
                                          l_dsr.name, r_dsr.name)
            state = self.get_state_from_string(state_str, domain=[l_dsr,r_dsr])

        elif category == 'Association': 
            l_dsr = self.df.get_association_domain_from_dict(row, 'A')
            # if l_dsr[1] or l_dsr[2]:
            #     l_dsr = "{0}/{1}{2}".format(l_dsr[0],l_dsr[1],l_dsr[2])
            # else:
            #     l_dsr = l_dsr[0]

            r_dsr = self.df.get_association_domain_from_dict(row, 'B')
            # if r_dsr[1] or r_dsr[2]:
            #     r_dsr = "{0}/{1}{2}".format(r_dsr[0],r_dsr[1],r_dsr[2])
            # else:
            #     r_dsr = r_dsr[0]
            state_str = '%s_[%s]--%s_[%s]' %(row['ComponentA[Name]'],
                                             l_dsr.name, row['ComponentB[Name]'], r_dsr.name)
            state = self.get_state_from_string(state_str,domain=[l_dsr,r_dsr])
        
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


    def get_state(self, row=None, reaction_obj=None, reactionName=None):
        """
        Switch between two functions:
        - get_state_from_reaction
        - get_state_from_string
        depends on arguments.
        """
        if type(row) == dict:
            return self.get_state_from_reaction(row, reaction_obj, reactionName)
        elif type(row) in [str, unicode]:
            return self.get_state_from_string(row, reaction_obj, reactionName)


get_state = StateFactory().get_state
