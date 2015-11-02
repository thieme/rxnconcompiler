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

class Domain:
    """domain onject"""

    def __init__(self,dsr):
        """Constructor for Domain"""
        self.main = ""
        self.sub = ""
        self.residue = ""
        self.get_domain_subdomain_residue(dsr)
        self.raw_name = dsr
        self.name = re.sub('[\(\)\]\[:/]', '',dsr)

    def __repr__(self):
        return self.raw_name

    def set_domain_info(self, main, sub, residue):
        dsr = ""
        if main:
            dsr += main
            if sub:
                dsr += "/%s"%sub
            if residue:
                dsr += "(%s)"%residue
        elif residue:
            dsr += "(%s)"%residue

        self.get_domain_subdomain_residue(dsr)
        self.raw_name = dsr
        self.name = re.sub('[\(\)\]\[:/]', '',dsr)

    def get_domain_subdomain_residue(self, dsr):
        domain = re.sub('\[|\]', "", dsr)
        domain = re.match('(\w*)/?(\w*)\(?(\w*)\)?',domain)
        self.main = domain.group(1)
        self.sub = domain.group(2)
        self.residue = domain.group(3)


class DomainFactory:
    """
    """
    def __init__(self):
        pass

    def get_localisation_domain(self):
        """
        """
        return Domain('loc') # loc domain object

    def get_dsr(self, row, ab='A', with_delimiters=False):
        """
        get the domain information from parsed row and translated this information in an domain object
        @param row: dictionary of the current information row
        @param ab: Compartment A or B
        @param with_delimiters:
        @return: Domain object
        """
        cmpnt = 'Component%s%%s' % ab
        if not with_delimiters:
            if row.has_key(cmpnt % '[DSR]'):
                domain = Domain(row[cmpnt % '[DSR]'])
                if domain:
                    return domain

            dsr = Domain("")
            dsr.set_domain_info(row[cmpnt%'[Domain]'], row[cmpnt%'[Subdomain]'], row[cmpnt%'[Residue]'])

            if dsr.name:
                dsr.name = re.sub('\W', '', dsr.name)
        elif row.has_key(cmpnt%'[DSR]'):
                return Domain(row[cmpnt%'[DSR]'])
        else:
            dsr = Domain("")
            dsr.set_domain_info(row[cmpnt%'[Domain]'], row[cmpnt%'[Subdomain]'], row[cmpnt%'[Residue]'])
        return dsr

    def get_association_domain_from_str(self, state_str, side='A', domain=None):
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
                if domain != None:
                    domain = domain
                else:
                    domain = Domain(comp[0].split('_')[1])

                return domain

            else:
                # default domain: name of the partner. 
                partner_name = re.sub('[\(\)\]\[:/]', '', comp[1].split('_')[0])  # In case of Intraprotein interaction there is a [ in the partner
                default_domain = '%s%s' % (ASSOCIATION_PRE, partner_name)
                domain = Domain(default_domain)

                return domain
        elif side == 'B':
            if '_' in comp[1]:
                # domain provided by the user.
                if domain is not None:
                    return domain
                else:
                    domain = Domain(comp[1].split('_')[1])
                return domain
            else:
                # default domain: name of the partner. 
                partner_name = re.sub('[\(\)\]\[:/]', '', comp[0].split('_')[0])
                default_domain = '%s%s' % (ASSOCIATION_PRE, partner_name)
                domain = Domain(default_domain)

                return domain

    def get_association_domain_from_dict(self, row, side='A'):
        """
        Returns name of domain for association.
        row - row from xls_tables.
        side - A or B indicating left or right side of association.
        A: get domain name for left reactant 
        (by defult name of partner - right reactant)
        """
        if side == 'A':

            a_dsr = self.get_dsr(row, 'A')
            if a_dsr.name:
                return a_dsr
            else:
                return Domain('%s%s' % (ASSOCIATION_PRE, row['ComponentB[Name]']))

        elif side == 'B':

            b_dsr = self.get_dsr(row, 'B')

            if b_dsr.name:
                return b_dsr
            else:
                return Domain('%s%s' % (ASSOCIATION_PRE, row['ComponentA[Name]']))
         
    def get_intraprotein_domain_from_dict(self, row, side='A'):
        """
        Returns name of domain for association.
        row - row from xls_tables.
        side - A or B indicating left or right side of association.
        A: get domain name for left reactant 
        (by defult name of partner - right reactant)
        """
        if side == 'A':

            a_dsr = self.get_dsr(row, 'A')

            if a_dsr.name:
                return a_dsr
            else:
                return Domain('%s%s%i' % (ASSOCIATION_PRE, row['ComponentB[Name]'], 1))

        elif side == 'B':

            b_dsr = self.get_dsr(row, 'B')
            if b_dsr.name:
                return b_dsr
            else:
                return Domain('%s%s%i' % (ASSOCIATION_PRE, row['ComponentA[Name]'], 2))


    def get_modification_domain_from_str(self, state_str):
        """ 

        """
        comp_name_dom = state_str.split('-{')[0].split('_')
        if len(comp_name_dom) == 1:
            return Domain('bd')
        else:
            return Domain(comp_name_dom[1])

    def get_modification_domain_from_dict(self, row, component='B'):
        """
        """
        if component == 'B':

            b_dsr = self.get_dsr(row, 'B')

            if b_dsr.name:
                return b_dsr
            else:
                domain = row['ComponentA[Name]']  # modification default domain
                return Domain(re.sub('\(|\)|\[|\]', '', domain))
            
        elif component == 'A':

            a_dsr = self.get_dsr(row, 'A')

            if a_dsr.name:
                return a_dsr
            else:
                domain = row['ComponentB[Name]'] # default domain for modification
                return Domain(re.sub('\(|\)|\[|\]', '', domain))