#!/usr/bin/env python

"""
Module bngl_output.py

Classes:
BnglTranslator - producess strings from rule/rxncon objects
                 (complex, molecule, species, rule, rule header, reaction header).
BnglOutput - producess sections of bngl file. 
"""

# TODO: Refactor get_molecule_str and get_complex_str ---> CODE DUPLICATION!!!

import re
from molecule.state import Component


class BnglTranslator:
    """
    BnglTranslator clips functions for
    translating objects into strings.

    String order:
    - molecules are sorted alphabetically
    - localisation is first in domain-string
    - then modifcation sites are sorted alphabetically
    (regardles whether these are sites and actual modifications)
    - then binding domains are sorted automatically 
    (regardles bound or not). 
    """
    def __init__(self):
        pass

    def get_complex_str(self, compl):
        """
        Produces complex string out of BiologicalComplex object.
        """
        result = ""
        molecules = []
        bonds = compl.get_bonds()

        mols_track = {} # for geting right domain from products with homodimers

        for mol in sorted(compl.molecules, key=lambda mol: mol.name):
            if mol.name not in mols_track:
                mols_track[mol.name] = 1
            else:
                mols_track[mol.name] += 1

            domains = []  # colects domain strings, order is important

            # 1. Localisation domains
            if mol.localisation: 
                dom = mol.localisation.components[0].domain
                if mol.localisation.loc:
                    modif = mol.localisation.modifier
                else:
                    modif = mol.localisation.not_modifier
                domains.append('%s~%s' % (dom, modif))

            # 2. Covalent modification domains
            mod_domains = []    
            for modif in mol.modifications:
                mod_domains.append('%s~%s' % (modif.components[0].domain, modif.modifier))
            for place in mol.modification_sites:
                mod_domains.append('%s~%s' % (place.components[0].domain, place.not_modifier))
            mod_domains.sort()
            domains += mod_domains

            # 3. Binding domains
            bind_domains = [] 

            # TODO: This (used_domains) prabobly should be done on the level of molecule:
            #       To remove empty domains when state gets added:
            #       e.g. when ! A_[x]--B and x A_[x]--C then 
            #            remove state A_[x]--C from empty domains.  
            used_domains = []   

            for binding in mol.binding_partners:
                if binding.type == 'Intraprotein':
                    doms = self.get_ipi_binding_domains(binding)
                    if bonds.has_key((mol, binding)):
                        if doms[0] not in used_domains:
                            bind_domains.append('%s!%i' %(doms[0], bonds[(mol,binding)]))
                            used_domains.append(doms[0])
                        if doms[1] not in used_domains:     
                            bind_domains.append('%s!%i' %(doms[1], bonds[(mol,binding)]))
                            used_domains.append(doms[1])
                else:
                    side = self.get_side(mol, compl, mols_track)
                    dom = self.get_binding_domain(mol.name, binding, mol.mid, side)
                    if bonds.has_key((mol, binding)) and dom not in used_domains:
                        bind_domains.append('%s!%i' %(dom, bonds[(mol,binding)]))
                        used_domains.append(dom)
            for site in mol.binding_sites:
                if site.type == 'Intraprotein':
                    doms = self.get_ipi_binding_domains(site)
                    for dom in doms:
                        if dom not in used_domains:
                            bind_domains.append(dom)
                            used_domains.append(dom)
                else:
                    side = self.get_side(mol, compl, mols_track)
                    dom = self.get_binding_domain(mol.name, site, mol.mid, compl.side)
                    if dom and dom not in used_domains:
                        bind_domains.append(dom)
                        used_domains.append(dom)
            bind_domains.sort()
            domains += bind_domains
            
            if domains:
                molecules.append("%s(%s)" %(mol.name, ','.join(domains)))
            else:
                molecules.append(mol.name)
        result = '.'.join(molecules)
        return re.sub('[-/]', '', result)

    def get_side(self, mol, compl, track_dict):
        """"""
        if compl.side in ['L', 'R']:
            return compl.side
        if track_dict[mol.name] % 2 == 1:
            return 'L'
        else:
            return 'R'

    def get_ipi_binding_domains(self, binding):
        """
        Returns binding domain.
        """
        comp = binding.components[0]
        return[comp.domain, comp.second_domain]

    def get_binding_domain(self, name, binding, mid=None, side='L'):
        """
        Returns binding domain from state and molecule name.
        Returns single string - 1 domain
        """
        if binding.homodimer:
            return binding.get_component(name, side).domain

        comp = Component(name=name, domain=None, cid=mid)
        if comp == binding.components[0]:
            return binding.components[0].domain
        elif comp == binding.components[1]:
            return binding.components[1].domain

    def get_binding_domain_for_molecules(self, name, binding, mid=None, side='L'):
        """
        Returns binding domain from state and molecule name.
        Returns a list.
        This funcion is used for genertion species and molecule strings.
        """
        if binding.homodimer:
            dom1 = binding.components[0].domain
            dom2 = binding.components[1].domain
            if dom1 == dom2:
                return [dom1]
            return [dom1, dom2]

        comp = Component(name=name, domain=None, cid=mid)
        if comp == binding.components[0]:
            return [binding.components[0].domain]
        elif comp == binding.components[1]:
            return [binding.components[1].domain]

    def get_molecule_str(self, mol, mode='molecule'):
        """
        Returns molecule string.
        String contains: 
        - all possible localisations
        - all all modification sites with both True and False modifiers
        - all binding domains as not bound.

        Modes: molecule, species
        """
  
        domains = []
        used_domains = []

        # 1. Localisation domain
        loc_str = ''

        if mode == 'species':
            if mol.localisation:
                loc_str += '~%s' % mol.localisation.not_modifier
        else:
            if mol.localisation:
                loc_str += '~%s~%s' % (mol.localisation.not_modifier, mol.localisation.modifier)
            if mol.alternative_localisations:
                for loc in sorted(mol.alternative_localisations):
                    loc_str += '~%s' % loc
        if loc_str:
            dom = mol.localisation.components[0].domain
            domains.append('%s%s' % (dom, loc_str))
            used_domains.append(dom)

        # 2. Covalent modification domains
        mod_domains = []    
        for modif in mol.modifications:
            if modif.components[0].domain not in used_domains:
                used_domains.append(modif.components[0].domain)
                if mode == 'species':
                    mod_domains.append('%s~%s' % (modif.components[0].domain, modif.not_modifier))
                else:
                    mod_domains.append('%s~%s~%s' % (modif.components[0].domain, modif.not_modifier, modif.modifier))
        for site in mol.modification_sites:
            if site.components[0].domain not in used_domains:
                used_domains.append(site.components[0].domain)
                if mode == 'species':
                    mod_domains.append('%s~%s' % (site.components[0].domain, site.not_modifier))
                else:
                    mod_domains.append('%s~%s~%s' % (site.components[0].domain, site.not_modifier, site.modifier))
        mod_domains.sort()
        domains += mod_domains

        # 3. Binding domains
        bind_domains = []    
        # This part is different for molecules and complexes 
        for binding in mol.binding_partners: # binding is a State object
            if binding.type == 'Intraprotein':
                doms = self.get_ipi_binding_domains(binding)
                for dom in doms:
                    if dom not in used_domains:
                        bind_domains.append(dom)
                        used_domains.append(dom)
            else:
                doms = self.get_binding_domain_for_molecules(mol.name, binding, mol.mid)
                for dom in doms:
                    if dom not in used_domains:
                        bind_domains.append(dom)
                        used_domains.append(dom)

        for site in mol.binding_sites:
            if site.type == 'Intraprotein':
                doms = self.get_ipi_binding_domains(site)
                for dom in doms:
                    if dom not in used_domains:
                        bind_domains.append(dom)
                        used_domains.append(dom)
            else:
                doms = self.get_binding_domain_for_molecules(mol.name, site, mol.mid)
                for dom in doms:
                    if dom not in used_domains:
                        bind_domains.append(dom)
                        used_domains.append(dom)

        bind_domains.sort()
        domains += bind_domains

        if domains:
            result = "%s(%s)" %(mol.name, ','.join(domains))
        else:
            result = mol.name
        return re.sub('[-/]', '', result)

    def get_species_str(self, mol):
        """
        Returns molecule string.
        String contains:
        - all modification sites with False modifier
        - all binding domains as not bound.
        - there is no localisation information included ???
        """
        return self.get_molecule_str(mol, 'species')

    def get_reaction_header(self, rule_container):
        """"""
        result = '%s%3s####%s###\n' % ('#'*27, rule_container.rid, rule_container.name) 
        cont = rule_container.contingencies
        if cont:       
            result += "# Contingencies: %s\n" % str(cont) 
        common_reqs = self.get_reqs_str(rule_container.common_reqs)
        if common_reqs:
            result += "# Absolute requirements: %s\n" % common_reqs
        result += "# Source states:  %s %s\n" % (str(rule_container.sp_state), 'False')
        result += "# Product states: %s %s\n" % (str(rule_container.sp_state), 'True')
        return result

    def get_rule_header(self, rule):
        """"""
        out = "#>>>>>>>>> Rule: %s\n" % rule.rid
        out += "# Optional requirements: %s\n" % self.get_reqs_str(rule.specific_reqs)#%s\n" % ', '.join([str(req) for req in additional_reqs])
        return out

    def get_rule_str(self, rule):
        """
        """    
        reactants = []
        for compl in sorted(rule.reaction.substrat_complexes, key=lambda comp: comp.side):
            #sorted(range(len(aa)), key=lambda a: aa[a])
            reactants.append(self.get_complex_str(compl))
        products = []
        for compl in sorted(rule.reaction.product_complexes, key=lambda comp: comp.side):
            products.append(self.get_complex_str(compl))
        reactant_str = ' + '.join(reactants)
        product_str = ' + '.join(products)
        rate_str = ', '.join(rule.rates)
        return "%s %s %s    %s\n" % (reactant_str, rule.arrow, product_str, rate_str)

    def get_reqs_str(self, cont_list):
        """"""
        present = lambda cont: 'False' if cont.ctype =='x' else 'True' 
        return ', '.join(['%s %s' % (str(cont.state), present(cont)) for cont in cont_list])

    def get_warning_str(self, warnings):
        """"""
        result = ''
        #if states_set:
        #    for state in states_set:
        #        result += "# WARNING: required state %s not produced in the reactions. \
        #Add the coresponding reaction or the appropriate molecule types and seed species.\n" % state
        if warnings:
            for state in warnings.not_in_products:
                result += "# WARNING: required state %s not produced in the reactions. \
Add the coresponding reaction or the appropriate molecule types and seed species.\n" % state
            for cont in warnings.produced_in_more.keys():
                result += "# WARNING: %s has two phosphorylation sites. \
Indicate which phosphorylation should be used in contingency by adding a domain \
.\n" % (cont.state.components[0].name) 
            for reaction in warnings.get_problem_reaction_str():
                result += "# WARNING: Contingencies can not be applied on reaction: %s.\n" % reaction
        return result

class BnglOutput:
    """
    BioNetGenOutput object creates all sections for BNGL file.
    Uses rule and molecules generated by BioNetGen. 
    """
    def __init__(self, rule_pool, molecule_pool, warnings=None):
        self.rule_pool  = rule_pool
        self.molecules = molecule_pool.get_system_molecules().values()
        self.translator = BnglTranslator()
        self.rates = []
        self.max_stoich = 4
        #self.warning_states = warning_states
        self.warnings = warnings

    def create_sections_txt(self):
        self.create_rules_section()
        self.create_molecule_type_section()
        self.create_seed_species_section()
        self.create_parameters_section()
        self.create_action()
        self.create_worning_section()

    def format_string(self, name, value):
        """Formats one section string."""
        return 'begin %s\n%s\nend %s\n\n' %(name, value.strip(), name)

    def get_src(self):
        """Returns BNGL source code as a string."""
        self.observables_txt = self.format_string('observables', '')
        self.create_sections_txt()
        model = '%s%s%s%s%s' %(self.parameters_txt, self.molecules_txt, self.species_txt, self.observables_txt, self.rules_txt)
        bngl_text = self.format_string('model', model) + self.action_txt.strip()
        bngl_text = self.worning_txt + bngl_text
        return bngl_text

    def format_string(self, name, value):
        """Formats one section string."""
        return 'begin %s\n%s\nend %s\n\n' %(name, value.strip(), name)

    def create_worning_section(self):
        """"""
        self.worning_txt = self.translator.get_warning_str(self.warnings)

    def create_molecule_type_section(self):
        """"""
        result = ""
        for mol in sorted(self.molecules, key=lambda molecule: molecule.name):
            mol_str = self.translator.get_molecule_str(mol)
            result += mol_str + '\n'
        self.molecules_txt = self.format_string('molecule types', result)

    def create_seed_species_section(self):
        """"""
        result = ""
        for mol in sorted(self.molecules, key=lambda molecule: molecule.name):
            result += "%-90s 100\n" % self.translator.get_species_str(mol)
        self.species_txt = self.format_string('seed species', result)

    def create_rules_section(self):
        """"""
        result = ""
        for rule_container in sorted(self.rule_pool, key=lambda rcont: rcont.rid):
            result += self.translator.get_reaction_header(rule_container)
            for rule in rule_container:
                if rule.header:

                    result += self.translator.get_rule_header(rule)
                result += self.translator.get_rule_str(rule)
                self.rates += rule.rates 
        self.rules_txt = self.format_string('reaction rules', result)

    def create_parameters_section(self):
        """"""
        special_rates = {}
        normal_rates = {}
        special_param_str = "# input parameters\n"
        normal_param_str = "# normal parameters\n"
        for rule_container in sorted(self.rule_pool, key=lambda rcont: rcont.rid):
            for rule in rule_container:
                for rate in sorted(rule.rate_values.keys()):
                    if rate.startswith('k_'):
                        special_rates[rate] = rule.rate_values[rate]
                    else:
                        if rate not in normal_rates.keys():
                            normal_param_str += "%s %s\n" % (rate, rule.rate_values[rate])
                            normal_rates[rate] = rule.rate_values[rate]
        for rate in special_rates.keys():
            special_param_str += "%s %s\n" % (rate, special_rates[rate])
        self.parameters_txt = self.format_string('parameters', special_param_str + normal_param_str.strip())
        #result = ""
        #for rate in self.rates:
        #    result += "%s 1\n" % rate
        #self.parameters_txt = self.format_string('parameters', result)

    def create_action(self):
        """"""
        self.action_txt = "generate_network({overwrite=>1,max_stoich=>{%s}});" % \
            ','.join(['%s=>%s' % (mol.name, self.max_stoich) for mol in sorted(self.molecules, key=lambda molecule: molecule.name)])
