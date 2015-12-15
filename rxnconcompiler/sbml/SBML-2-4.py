from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from libsbml import * # TODO imported all the libSBML, maybe specifie what is realy needed in the end

class SBMLBuilder(object):

    def __init__(self, level = 2, version = 4):
        # creates a SBML document of given level and version, default is 2.4 because of Celldesigner specs
        try:
            self.document = SBMLDocument(level, version)
            print("\nDocument created")
        except ValueError:
            print("\nerror in init of sbml doc")
            raise SystemExit("SBML Document creation failed")    # TODO another exception handle requiered?


    def build_model(self, rPDTree):
        # build_model

        print("\nmodel creating")
        model = self.document.createModel()
        #model.setTimeUnits("second")
        return(self.document)

if __name__ == "__main__":
    TOY1 = """
    a_p+_b
    """

    rxncon = Rxncon(TOY1)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    #sb = SBMLBuilder(level = 3, version = 1)
    sb = SBMLBuilder()
    toy1sbml =  sb.build_model(reducedPD.tree)
    print("\n" + writeSBMLToString(toy1sbml) + "\n")
    #print(toy1sbml.model.getTimeUnits)