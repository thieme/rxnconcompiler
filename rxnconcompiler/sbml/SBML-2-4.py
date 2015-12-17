from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
import os
from libsbml import * # TODO imported all the libSBML, maybe specifie what is realy needed in the end
# libsbml import always marked as unused and (some of) the depending methods as unresolved but work as intended when run


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

    def process_node(self, visitId):
        #takes an unvisited node and creates species out of it
        #TODO only minimal necessary information are set, mostly defaults
        #optional values are commented commented out until a rxncon variable is found

        species = self.model.createSpecies()
        for node in self.tree.nodes:
            if node.id == visitId:

                species.setId("s" + str(node.id))          #ist das sinnvoll, muss nicht der complex und seine molecules betrachtet werden
                species.setName(str(node.name))
                # optional set species.setSpeciesType()     #optional attribute
                species.setCompartment('c1')                #TODO Compartment is set to default comp c1, find alternative
                #species.setInitialAmount()
                #species.setInitialConcentration()
                #species.setSubstanceUnits('mole')
                #species.setHasOnlySubstanceUnits(False)
                #species.setBoundaryCondition(False)
                #species.setConstant(False)


    def process_reaction(self, anReaction):
        # gets an unhandled reaction  an prcoesses stored information

        # reaction.id is r + a running number, so that each reaction has a unique id
        reaction = self.model.createReaction()
        reaction.setId('r' + str(self.numOfReactions))
        self.numOfReactions = self.numOfReactions +1

            #idea to use idea not as abstract number but as a combination of name and an number, fails to rxncon names with forbidden characters may be used with some refinemend
            #value = self.numOfReactions.get(anReaction.name, 0)
            #reaction.setId(str(anReaction.name) + str(value +1) )
            #reaction.setId('r' + str(value +1) )
            #self.numOfReactions[anReaction.name] = value +1

        #reaction.setId("r" + str(anReaction.rid ) )
        reaction.setName(anReaction.name)
        #reaction.setKineticLaw()
        reaction.setReversible(anReaction.definition["Reversibility"] == "reversible")
        #reaction.setFast()
        #reaction.setSBOTerm()
        #reaction.setCompartment()                          # exist not before SBML L3V1

        #TODO work with SpeciesReference
        for reactand in anReaction.substrat_complexes:
            for mol in reactand.molecules:
                reactRef = reaction.createReactant()
                reactRef.setSpecies("s" + str(mol._id))      #TODO find more elaborate way to compute this, serach for species the name of the right reactant

        for reactand in anReaction.product_complexes:
            for mol in reactand.molecules:
                prodRef = reaction.createProduct()
                prodRef.setSpecies("s" + str(mol._id))      #TODO find more elaborate way to compute this, serach for species the name of the right reactant


    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree
        self.tree = rPDTree

        #TODO handle compartments, default compartment until further change (from SBML examples)
        c = self.model.createCompartment()
        c.setId('c1')
        #c.setConstant(True)
        #c.setSize(1)
        #c.setSpatialDimensions(3)
        #c.setUnits('litre')


        visited_nodes = []
        handled_reactions= []

        # for all edges it is checked if the nodes are already visited, if not they are added as species in process_node
        # the same will happen for each edge and their reaction
        # TODO handle the edge itself with reaction etc.
        for edge in rPDTree.edges:
            #print(edge.id)
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])
            if edge.reaction.rid not in handled_reactions :
                self.process_reaction(edge.reaction)
                handled_reactions.append(edge.reaction.rid)



        return(self.document)

    def save_SBML(self, document, path):
        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("file save xuscessful")
        else:
            print('file save failed')


if __name__ == "__main__":
    TOY1 = """
    a_p+_b
    """

    rxncon = Rxncon(TOY1)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    # sb = SBMLBuilder(level = 3, version = 1)
    sb = SBMLBuilder()
    toy1sbml =  sb.build_model(reducedPD.tree)
    sb.save_SBML(toy1sbml, os.path.expanduser("~/Desktop/testsbml.sbml"))
    print("\n" + writeSBMLToString(toy1sbml) + "\n")