#!/usr/bin/env python

"""
Module bngl.py

Classes:
Bngl - main class from bngl.
       Connects all functionalities from bngl to create
       output BNGL file. 
"""

from bngl_output import BnglOutput
from rule_factory import RuleFactory

class Bngl:
    """
    Translates rxncon reactions into BNGL string. 
    Creates BNGL objects that mirror the Rxncon objects but are simpler.
    Main object used: BnglOutput - menages all strings production. 

    @type reactions:      ReactionPool
    @param reactions:     dictionary of ReactionContainer objects.
                          Used to create RulePool (production done by RuleFactory).
    @type molecules:      MoleculePool
    @param molecules:     dictionary of all molecules present in the system.
                          Used to create molecules and species section.
    @type contingencies:  ContingencyPool
    @param contingencies: all contingencise for the system.
                          Used to generate warnings (list states that are not present).
    """
    def __init__(self, reaction_pool, molecules, contingencies, warnings=None):
        self.reaction_pool = reaction_pool  # list of ReactionContainer objects.
        self.molecule_pool = molecules  # all molecules in the system.
        self.contingency_pool = contingencies
        rule_factory = RuleFactory(self.reaction_pool, self.contingency_pool)
        self.rule_pool = rule_factory.rule_pool
        self.warnings = warnings

    def get_src(self):
        """
        Returns BNGL source code as a string.
        """
        output = BnglOutput(self.rule_pool, self.molecule_pool, self.warnings)
        return output.get_src() 