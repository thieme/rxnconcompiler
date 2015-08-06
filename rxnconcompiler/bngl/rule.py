#!/usr/bin/env python

"""
Module rule.py.

Reflects structure in rxncon 
now it is mostly redundant.
Has onle some small additional functions.
To remove? Do we want to make rules and reactions different.

Classes:
RulePool
RuleContainer
Rule         
"""

from rxnconcompiler.molecule.component import Component


class RulePool(dict):
    """
    RulePool object is a dictionary that stores all 
    RuleContainer objects for one system.

    Key: reaction string.
    Value: RuleContainer.
    """

    def __init__(self):
        pass

    def __iter__(self):
        all_rules = sorted(self.values(), key=lambda r: r.rid)
        return iter(all_rules)

class RuleContainer(list):
    def __init__(self, reaction_container):
        self.reactions = reaction_container
        self.reaction_name = self.reactions.name
        self.name = self.get_name()
        self.rid = self.reactions.rid
        self.sp_state = None
        self.common_reqs = []
        self.contingencies = None # only to produce contingency string

    def add_rule(self, rule):
        self.append(rule)

    def get_name(self):
        """
        @rtype: string
        """
        react = self.reactions[0]
        return '%s %s %s' % (react.left_reactant.name, react.rtype, react.right_reactant.name)


class Rule:
    def __init__(self, reaction):
        self.reaction = reaction
        self.name = self.reaction.name
        self.rid = self.reaction.rid
        self.specific_reqs = []
        self.header = False

    @property
    def arrow(self):
        """Returns reaction arrow depending on reaction reversibility."""
        if self.reaction.definition['Reversibility'] == 'irreversible':
            return '->' 
        elif self.reaction.definition['Reversibility'] == 'reversible':
            return '<->'
    @property
    def rates(self):
        """"""
        return self.reaction.rate.get_rates_for_reaction()

    @property
    def rate_values(self):
        """"""
        return self.reaction.rate.get_rate_values()

