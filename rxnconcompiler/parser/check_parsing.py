__author__ = 'thiemese'

from rxnconcompiler.util.rxncon_errors import RxnconParserError
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.molecule.domain_factory import DomainFactory
import re

class InputCheck(object):
    """"""
 
    def __init__(self,parsed_information):
        """Constructor for InputCheck"""
        self.parsed_contingencies = parsed_information["contingency_list"]
        self.parsed_reactions = parsed_information["reaction_list"]
        self.parsed_definition = parsed_information['reaction_definition']

    def testContingencySign(self):
        for contingency in self.parsed_contingencies:
            if contingency['Contingency'].lower() in ["!","x","0","?","k+","k-", "and","or","not"] or "--" in contingency['Contingency'] or re.match("^[1-9]*$", contingency['Contingency']):
                continue
            else:
                raise RxnconParserError("Contingency {0} not known.".format(contingency['Contingency']))

class ContingenciesManipulation(object):
    """This class checks if all contingencies are proper defined and applies changes according the set definition
       explained in the documentation.
    e.g. replacing Modifiers like A-{P} with A_[x]-{P}, A_[y]-{P} and A-{P} if defined"""

    def __init__(self, parsed_information):
        """Constructor for CheckContingencies"""
        self.parsed_contingencies = parsed_information["contingency_list"]
        self.parsed_reactions = parsed_information["reaction_list"]
        self.parsed_definition = parsed_information['reaction_definition']
        self.df = DomainFactory()
        self.new_contingencies = {}
        self.to_add = []
        self.to_delete = []
        self.new_complex = 0


    def update_new_contingency(self, key, value):
        if key not in self.new_contingencies:
            self.new_contingencies[key] = {'modifiers' : [value], 'name': ''}
        elif value not in self.new_contingencies[key]['modifiers']:
            self.new_contingencies[key]['modifiers'].append(value)

    def domain_overlapping(self, modifier_state, modifier_comp, reaction_product_state, product_comp):

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
            if modifier_comp.domain_info.residue == product_comp.domain_info.residue:
                #Case: covalent modification and residue defined
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
        elif modifier_comp.domain_info.main != "" and modifier_comp.domain_info.main == product_comp.domain_info.main:
            # Case: not a covalent modification
            #       or no residue defined
            #       but main domain defined
            if modifier_comp.domain_info.sub != "":
                # Case: modifier main/sub domain defined
                if modifier_comp.domain_info.sub == product_comp.domain_info.sub:
                # Case: modifier main/sub domain defined and product main/sub domain defined and equal
                    if modifier_comp.domain_info.residue != "":
                        # Case: modifier main/sub/residue defined
                        if modifier_comp.domain_info.residue == product_comp.domain_info.residue:
                        # Case: modifier main/sub/residue defined (Association) and product main/sub/residue defined and equal
                            self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
                    else:
                        # Case: modifier main/sub no residue defined
                        self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
            elif modifier_comp.domain_info.residue != "" and modifier_comp.domain_info.residue == product_comp.domain_info.residue:
                # Case: main/residue defined
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
            else:
                # Case: main
                #       no sub
                #       no residue
                self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)
        elif modifier_comp.domain_info.residue != "" and modifier_comp.domain_info.residue == product_comp.domain_info.residue:
            # Case: if residue
            #       no main
            #       no sub
            self.update_new_contingency(modifier_state.state_str, reaction_product_state.state_str)


    def check_if_complex_exists(self, state_str):
        for state in self.new_contingencies:
            if state != state_str and set(self.new_contingencies[state]['modifiers']) == set(self.new_contingencies[state_str]['modifiers']):
                return self.new_contingencies[state]['name']
        return ""

    def delete_contingency_from_CL(self):
        to_delete = self.to_delete[::-1]
        for del_ele in to_delete:
            del self.parsed_contingencies[del_ele]

    def update_CL(self):
        for cont in self.to_add:
            self.parsed_contingencies.append(cont)

    def evaluate_processed_contingency(self, modifier_state, cont, idx):
        if modifier_state.state_str not in self.new_contingencies:
            # in this case we know that the modifier is not produced by a reaction
            self.to_delete.append(idx) # delete/error
        elif len(self.new_contingencies[modifier_state.state_str]['modifiers']) == 1:
            # in this case we know that the modifier is produced by a reaction or a overlapping state is produced by a reaction
            if  modifier_state.state_str != self.new_contingencies[modifier_state.state_str]['modifiers'][0]:
                # check if difference if yes replace warn
                # here we know that an overlapping state is produced which differs from the modifier
                cont['Modifier'] = self.new_contingencies[modifier_state.state_str]['modifiers'][0]

        elif len(self.new_contingencies[modifier_state.state_str]['modifiers']) > 1:
            complex_name = self.check_if_complex_exists(modifier_state.state_str)
            if complex_name:
                cont['Modifier'] = complex_name
                self.new_contingencies[modifier_state.state_str]['name'] = complex_name
            else:
                next_complex = True
                self.new_complex +=1
                ContingencyID = len(self.parsed_contingencies) + len(self.to_add) + 1
                complex_name = "<AutomaticGeneratedComplex{0}>".format(self.new_complex)
                cont['Modifier'] = complex_name
                self.new_contingencies[modifier_state.state_str]['name'] = complex_name
                for new in self.new_contingencies[modifier_state.state_str]['modifiers']:
                    if self.to_add and not next_complex:
                        ContingencyID += 1
                    next_complex = False
                    self.to_add.append({'Contingency': 'OR', 'Modifier': new, 'Target': complex_name, 'ContingencyID': ContingencyID})
    def update_reaction_product_state(self, reaction, product_comp, reaction_product_state):
        comp_dom = self.df.get_modification_domain_from_dict(reaction)
        product_comp.domain_info = comp_dom
        product_comp.domain = comp_dom.name
        reaction_product_state.domain = comp_dom.name
        reaction_product_state.state_str = '%s_[%s]-{%s}' % (product_comp.name, comp_dom.name, reaction_product_state.modifier)

    def LumpedContingencyModifier(self):
        """
        This function itters over the user defined Contingencies does three things:
            1) finds overlapping modifier which are defined by reactions
            2) deletes a contingency if the modifier is not defined
            3) generates an boolean OR complex if there are more than 1 reaction output
               which fits the domain overlapping table in def domain_overlapping()

        @return:
        """
        for idx, cont in enumerate(self.parsed_contingencies):
            if "<" not in cont['Modifier'] and "[" not in cont['Modifier'][0] and cont['Modifier'] not in self.new_contingencies:
                modifier_state = get_state(cont['Modifier'])
                for reaction in self.parsed_reactions:
                    #stateFactory = StateFactory()
                    #for r_def in self.parsed_definition:
                        #if r_def['UID:Reaction'].lower() == reaction["UID:Reaction"].lower()
                        #    category = r_def['Category']
                        #    stateFactory.get_state_from_reaction(reaction,r_def['Category'])
                    reaction_product_state = get_state(reaction["ProductState"])


                    if modifier_state.type == reaction_product_state.type:
                        if modifier_state.type == "Covalent Modification":
                            modifier_comp = modifier_state.get_component(reaction_product_state.components[0].name)
                            if modifier_comp is not None:
                                product_comp = reaction_product_state.get_component(modifier_comp.name)
                                if product_comp.domain_info.main == "bd":
                                    self.update_reaction_product_state(reaction, product_comp, reaction_product_state)
                        if modifier_state.type == "Association":
                            modifier_comp = None
                            if modifier_state.has_component(reaction_product_state.components[0]) and modifier_state.has_component(reaction_product_state.components[1]):
                                modifier_comp = modifier_state.get_component(reaction_product_state.components[0].name)
                                product_comp = reaction_product_state.get_component(modifier_comp.name)
                        if modifier_comp is not None:
                            if modifier_state.modifier == reaction_product_state.modifier:
                                self.domain_overlapping(modifier_state, modifier_comp, reaction_product_state,product_comp)
                self.evaluate_processed_contingency(modifier_state, cont, idx)

            elif cont['Modifier'] in self.new_contingencies:
                cont['Modifier'] = self.new_contingencies[cont['Modifier']]['name']
        self.delete_contingency_from_CL()
        self.update_CL()
        pass


