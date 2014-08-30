#!/usr/bin/env python

"""
Module contingency_factory parses Contingency objects from xls_table
and put them in ContingencyPool. 

ContingencyWrapper   - adaptor for Contingency object. 
                       Anables having one Contingency object with different signs: x or !. 
ContingencyPool      - dict of reaction (key) - Contingency root (value)
ContingencyFactory   - parses contingencies from xls to a tree.
"""

from contingency import Contingency
from rxnconcompiler.molecule.state import get_state, Component


class ContingencyWrapper:
    """
    Adapts Contingency to situation when the ctype will changed.
    One Contingency object can have two 'signs': positive and negative. 
    It is used e.g. when flattening K+ into ! and x
    """

    def __init__(self, contingency, mode='positive'):
        """
        Adapter pattern for ContingencyComponent. 
        """
        self.contingency = contingency
        self.mode = mode

    def __repr__(self):
        return '%s %s' % (self.mode, self.contingency)

    def get_ctype(self):
        """
        Returns contingency type based on
        the mode (positive or negative)
        and the oryginal type. 
        """
        if self.mode == 'positive':
            if self.contingency.ctype in ['!', 'k+', 'and', 'or']:
                return '!'
            elif self.contingency.ctype in ['x', 'k-']:
                return 'x'
        elif self.mode == 'negative':
            if self.contingency.ctype in ['!', 'k+', 'and', 'or']:
                return 'x'
            elif self.contingency.ctype in ['x', 'k-']:
                return '!'

    def get_contingency(self):
        """
        Creates new contingency object with 
        type asign based on mode and old type.
        """
        new_type = self.get_ctype()
        return self.contingency.clone(new_type)


class ContingencyPool(dict):
    """
    ContingencyPool object is a container for all
    contingencies parsed from xls_tables['contingency_list'].
    """
    def __init__(self):
        dict.__init__(self)
        pass

    def get_all_booleans(self):
        """
        Returns a list of all boolean contingencies.
        """
        result =  []
        for root in self.values():
            leafs = root.get_children()
            for leaf in leafs:
                if leaf.state.type == 'Boolean':
                    result.append(leaf)
        return result

    def get_top_booleans(self):
        """
        Returns a list of boolean contingencies 
        that are direct children of the root contingency.
        """
        result =  []
        for root in self.values():
            for leaf in root.children:
                if leaf.state.type == 'Boolean':
                    result.append(leaf)
        return result

    def remove_contingency(self, cont):
        """
        Removes contingency but only if it is in the top level
        (directly under the root).
        """
        for root in self.values():
            for child in root.children:
                if cont == child:
                    root.children.remove(cont)

    def get_required_states(self):
        """
        Allows to obtein states that need to be present in the system
        to allow contingencies (the context) to be fulfilled.
        (States that should be produced be reactions).

        @return: all states from x, !, and K contingencies except input states
        @rtype:  set

        @todo:   what about ! <OR> are all states required? 
        """
        result = [] 
        for root in self.values():
            children = root.get_leafs()
            for cont in children:
                if cont.ctype in ['!', 'k+', 'k-', 'x'] or cont.inherited_ctype in ['!', 'k+', 'k-', 'x']:
                    if cont.state.type in ['Association', 'Covalent Modification', 'Relocalisation']:
                        result.append(cont.state)
        return set(result)

    def get_kind_contingencies(self, kind):
        """
        Returns all contingencies with Covalent Modification state.

        Used when updating contingencies.
        """
        result = []
        for root in self.values():
            children = root.get_leafs()
            for cont in children:
                if cont.ctype in ['!', 'k+', 'k-'] or cont.inherited_ctype in ['!', 'k+', 'k-']:
                    if cont.state.type in [kind]:
                        result.append(cont)
        return set(result)

    def get_modification_contingencies(self):
        """
        Returns all contingencies with Covalent Modification state.

        Used when updating contingencies.
        """
        return self.get_kind_contingencies("Covalent Modification")

    def get_relocalisation_contingencies(self):
        """
        Returns all contingencies with Relocalisation state.

        Used when updating contingencies.
        """
        return self.get_kind_contingencies("Relocalisation")


class ContingencyFactory(dict):
    """
    Parses all contingencies from xls_tables['contingency_list'].

    E.g.
    A_ppi_B; ! A--C
    A_ppi_B; ! A--D
    A_ppi_B; K+ <MM> 
    <MM>; AND B-{P} 
    <MM>; AND <MM2>
    <MM2>; OR C-{P}
    <MM2>; OR D-{P}

    A_ppi_B : root
    root.children ---> [! A--C, ! A--D, K+ <MM>]
    """
    def __init__(self, xls_tables):
        dict.__init__(self)
        self.xls_tables = xls_tables
        self.pool = ContingencyPool()
        
    def parse_contingencies(self):
        """
        Returns a ContingencyPool object.
        It is a dict that holds all top nodes contingencies of a reaction.
        Key - reaction string. Value - list of contingencies. 
        """
        # Could be recurent because of boolean nodes
        # (we cannot add child if the parent is not there)
        # but then we have risk that we have infinit loop 
        # if the parent does not exist.
        # For now we have parse_later but it may not be sufficient in all cases.
        parse_later = []
        complexes = []

        for row in self.xls_tables['contingency_list']:      
            result = self.parse_contingency(row)
            if result and result[0] == 'no parent':
                parse_later.append(result[1])
            elif result and result[0] == 'complex':
                complexes.append(result[1])
        # children for booleans for which there was no parent in first round
        for row in parse_later:
            self.parse_contingency(row)

        #self.parse_complexes(complexes)
        return self.pool

    def parse_contingency(self, row):
        """
        Parses single contingency from row.
        If it os not possible - parent is not yet there returns row.
        """
        reaction = row['Target']
        ctype = row['Contingency']
        if '--' in ctype:
            sid = ctype 
        else:
            sid = None
        state = get_state(row['Modifier'], sid)
        cont = self.create_contingency(reaction, ctype, state)
        if not reaction.startswith('<'):
            self.pool.setdefault(reaction, Contingency(reaction))        
            self.pool[reaction].add_child(cont)
        elif reaction.startswith('<'):
            parents  = self.find_parent(cont)
            if not parents:
                return 'no parent', row
            for parent in parents:
                if cont not in parent.children:
                    parent.add_child(cont)

    def get_components_from_reaction(self, reaction_string):
        """
        Gets components from a reaction string.
        E.g. 
        A_ppi_B
        A_[domain]_P+_C
        A_ppi_X_[domain]
        """
        # TODO: does not belong here - should be done in a different place.
        react = reaction_string.split('_')
        component1 = Component(react[0])
        if react[1].startswith('['):
            component2 = Component(react[3])
        else:
            component2 = Component(react[2])
        return component1, component2

    def find_parent(self, contingency):
        """
        Returns a parent (BooleanContingency object)
        for given contingency.
        """
        bools = []
        for reaction in self.pool:
            bools += self.get_booleans(self.pool[reaction].children)
        parents = []
        for cont in bools:
            if cont.is_parent(contingency):
                parents.append(cont)
        if parents:
            return parents 
        return None   

    def get_booleans(self, cont_list):
        """
        Returns a list of all BooleanContingencies 
        from given list of contingencies.
        It uses recurrence to check 
        whether there are any booleans among children 
        of the boolean that has been already found.
        """
        bools = []
        for cont in cont_list:
            if cont.state.type == 'Boolean':
                bools.append(cont)
                if cont.children:
                    bools += self.get_booleans(cont.children)
        return bools

    def create_contingency(self, target_reaction, ctype, state):
        """
        Creates Contingency objects.
        """
        if str(state).startswith('['):
            state.state_str.replace('[','xXx').replace(']','xXx')
        else:
            state.state_str.replace('[','').replace(']','')
        return Contingency(target_reaction, ctype, state)

