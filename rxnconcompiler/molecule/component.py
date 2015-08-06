#!/usr/bin/env python

"""
Class Component    - cleaps information about name, domain and id.
"""

from domain_factory import DomainFactory

class Component:
    """
    Component object keeps informations about name, domain and id.
    It is used in State. 
    """
    def __init__(self, name, domain=None, cid=None):
        self.name = name.strip()
        self.domain = domain
        if self.domain:
            self.domain = self.domain.strip()
        self.cid = cid
        self.second_domain = None  # for ipi states

    def __repr__(self):
        #return str((self.name , self.domain, self.cid))
        if self.second_domain:
            return '%s_[%s]_[%s]' % (self.name, self.domain, self.second_domain)
        elif self.domain:
            return '%s_[%s]' % (self.name, self.domain)
        return self.name 

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if self.cid and other.cid and self.cid != other.cid:
            return False
        return True

    def __cmp__(self, other):
        if self.name < other.name:  # compare name value (should be unique)
            return -1
        elif self.name > other.name:
            return 1
        elif self.name == other.name and self.cid and other.cid:
            if self.cid < other.cid:
                return -1
            elif self.cid > other.cid:
                return 1
        else: return 0        

    def exact_compare(self, other):
        """
        Checks not only name (__cmp__) but also domain.
        """
        if not self == other:
            return False
        if self.domain != other.domain: 
            return False
        if self.second_domain != other.second_domain:
            return False
        return True