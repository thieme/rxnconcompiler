#!/usr/bin/env python

"""
Module domain_factory.py
Names all domains in rxncon.

--------------------
Association Domains:
--------------------

Default domain is ASSOCIATION_PRE + name of the binding partner. 
Uper and lower case preserved as it is.
No conflicts. It is possible to match reactions with contingencies.

Examples:
Reaction: A_ppi_B --> A_[AssocB]--B_[AssocA] (BNGL: A(AssocB!1).B(AssocA!1))
Contingency: A--B --> A_[AssocB]--B_[AssocA]
Reaction: X_BIND_DNA --> X_[AssocDNA]--DNA_[AssocX] (BNGL: X(AssocDNA!1).DNA(AssocX!1))
Contingency: X--DNA --> X_[AssocDNA]--DNA_[AssocX]

------------------------------
Covalent Modification Domains:
------------------------------

Problem: default domain created in a reaction is not identical with default domain used in contingencies.
Solution: rxncon recognises that default A_[bd]-{P} can match A-[anything]-{P}.
1. rxncon searches through the present product states.
2. It exchanges bd with other domain name (to avoid errors while runing BioNetGen).
3. If there are no reaction that produces A-{P} - generates WARNING. 
4. When there are two such reactions: takes the first one as a default and generates WARNING.

Example:
Reaction: X_P+_A --> A_[X]-{P} (BNGL: A(X~P))
Reaction: Y_P+_A --> A_[Y]-{P} (BNGL: A(Y~P))
Contingency: A-{P} 
If no reaction that phosphorylates A is present: --> A_[bd]-{P} (BNGL: A(bd~P))
# WARNING: required state A_[bd]-{P} not produced in the reactions. Add the corresponding reaction or the appropriate molecule types and seed species.
If the reactions above are present: --> A_[X]-{P} (BNGL: A(X~P))
# WARNING: A has two phosphorylation sites. Indicate which phosphorylation should be used in contingency by adding a domain (by default: A_[X]-{P})
If only one phosphorylation reaction is present --> no WARNING.

----------------------
Relocalisation Domains:
----------------------

loc

-------
General:
-------

- sign '-' and '/' should not appear in domain names ---> errors in BioNetGen
  (Now it is removed in bngl_output.py)

"""

# TODO: would be great to have get_domain and 
#       automatically recognize input (dict or str)
#       and type of state.
#       Could be Abstract Domain Pattern with 
#       DomainFactory and DictDomainFactory and StrDomainFactory.

import re

ASSOCIATION_PRE = 'Assoc'

class DomainFactory:
    """
    """
    def __init__(self):
        pass

    def get_localisation_domain(self):
        """
        """
        return 'loc'

    def get_dsr(self, row, ab='A', with_delimiters=False):
        cmpnt = 'Component%s%%s' % ab
        if not with_delimiters:
            if row.has_key(cmpnt % '[DSR]'):
                return re.sub('[/\(\)]', '', row[cmpnt % '[DSR]']) if row[cmpnt % '[DSR]'] else None
            dsr = "%s%s%s" % (
                    "%s" % row[cmpnt%'[Domain]'] if row[cmpnt%'[Domain]'] else '',
                    "%s" % row[cmpnt%'[Subdomain]'] if row[cmpnt%'[Subdomain]'] else '',
                    "%s" % row[cmpnt%'[Residue]'] if row[cmpnt%'[Residue]'] else '',
                )
            if not dsr:
                #dsr = 'bd0'+row['Component%s[Name]'%('A' if ab=='B' else 'B')]
                dsr = None
            if dsr:
                dsr = re.sub('\W', '', dsr)
        elif row.has_key(cmpnt%'[DSR]'):
                return row[cmpnt%'[DSR]']
        else:
            dsr = "%s%s%s"%(
                    "%s"%row[cmpnt%'[Domain]'] if row[cmpnt%'[Domain]'] else '',
                    "/%s"%row[cmpnt%'[Subdomain]'] if row[cmpnt%'[Subdomain]'] else '',
                    "(%s)"%row[cmpnt%'[Residue]'] if row[cmpnt%'[Residue]'] else '',
                )
        return dsr

    def get_association_domain_from_str(self, state_str, side='A'):
        """
        Produces domain string for associations.
        It gets state string as an input.
        Domain can be provided by the user. 
        If not default domain is a name of the partner.
        'A' or 'B' indicates wheter function should return domain for 
        left or for right partner.

        e.g. 
        Fu--Bla, 'A' --> 'Bla'  
        Fu_[x]--Bla_[y], 'B' --> 'y'

        Used e.g. in contingencies parsing.
        """
        comp = state_str.split('--')
        if side == 'A':
            if '_' in comp[0]:
                # domain provided by the user.
                return re.sub('[\(\)\]\[:/]', '', comp[0].split('_')[1])
            else:
                # default domain: name of the partner. 
                partner_name = re.sub('[\(\)\]\[:/]', '', comp[1].split('_')[0])
                return '%s%s' % (ASSOCIATION_PRE, partner_name)
        elif side == 'B':
            if '_' in comp[1]:
                # domain provided by the user.
                return re.sub('[\(\)\]\[:/]', '', comp[1].split('_')[1])
            else:
                # default domain: name of the partner. 
                partner_name = re.sub('[\(\)\]\[:/]', '', comp[0].split('_')[0])
                return '%s%s' % (ASSOCIATION_PRE, partner_name)

    def get_association_domain_from_dict(self, row, side='A'):
        """
        Returns name of domain for association.
        row - row from xls_tables.
        side - A or B indicating left or right side of association.
        A: get domain name for left reactant 
        (by defult name of partner - right reactant)
        """
        if side == 'A':
            if row.has_key('ComponentA[DSR]'):
                a_dsr = row['ComponentA[DSR]']
            else:
                a_dsr = self.get_dsr(row, 'A')
            return a_dsr or ('%s%s' % (ASSOCIATION_PRE, row['ComponentB[Name]']))

        elif side == 'B':
            if row.has_key('ComponentB[DSR]'):
                b_dsr = row['ComponentB[DSR]']
            else:
                b_dsr = self.get_dsr(row, 'B')
            return b_dsr or ('%s%s' % (ASSOCIATION_PRE, row['ComponentA[Name]']))
         
    def get_intraprotein_domain_from_dict(self, row, side='A'):
        """
        Returns name of domain for association.
        row - row from xls_tables.
        side - A or B indicating left or right side of association.
        A: get domain name for left reactant 
        (by defult name of partner - right reactant)
        """
        if side == 'A':
            if row.has_key('ComponentA[DSR]'):
                a_dsr = row['ComponentA[DSR]']
            else:
                a_dsr = self.get_dsr(row, 'A')
            return a_dsr or ('%s%s%i' % (ASSOCIATION_PRE, row['ComponentB[Name]'], 1))

        elif side == 'B':
            if row.has_key('ComponentB[DSR]'):
                b_dsr = row['ComponentB[DSR]']
            else:
                b_dsr = self.get_dsr(row, 'B')
            return b_dsr or ('%s%s%i' % (ASSOCIATION_PRE, row['ComponentA[Name]'], 2))

    def get_modification_domain_from_str(self, state_str):
        """ 
        It is used in ...
        """
        comp_name_dom = state_str.split('-{')[0].split('_')
        if len(comp_name_dom) == 1:
            return 'bd'
        else:
            return re.sub('\(|\)|\[|\]', '', comp_name_dom[1])

    def get_modification_domain_from_dict(self, row, reaction):
        """
        """
        if row.has_key('ComponentB[DSR]'):
            b_dsr = row['ComponentB[DSR]']
        else:
            b_dsr = self.get_dsr(row, 'B')
        if b_dsr:
            return re.sub('\(|\)|\[|\]', '', b_dsr)
      
        domain = row['ComponentA[Name]'] 
        return re.sub('\(|\)|\[|\]', '', domain)  
            
