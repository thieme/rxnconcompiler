#!/usr/bin/env python

"""
Class Reaction          - abstract class for all reactions used in rxncon.
Class Interaction       - Reaction subclass
Class Modification      - Reaction subclass
Class SyntDeg           - Reaction subclass
Class Relocalisation    - Reaction subclass

MODIFIER - a participant of a reaction that doesn't change
           (e.g. enzyme, channel, transporter, ribosom, mRNA).
           Some reactions can have two modifiers e.g.
           translation: ribosom and mRNA
"""

import copy
from molecule.state import get_state
from molecule.molecule import Molecule
from biological_complex.biological_complex import BiologicalComplex
from contingency.contingency import Contingency

#TODO: should modifiers be the same object 
#      in the reaction (no substrat and product)?
#      and perhaps even across the reactions in the container?

#TODO: Specific Reaction class (e.g. SyntDeg) has a lot of reaction
#      subtypes inside that behave in a different way? Add classes?


class Reaction:
    """
    Abstract class for rxncon reactions.
    Concrete classes are: Interaction, Modification, SyntDeg, Relocalisation.

    left_reactant:
    right_reactant:
    substrate_complexes:
    """
    def __init__(self):
        self.name = None
        self.rid = None
        self.rtype = None
        self.definition = None
        self.left_reactant = None # RxnconMolecule object
        self.right_reactant = None # RxnconMolecule object
        self.substrat_complexes = []
        self.product_complexes = [] #RxnconMolecule objects
        self.conditions = None # e.g. ['Start'], ['Turgor'] ...
        self.to_change = None # domain that will chage during reaction.
        self.rate = None # Rate object

    def __repr__(self):
        """e.g. A_ppi_B"""
        return self.name

    def inspect(self):
        """
        Prints detail information about reaction.
        """
        print "### REACTION: %s, %s" % (self.name, self.rid)
        print 'Substrates:'
        for subs in self.substrat_complexes:
            subs.inspect()
        #for prod in self.product_complexes:
        #    prod.inspect()
        #print "Input conditions: %s" % str(self.conditions)
        #print "Changed state:    %s" % str(self.to_change) 
        #print "Reaction rate:    %s" % str(self.rate) 


    def run_reaction(self):
        """
        Function specific for each type of reaction.
        Makes ready reaction out of one that has only substrate complexes.
        - updates substrate complexes
          (e.g.: TRSC has in substrate 2 complexes: polymerase and gene,
                  needs to be updated to just polymerase).
        - creates and adds product complexes 
        """
        pass

    def clone(self):
        """Returns new instance."""
        new = self.__class__()
        new.name = copy.deepcopy(self.name)
        new.rid = copy.deepcopy(self.rid)
        new.rtype = self.rtype
        new.definition = self.definition
        new.left_reactant = self.left_reactant #None # RxnconMolecule object
        new.right_reactant = self.right_reactant #None # RxnconMolecule object
        new.substrat_complexes = copy.deepcopy(self.substrat_complexes)
        new.product_complexes = copy.deepcopy(self.product_complexes)
        new.conditions = copy.deepcopy(self.conditions)
        new.to_change = copy.deepcopy(self.to_change)
        new.rate = copy.deepcopy(self.rate)
        return new

    def get_domain(self):
        """Function specific for each type of reaction."""
        pass

    def add_substrate_complex(compl):
        """Function specific for each type of reaction."""
        pass

    def get_sp_state(self):
        """
        Returns State object that will change during the reaction:
        source state:  x State
        product state: ! State
        """
        return self.to_change

    def get_contingencies(self):
        """
        Returns contingencies list.
        Contingencies define a context for a given reaction. 
        """
        result = []
        for compl in self.substrat_complexes:
            result += compl.get_contingencies()
        scont = Contingency(None, 'x', self.get_sp_state())
        result = set(result)
        result = result - set([scont])
        for cont in result:
            cont.target_reaction = self.name
        return list(result)

    def get_specific_contingencies(self, common_cont):
        """"""
        all_cont = set(self.get_contingencies())
        return list(all_cont - set(common_cont))

    def get_substrate_complex(self, side):
        """
        Finds left and right complex in substrate_complexes.

        @param side: 'L', 'R', or 'LR' (stends for Left and Right)  
        @type side: string
    
        @return: left or right complex.
        @rtype: BiologicalComplex.
        """
        for compl in self.substrat_complexes:
            if compl.side == side:
                return compl

    def join_substrate_complexes(self, state):
        """"""
        if state.type != 'Association': print 'WARNING', state.type

        left = self.get_substrate_complex('L')
        right = self.get_substrate_complex('R')

        if not left and right: print 'WARNING'

        # useing state_comp instead of state.components
        # to avoid that A--A will be added as binding partner to A only once.
        state_comp = state.components
        if len(state_comp):
            if state_comp[0].name == state_comp[1].name:
                state_comp = [state.components[0]]

        for compl in [left, right]:
            for compon in state_comp:#state.components:

                mols = compl.get_molecules(compon.name, compon.cid)
                if mols:
                    mols[0].binding_partners.append(state)

        new_comp = left.complex_addition(right)
        new_comp.side = 'LR'
        self.substrat_complexes = [new_comp]

    def get_product_contingency(self):
        """
        Returns product state as a contingency:
        x if state is destroyed
        ! if state is produced
        """ 
        return Contingency(self.name, '!', self.to_change)

    def get_source_contingency(self):
        """
        Returns source state as a contingency
        """
        return Contingency(self.name, 'x', self.to_change)      

    def get_modifier(self):
        """
        Returns a list of complexes that don't change during the reaction.

        """
        return []    

    @property
    def main_id(self):
        """
        Returns the main id number e.g.
        1_1 ---> 1
        120_1 ---> 120
        33 ---> 33
        """  
        return str(self.rid).split('_')[0]    
        

class Interaction(Reaction):
    """"""
    def run_ipi_reaction(self):
        """
        Creates product_complexes.
        ipi has separate function because it is special - 
        has only one substrate complex (the same protein, a bond inside is added).
        """
        comp = self.substrat_complexes[0].clone()
        mol = comp.get_molecules(self.left_reactant.name, self.left_reactant.mid)[0]
        mol.add_bond(self.to_change)
        self.product_complexes.append(comp)

    def run_reaction(self):
        """
        Assumes that there are always two substrate complexes.
        """
        if self.rtype == 'ipi':
            self.run_ipi_reaction()
        else:
            #if len(self.substrat_complexes) != 2:
            #    raise TypeError('Protein-protein interaction can only happen between two complexes.')
            new = BiologicalComplex()
            new.side = 'LR'
            for compl in self.substrat_complexes:
                if compl.is_modifier:
                    self.product_complexes.append(compl)
                else:
                    for mol in compl.molecules:
                        if mol.is_reactant:
                            mol = mol.clone()
                            mol.add_bond(self.to_change)
                        else:
                            mol = mol.clone()
                        new.molecules.append(mol)
            self.product_complexes.append(new)



class Modification(Reaction):
    """"""
    def get_modifier(self):
        """
        Returns complex that doesn't change during reaction.
        (works after run_process() is executed in rulebased).
        Enzyme.
        In rxncon syntax it is a left complex or [] (when autophosphorylation).
        A substrate complex is returned.
        (it is the same as product but has different _id)
        """
        lcompl = self.get_substrate_complex('L')  
        if lcompl:
            return [lcompl]
        return []

    def run_reaction(self):
        """
        """
        if self.rtype == 'pt':
            self.run_reaction_pt()
        else:
            rmol = self.right_reactant
            lmol = self.left_reactant
            srcomp = self.get_substrate_complex('LR') or self.get_substrate_complex('R')
            srmol = srcomp.get_molecules_on_state_condition(name=rmol.name, state=self.to_change, mid=rmol.mid)[0]
            prcomp = srcomp.clone()
            prmol = prcomp.get_molecules_on_state_condition(name=rmol.name, state=self.to_change, mid=rmol.mid)[0]


            if '-' in self.rtype or self.rtype in ['gap']:
                prmol.remove_modification(self.to_change)
            else:  
                prmol.add_modification(self.to_change)
     
            self.product_complexes.append(prcomp)
   
            if len(self.substrat_complexes) == 2 and self.rtype != 'pt':

                lcomp = self.get_substrate_complex('L')
                if lcomp:
                    self.product_complexes.append(lcomp)

        # add input to the reaction e.g. [Start]
        input_complex = self.get_substrate_complex('Z')
        if input_complex:
            self.product_complexes.append(input_complex)   

    def run_reaction_pt(self):
        """"""
        # mol - molecule, comp - complex
        # r - right, l - left
        # s - substrate, p - product
        rmol = self.right_reactant
        lmol = self.left_reactant

        scomp = self.get_substrate_complex('LR')
        if scomp:
            slmol = scomp.get_molecules(lmol.name, lmol.mid)[0] 
            srmol = scomp.get_molecules(rmol.name, rmol.mid)[0] 
            pcomp = scomp.clone()     
            plmol = pcomp.get_molecules(lmol.name, lmol.mid)[0] 
            prmol = pcomp.get_molecules(rmol.name, rmol.mid)[0] 
            prmol.add_modification(self.to_change)
            plmol.remove_modification(self.to_change) 

            self.product_complexes += [pcomp]    
        else:
            srcomp = self.get_substrate_complex('R')
            srmol = srcomp.get_molecules(rmol.name, rmol.mid)[0]        
            prcomp = srcomp.clone()
            prmol = prcomp.get_molecules(rmol.name, rmol.mid)[0]
            prmol.add_modification(self.to_change)

            slcomp = self.get_substrate_complex('L')
            slmol = slcomp.get_molecules(lmol.name, lmol.mid)[0]        
            plcomp = slcomp.clone()
            plmol = plcomp.get_molecules(lmol.name, lmol.mid)[0]
            plmol.remove_modification(self.to_change)        

            self.product_complexes += [prcomp, plcomp]
   

    def get_sp_state(self):
        """"""
        return self.to_change#.get_state(self.right_reactant.name)

    def get_product_contingency(self):
        """
        Returns a contingency that describes what is 
        prodused/destroyed within a reaction.
        """
        if '+' in self.rtype or self.rtype in ['pt', 'gap']:
            return Contingency(self.name, '!', self.to_change)
        elif '-' in self.rtype or self.rtype in ['ap', 'gef', 'cut']: 
            return Contingency(self.name, 'x', self.to_change)

    def get_source_contingency(self):
        """
        Describes state of substrates neccesary for reaction to happen.
        """
        if '+' in self.rtype or self.rtype in ['pt', 'gap']:
            return Contingency(self.name, 'x', self.to_change)
        elif '-' in self.rtype or self.rtype in ['ap', 'gef', 'cut']: 
            return Contingency(self.name, '!', self.to_change)

class SyntDeg(Reaction):
    """
    Reactions: 
    trsc (trancsription)
    trsl (translation)
    deg (degradation)
    """
    def get_modifier(self):
        """
        Returns complex that doesn't change during reaction:
        - protein that degrades other protein
        - polymerase
        - ribosom, mRNA
        A substrate complex is returned.
        (it is the same as product but has different _id)    
        """
        if self.rtype in ['trsc', 'deg']:
            lcompl = self.get_substrate_complex('L')
            if lcompl:
                return [lcompl]
        elif self.rtype == 'trsl':
            return self.substrat_complexes
        return []

    def run_reaction(self):
        """"""
        if self.rtype == 'trsc':
            rcomp = self.get_substrate_complex('R')
            self.substrat_complexes.remove(rcomp)
            rcomp.molecules[0].name += 'mRNA' 
            rcomp.side = 'Z'
            self.product_complexes += self.substrat_complexes
            self.product_complexes.append(rcomp)
        elif self.rtype == 'trsl':
            self.product_complexes += self.substrat_complexes
            rcomp = self.get_substrate_complex('R')
            self.substrat_complexes.remove(rcomp)
            new_comp = rcomp.clone()
            new_comp.molecules[0].name += 'mRNA' 
            rcomp.side = 'Z'
            self.substrat_complexes.append(new_comp)
            self.product_complexes.append(new_comp) 
        elif self.rtype == 'deg':
            lcomp = self.get_substrate_complex('L')
            self.product_complexes.append(lcomp) 
            rcomp = self.get_substrate_complex('R').clone()
            rcomp.remove_molecule(self.right_reactant)
            if rcomp.molecules:
                self.product_complexes.append(rcomp) 
        elif self.rtype == 'produce':
            rcomp = self.get_substrate_complex('R')
            self.substrat_complexes.remove(rcomp)
            self.product_complexes += self.substrat_complexes
            self.product_complexes.append(rcomp)
        elif self.rtype == 'consume':
            lcomp = self.get_substrate_complex('L')
            self.product_complexes.append(lcomp)


class Relocalisation(Reaction):
    """"""
    def get_modifier(self):
        """
        Returns complex that doesn't change during reaction:
        - channel
        - transporter
        The substrate complex is returned 
        (the same as product but different _id).
        """
        lcompl = self.get_substrate_complex('L')
        if lcompl:
            return [lcompl]
        return []

    def run_reaction(self):
        """
        Runs relocalisation reaction.
        Adds product complexes.
        Changes loc attrib for localisation of right molecule. 
        """
        rmol = self.right_reactant
        lmol = self.left_reactant
        srcomp = self.get_substrate_complex('LR') or self.get_substrate_complex('R')        
        prcomp = srcomp.clone()
        prmol = prcomp.get_molecules(rmol.name, rmol.mid)[0]
        prmol.localisation.loc = True
        self.product_complexes.append(prcomp)
        if len(self.substrat_complexes) > 1:
            self.product_complexes.append(self.get_substrate_complex('L'))