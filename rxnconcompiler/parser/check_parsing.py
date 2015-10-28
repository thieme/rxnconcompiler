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
        self.new_contingencies = {}

    def testContingencySign(self):
        for contingency in self.parsed_contingencies:
            if contingency['Contingency'].lower() in ["!","x","0","?","k+","k-", "and","or","not"] or "--" in contingency['Contingency'] or re.match("^[1-9]*$", contingency['Contingency']):
                continue
            else:
                raise RxnconParserError("Contingency {0} not known.".format(contingency['Contingency']))

    def update_new_contingency(self, key, value):
        if key not in self.new_contingencies:
            self.new_contingencies[key] = {'modifiers' : [value], 'name': ''}
        elif value not in self.new_contingencies[key]['modifiers']:
            self.new_contingencies[key]['modifiers'].append(value)

    def domain_overlapping(self, modifier_state, modifier_comp, reaction_product_state):

        """
        Matching table:

        If Contingency
        Modifier has    | No domain |   main   | main/sub |    main/sub/residue    |      main/residue      |       residue          |
                        |           |          |          |                        |                        |                        |
        No domain       |    ok     |    ok    |   ok     |           ok           |           ok           |           ok           |
        ----------------|-----------|----------|----------|------------------------|------------------------|------------------------|
        main            |    Not    | if exact | if exact |        if exact        |        if exact        |           Not          |
        ----------------|-----------|----------|----------|------------------------|------------------------|------------------------|
        main/sub        |    Not    |    Not   | if exact |        if exact        |            Not         |           Not          |
        ----------------|-----------|----------|----------|------------------------|------------------------|------------------------|
        main/sub/residue|    Not    |    Not   |   Not    |covalent mod: if residue|covalent mod: if residue|covalent mod: if residue|
                                                          |               is exact |              is exact  |              is exact  |
                                                          |------------------------|------------------------|------------------------|
                                                          |   else:       if exact |   else:       Not      |   else:       Not      |
        ----------------|-----------|----------|----------|------------------------|------------------------|------------------------|
        main/residue    |    Not    |    Not   |   Not    |covalent mod: if residue|covalent mod: if residue|covalent mod: if residue|
                                                          |               is exact |              is exact  |              is exact  |
                                                          |------------------------|------------------------|------------------------|
                                                          |   else:       if exact |   else:       if exact |   else:       Not      |
        ----------------|-----------|----------|----------|------------------------|------------------------|------------------------|
        residue         |    Not    |    Not   |   Not    |        if exact        |        if exact        |        if exact        |

        @param modifier_state:
        @param modifier_comp:
        @param reaction_product_state:
        @return:
        """
        if modifier_comp.domain_info.main == 'bd' or "Assoc" in modifier_comp.domain_info.main:
            #Case: no domain defined by user
            self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)

        elif modifier_state.type == "Covalent Modification" and modifier_comp.domain_info.residue != "":
            if modifier_comp.domain_info.residue == reaction_product_state.domain_info.residue:
                #Case: covalent modification and residue defined
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
        elif modifier_comp.domain_info.main != "" and modifier_comp.domain_info.main == reaction_product_state.domain_info.main:
            # Case: not a covalent modification
            #       or no residue defined
            #       but main domain defined
            if modifier_comp.domain_info.sub != "" and modifier_comp.domain_info.sub == reaction_product_state.domain_info.sub:
                # Case: main/sub domain defined
                if modifier_comp.domain_info.residue != "" and modifier_comp.domain_info.residue == reaction_product_state.domain_info.residue:
                    # Case: main/sub/residue defined (Association)
                    self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
                else:
                    # Case: main/sub no residue
                    self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
            elif modifier_comp.domain_info.residue != "" and modifier_comp.domain_info.residue == reaction_product_state.domain_info.residue:
                # Case: main/residue defined
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
            else:
                # Case: main
                #       no sub
                #       no residue
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
        elif modifier_comp.domain_info.residue != "" and modifier_comp.domain_info.residue == reaction_product_state.domain_info.residue:
            # Case: if residue
            #       no main
            #       no sub
            self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)



    def testContingencyModifier(self):
        new_contingencies = {}
        new_complex = 0
        to_delete = []
        to_add = []
        for i, cont in enumerate(self.parsed_contingencies):

            if "<" not in cont['Modifier'] and "[" not in cont['Modifier'] and cont['Modifier'] not in new_contingencies:
                #produced = False
                modifier_state = get_state(cont['Modifier'])
                for reaction in self.parsed_reactions:
                    reaction_product_state = get_state(reaction["ProductState"])
                    if modifier_state.type == reaction_product_state.type:
                        if modifier_state.type == "Covalent Modification":
                        #for reaction_component in reaction_product_state.components:
                            modifier_comp = modifier_state.get_component(reaction_product_state.components[0].name)
                        if modifier_state.type == "Association":
                            modifier_comp = None
                            if modifier_state.has_component(reaction_product_state.components[0]) and modifier_state.has_component(reaction_product_state.components[1]):
                                modifier_comp = modifier_state.get_component(reaction_product_state.components[0].name)
                        if modifier_comp is not None:
                            if modifier_state.modifier == reaction_product_state.modifier:
                                self.domain_overlapping(modifier_state, modifier_comp, reaction_product_state)

                if len(new_contingencies[modifier_state.state_str]['modifiers']) == 0:
                    to_delete.append(i) # delete/error
                elif len(new_contingencies[modifier_state.state_str]['modifiers']) == 1:
                    if  modifier_state.state_str != new_contingencies[modifier_state.state_str]['modifiers'][0]:
                        # check if difference if yes replace warn
                        print "differs"
                        cont['Modifier'] = new_contingencies[modifier_state.state_str]['modifiers'][0]

                elif len(new_contingencies[modifier_state.state_str]['modifiers']) > 1:
                    pass # replace with boolean or
                    new_complex +=1
                    ContingencyID = len(self.parsed_contingencies) + 1
                    complex_name = "<AutomaticGeneratedComplex{0}>".format(new_complex)
                    cont['Modifier'] = complex_name
                    new_contingencies[modifier_state.state_str]['name'] = complex_name
                    for new in new_contingencies[modifier_state.state_str]['modifiers']:
                        ContingencyID = ContingencyID + len(to_add)
                        to_add.append({'Contingency': 'OR', 'Modifier': new, 'Target': complex_name, 'ContingencyID': ContingencyID})
            elif cont['Modifier'] in new_contingencies:
                cont['Modifier'] = new_contingencies[cont['Modifier']]['name']
        for cont in to_add:
            self.parsed_contingencies.append(cont)
        pass


