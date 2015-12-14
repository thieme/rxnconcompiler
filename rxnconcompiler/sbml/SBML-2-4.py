from rxnconcompiler.SBGN.PD import ReducedProcessDescription
from rxnconcompiler.rxncon import Rxncon
from libsbml import *  #TODO imported all the libSBML, maybe specifie what is realy needed in the end

class SBMLBuilder(object):

    def build_model(self, ReducedPDTree):

        try:
            document = SBMLDocument()
        except ValueError:
            raise SystemExit('SBML Document creation faile') #TODO another exception handle requiered?
        model = document.createModel()
        model.setTimeUnits("second")

if __name__ == "__main__":
    TOY1 = """
    a_p+_b
    """

    rxncon = Rxncon(TOY1)
    rxncon.run_process()
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    reducedPD.build_reaction_Tree()
    sb = SBMLBuilder()
    toy1sbml =  sb.build_model(reducedPD.tree)