#!/usr/bin/env python

"""
Class RxnconWarnings: collects info on problems
                      so they can be included in BNGL file as comments.
"""


class RxnconWarnings:
    """
    Stores information on logical problems in the rxncon input.
    """
    def __init__(self):
        """"""
        # state used in a contingency is not produced by the reactions.
        self.not_in_products = []
        # there are more than one modification states produced.
        # Contingency state must indicate (via the domain) which product to use.
        self.produced_in_more = {}
        self.mutual_exclusive_reactions = {}
        self.not_applied_contingencies = []

    def calculate_missing_states(self, reaction_pool, contingency_pool):
        """
        Based on given reaction and contingencies pool checks
        which states are missing (used in contingencies and not
        produced in reactions).
        Returns list of states.
        """
        # states in reactions like P- or GAP, Ub-
        destroyed_states = reaction_pool.get_destroyed_states()
        # states from !, K+, K- contingencies
        # and also x ---> domains from x need to be present and domains are only
        #                 collected from produced states
        contingency_states = contingency_pool.get_required_states()

        product_states = set(reaction_pool.get_product_states())
        required_states = contingency_states.union(destroyed_states)
        self.not_in_products = required_states - product_states
        return self.not_in_products

    def _fill_mutual_exclusive_reactions_dict(self, key, value):
        """
        function to fill the dictionary saving mutual exclusive reactions.

        """
        if key not in self.mutual_exclusive_reactions.keys():
            self.mutual_exclusive_reactions[key] = [value]
        else:
            self.mutual_exclusive_reactions.append(value)

    def get_mutual_exclusive_reactions(self, reaction_pool):
        """
        Based on the reaction pool this function checks if interaction reactions (ppi, i, BIND, ...) are using the same domain.
        modification reactions are not tested here because in case of e.g. phosphorylating the same domain of a certain protein the same state will be created.
        In case of interaction reactions the state will be different.
cd
        @return: dictionary key: reaction value: a tuple of reaction and state of all mutually exclusive reactions
        @rtype:  dict
        @param reaction_pool: collection of all reactions. object of ReactionContainer class
        """
        product_states = reaction_pool.get_product_states()  # get all produced states

        for product_state_1 in product_states:  # iterate over the produced state
            if product_state_1.type == 'Association':  # check only association reactions
                for product_state_2 in product_states:
                    if product_state_2.type == 'Association' and product_state_1.reaction_str != product_state_2.reaction_str:
                        if product_state_1.reaction_str in self.mutual_exclusive_reactions.keys() and (product_state_2.reaction_str, product_state_2) in self.mutual_exclusive_reactions[product_state_1.reaction_str]:
                            continue

                        if product_state_1.exact_compare(product_state_2.components):
                            self._fill_mutual_exclusive_reactions_dict(product_state_1.reaction_str, (product_state_2.reaction_str, product_state_2))
                            self._fill_mutual_exclusive_reactions_dict(product_state_2.reaction_str, (product_state_1.reaction_str, product_state_1))
        return self.mutual_exclusive_reactions

    def get_problem_reaction_str(self):
        """
        makes set of strings out of self.not_applied_contingencies
        (list of objects).
        Removes redundant reactions.
        """
        #print "get_problem_reaction_str"
        result = [str(react) for react in self.not_applied_contingencies]
        return set(result)
