from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.util.rxncon_errors import RxnconRateError
import os
from libsbml import *
# libsbml import always marked as unused and (some of) the depending methods as unresolved but work as intended when run
#TODO import only needed packages (when its clear which are needed)


class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4, cd = False):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        # Boolean cd indicates weahter CellDesigner Annotations should be added or not
        try:
            self.namespace = SBMLNamespaces(level, version)
            if cd:
                self.namespace.addNamespace("http://www.sbml.org/2001/ns/celldesigner", "celldesigner")
            self.document = SBMLDocument(self.namespace)
        except ValueError:
            raise SystemExit("SBML Document creation failed")
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
        # gets a list of tuple (reaction, edge.id)  and processes stored information

        reaction = self.model.createReaction()
        id = 'r' + str(rxnconReactions[0][0].rid)   # id is a string "r[rid]" where rid is the number from the rxncon-reaction
        reaction.setId(id)

        #creates a name out of the unique reaction names that are part of this reaction
        names = set()
        for reactionTuple in rxnconReactions:
            names.add(reactionTuple[0].name)
        names = list(names)
        reaction.setName(";".join(names))

        reaction.setReversible(rxnconReactions[0][0].definition["Reversibility"] == "reversible")  # sets a bool according to Reversibility, True for reversible False for irreversible
        #reaction.setFast()
        #reaction.setSBOTerm()
        if(self.namespace.getLevel >=3):
            reaction.setCompartment('cell')                          # Reaction_Compartment exists not before SBML L3V1

        #adds SpeciesReferences to the reaction and gives back a tupel of (reactantList, prodList, rxncon-reaction.rid)
        [self.add_references(id, reactionTuple[1]) for reactionTuple in rxnconReactions]

        self.compute_KineticLaw(id, rxnconReactions)

    def set_reference(self, reaction, reactant, is_substrate):
        # sets the reactant/product/modifier references for the given reaction

        if not reactant._BiologicalComplex__is_modifier:
            if is_substrate:
                reactRef = reaction.createReactant()
                reactRef.setSpecies(self.process_complex_id(reactant))
            else:
                prodRef =  reaction.createProduct()
                prodRef.setSpecies(self.process_complex_id(reactant))
        else:
            modRef = reaction.createModifier()
            modRef.setSpecies(self.process_complex_id(reactant))


    def add_references(self, id, edge_id):
        # adds new reactants to an reaction

        reaction = self.model.getReaction(id)

        substrate = self.tree.get_node(edge_id[0]).node_object
        if reaction.getReactant(self.process_complex_id(substrate)) is None and reaction.getModifier(self.process_complex_id(substrate)) is None:
            reactRefs = (self.set_reference(reaction, substrate, True))

        product = self.tree.get_node(edge_id[1]).node_object
        if reaction.getProduct(self.process_complex_id(product)) is None and reaction.getModifier(self.process_complex_id(product)) is None:
          self.set_reference(reaction, product, False)

    def compute_KineticLaw(self, reaction_id, rxnconReactions):
        handledReaction=[]
        rule = ""
        for reactions in rxnconReactions:
            if reactions[0].rid not in handledReaction:
                handledReaction.append(reactions[0].rid)
                handledNode = []
                if reactions[0].rate.rate is not None:
                    if rule:
                        rule += " + "
                    rule += reactions[0].rate.rate
                    for reactionTuple in rxnconReactions:
                        if reactionTuple[0].rid == reactions[0].rid:
                            if reactionTuple[1][0] not in handledNode:
                                rule += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                handledNode.append(reactionTuple[1][0])

                elif reactions[0].rate.rate is None and reactions[0].rate.rrate is not None and reactions[0].rate.frate is not None:
                    there =" "+ reactions[0].rate.frate
                    back =" "+ reactions[0].rate.rrate
                    for reactionTuple in rxnconReactions:
                        if reactionTuple[0].rid == reactions[0].rid:
                            if reactionTuple[1][0] not in handledNode:
                                there += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][0]).node_object)
                                handledNode.append(reactionTuple[1][0])
                            if reactionTuple[1][1] not in handledNode:
                                back += " * " + self.process_complex_id( self.tree.get_node(reactionTuple[1][1]).node_object)
                                handledNode.append(reactionTuple[1][1])
                    rule += there + " - " + back
                else:
                    raise RxnconRateError("failed to set Kinetic law for reaction " + str(reactions[0].rid ))

        reaction = self.model.getReaction(reaction_id)
        kineticLaw = reaction.createKineticLaw()
        kineticLaw.setMath(parseL3Formula(rule))

    def save_SBML(self, document, path):
        # writes the SBML Document to a textfile

        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("file save xuscessful")
        else:
            print('file save failed')



    def build_model(self, rPDTree, cd = False):
        # build_model takes a reducedPD.tree and calls the functions to build a species for each node and reaction for each edge
        self.tree = rPDTree

        # default compartment until further changes to rxncon
        c = self.model.createCompartment()
        c.setId('cell')
        # example values for compartments
        #c.setConstant(True)
        c.setSize(1)
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

# TODO everything with Celldesigner should go here so that the basic SBML isn't changed in the process
class CDBuilder(SBMLBuilder):
    def model_CdAnnotation(self):
        theAnnotation = "<celldesigner:extension>"
        theAnnotation += "<celldesigner:modelVersion>4.0</celldesigner:modelVersion>"
        theAnnotation += "<celldesigner:modelDisplay sizeX=\"600\" sizeY=\"400\"/>"
        #theAnnotation += addlistOfCompartmentAliases       # will probaly needed when rxncon gets compartments
        #theAnnotation += addlistOfComplexSpeciesAliases    # TODO will needed for complexes that are formed in ppi
        #theAnnotation += addlistOfSpeciesAliases           # TODO this will be needed ASAP
        #theAnnotation += addlistOfProtein                  # TODO second objective


        theAnnotation += "</celldesigner:extension>"
        #self.model.setAnnotation(theAnnotation)        #currently adding the model annotation makes the file not readable for CD

if __name__ == "__main__":

    simple = """
    a_ppi_b
    """

    TOY1 = """
    a_p+_b_[x]; ! b_[y]-{P}
    c_p+_b_[y]
    d_ppi_e
    """

    TOY3 = """
    a_p+_b_[x]
    c_p+_b_[x]
    d_ppi_e
    """
    #d_ppi_e

    TOY2 = """
    C_p+_A_[x]
    A_ppi_B; X A_[x]-{P}
    """
    TOY4 = """
    C_p+_A_[x]
    A_ppi_B; K+ A_[x]-{P}
    """

    cellDesigner = False
    #rxncon = Rxncon(TOY3)
    #rxncon = Rxncon(TOY2)
    #rxncon = Rxncon(TOY4)
    #rxncon = Rxncon(TOY1)
    rxncon = Rxncon(simple)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    #sb = SBMLBuilder(level = 3, version = 1, cd = True)
    sb = SBMLBuilder(cd = cellDesigner)
    toy1sbml =  sb.build_model(reducedPD.tree, cellDesigner)
    sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/test.xml"))
    #sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/test.sbml"))
    print("\n" + writeSBMLToString(toy1sbml) + "\n")