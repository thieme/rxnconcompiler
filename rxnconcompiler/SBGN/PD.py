from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.tree import Tree
class ReducedProcessDescription(object):

    """"""

    def __init__(self,reaction_pool):
        """Constructor for ReducedProcessDescription"""
        self.tree = Tree()

    def build_Tree(self):
        pass

if __name__ == "__main__":
    TOY1 = """
    Ste11_ppi_Ste7
    Ste11_[KD]_P+_Ste7_[(ALS359)]; ! Ste11--Ste7
    """
    rxncon = Rxncon(TOY1)
    reducedPD = ReducedProcessDescription(rxncon.reaction_pool)
    # TOY2 = """Ste5_ppi_Ste11
    # Ste5_ppi_Ste7
    # Ste5_ppi_Ste5
    # Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <b>
    # <b>; AND Ste5--Ste11
    # <b>; AND Ste5--Ste7
    # <b>; AND Ste5--Ste5"""
    #
    # TOY3 = """
    # a_p+_b
    # a_p+_c
    # """
    # TOY4 = """
    # a_p+_b_[x]
    # c_p+_b_[x]
    # """
    # TOY5 = """
    # Ste5_ppi_Ste11
    # Ste5_ppi_Ste7; ! Ste5--Ste11
    # Ste5_ppi_Fus3
    # Fus3_ppi_Ste7; ! Ste5--Fus3
    # Fus3_ppi_Ste7; ! Ste5--Ste7
    # """
    #
    # TOY6 = """
    # Ste5_ppi_Ste11
    # Ste5_ppi_Ste7
    # Ste5_ppi_Fus3
    # Fus3_ppi_Ste7; ! Ste5--Fus3
    # Fus3_ppi_Ste7; ! Ste5--Ste7
    # Ste7_P+_Fus3; ! <ComplexC>
    # <ComplexC>; AND Fus3--Ste7
    # <ComplexC>; AND Ste5--Ste11
    # <ComplexC>; AND Ste5--Ste7
    # """
