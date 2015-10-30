__author__ = 'thiemese'

from rxnconcompiler.util.rxncon_errors import RxnconParserError
from rxnconcompiler.molecule.state import get_state
import re

class CheckContingencies(object):
    """This class checks if all contingencies are proper defined and applies changes according the set definition
       explained in the documentation.
    e.g. replacing Modifiers like A-{P} with A_[x]-{P}, A_[y]-{P} and A-{P} if defined"""

    def __init__(self, parsed_information):
        """Constructor for CheckContingencies"""
        self.parsed_contingencies = parsed_information["contingency_list"]
        self.parsed_reactions = parsed_information["reaction_list"]

    def testContingencySign(self):
        for contingency in self.parsed_contingencies:
            if contingency['Contingency'].lower() in ["!","x","0","?","k+","k-", "and","or","not"] or "--" in contingency['Contingency'] or re.match("^[1-9]*$", contingency['Contingency']):
                continue
            else:
                raise RxnconParserError("Contingency {0} not known.".format(contingency['Contingency']))

    def getDomainSubdomainResidueFromModifier(self,state_str):
        comp_name_dom = state_str.split("_")



    def testContingencyModifier(self):
        for cont in self.parsed_contingencies:

            if "<" not in cont['Modifier'] or "[" not in cont['Modifier']:
                produced = False
                modifier_state = get_state(cont['Modifier'])
                for reaction in self.parsed_reactions:
                    reaction_product_state = get_state(reaction["ProductState"])
                    if modifier_state.type == reaction_product_state.type:
                        if modifier_state.modifier == reaction_product_state.modifier:


                            pass

