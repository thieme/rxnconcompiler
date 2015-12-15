from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from libsbml import * # TODO imported all the libSBML, maybe specifie what is realy needed in the end
# libsbml import always marked as unused and the depending methods as unresolved but work as intended when run


class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.document = SBMLDocument(level, version)
            print("\nDocument created")
        except ValueError:
            print("\nerror in init of sbml doc")
            raise SystemExit("SBML Document creation failed")    # TODO another exception handle requiered?
        self.model = self.document.createModel()

    def process_node(self, visitId):
        #takes an unvisited node and creates species out of it
        #TODO only minimal necessary information are set, mostly defaults
        #print(visitId)

        species = self.model.createSpecies()
        for node in self.tree.nodes:
            if node.id == visitId:
                species.setId("s" + str(node.id) )          #TODO SBML prefers ID with meaning so may be changed and become dependend on the name!?
                species.setCompartment('c1')                #TODO Compartment is static set to default comp c1
                species.setConstant(False)                  #TODO find coresponding value in rxncon
                species.setInitialAmount(node.id*2)         #TODO find coresponding value in rxncon actual value just for identification
                species.setSubstanceUnits('mole')           #TODO find coresponding value in rxncon
                species.setBoundaryCondition(False)         #TODO find coresponding value in rxncon
                species.setHasOnlySubstanceUnits(False)     #TODO find coresponding value in rxncon

        # TODO handle both nodes: already visited? if not insert the species

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
        for edge in rPDTree.edges:      # TODO handle the edge itself with reaction etc.
            print(edge.id)
            if edge.id[0] not in visited_nodes :
                self.process_node(edge.id[0])
                visited_nodes.append(edge.id[0])
            if edge.id[1] not in visited_nodes :
                self.process_node(edge.id[1])
                visited_nodes.append(edge.id[1])


        return(self.document)

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
    print("\n" + writeSBMLToString(toy1sbml) + "\n")