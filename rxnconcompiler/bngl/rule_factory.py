#!/usr/bin/env python

"""
Module rule_factory.py

Contains: RuleFactory class.

Creates RoolPool from reaction_pool and contingency_pool

Not neccesary?
"""

from rule import RulePool, RuleContainer, Rule
from requirements import RequirementsGenerator
from molecule.state import Component

class RuleFactory:
    """"""
    def __init__(self, reaction_pool, contingency_pool):
        self.reaction_pool = reaction_pool
        self.contingency_pool = contingency_pool
        self.rule_pool = RulePool()
        self.generate_rules()

    def generate_rules(self):
        """"""
        for reaction_container in self.reaction_pool:
            rule_container =  RuleContainer(reaction_container)
            rule_container.sp_state = reaction_container.sp_state
            common_cont = reaction_container.get_common_contingencies()
            rule_container.common_reqs = common_cont
            if self.contingency_pool.has_key(reaction_container.name):
                gen = RequirementsGenerator(self.contingency_pool[reaction_container.name])
                rule_container.contingencies = gen
            else:
                rule_container.contingencies = None
            # add source and product states and reqs change name.
            header = True if len(reaction_container) > 1 else False
            for reaction in reaction_container:
                rule = Rule(reaction)
                rule.header = header
                # add specific reqs and cont.
                rule_container.add_rule(rule)
                if header:
                    rule.specific_reqs = reaction.get_specific_contingencies(common_cont)
            self.rule_pool[reaction_container.name] = rule_container
