#!/usr/bin/env python

"""
Class ReactionDefinitions - facilitates using reaction definitions.
"""

import re
from rxnconcompiler.definitions.reaction_template import REACTION_TEMPLATE
STATE_DOMAIN_PATTERN = re.compile(r'(.*)-\{(.*)}')

class ReactionDefinitions(dict):
    """Class that gathers all reaction definitions parsing."""

    def __init__(self, xls_tables):
        dict.__init__(self)
        self.xls_tables = xls_tables

        self.def_template = self.get_reaction_defintions_template_dict(REACTION_TEMPLATE)
        self.get_reaction_definitions_dict()

    def get_reaction_defintions_template_dict(self, template_list):
        def_template = {}
        for template in template_list:
            def_template[template['ReactionTypeID']] = template
        return def_template

    def get_reaction_definitions_dict(self):
        """returns row from reaction_definition table."""
        for rrow in self.xls_tables['reaction_definition']:
            if 'UID:Reaction' in rrow:
                self[rrow['UID:Reaction'].lower()] = rrow

                self[rrow['UID:Reaction'].lower()].update(self.def_template[rrow['ReactionTypeID']])
            else:
                self[rrow['Reaction'].lower()] = rrow

    def get_localization_modifications(self):
        """
        Parsing possible localizations from reactions definitions from xls.
        Result is a dict {'Endosome':'Endosome', ...}
        """
        localization_modifications = {}
        for row in self.xls_tables['reaction_definition']:
            if row['ReactionTypeID'] and (int(row['ReactionTypeID'].split(".")[0]) == 4):

                mod_list = row['SourceState[Modification]'].split(',')
                mod_list += row['ProductState[Modification]'].split(',')
                mod_list = [x.strip() for x in mod_list]           
                for loc_mod in mod_list:
                    state = re.match(STATE_DOMAIN_PATTERN, loc_mod).group(2)
                    localization_modifications[state] = state
        return localization_modifications

    @property
    def directionality_dict(self):
        """returns a dictionary of reaction definitions -> directionality"""
        result = {}
        for row in self.xls_tables['reaction_definition']:
            if row['Reaction']:
                assert type(row['Reaction']) in (type(u"a"), type("a"))  # raise serious cases
                reaction_id = re.sub('\+','_plus', row['Reaction']).lower()
                result[reaction_id] = row['Directionality']
            #else:
                #TODO: reaction definition has no proper ID. What to do? Raise or fold?
                #print 'WARNING: Reaction definition has no proper ID: %s'%str(row)
        return result

    def get_reaction_category(self, rtype):
        """Given p+ returns 'Covalent Modification'"""
        return self[rtype]['Category'] 

    def get_reaction_subclass(self, rtype):
        """
        Given reaction type returns subclass.
        e.g. for p+ returns 'Covalent_trans_positive'
        """
        pass

    @property
    def categories_dict(self):
        """
        Returns dict with four categories as keys 
        and all reactions list as value.
        """      
        cat_dict = {}
        for definition in self:
            if 'Category' in self[definition]: # if Category is not in self[definition] we don't saw this definition during the parsing step and don't need it
                cat = self[definition]['Category']
                cat_dict.setdefault(cat, [])
                if 'Reaction' in self[definition]:
                    cat_dict[cat].append(self[definition]['Reaction'].lower())
                else:
                    cat_dict[cat].append(self[definition]['UID:Reaction'].lower())
        if cat_dict.has_key(''): 
            del(cat_dict[''])
        return cat_dict
        
