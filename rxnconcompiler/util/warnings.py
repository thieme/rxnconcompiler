#!/usr/bin/env python

"""
Class RxnconWarnings: colects info on problems 
                      so they can be included in BNGL file as comments.
"""
class RxnconWarnings:
    """
    Stores inforation on logical problems in the rxncon input.
    """
    def __init__(self):
        """"""
        # state used in a contingency is not produced by the reactions.
        self.not_in_products = []
        # there are more than one modification states produced.
        # Contingncy state must indicate (via the domain) which product to use.  
        self.produced_in_more = {}
        self.not_applied_contingencies = []

    def calculate_missing_states(self, reaction_pool, contingency_pool):
        """
        Based on given reacion and contingencies pool checks
        which states are missing (used in contingencies and not 
        produced in reactions).
        Returns list of states. 
        """
        # states in reactions like P- or GAP, Ub-
        destroyed_states = reaction_pool.get_destroyed_states()
        # states from !, K+, K- contingencies
        # and also x ---> domains from x need to be present and domains are only 
        #                 colected from produced states
        contingency_states = contingency_pool.get_required_states()
        product_states = reaction_pool.get_product_states()
        required_states = contingency_states.union(destroyed_states)
        self.not_in_products = required_states - product_states
        return self.not_in_products

    def get_problem_reaction_str(self):
        """
        makes set of strings out of self.not_applied_contingencies
        (list of objects).
        Removes redundant reactions.
        """
        result = [str(react) for react in self.not_applied_contingencies]
        return set(result)