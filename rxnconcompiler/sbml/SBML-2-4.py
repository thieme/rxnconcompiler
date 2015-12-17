from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
import os
from libsbml import * # TODO imported all the libSBML, maybe specifie what is realy needed in the end
# libsbml import always marked as unused and the depending methods as unresolved but work as intended when run


class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.document = SBMLDocument(level, version)
            #print("\nDocument created")
        except ValueError:
            print("\nerror in init of sbml doc")
            raise SystemExit("SBML Document creation failed")    # TODO another exception handle requiered?
        self.model = self.document.createModel()

    def process_node(self, visitId):
        #takes an unvisited node and creates species out of it
        #TODO only minimal necessary information are set, mostly defaults
        #optional values are commented commented out until a rxncon variable is found

        species = self.model.createSpecies()
        for node in self.tree.nodes:
            if node.id == visitId:

                species.setId("s" + str(node.id) )
                species.setName(str(node.name))
                # optional set species.setSpeciesType()               #optional attribute
                species.setCompartment('c1')                #TODO Compartment is set to default comp c1, find alternative
                #species.setInitialAmount(
                #species.setInitialConcentration()
                #species.setSubstanceUnits('mole')
                #species.setHasOnlySubstanceUnits(False)
                #species.setBoundaryCondition(False)
                #species.setConstant(False)





    def build_model(self, rPDTree):
        # build_model takes a reducedPD.tree
        self.tree = rPDTree

        #TODO handle compartments, default compartment until further change (from SBML examples)
        c = self.model.createCompartment()
        c.setId('c1')
        c.setConstant(True)
        c.setSize(1)
        c.setSpatialDimensions(3)
        c.setUnits('litre')


        visited_nodes=[]
        # for all edges it is checked if the nodes are already visited, if not they are added as species in process_node
        # the same will happen for each edge their reaction
        # TODO handle the edge itself with reaction etc.
        for edge in rPDTree.edges:
            #print(edge.id)
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])


        return(self.document)

    def save_SBML(self, document, path):
        #TODO validation of model before writing to file!?
        if writeSBMLToFile(document, path):
            print("print  xuscessful")
        else:
            print('file failed')


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