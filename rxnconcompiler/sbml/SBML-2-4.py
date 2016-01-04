from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
import os
from libsbml import *
# libsbml import always marked as unused and (some of) the depending methods as unresolved but work as intended when run
#TODO import only needed packages


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
        # generates the species id for complexes with one or more molecules
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

        #species.setId("s" + str(node.id))         # ist das sinnvoll, muss nicht der complex und seine molecules betrachtet werden

        species.setId( self.process_complex_id(node.node_object) )
        species.setName(str(node.name))
        #optional set species.setSpeciesType()      # optional attribute
        species.setCompartment('c1')                # Compartment is set to default comp c1, has to be changed if compartments are added to rxncon
        species.setInitialAmount(100)               # Default set to 100
        #species.setInitialConcentration()
        #species.setSubstanceUnits('mole')
        #species.setHasOnlySubstanceUnits(False)
        #species.setBoundaryCondition(False)
        #species.setConstant(False)


    def process_reaction(self, rxnconReaction):
        # gets an unhandled reaction  an processes stored information

        # reaction.id is r + a running number, so that each reaction has a unique id
        reaction = self.model.createReaction()
        reaction.setId('r' + str(rxnconReaction.rid))

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

        #alternative way to set references for commented block
        self.set_references(reaction, rxnconReaction.substrat_complexes, True)
        self.set_references(reaction, rxnconReaction.product_complexes, False)

        # for reactant in rxnconReaction.substrat_complexes:
        #     if not reactant._BiologicalComplex__is_modifier:
        #         reactRef = reaction.createReactant()
        #         reactRef.setSpecies(self.process_complex_id(reactant))
        #     else:
        #             modRef = reaction.createModifier()
        #             modRef.setSpecies(self.process_complex_id(reactant))
        #
        # for reactant in rxnconReaction.product_complexes:
        #     if not reactant._BiologicalComplex__is_modifier:
        #         prodRef = reaction.createProduct()
        #         prodRef.setSpecies(self.process_complex_id(reactant))
        #     else:
        #         modRef = reaction.createModifier()
        #         modRef.setSpecies(self.process_complex_id(reactant))

    # sets the reactant/product/modifier references for a reaction
    def set_references(self, reaction, complex, is_substrate):
        refs = []
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

    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree
        self.tree = rPDTree

        #handle compartments, default compartment until further changes to rxncon
        c = self.model.createCompartment()
        c.setId('c1')
        #example values for compartments
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

            # TODO check if it is ok to skip a reaction if it was processed on an other edge already
            for reaction in edge.reaction:
                if reaction.rid not in handled_reactions :
                    self.process_reaction(reaction)
                    handled_reactions.append(reaction.rid)



        return(self.document)

    def save_SBML(self, document, path):
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