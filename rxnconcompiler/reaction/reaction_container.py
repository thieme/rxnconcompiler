#!/usr/bin/env python

"""
Module reaction_container.py 
containes classes that store the reactions for the entire rxncon system.

Class ReactionContainer(list) - container for alternative reactions 
                                (e.g. reaction that has boolean, 
                                complex or K+/K- contingencies).
                                Stores one ore more Reaction objects.
Class ReactionPool(dict)      - dictionary for all ReactionContainers 
                                present in the system. 
"""

class ReactionContainer(list):
    """
    Container for alternative reactions as one reaction can happen
    in many contexts (e.g. K+/K- contingency).
    Enables obtaining info about properties common for all reactions inside
    """
    def __init__(self):
        """
        Common features of reactions in a single container:
        name -  describs basic reaction e.g. A_[domainX]_ppi_B
                (only left and right reactant included, no complexes).
        rid -   reaction identifier.
        rtype - reaction type e.g. ppi, i, P+
        """
        list.__init__(self)
        self.name = None
        self.rid = None
        self.rtype = None

    def __repr__(self):
        """
        @return: name and number of reactions in the container.
        """
        return "ReacionConteiner for %s: %i reactions present" % (self.name, len(self)) 

    def add_reaction(self, reaction):
        """
        Adds given reaction to the container.

        @type reaction:  Reaction object
        @param reaction: Reaction to add.
        """
        # TODO: check whether it is reaction. 
        # TODO: check whether it belongs to the container (same name).
        # TODO: check whether id is free.
        if len(self) != 0:
            temp_rid = str(self[-1].rid).split('_')
            main_rid = temp_rid[0]
            if len(temp_rid) == 1:
                self[-1].rid = '%s_%s' % (main_rid, '1')
                sup_rid = 2
            else:
                sup_rid = int(temp_rid[1]) + 1
            reaction.rid = "%s_%s" % (main_rid, str(sup_rid))
        else:
            reaction.rid = self.rid
        self.append(reaction)
  
    def update_rid(self, new_id):
        """
        Changs conteiner.rid and rid of each reaction.
        Subnumbers stay the same
        e.g. update_rid(8)
        container.rid = 8
        reaction1.rid = 8_1
        reaction2.rid = 8_2
        Automatically updates rate.
        """
        self.rid = str(new_id)
        for reaction in self:
            splited = str(reaction.rid).split('_')
            splited[0] = str(new_id)
            reaction.rid = '_'.join(splited)
            reaction.rate.update_name(reaction.rid)

    @property
    def sp_state(self):
        """
        The source/product state of all reactions present in the continer.
        """
        if len(self) > 0:
            return self[0].get_sp_state()
        else:
            return None

    @property
    def product_contingency(self):
        """
        The product state of all reactions present in the continer.
        """
        if len(self) > 0:
            return self[0].get_product_contingency()
        else:
            return None

    @property
    def source_contingency(self):
        """
        The source state of all reactions present in the continer.
        """
        if len(self) > 0:
            return self[0].get_source_contingency()
        else:
            return None

    def get_common_contingencies(self):
        """
        Requirements common for all reactions in the container.

        @rtype:  list of Contingency objects.
        @return: intersection of contingencies (context) 
                 read from all reaction object.
        """
        all_cont = []
        for reaction in self:
            all_cont.append(set(reaction.get_contingencies()))
        if len(all_cont) > 0:
            return list(all_cont[0].intersection(*all_cont))
        else:
            return []

    def get_modifier(self):
        """
        Returns a list of complexe that don't change during the reaction.
        They are common for all the reactions in the container.

        @rtype:  list of BiologicalComplex objects.
        @return: substrat complexes that are not changed in the reaction.
        """
        if len(self) > 0:
            return self[0].get_modifier()

    @property
    def highest_subrate(self):
        """
        For ich reaction chaecks all rates. 
        From all rates checks which number after '_', is the highest.
        If reaction has only single rate returns 0.
        Returns int.

        e.g.
        kf1_1, kr1_1; kf1_2, kr1_2; kf1_3, kr1_3 ---> 3
        k1; k1 ---> 0 
        """
        all_subrates = []
        for reaction in self:
            if '_' not in reaction.rate._rate_names[0]:
                return 0
            else:
                all_subrates += [int(rate.split('_')[1]) for rate in reaction.rate._rate_names]
        return max(all_subrates)

    def empty(self):
        """
        Removes all reactions.
        """
        while self:
            self.pop()    


class ReactionPool(dict):
    """
    Contains all ReactionContainers for the system.
    """
    def __init__(self):
        dict.__init__(self)

    def __iter__(self):
        """
        Allows to iter reactions sorted by id.
        """
        all_reactions = sorted(self.values(), key=lambda r: r.rid)
        return iter(all_reactions)

    def get_highest_id(self):
        """
        Return the highest id of the containers present.
        """
        ids = []
        for cont in self:
            ids.append(int(cont.rid))
        return max(ids)

    def update_pool(self, second_pool):
        """Adds reactions from another pool."""
        counter = self.get_highest_id()
        for container in second_pool.values():
            counter += 1
            container.update_rid(counter)
        self.update(second_pool)

    def get_product_states(self):
        """
        @return: states that are produced in the reactions
        @rtype:  set
        """
        result = []
        for react_cont in self.values():
            product_cont = react_cont.product_contingency
            if product_cont and product_cont.ctype == '!':
                result.append(product_cont.state)
        return set(result)

    def get_product_contingencies(self):
        """
        Produces collection of all states generated by this reaction pool as contingencies.

        @return: states that are produced in the reactions.
        @rtype:  set.
        """
        result = []
        for react_cont in self.values():
            product_cont = react_cont.product_contingency
            if product_cont:
                result.append(product_cont)
        return set(result)

    def get_destroyed_states(self):
        """
        Returns set of sets that are destroyed in the pool.
        E.g. in P-, Ub- GAP reactions.
        """
        result = []
        for react_cont in self.values():
            product_cont = react_cont.product_contingency
            if product_cont and product_cont.ctype == 'x':
                result.append(product_cont.state)
        return set(result)

    def find_modification_product(self, state):
        """
        Finds Covalent Modification state in products of all reactions,
        when gicen state - check with name and modifier not with domain.

        Used when exchenging default bd domain in contingency.
        """
        result = []
        products = self.get_product_contingencies()
        for cont in products:
            if cont.ctype == '!' and cont.state and cont.state.type == 'Covalent Modification':
                if cont.state.components[0].name == state.components[0].name:
                    if cont.state.modifier == state.modifier:
                        result.append(cont.state)
        return result 

    def find_relocalisation_product(self, state):
        """
        Findes relocalisation reactions.
        Returns a list of relocalisation states that have given mol name.
        """
        result = []
        for container in self:
            product = container.sp_state
            if product.type == 'Relocalisation':
                if product.components[0] == state.components[0]:
                    result.append(product)
        return result