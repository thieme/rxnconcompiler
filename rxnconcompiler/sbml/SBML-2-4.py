from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
import os
from libsbml import *
# libsbml import always marked as unused and (some of) the depending methods as unresolved but work as intended when run
#TODO import only needed packages (when its clear which are needed)


class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.namespace = SBMLNamespaces(level, version)
            self.document = SBMLDocument(self.namespace)
        except ValueError:
            raise SystemExit("SBML Document creation failed")    # TODO another exception handle required?
        self.model = self.document.createModel()

    def process_complex_id(self, complex):
        # generates the species id for complexes with one or more molecules consisting of "s_m[id of molecule]_m..."
        compId = "s"
        for mol in complex.molecules:
             compId = compId + "_m" + str(mol._id)

        return compId

    def process_node(self, visitId):
        # takes an unvisited node and creates species out of it
        # optional values are commented out until an according rxncon variable is found
        # TODO only minimal necessary information is set, mostly defaults

        species = self.model.createSpecies()
        node = self.tree.get_node(visitId)

        species.setId( self.process_complex_id(node.node_object) )
        species.setName(str(node.name))
        #optional set species.setSpeciesType()      # optional attribute
        species.setCompartment('cell')                # Compartment is set to default comp cell, has to be changed if compartments are added to rxncon
        species.setInitialAmount(100)               # Default set to 100
        #species.setInitialConcentration()
        #species.setSubstanceUnits('mole')          #there are no units in rxncon
        #species.setHasOnlySubstanceUnits(False)
        #species.setBoundaryCondition(False)
        #species.setConstant(False)

    def process_reaction(self, rxnconReactions):
        # gets a list of tupel (reaction, edge.id)  and processes stored information

        reaction = self.model.createReaction()
        rid = 'r' + str(rxnconReactions[0][0].rid)   # id is a string "r[id]" where id is the number
        reaction.setId(rid)

        #creates a name out of the unique reaction names that are part of this reaction
        names = set()
        for reactionTupel in rxnconReactions:
            names.add(reactionTupel[0].name)
        names = list(names)
        reaction.setName(";".join(names))

        reaction.setReversible(rxnconReactions[0][0].definition["Reversibility"] == "reversible")  # sets a bool according to Reversibility, True for reversible False for irreversible
        #reaction.setFast()
        #reaction.setSBOTerm()
        if(self.namespace.getLevel >=3):
            reaction.setCompartment('cell')                          # Reaction_Compartment exists not before SBML L3V1

        references = []
        #adds SpeciesReferences to the reaction and gives back the reactants Id for further use
        for reactionTupel in rxnconReactions:
            references.append((self.add_references(rid, reactionTupel[1]), reactionTupel[0].rid))

        self.compute_KineticLaw(rid, references)

    def set_reference(self, reaction, reactant, is_substrate):
        # sets the reactant/product/modifier references for the given reaction
        # returns the id of the added speciesReference
        if not reactant._BiologicalComplex__is_modifier:
            if is_substrate:
                reactRef = reaction.createReactant()
                reactRef.setSpecies(self.process_complex_id(reactant))
                return self.process_complex_id(reactant)
            else:
                prodRef =  reaction.createProduct()
                prodRef.setSpecies(self.process_complex_id(reactant))
                return self.process_complex_id(reactant)
        else:
            modRef = reaction.createModifier()
            modRef.setSpecies(self.process_complex_id(reactant))
            return self.process_complex_id(reactant)

    def add_references(self, rid, edge_id):
        # adds new reactants to an reaction
        # passes the returned reference
        reaction = self.model.getReaction(rid)
        refs = None

        substrate = self.tree.get_node(edge_id[0]).node_object
        if reaction.getReactant(self.process_complex_id(substrate)) is None and reaction.getModifier(self.process_complex_id(substrate)) is None:
            refs = (self.set_reference(reaction, substrate, True))
        else:
            refs = self.process_complex_id(substrate)   # is needed so no (None, int) Tupel get get created which would produce wrong Kinetic Laws

        product = self.tree.get_node(edge_id[1]).node_object
        if reaction.getProduct(self.process_complex_id(product)) is None and reaction.getModifier(self.process_complex_id(product)) is None:
            self.set_reference(reaction, product, False)

        return refs

    def compute_KineticLaw(self, reaction_id, references):
        # takes the id of an otherwise fully handled reaction and the list of (SpeciesReferences, reaction)
        reaction = self.model.getReaction(reaction_id)
        parameters = set()
        rule = ""
        # set of unique Parameters one for each reaction in rxncon_ReducedPDTree relevant for this KineticLaw
        for ref in references:
            parameters.add(ref[1])

        # a string based rule is created based on: Sum of ([Parameter of Reaction] * SpeciesRef1 * SpeciesRef2...)
        for par in list(parameters):
            k = self.model.createParameter()
            k.setId("k"+str(par))
            k.setValue(1)
            if rule:
                rule = rule + " + "

            rule = rule +  "k"+str(par)
            for ref in references:
                if ref[1] == par and ref[0] is not None:
                    rule = rule + " * " + ref[0]

        kineticLaw = reaction.createKineticLaw()
        kineticLaw.setMath(parseL3Formula(rule))


    def save_SBML(self, document, path):
        # writes the SBML Document to a textfile

        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("file save xuscessful")
        else:
            print('file save failed')

    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree and calls the functions to build a species for each node and reaction for each edge
        self.tree = rPDTree

        # default compartment until further changes to rxncon
        c = self.model.createCompartment()
        c.setId('cell')
        # example values for compartments
        #c.setConstant(True)
        #c.setSize(1)
        #c.setSpatialDimensions(3)
        #c.setUnits('litre')


        visited_nodes = []
        handled_reactions= []

        # for all edges it is checked if the nodes are already visited, if not they are added as species in process_node
        # the same will happen for each edge and their reaction, an reaction can be on two different edges so it has to be checked if this reaction was already added
        for edge in rPDTree.edges:
            # add all nodes as species
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])

        for edge in rPDTree.edges:
            #handle edges, so that all reactions with the same product(s) get handled at once
            for reaction in edge.reaction:
                if reaction.rid not in handled_reactions:
                    reactions = [(reaction, edge.id)]
                    handled_reactions.append(reaction.rid)
                    products = []
                    for prod in reaction.product_complexes:
                        if not prod.is_modifier:
                            products.append(edge.id[1])
                    for other_edge in rPDTree.edges:
                        for other_reaction in other_edge.reaction:
                            if other_edge.id != edge.id:
                                if other_edge.id[1] in products:
                                    reactions.append((other_reaction, other_edge.id ))
                                    handled_reactions.append(other_reaction.rid)
                    self.process_reaction(reactions)

        return(self.document)


if __name__ == "__main__":
    TOY1 = """
    a_p+_b_[x]
    c_p+_b_[x]

    """
    #d_ppi_e

    rxncon = Rxncon(TOY1)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    #sb = SBMLBuilder(level = 3, version = 1)
    sb = SBMLBuilder()
    toy1sbml =  sb.build_model(reducedPD.tree)
    sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/testsbml.sbml"))
    print("\n" + writeSBMLToString(toy1sbml) + "\n")