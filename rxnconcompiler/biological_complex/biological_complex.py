#!/usr/bin/env python

"""
Module biological_complex.py

Classes:
BiologicalComplex: Contans Molecule[s].
                   Molecules have particular states.
                   Based on Molecules composition and their states enables to obtain 
                   information about conections.
                   Molecules can be added and removed.

AlternativeComplexes: Contains BiologicalComplex[es].
                      that may be build in alternative way (boolean OR)

ComplexPool: Stors all (positive) complexes in the system.
"""

import copy
from contingency.contingency import Contingency
from molecule.molecule import Molecule

#KR: please complete docstrings

class BiologicalComplex:
    """"""
    def __init__(self):
        self.molecules = []
        self.side = None #: indicate where complex appears: L, R, LR
        self.input_conditions = [] # defines that e.g. complex exists only when Start, Osmostress ...
        self.is_positive = True
        self.is_modifier = False # indicates that complex does not change during the reaction

    def __repr__(self):
        mols = ', '.join(sorted([mol.name for mol in self.molecules]))
        return 'Complex: ' + mols

    def __len__(self):
        """
        Complex length is equal to the number of its molecules.

        @rtype:  int
        @return: number of molecules.
        """
        return len(self.molecules)

    def inspect(self):
        """
        Prints detailed information about a complex.
        """
        print '### %s' % self
        for mol in self.molecules:
            mol.inspect()

    def complex_addition(self, other, root=None):
        """
        Complex A + Complex B
        """
        # MR: TODO: add BiologicalCalculator
        #KR: split into two methods (with/without root)
        new = self.clone()
        for mol in other.molecules:
            if mol not in new.molecules:
                new.molecules.append(mol)
            elif not root:
                new.molecules.append(mol)
            elif root:
                path = self.get_shortest_path(root, mol)
                path_other = other.get_shortest_path(root, mol)
                if str(path) == str(path_other) or mol == root:
                    dup_mol = new.get_molecules(mol.name, mol.mid)[0]
                    dup_mol = dup_mol + mol
                else:
                    new.molecules.append(mol)
        return new

    def get_partners(self, mol_name, mid=None):
        """
        Returns a list of all molecules 
        adjacent to the molecule with the given name 
        (and optionally id).
        """
        result = []
        mol = self.get_molecules(mol_name, mid)[0]
        component = mol.get_component()
        for state in mol.binding_partners:   
            partner = state.get_partner(component)
            result += self.get_molecules(partner.name, partner.cid)
        return result

    def get_branches(self, mol_name, mid=None):
        """
        Returns a list of all possible paths 
        from root to leaf nodes
        in a tree rooted at the given molecule.
        (paths represented as lists of molecules)
        """
        result = []
        stack = []
        for mol in self.get_partners(mol_name, mid):
            stack.append([mol])

        while stack:
            branch = stack.pop()
            mols = self.get_partners(branch[-1].name, branch[-1].mid)
            if len(mols) == 1: # one node - the one we came from
                result.append(branch)
            else:
                for mol in mols:
                    if len(branch) == 1 and mol.name != mol_name:
                        stack.append(branch + [mol])
                    elif len(branch) > 1 and branch[-2].name != mol.name:
                        stack.append(branch + [mol])
        return result

    def get_top_branches(self, mol_name, mid=None):
        """
        Returns a list of molecules for each 
        subgraph originating from the given molecule.
        """
        #KR: is it used?
        result = {}
        stack = []
        for mol in self.get_partners(mol_name, mid):
            result[(mol.name, mol.mid)] = [mol]
            stack.append([mol])
        while stack:
            branch = stack.pop()          
            mols = self.get_partners(branch[-1].name, branch[-1].mid)
            if len(mols) > 1:
                for mol in mols:
                    if len(branch) == 1 and mol.name != mol_name:
                        stack.append(branch + [mol])
                        result[(branch[0].name, branch[0].mid)].append(mol)
                    elif len(branch) > 1 and branch[-2].name != mol.name:
                        stack.append(branch + [mol])
                        result[(branch[0].name, branch[0].mid)].append(mol)
        return result.values()
        
    def get_paths(self, mol1, mol2):
        """
        Returns a list of all paths from mol1
        to nodes that have the same name as mol2
        except if mol1 and mol2 are adjacent, in which case the 
        molecules' mid must match as well.
        The paths are returned sorted by length (ascending).
        """
        #KR: eventually, a method that returns a single path
        #    between two exact nodes might be useful.
        if mol1 not in self.molecules or mol2 not in self.molecules:
            return None 

        result = []
        stack = []
        for mol in self.get_partners(mol1.name, mol1.mid):
            if mol == mol2: # matches mid here, but below not
                result.append([mol])
            else:
                stack.append([mol])
        while stack:
            branch = stack.pop()
            mols = self.get_partners(branch[-1].name, branch[-1].mid)
            if len(mols) == 1:
                pass
                #KR: if len(mols) != 1: 
            else:
                for mol in mols:
                    if len(branch) == 1 and mol.name != mol1.name:
                        if mol == mol2:
                            result.append(branch + [mol])
                        else: 
                            stack.append(branch + [mol])
                    elif len(branch) > 1 and branch[-2].name != mol.name:
                        if mol == mol2:
                            result.append(branch + [mol])
                        else: 
                            stack.append(branch + [mol])
                        #KR: if..else block identical to previous one
                        #    if condition could be optimized.
        result = [[mol1] + li for li in result]
        result = sorted(result, key=lambda x: len(x))
        return result
        
    def get_shortest_path(self, mol1, mol2):
        """
        Returns the shortest path between two molecules
        that comes first alphabetically.
        """
        all_paths = self.get_paths(mol1, mol2)
        if not all_paths:
            return []
        length = len(all_paths[0])
        result = [path for path in all_paths if len(path) == length]
        result = sorted(result, key=lambda x: str(x))
        return result[0]
        

    def clone(self):
        """
        Creates a new instance of BiologicalComplex identical to itself.

        @rtype:  BiologicalComplex
        @return: identical complex
        """
        new = BiologicalComplex()
        temp = []
        for mol in self.molecules:
            temp.append(mol.clone())
        new.molecules = temp
        #new.molecules = copy.deepcopy(self.molecules)
        new.side = copy.deepcopy(self.side)
        new.input_condition = copy.deepcopy(self.input_conditions)
        return new

    def get_bonds(self):
        """
        Returns a dictionare with bonds prepared 
        based on molecule.binding_partners of each molecule.
        {state: number}
        e.g.
        {A_[B]--B_[A]: 1}
        """
        #print self
        #print self.inspect()
        # get all molecule-state data:
        mol_state = []
        mols = sorted(self.molecules, key=lambda mol: mol.name)
        for mol in mols:
            for state in mol.binding_partners:
                mol_state.append((mol, state))
        
        # get pairs molecule-state & molecule-state
        pairs = []
        while mol_state:
            ms = mol_state.pop()
            done = False
            for p in pairs:
                if len(p) == 1:
                   if p[0][1] == ms[1]:  # state is the same
                        if not done and (ms[1].homodimer or p[0][0].name != ms[0].name):
                            p.append(ms)
                            done = True
            if not done:
                pairs.append([ms])

        # get bonds numbers
        bonds = {}
        counter = 1
        for p in pairs:
            if len(p) == 2:
                bonds[p[0]] = counter
                bonds[p[1]] = counter
                counter += 1
            elif len(p) == 1 and p[0][1].type == 'Intraprotein':
                bonds[p[0]] = counter
                counter += 1
            else:
                print 'Adding bond - sth strange', self 
        return bonds


    def get_molecules(self, name, mid=None, _id=None):
        """
        Returns a list of molecules with given: name, mid and _id.
        - name (obligatory)
        - mid (not neccessary) - molecule id from contingency
        - _id (not neccessary) - uniq id of Molecule object.
        """
        result = []
        for mol in self.molecules:
            if mol.name == name:
                if not mid or not mol.mid or (mid and mid == mol.mid):
                    if not _id or (_id and _id == mol._id):
                        result.append(mol)      
        return result

    def get_molecules_on_state_condition(self, name, state=None, mid=None, _id=None):
        """
        TODO: Perhaps needs further attention.

        Gets molecules from complex and then filters them with given state.
        Returns only these molecules that have state 
        (in any of attribute lists - modifications, modification_sites ...)
        """
        result = []
        mols = self.get_molecules(name, mid, _id)
        for mol in mols:
            if mol.has_state(state):
                result.append(mol)
        return result

    def has_molecule(self, name, mid=None):
        """
        Checks whether molecule with given name and mid (not obligatory)
        is present in complex.molecules.
        Returns False or True
        """
        all_mols = [(mol.name, mol.mid) for mol in self.molecules]
        if (name, mid) in all_mols: 
            return True
        return False


    def add_state(self, state):
        """
        """
        if state.type == 'Input':
            self.input_conditions = Contingency('','!',state)
        elif state.type == 'Association':
            mol1 = Molecule(state.components[0].name)
            mol1.mid = state.components[0].cid
            mol1.binding_partners.append(state)
            mol2 = Molecule(state.components[1].name)
            mol2.mid = state.components[1].cid
            mol2.binding_partners.append(state)

            partners = self.get_molecules(mol1.name, mol1.mid)
            if not partners:
                self.molecules.append(mol1)
                #KR: append to mol1.binding_partners here
                #    or add method create_molecule(component)
            else:
                if state not in partners[0].binding_partners:
                    #KR: this if could be delegated to Molecule
                    partners[0].add_bond(state)
          
            partners = self.get_molecules(mol2.name, mol2.mid)
            if not partners or mol1 == mol2:
                self.molecules.append(mol2)
            else:
                if state not in partners[0].binding_partners:
                    partners[0].add_bond(state)

    def get_contingencies(self):
        """
        Colects all contingencies that are fulfilled in the complex.

        @rtypr:  list
        @return: contingencies neccesarry to build the complex.
        """
        result = []
        for molecule in self.molecules:
            result += molecule.get_contingencies()
        return list(set(result))  

    def remove_molecule(self, mol):
        """
        Remove molecule from comoplex.
        """
        # TODO: what if afterwords we have two complexes?
        #       Check whether all mols are connected and
        #       we have 2 complexes then return them?
        if mol in self.molecules:
            cmol = self.get_molecules(mol.name, mol.mid)[0]
            for m in self.molecules:
                if m != cmol:
                    for bond1 in m.binding_partners:
                        for bond2 in cmol.binding_partners:
                            if bond1 == bond2:
                                m.remove_bond(bond1)
            self.molecules.remove(cmol)


class AlternativeComplexes(list):
    """
    Object AlternativeComplexes keeps all complexes with the same identificator.
    E.g. obtained from the same boolean or complex contingency.
    """
    def __init__(self, name):
        list.__init__(self)
        self.name = name
        self.ctype = None #: contingency type
        self.input_condition = None 

    def add_complex(self, comp):
        self.append(comp)

    def get_first_non_empty(self):
        """
        Returns  first complex that is not empty
        (contains molecules).
        """
        for comp in self:
            if comp.molecules:
                return comp

    def empty(self):
        """
        Removes all complexes from the AlternativeComplexes object
        """
        while self:
            self.pop()

    def clone(self):
        """
        Clones complexes inside so they become new objects
        """
        new = AlternativeComplexes(self.name)
        for compl in self:
            new_compl = compl.clone()
            new.add_complex(new_compl)
        new.ctype = self.ctype
        new.input_condition = self.input_condition
        return new


class ComplexPool(dict):
    """
    """
    pass




