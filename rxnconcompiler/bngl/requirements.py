#!/usr/bin/env python

"""
Class RequirementsPool      - class that stores requirements for all reactions.
Class RequirementNode       - class that generates and stores requirements 
                              for single contingency given its children.
Class RequirementsGenerator - class that generates requirements from contingencies 
                              for single reaction.
Class RequirementsFactory   - class that produces RequirementsPool objects                        
"""

import re
from contingency.contingency_factory import ContingencyWrapper, ContingencyFactory
from util.util import product, flatten


class RequirementsPool(dict):
    """
    Disctionary for requirements.

    Key: reaction as string e.g. 'A_ppi_B'
    Value: list of requirement lists.
    """
    def __init__(self):
        pass


class RequirementNode:
    """
    RequirementNode object calculates 
    requirements for itself based on list of contingency children.
    """
    def __init__(self):
        self.positive = [[]]

    def __repr__(self):
        """String with number of positive, negative and total requirements."""
        return "Positive: %i" % (len(self.positive))

    def get_or_positive(self, nodes):
        """
        P = P1 + P2 + P3 ...
                <MM>
             /       \
         OR A-{P}    OR B-{P}

        P1 = [[!A-{P}]]    
        P2 = [[!B-{P}]]    
        P  = [[!A-{P}] + [!B-{P}] = [[!A-{P}], [!B-{P}]] 
        """
        result = []
        for node in nodes:
            result += node.positive
        self.positive = result

    def get_and_positive(self, nodes):
        """
        P = P1 * P2 * P3 ...
        where P is a list of lists of positive combinations,
        P1, P2, P3 - positive combinations from children.
        e.g.
                <MM>
             /       \
        AND A-{P}    AND B-{P}

        P1 = [[!A-{P}]]
        P2 = [[!B-{P}]]
        P  = [!A-{P}] * [!B-{P}] = [[!A-{P}, !B-{P}]]
        """
        all_pos = [node.positive for node in nodes]
        result = reduce(product, all_pos)
        self.positive = [flatten(x) for x in result]
        
    def get_leaf(self, node):
        """
        Asignes requirements to contingencies 
        with no children and which are not K+ and not K-.
        """
        if node.ctype == '!' or node.inherited_ctype == '!':
            self.positive = [[ContingencyWrapper(node, 'positive')]]
        elif node.ctype == 'x' or node.inherited_ctype == 'x':
            self.positive = [[ContingencyWrapper(node, 'negative')]]


class RequirementsGenerator:
    """
    The RequirementsGenerator object goes through all contingencies 
    using a tree traversal algorithm
    and generates requirements with only x and ! signs. 

    Input: contingency root node
    Deals with !, x, boolean contingencies, ignores K+, K-, 0, ?
    """
    def __init__(self, root_node):
        self.root = root_node       
        self.requirements = []
        self.nodes_dict = {}
        self._create_node_dict(self.root)

    def __str__(self):
        """
        Human readable string for boolean contingencies.
        """
        result = self._get_str(self.root)
        result = result.strip()
        if len(result) > 0 and result[-1] == ',':
            result = result[:-1]

        return result

    def _get_str(self, node=None):
        """
        Produces a string with all contingencies from the given node.
        Traverse contingencies downstream from the given node. 
        When given root node creates complete string.
        """
        result = ''
        if not node: 
            return result
        elif not node.has_children:
            if node.ctype == 'none' or not node.ctype: return '' 
            result += ' ' + str(node)
            if node.ctype in ['k+', 'k-', '!', '0', 'x', '?']:
                result += ', '
        elif node.has_children:
            children_str = ''
            for child in node.children: 
                children_str += self._get_str(child)
            if node.ctype and node.ctype != 'none':
                result += ' %s (%s)' % (node.ctype, children_str)
            else:
                result += children_str
        result = re.sub('\( or |\( and |\( xor |\( not', '(', result)
        result = re.sub('\s{2,3}', ' ', result)
        return result

    def _create_node_dict(self, node):
        """
        Prepares a dict where requirements will be asign to contingencies.
        Key: contingency
        Value: empty RequirementNode object.
        """
        if node not in self.nodes_dict:
            self.nodes_dict[node] = RequirementNode()
        if node.has_children:
            for child in node.children:
                self._create_node_dict(child)
        
    def requirements2nodes(self, cont):
        """
        Recursively assigns requirements to given contingency.
        """

        req_node = self.nodes_dict[cont]
        if not cont.has_children: # and cont.ctype not in ['0', '?', 'k+', 'k-', 'x']:
            req_node.get_leaf(cont)

        elif cont.has_children: #and  cont.ctype not in ['0', '?', 'k+', 'k-', 'x']: 
            for child in cont.children:
                self.requirements2nodes(child)

            child_nodes = [self.nodes_dict[child] for child in cont.children]
            
            if cont.children[0].ctype == 'or':
                req_node.get_or_positive(child_nodes)
            
            elif cont.children[0].ctype == 'and' \
                or cont.ctype == 'none' or not cont.ctype:
                req_node.get_and_positive(child_nodes)
        
    def get_requirements(self):
        """
        Creates the final list of requirements.
        It is a list of lists where each list responds to one rule.
        When reaction has no contingencies it is equal [[]].
        """
        self.requirements2nodes(self.root)
        for req_list in self.nodes_dict[self.root].positive:
            temp = []
            for req in req_list:
                temp.append(req.get_contingency())
            self.requirements.append(temp)
        return self.requirements

        
class RequirementsFactory:
    """
    Produces dictionary with requirements for all reactions.
    """
    def __init__(self, xls_tables):
        self.xls_tables = xls_tables
        self.contingencies = ContingencyFactory(self.xls_tables).parse_contingencies()
        self.requirements = self.generate_requirements()

    def generate_requirements(self):
        """
        Prepares dictionary with requirements.
        """
        reqs = RequirementsPool()
        for reaction in self.contingencies.keys():
            req_gen = RequirementsGenerator(self.contingencies[reaction])
            reqs[reaction] = req_gen.get_requirements()
        return reqs

    def get_requirements_dict(self):
        """
        Prepares dictionary with requirement lists
        (requirements are strings).

        E.g.
        A_ppi_B; x A--C
        A_ppi_B; ! <Bool>
        <Bool>; OR A-{P}; OR B-{P}

        'A_ppi_B': [['x A--C', '! A-{P}'], ['x A--C', '! B-{P}']] 
        """
        result = {}
        for reaction in self.requirements.keys():
            result[reaction] = []                
            for req_list in self.requirements[reaction]:
                temp = [str(req) for req in req_list]
                result[reaction].append(temp)
        return result