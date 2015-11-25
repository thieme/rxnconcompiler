__author__ = 'thiemese'

from rxnconcompiler.util.rxncon_errors import RxnconParserError

class CheckContingencies(object):
    """This class checks if all contingencies are proper defined and applies changes according the set definition
       explained in the documentation.
    e.g. replacing Modifiers like A-{P} with A_[x]-{P}, A_[y]-{P} and A-{P} if defined"""

    def __init__(self, parsed_information):
        """Constructor for CheckContingencies"""
        self.parsed_contingencies = parsed_information["contingency_list"]
        self.parsed_reactions = parsed_information["reaction_list"]

    def test_contingency_sign(self):
        for contingency in self.parsed_contingencies:
            if contingency['Contingency'].lower() not in ["!","x","0","?","k+","k-","and","or","not"]:
                raise RxnconParserError("Contingency {0} not known.".format(contingency['Contingency']))


