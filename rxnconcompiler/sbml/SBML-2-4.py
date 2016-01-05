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
            raise SystemExit("SBML Document creation failed")    # TODO another exception handle requiered?
        self.model = self.document.createModel()
        #self.numOfReactions = {}           # a dict for reaction name : how often the reaction is already in the modell
        self.numOfReactions = 0             # easier but abstract number for reaction id

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
        species.setCompartment('c1')                # Compartment is set to default comp c1, has to be changed if compartments are added to rxncon
        species.setInitialAmount(100)               # Default set to 100
        #species.setInitialConcentration()
        #species.setSubstanceUnits('mole')          #there are no units in rxncon
        #species.setHasOnlySubstanceUnits(False)
        #species.setBoundaryCondition(False)
        #species.setConstant(False)


    def process_reaction(self, rxnconReaction, edge_id):
        # gets an unhandled reaction  an processes stored information

        reaction = self.model.createReaction()
        reaction.setId('r' + str(rxnconReaction.rid))   # id is a string "r[id]" where id is the number

            #idea to use id not as abstract number but as a combination of name and an number, fails to rxncon names with forbidden characters, may be used with some refinement
            #value = self.numOfReactions.get(rxnconReaction.name, 0)
            #reaction.setId(str(rxnconReaction.name) + str(value +1) )
            #reaction.setId('r' + str(value +1) )
            #self.numOfReactions[rxnconReaction.name] = value +1

        reaction.setName(rxnconReaction.name)
        #reaction.setKineticLaw()       # TODO set
        reaction.setReversible(rxnconReaction.definition["Reversibility"] == "reversible")  # sets a bool according to Reversibility, True for reversible False for irreversible
        #reaction.setFast()
        #reaction.setSBOTerm()
        if(self.namespace.getLevel >=3):
            reaction.setCompartment('c1')                          # Reaction_Compartment exists not before SBML L3V1

        # molecules in substrate/product_complex have different id than in the nodes so use the nodes of the reaction old
        #self.set_references(reaction, rxnconReaction.substrat_complexes, True)
        #self.set_references(reaction, rxnconReaction.product_complexes, False)

        #edge_id[0] refers to the reactant of the edge, edge[1] to the substrat, adds them as reference to the reaction
        self.set_reference(reaction, self.tree.get_node(edge_id[0]).node_object, True)
        self.set_reference(reaction, self.tree.get_node(edge_id[1]).node_object, False)

    # sets the reactant/product/modifier references for the given reaction TODO this is an old try set_reference is the new version this should be deleted when the new approach works
    def set_references(self, reaction, complex, is_substrate):
        for reactant in complex:
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

    def set_reference(self, reaction, reactant, is_substrate):
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

    def add_references(self, rid, edge_id):
        reaction = self.model.getReaction('r' + str(rid))
        substrate = self.tree.get_node(edge_id[0]).node_object
        if reaction.getReactant(self.process_complex_id(substrate)) == None:
            self.set_reference(reaction, substrate, True)

        product = self.tree.get_node(edge_id[0]).node_object
        if reaction.getReactant(self.process_complex_id(product)) == None:
            self.set_reference(reaction, product)

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
            #print(edge.id)
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])

            for reaction in edge.reaction:
                if reaction.rid not in handled_reactions :
                    self.process_reaction(reaction, edge.id)
                    handled_reactions.append(reaction.rid)
                else:
                    self.add_references(reaction.rid, edge.id)



        return(self.document)

    def save_SBML(self, document, path):
        # writes the SBML Document to a textfile

        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("file save xuscessful")
        else:
            print('file save failed')


if __name__ == "__main__":
    TOY1 = """
    a_p+_b_[x]
    c_p+_b_[x]
    """

    rxncon = Rxncon(TOY1)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    #sb = SBMLBuilder(level = 3, version = 1)
    sb = SBMLBuilder()
    toy1sbml =  sb.build_model(reducedPD.tree)
    sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/testsbml.sbml"))
    print("\n" + writeSBMLToString(toy1sbml) + "\n")