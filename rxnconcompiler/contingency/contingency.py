#!/usr/bin/env python

"""
Module contingency contains data structure for rxncon contingencies.
Composite Design Pattern.
"""

import copy

class Contingency:
    """
    Contingency object is a data structure for rxncon contingency.
    It contain information about target reaction, type of contingency,
    and state that influences the target reaction. 
    Every contingency may have children.
    """
    def __init__(self, target_reaction=None, ctype=None, state=None):
        """
        @param target_reaction: A_ppi_B, <Bool>
        @type target_reaction: string
        @param ctype: !, x, k+, k-, 0, and, or, 1--2
                    (normal: !, x, k+, k-, 0
                     boolean: and, or
                     complexes with defined geometry: 1--2)
        @type ctype: string
        @param state: A--B, A-{P}, B-{Mito}, <Bool>
        @type state: State object

        @ivar children: each contingency (complex or boolean)
                        may contain children - other contingencies.
        @type children: list
        @ivar inharited_ctype: keeps normal ctype for contingencies 
                               with boolean or complex ctype. It is 
                               ctype of a parent.
        @type inharited_ctype: string
        """
        self.target_reaction = target_reaction
        self.ctype = str(ctype).lower() if ctype else None
        self.state = state
        self.children = []
        self.inherited_ctype = None


    def __repr__(self):
        """Representation of contingency: ctype state, e.g. ! A--B"""
        return "%s %s" % (self.ctype, self.state)

    def __eq__(self, other):
        """
        Two ContingencyComponent objests are eqal when 
        target reaction, ctype and states are eqal.
        """
        if self.target_reaction == other.target_reaction:
            if self.ctype == other.ctype:
                if self.state == other.state: 
                    return True
        return False

    def __hash__(self):
        """Anables set operstion."""
        return str(self).__hash__()

    @property 
    def has_children(self):
        """"""
        if len(self.children) == 0:
            return False
        return True

    def count_leafs(self, node = None):
        """
        Counts all leaf contingencies.

                <MM>
                /  \
            <MM2>   D-{P}
            /   \
        E-{P}  F-{P}

        <MM> has 3 leafs
        """
        if not node:
            node = self
        result = 0
        if not node.has_children:
            return 0 
        for child in node.children:
            if not child.has_children:
                result += 1
            else: 
                result += self.count_leafs(child)
        return result

    def get_leafs(self, node = None):
        """
        Returns all leaf contingencies.
        """
        if not node:
            node = self
        result = []
        if not node.has_children:
            return [] 
        for child in node.children:
            if not child.has_children:
                result += [child]
            else: 
                result += self.get_leafs(child)
        return result

    def get_children(self, node=None):
        """
        Returns all children - leafs and booleans.
        """
        result = []
        if not node:
            node = self            
        for child in node.children:
                result += [child]
                result += self.get_children(child)
        return result

    def add_child(self, contingency):
        """
        Adds given cotingency to children list.
        """
        if self.inherited_ctype and self.inherited_ctype != 'none':
            contingency.inherited_ctype = self.inherited_ctype
        else:
            contingency.inherited_ctype = self.ctype
        self.children.append(contingency)
        
    def is_parent(self, contingency):
        """
        Checks whether given contingecy is a child.
        """
        if str(self.state) == contingency.target_reaction:
            return True
        else:
            return False 

    def clone(self, ctype=None):
        """
        Returns new Contingency object.
        It can have different ctype if specified.
        """
        if ctype:
            new_type = ctype
        else:
            new_type = copy.deepcopy(self.ctype)

        new_cont = Contingency(\
            copy.deepcopy(self.target_reaction),\
            new_type, copy.deepcopy(self.state))

        new_cont.inherited_ctype = copy.deepcopy(self.inherited_ctype)
        for child in self.children:
            new_cont.add_child(copy.deepcopy(child))
        return new_cont
