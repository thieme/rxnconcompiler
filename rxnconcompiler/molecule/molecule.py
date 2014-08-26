#!/usr/bin/env python

"""
Module molecule.py.
"""

import copy 
from state import get_state, Component
from contingency.contingency import Contingency

# TODO: function __add__ in Molecules requires more attention.
# TODO: more attention needed for domains in the small functions.
#       what to do when domain is already there?
# TODO: use cases how to add and remove states should be better defined.

"""
Each molecule gets its own internal id.
Molecules in the complex are unique,
even when they have the same name.
"""
def id_gen():
    counter = 1
    while True:
        yield counter
        counter += 1

get_id = id_gen()

class MoleculePool(list):
    """
    MoleculePool object is a list of all reactants.
    During reactions parsing left and right reactant 
    are added to molecule_pool. 
    Containes Molecule instances. 
    """
    def __init__(self):
        list.__init__(self) 

    def get_system_molecules(self):
        """
        Returns a dictionery of all molecules present in the system.
        Molecules have all possible domains and alternative localisations recorded.
        Molecule that appears in two independent reactions as independent instance
        will be represented as one molecule with domains from both reactions.

        molecule_name: MoleculeInstance
        """
        temp = {}
        for mol in self:
            
            conts = mol.get_contingencies()


            if mol.name in temp.keys():
                conts_in = temp[mol.name]
                for cont in conts:
                    if str(cont) not in [str(x) for x in conts_in]:
                        temp[mol.name].append(cont)
            else:
                temp[mol.name] = mol.get_contingencies()

        result = {}
        for mol in temp.keys():
            mol_ob = Molecule(mol)
            for cont in temp[mol]:
                mol_ob.add_contingency(cont)
            result[mol] = mol_ob
        return result



class Molecule:
    """
    Keeps data about a single molecule and its state.
    Molecule objects can be added.
    States can be added and removed to Molecule (e.g. add_bond, ...).
    Information about states, contingencies and domains can be obtained.
    """
    def __init__(self, name):
        """
        Molecule holds information about:
        - name
        - bound molecules
        - empty binding sites  
        - modifications
        - empty modification sites
        - localisation
        """
        self.name = name
        self._id = get_id.next()
        self.binding_partners = [] 
        self.binding_sites = [] # empty
        self.modifications = [] 
        self.modification_sites = [] #
        self.localisation = None   
        self.mid = None  
        self.alternative_localisations = []
        self.is_reactant = False  # indictes that molecule take part in a reaction.

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not self.name == other.name:
            return False
        if self.mid and other.mid and self.mid != other.mid:
            return False
        return True

    def __hash__(self):
        """
        Hash is molecule name and _id).
        """
        return (self.name+str(self._id)).__hash__()

    def __add__(self, other):
        """
        molA + molB means that molA will have additional:
        - modifications
        - modification_sites
        - binding_partners
        - binding_sites
        - info about alternative localisations
        comming from molB.
        Mol B won't change.
        """
        for mod in other.modifications:
            if mod not in self.modifications:
                self.modifications.append(mod)
        for site in other.modification_sites:
            if site not in self.modification_sites:
                self.modification_sites.append(site)
        for partner in other.binding_partners:
            if partner not in self.binding_partners:
                self.binding_partners.append(partner)
        for site in other.binding_sites:
            if site not in self.binding_sites:
                self.binding_sites.append(site)
        if self.localisation != other.localisation:
            self.alternative_localisations.append(other.localisation)
        #KR: when overloading the '+' operator with __add__
        #    I expect the method to return something.
        #    If it doesnt this is confusing.
        #    Probably it would be better to rename the method
        #    to any of merge(), join(), combine() 
        """
        TODO: change this method into:
        new = self.clone()
        for mod in other.modifications:
            if mod not in new.modifications:
                new.modifications.append(mod)
        for site in other.modification_sites:
            if site not in new.modification_sites:
                new.modification_sites.append(site)
        for partner in other.binding_partners:
            if partner not in new.binding_partners:
                new.binding_partners.append(partner)
        for site in other.binding_sites:
            if site not in new.binding_sites:
                new.binding_sites.append(site)
        if new.localisation != other.localisation:
            new.alternative_localisations.append(other.localisation)
        return new
        """

    def inspect(self):
        """
        Prints long summary about the molecule
        """
        print "### MOLECULE: %s (%s, %s)" % (self.name, self._id, self.mid)
        print "Binding sites:      %s" % str(self.binding_sites)
        print "Binding partners:   %s" % str(self.binding_partners)
        print "Modifications:      %s" % str(self.modifications)
        print "Modification sites: %s" % str(self.modification_sites)
        # print "Localisation:       %s" % str(self.localisation) 

    def clone(self):
        """
        Clones itself.
        E.g. returns another instance of itself
        which can be modified without modifing the origin.
        """
        #KR: this copying means we're in performance hell.
        #    As long as the MAPK runs OK --> no problem.
        #    
        #    long-term question: 
        #       When MK wrote in the grant that his approach avoids
        #       performance isssues of other methods,
        #       does it really?

        name = copy.deepcopy(self.name)
        new = Molecule(name)
        new.binding_partners = copy.deepcopy(self.binding_partners) 
        new.binding_sites = copy.deepcopy(self.binding_sites)
        new.modifications = copy.deepcopy(self.modifications) 
        new.modification_sites = copy.deepcopy(self.modification_sites) 
        new.localisation = copy.deepcopy(self.localisation)   
        new.mid = copy.deepcopy(self.mid)  
        new.alternative_localisations = copy.deepcopy(self.alternative_localisations)
        new.is_reactant = copy.deepcopy(self.is_reactant)
        return new

    def get_contingencies(self):
        """
        Returns all states asociated with this molecule
        based on associations, modifications and localisation

        """ 
        result = [] 
        for site in self.binding_sites:
            result.append(Contingency(None, 'x', site))
        for partner in self.binding_partners:
            result.append(Contingency(None, '!', partner))
        for site in self.modification_sites:            
            result.append(Contingency(None, 'x', site))#.get_state(self.name)))
        for modif in self.modifications:            
            result.append(Contingency(None, '!', modif))#.get_state(self.name)))
        if self.localisation:
            result.append(Contingency(None, '!', self.localisation))
        return result
          
    def get_component(self):
        """
        Returns molecule as Component instance.
        There is just information about name and no domains.
        @rtype: Component
        """
        return Component(self.name, None, self.mid)

    def has_state(self, state):
        if state in self.binding_partners:
            return True
        if state in self.binding_sites:
            return True
        if state in self.modifications:
            return True
        if state in self.modification_sites:
            return True
        if self.localisation and state == self.localisation:
            return True
        return False

    def has_bond(self, state):
        """"""
        # TODO: exchange all the small functions with StateApplicator. 
        if state in self.binding_partners:
            return True
        return False

    def has_binding_site(self, state):
        """
        TODO: collaps all has functions to one.
        #KR: why? I like it.
        """
        if state in self.binding_sites:
            return True
        return False

    def add_bond(self, state):
        """
        TODO: find a comon interface and colaps all 
              add/remove functions to add_state
        """
        self.binding_partners.append(state)
        #KR: can one molecule have the same state twice?
        if state in self.binding_sites:
            self.binding_sites.remove(state)
        empty_domains = self.get_empty_binding_domains_states_dict()
        comp = state.get_component(self.name)
        if comp.domain in empty_domains.keys():
            self.binding_sites.remove(empty_domains[comp.domain]) 

    def get_empty_binding_domains_states_dict(self, side = 'L'):
        """
        Goes throughmolecule.binding_sites and
        returns {'a': A_[a]--B_[b], ...}
        """
        result = {}
        for state in self.binding_sites:
            result[state.get_component(self.name, side).domain] = state
        return result

    def get_domains(self, mode, occupied, side = 'L'):
        """
        Returns a list of domains.
        mode and occupied indicate which domains are we looking for:
        binding or covlent or binding, occupied or free.

        Side indicates which domain to pick in case of homodimers.
        """
        # decide for which type of domains to search:
        if mode == 'binding' and occupied:
            to_search = self.binding_partners
        elif mode == 'binding' and not occupied:
            to_search = self.binding_sites
        elif mode == 'modification' and occupied:
            to_search = self.modifications
        elif mode == 'modification' and not occupied:
            to_search = self.modification_sites
        else:
            raise 'Wrong domain search mode'

        # looking for domains in proper list
        result = []
        for state in to_search:
                component = state.get_component(self.name, side)
                if component:
                    result.append(component.domain)
                    if state.type == "Intraprotein":
                        result.append(component.second_domain)
        return result

    def get_all_domains(self, side='L'):
        """
        Returns a list of all domains
        (both binding and modification and
        both empty and occupied).

        side - indicaes which domain to pick when 
               there is an association which is a homodimer.

        Localisation is not included.
        """
        doms = self.get_domains('binding', True, side)
        doms += self.get_domains('binding', False, side)
        doms += self.get_domains('modification', True, side)
        doms += self.get_domains('modification', False, side)
        return list(set(doms))

    def domain_is_present(self, domain, side = 'L'):        
        """
        Checks whether domain name is present already.
        """
        doms = self.get_all_domains(side)
        if domain in doms:
            return True
        return False


    def add_binding_site(self, state, side = 'L'):
        """
        side indicates in case of homodimers which 
        component (domain) should be taken into account.
        """
        # we cannot have two identical binding sites,
        # domain names need to be different.
        dom = state.get_component(self.name).domain
        if not self.domain_is_present(dom, side):

        #if hash(state) not in [hash(st) for st in self.binding_sites]:
            state_comp = state.get_component(self.name)
            if not state_comp:
                self.binding_sites.append(state)
            elif state_comp :#and state_comp.domain not in self.get_empty_binding_domains():
                self.binding_sites.append(state)

    def remove_bond(self, state, empty_domain=True):
        """"""
        if self.has_bond(state):
            self.binding_partners.remove(state)
            if empty_domain:
                self.binding_sites.append(state)

    def remove_binding_site(self):
        """"""
        if self.has_binding_site(state):
            self.binding_sites.remove(state)

    def add_modification(self, mod):
        """
        Adds modification state to molecule.modifictions.
        If this modification in present in molecule.modification_sites
        then checks whether domain is the same and if yes, removes 
        state from molecule.modification_sites.
        """
        self.modifications.append(mod)
        to_remove = None
        for mod_site in self.modification_sites:
            if mod_site == mod and \
            mod_site.components[0].domain == mod.components[0].domain:
                to_remove = mod_site
        #if to_remove:

        if to_remove:
            temp = []
            for x in self.modification_sites:
                if x == to_remove:
                    if x.components[0].domain == to_remove.components[0].domain:
                        pass
                    else:
                        temp.append(x)
                else:
                    temp.append(x) 

                # Possible we have bug there
            self.modification_sites = temp


    def add_modification_site(self, mod):
        """"""
        #if mod not in self.modification_sites:
        self.modification_sites.append(mod)

    def remove_modification(self, mod):
        """"""
        self.modifications.remove(mod)
        self.modification_sites.append(mod)

    def add_contingency(self, cont):
        """
        Adds given contingency to the molecule.
        """
        if cont.ctype == 'x' and cont.state.type in ['Association', 'Intraprotein']:
            self.add_binding_site(cont.state)
        elif cont.ctype == '!' and cont.state.type in ['Association', 'Intraprotein']:
            self.add_bond(cont.state)
        elif cont.ctype == 'x' and cont.state.type == 'Covalent Modification':
            self.add_modification_site(cont.state)
        elif cont.ctype == '!' and cont.state.type == 'Covalent Modification':
            self.add_modification(cont.state)
        elif cont.ctype == '!' and cont.state.type == 'Relocalisation':
            self.localisation = cont.state
        elif cont.ctype == 'x' and cont.state.type == 'Relocalisation':
            self.alternative_localisations.append(cont.state)
