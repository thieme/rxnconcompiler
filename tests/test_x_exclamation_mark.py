from rxnconcompiler.rxncon import Rxncon
from unittest import main, TestCase

from unittest import main, TestCase
from rxnconcompiler.bngl.bngl import Bngl
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.parser.rxncon_parser import parse_rxncon


# MR 19.10.2014
# Name of this test sounds to me like
# acceptance test - testing the end product - bngl.
# If you look for some inspiration for asserts you can go other
# acceptance tests.
# Perhaps it would also help to have unit tests -
# just testting whether new functions work.
#
# You can also use oposite case
# A_ppi_B; x A-{P}
# X_P+_A
from unittest import main, TestCase
from rxnconcompiler.rxncon import Rxncon

from rxnconcompiler.contingency.contingency_applicator import ContingencyApplicator
from rxnconcompiler.contingency.contingency import Contingency
from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.biological_complex.complex_applicator import ComplexApplicator
from rxnconcompiler.biological_complex.biological_complex import BiologicalComplex
from rxnconcompiler.molecule.molecule import Molecule
from rxnconcompiler.biological_complex.complex_builder import ComplexBuilder
import copy


class x_exclamation_mark_Tests(TestCase):

    """
    Unit tests for Rxncon class.

    Tests top rxncon objects.
    """

    def setUp(self):
        """
        Prepares data for tests.
        """

        # basic reaction with one contingency.
        #input_data = "/home/thiemese/project/rxncon/rxncon-compiler/tests/test_data/xls_files/Tiger_et_al_TableS1.xls"
        input_data = "/home/thiemese/project/rxncon/rxncon-compiler/tests/test_data/xls_files/150120_PheromoneModel_BNGL2rxncon.xls"


#######################################   Presentation ########################################
        # rxncon = Rxncon("""A_ppi_B; ! <comp1>
        #                  <comp1>; OR <comp1C1>
        #                  <comp1>; OR <comp2C1>
        #                  <comp2C1>; AND A--C [A1]
        #                  <comp2C1>; AND B--E [A2]
        #                  <comp1C1>; AND A--C [B1]
        #                  <comp1C1>; AND C--D [B2]""")

        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp>
        #                 <comp>; AND <c1>
        #                 <comp>; AND <c2>
        #                 <c1>; OR A--C
        #                 <c1>; OR A--D
        #                 <c2>; OR A--E
        #                 <c2>; OR A--F""")


# genauer anschauen
#         rxncon = Rxncon("""
#
#                         A_ppi_B; ! <comp> \n <comp>; AND <c1> \n <comp>; AND <c2> \n <c2>; OR A--E \n <c2>; OR A--F \n <c1>; OR A--C \n <c1>; OR A--D
#                         """)

        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp1>
        #                 <comp1>; OR <comp1C1>
        #                 <comp1>; OR <comp1C2>
        #                 <comp1C1>; AND A--A1
        #                 <comp1C1>; AND A--A2
        #                 <comp1C2>; AND B--B2
        #                 <comp1C2>; AND B2--B1
        #                 A_ppi_B; x <comp2>
        #                 <comp2>; OR <comp2C1>
        #                 <comp2>; OR <comp2C2>
        #                 <comp2C1>; AND A--C1
        #                 <comp2C1>; AND A--C2
        #                 <comp2C2>; AND A--D1
        #                 <comp2C2>; AND A--D2
        #                 """)
        # rxncon = Rxncon("""SCF_p+_Tec1; ! <bool>
        #                     <bool>; and Cdc4_[SCF]--SCF_[Cdc4]
        #                     <bool>; and Cdc4_[WD40]--Tec1_[CPD]
        #                     """)



        # rxncon = Rxncon("""SCF_p+_Tec1; ! Cdc4_[SCF]--SCF_[Cdc4]
        #                     SCF_p+_Tec1; ! Cdc4_[WD40]--Tec1_[CPD]
        #                      """)
# have to check
#         rxncon = Rxncon("""SCF_PT_Tec1; ! <bool>
#                             <bool>; and Cdc4_[SCF]--SCF_[Cdc4]
#                             <bool>; and Cdc4_[WD40]--Tec1_[CPD]
#                             """)
##### ordered bool ####
 #        rxncon = Rxncon("""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Comp>
 # <Comp>; OR <C1>; OR <C2>
 # <C1>; 1--2 Ste7--Ste11
 # <C2>; 1--2 Ste5_[MEKK]--Ste11; 3--4 Ste5_[MEK]--Ste7; 1--3 Ste5_[BDSte5]--Ste5_[BDSte5]
 #         """)
#### adding normal contingency to bool complex ###############
        # rxncon = Rxncon("""
        #                 A_ppi_B; k+ A--F
        #                 A_ppi_B; ! <comp1>
        #                     <comp1>; OR <comp1C1>
        #                     <comp1>; OR <comp2C1>
        #                     <comp1C1>; AND A--C
        #                     <comp1C1>; AND C--D
        #                     <comp2C1>; AND A--C
        #                     <comp2C1>; AND B--E
        #
        #                  """)

        ##### connected by contingency ###############
#         rxncon = Rxncon("""
#                         Sho1_ppi_Ste11; x Ste5_[MEKK]--Ste11; k+ Hkr1--Sho1; k+ Msb2--Sho1; k+ Msb2_[CyT]--Sho1_[CyT]; ! <Ste11^{M/50}>
# <Ste11^{M/50}>; and Opy2_[BDSte50]--Ste50_[RA]
# <Ste11^{M/50}>; and Ste11_[SAM]--Ste50_[SAM]
#                         """)


        # rxncon = Rxncon("""
        #                   A_ppi_B; ! <comp1>
        #                   <comp1>; OR <comp1C1>
        #                   <comp1>; OR <comp2C1>
        #                   <comp1C1>; AND A--C
        #                   <comp1C1>; AND C--D
        #                  <comp2C1>; AND A--C
        #                  <comp2C1>; AND B--E
        #
        #                 """)


        # rxncon = Rxncon("""A_ppi_B; ! <comp1>
        #                 <comp1>; OR <comp1C1>
        #                 <comp1>; OR <comp1C2>
        #                 <comp1C1>; AND A--A1
        #                 <comp1C1>; AND A--A2
        #                 <comp1C2>; AND B--B1
        #                 <comp1C2>; AND B--B2""")

########################## !x combination one is fully connected ###########


        # rxncon = Rxncon(""" A_ppi_B; ! <comp1>
        #                 <comp1>; OR <comp1C1>
        #                 <comp1>; OR <comp1C2>
        #                 <comp1C1>; AND A--A1
        #                 <comp1C1>; AND A--A2
        #                 <comp1C2>; AND B--B1
        #                 <comp1C2>; AND B--B2
        #
        #                 A_ppi_B; x <comp2>
        #                 <comp2>; OR <comp2C1>
        #                 <comp2>; OR <comp2C2>
        #                 <comp2C1>; AND A--C1
        #                 <comp2C1>; AND A--C2
        #                 <comp2C2>; AND A--D1
        #                 <comp2C2>; AND A--D2""")

######### complete OR ###############
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <AorC>
        #                 <AorC>; OR A_[x]-{P}
        #                 <AorC>; OR B_[y]-{P}
        #                 <AorC>; OR A--C
        #                 <AorC>; OR B--D
        #                 <AorC>; OR B_[z]-{P}""")

        # rxncon = Rxncon("""
        #                 C_p+_A_[x]
        #                 C_p+_A_[y]
        #                 C_p+_A_[z]
        #                 A_ppi_B; ! A-{P}
        #                 A_ppi_B; ! A_[z]-{P}
        #                 """)


        # rxncon = Rxncon(""" Sho1_ppi_Ste11; x Ste5_[MEKK]--Ste11; k+ Hkr1--Sho1; k+ Msb2--Sho1; k+ Msb2_[CyT]--Sho1_[CyT]; ! <Ste11^{M/50}>
        #                 <Ste11^{M/50}>; and Opy2_[BDSte50]--Ste50_[RA]
        #                 <Ste11^{M/50}>; and Ste11_[SAM]--Ste50_[SAM]""")

######## k+ #################
#         rxncon = Rxncon(""" A_ppi_C; K+ <bool>
# <bool>; AND A--D; AND A--E; AND [START]""")

########  k+ ! x combination ####
        # rxncon = Rxncon("""A_ppi_B; k+ <bool>
        #                 <bool>; AND A--Db; AND A--Eb
        #                 A_ppi_B; x <bool2>
        #                 <bool2>; AND B--Fb2; AND B--Gb2
        #                 A_ppi_B; ! <bool3>
        #                 <bool3>; AND B--Hb3; AND B--Ib3
        #                 """)



        #rxncon = Rxncon("""A_ppi_B; k+ A--C""")
        # rxncon = Rxncon("""  A_ppi_B; k+ A--F [C1]
        #                 A_ppi_B; ! <comp1>
        #                     <comp1>; OR <comp1C1>
        #                     <comp1>; OR <comp2C1>
        #                     <comp1C1>; AND A--C
        #                     <comp1C1>; AND C--D
        #                     <comp2C1>; AND A--C
        #                     <comp2C1>; AND B--E""")



# conflicting example ################################

#! Cdc24_[AssocFar1]--Far1_[c], ! Ste4_[AssocSte18]--Ste18_[AssocSte4], ! Far1_[nRING-H2]--Ste4_[AssocFar1], ! Cdc24_[AssocSte4]--Ste4_[AssocCdc24], x Ste4_[AssocSte18]--Ste18_[AssocSte4]

        # rxncon = Rxncon('''Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}>
        #         <Cdc24^{M}>; or <Cdc24^{M/4}>
        #         <Cdc24^{M/4}>; and Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
        #         <Cdc24^{M/4}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
        #         <Cdc24^{M}>; or <Cdc24^{M/F}>
        #         <Cdc24^{M/F}>; and Cdc24_[AssocFar1]--Far1_[c]
        #         <Cdc24^{M/F}>; and <Far1^{M}>
        #         <Far1^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
        #         <Far1^{M}>; and Far1_[nRING-H2]--Ste4_[AssocFar1]
        # ''')
        # rxncon = Rxncon("""A_ppi_E; ! <comp>
        #                     <comp>; 5--25 A--B
        #                     <comp>; 25--7 B--B
        #                     <comp>; 7--8 B--C
        #                     <comp>; 25--9 B--D
        #                     <comp>; 5--10 A--F
        #                     <comp>; 10--11 F--B
        #                     <comp>; 11--12 B--G
        #                      <comp>; 25 B-{P}
        #                     """)


        rxncon = Rxncon("""A_ppi_E; ! <comp>
                            <comp>; 5--25 A--B
                            <comp>; 25--7 B--B
                            <comp>; 7--8 B--C
                            <comp>; 25--9 B--D
                            <comp>; 5--10 A--F
                            <comp>; 10--11 F--B
                            <comp>; 11--12 B--G
                            A_ppi_E; ! <comp2>
                            <comp2>; 36--37 A--B
                            <comp2>; 37--38 B--C
                            <comp2>; 37--39 B--B
                            <comp2>; 39--40 B--G

                            """)
        # rxncon = Rxncon("""A_ppi_E; ! <comp>
        #                     <comp>; 5--6 A--B
        #                     <comp>; 6--7 B--B
        #                     <comp>; 7--8 B--C
        #                     <comp>; 6--9 B--D
        #                     <comp>; 5--10 A--F
        #                     <comp>; 10--11 F--B
        #                     <comp>; 11--12 B--G
        #                     A_ppi_E; ! <comp2>
        #                     <comp2>; 1--2 A--B
        #                     <comp2>; 2--3 B--C
        #                     <comp2>; 2--4 B--B
        #                     <comp2>; 4--5 B--G
        #
        #                     """)
# # # example for [! Cdc24_[AssocFar1]--Far1_[c], ! Ste4_[AssocSte18]--Ste18_[AssocSte4], ! Far1_[nRING-H2]--Ste4_[AssocFar1], x Cdc24_[AssocSte4]--Ste4_[AssocCdc24]]
#         rxncon = Rxncon("""Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <comp>
#                             <comp>; AND Cdc24_[AssocFar1]--Far1_[c]
#                             <comp>; AND Far1_[nRING-H2]--Ste4_[AssocFar1]
#                             <comp>; AND Ste4_[AssocSte18]--Ste18_[AssocSte4]
#                         Cdc24_[GEF]_GEF_Cdc42_[GnP]; x <comp1>
#                         <comp1>; AND Cdc24_[AssocSte4]--Ste4_[AssocCdc24]""")


#error example
 #        rxncon = Rxncon('''Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}>
 #                <Cdc24^{M}>; or <Cdc24^{M/4}>
 #                <Cdc24^{M/4}>; 1--5 Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
 #                <Cdc24^{M/4}>; 5--6 Ste4_[AssocSte18]--Ste18_[AssocSte4]
 #                <Cdc24^{M}>; or <Cdc24^{M/F}>
 #                <Cdc24^{M/F}>; 1--2 Cdc24_[AssocFar1]--Far1_[c]
 #                <Cdc24^{M/F}>; 3--4 Ste4_[AssocSte18]--Ste18_[AssocSte4]
 #                <Cdc24^{M/F}>; 2--3 Far1_[nRING-H2]--Ste4_[AssocFar1]
 #
 #
 # ''')


        # rxncon = Rxncon('''Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}>
        #         <Cdc24^{M}>; or <Cdc24^{M/4}>
        #         <Cdc24^{M/4}>; AND Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
        #         <Cdc24^{M/4}>; AND Ste4_[AssocSteTEST]--Ste18_[AssocTEST2]
        #         <Cdc24^{M}>; or <Cdc24^{M/F}>
        #         <Cdc24^{M/F}>; AND Cdc24_[AssocFar1]--Far1_[c]
        #         <Cdc24^{M/F}>; AND Far1_[nRING-H2]--Ste4_[AssocFar1]
        #         <Cdc24^{M/F}>; AND Ste4_[AssocSte18]--Ste18_[AssocSte4]
        #         Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Comp>
        #         <Comp>; AND Cdc24_[AssocSte4_1]--Ste4_[AssocCdc24_2]
        #         <Comp>; AND Ste4--SteTest
        #
        # ''')

        #rxncon = Rxncon('''Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}> \n <Cdc24^{M}>; or <Cdc24^{M/4}> \n <Cdc24^{M/4}>; and Cdc24_[AssocSte4]--Ste4_[AssocCdc24] \n <Cdc24^{M/4}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4] \n <Cdc24^{M}>; or <Cdc24^{M/F}> \n <Cdc24^{M/F}>; and Cdc24_[AssocFar1]--Far1_[c] \n <Cdc24^{M/F}>; and <Far1^{M}> \n <Far1^{M}>; and Far1_[nRING-H2]--Ste4_[AssocFar1] \n <Far1^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
        #''')


        #rxncon = Rxncon(""" A_SymExtCyt_B,C,D,E""")
        #rxncon = Rxncon(""" A_SymCytVac_B,C,D,E""")
        #rxncon = Rxncon(""" A_APCytVac_B,C""")
        #rxncon = Rxncon(""" A_APCytMit_B,C""")


####### xOR ###########################
        # rxncon = Rxncon(""" A_ppi_B; ! <comp>
        #                     <comp>; OR <comp1>
        #                     <comp>; OR <comp2>
        #                     <comp1>; AND A--C
        #                     <comp1>; AND <NOT1>
        #                     <NOT1>; NOT A--D
        #                     <comp2>; AND A--D
        #                     <comp2>; AND <NOT2>
        #                     <NOT2>; NOT A--C""")

        # rxncon = Rxncon(""" A_ppi_B; ! <comp>
        #                     <comp>; OR <comp1>
        #                     <comp>; OR <comp2>
        #                     <comp1>; 1--2 A--C
        #                     <comp1>; AND <NOT1>
        #                     <NOT1>; NOT A--D
        #                     <comp2>; 1--3 A--D
        #                     <comp2>; AND <NOT2>
        #                     <NOT2>; NOT A--C""")

#    [! A--C, x A--D][! A--D, x A--C]

#    [! A--C, x A--D, x A--C], [! A--D, x A--C]

        #print rxncon
        #pass

# wrong definition
        # Ste20_[KD]_P+_Ste11_[CBD(S302)]; k+ Ste20_[SerThr]-{P}; x Ste20_[KD]--Ste20_[CRIB]; ! <Ste11^{M}>; k+ <FIL-signal>
        # Ste20_[KD]_P+_Ste11_[CBD(S302)]; k+ Ste20_[SerThr]-{P}; x Ste20_[KD]--Ste20_[CRIB]; ! <Ste11^{M}>
        #
        # <FIL-signal>; and Cdc42_[AssocMsb2]--Msb2_[CyT]
        # <FIL-signal>; and Msb2_[CyT]--Sho1_[CyT]


#         rxncon = Rxncon("""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Comp>
# <Comp>; 1--2 Ste5_[MEKK]--Ste11; 3--4 Ste5_[MEK]--Ste7; 1--3 Ste5_[BDSte5]--Ste5_[BDSte5]
#         """)
#         rxncon = Rxncon("""
#                    Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste7-5-5-11>
#                   <Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]
#                        """)
###### genauer beobachten #####
#         rxncon = Rxncon("""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Comp>
# <Comp>; OR <C1>; OR <C2>
# <C1>; AND Ste7--Ste11
# <C2>; 1--2 Ste5_[MEKK]--Ste11; 3--4 Ste5_[MEK]--Ste7; 1--3 Ste5_[BDSte5]--Ste5_[BDSte5]""")

#####################################################################################################################################
        #simple chain
        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n B_ppi_C; x A--B \n C_ppi_D; ! B--C')

        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B \n B_ppi_C; ! A--B \n C_ppi_D; ! B--C')
        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B; x A--C \n A_ppi_C; ! A--B; x A--F \n C_ppi_D; ! A--C')
        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B \n A_ppi_C; ! A--B; x A--F \n C_ppi_D; ! A--C')  ## prob
        #rxncon = Rxncon('A_ppi_C; ! A--B \n C_ppi_D; ! A--C')
                        
        #rxncon = Rxncon('A_ppi_B \n A_ppi_F; ! A--B \n A_ppi_C; ! A--B; x A--F')# \n C_ppi_D; ! A--C')
        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B \n B_ppi_C; ! A--B \n C_ppi_D; ! B--C')
        #rxncon = Rxncon('A_ppi_B; x B--C \n B_ppi_C; x A--B')
        #rxncon = Rxncon('A_ppi_B \n B_ppi_C; ! A--B')
        #rxncon = Rxncon('A_ppi_B; k+ A--F \n B_ppi_C; ! A--B')
        
        #rxncon = Rxncon('Slt2_[DB]_ppi_Swi4_[c] \n Swi4_BIND_SCBG1; x Slt2_[DB]--Swi4_[c]; x Swi4_[n]--[c] \n Swi4_[n]_ipi_Swi4_[c]; x Slt2_[DB]--Swi4_[c]')

        #rxncon = Rxncon('X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B; x A--C \n A_ppi_C; x A--F')  ## prob
        ### states koennen nicht existieren wenn sie mutually exclussive sind (ueberschreibe nicht die orginal contingencies)

        #rxncon = Rxncon('Cdc42_ppi_Ste20; ! Cdc42_[GnP]-{P}; ! Ste20_[KD]--[CRIB2] \n Ste20_[KD]_ipi_Ste20_[CRIB2]')
        
        
        #rxncon = Rxncon('A_ppi_B; ! A_[X]-{P} \n Z_TRSC_C \n B_TRSL_C; x <complex> \n <complex>; OR A--B; OR D--B \n X_p-_A_[X] ')

        #rxncon = Rxncon('X_p-_A_[X] \n A_ppi_B; ! A_[X]-{P} Fus3_[docking_site]_ppi_Sst2_[MAPK_site]; ! <Fus3_phos> \n <Fus3_phos>; OR  Fus3_[(T180)]-{P}; OR  Fus3_[(Y182)]-{P}')
        #complex issue AND OR
        #rxncon = Rxncon('Enzyme_GEF_Gpa1; K+  <Ste2_state> \n <Ste2_state>; AND  Gpa1_[Ste2_site]--Ste2_[Gpa1_site]; OR  Pheromone_[Ste2_site]--Ste2_[Pheromone_site]')

        #rxncon = Rxncon('Fus3_[docking_site]_ppi_Sst2_[MAPK_site] \n Kss1_[docking_site]_ppi_Sst2_[MAPK_site]')
        #print dir(rxncon.reaction_pool['B_TRSL_C'])
        #print rxncon.reaction_pool['B_TRSL_C'].sp_state
        #rxncon = Rxncon('A_ppi_B; ! A_[X]-{P} \n Ste12_TRSL_Dig2; x <Ste12_non_monomer> \n <Ste12_non_monomer>; OR Dig1_[Ste12_site]--Ste12_[Dig1_site]; OR Dig2_[Ste12_site]--Ste12_[Dig2_site]; OR Kss1_[docking_site]--Ste12_[MAPK_site]; OR Fus3_[docking_site]--Ste12_[MAPK_site] \n X_p-_A_[X]')
        #rxncon = Rxncon('Swi4_[c]_ppi_Swi6_[c] \n Swi4_[n]_ipi_Swi4_[c]; x Swi4_[c]--Swi6_[c]')

        #rxncon = Rxncon('Swi4_ppi_Swi6; ! Swi4_[n]--[d] \n Swi4_[n]_ipi_Swi4_[c]')

        #rxncon = Rxncon('Swi6_[c]_ppi_Swi4_[c]; ! Swi4_[n]--[c]')

        #rxncon = Rxncon('Swi4_[c]_ppi_Swi6_[c]; k+ Swi4_[n]--[d]')

        #rxncon = Rxncon('Swi6_[c]_ppi_Swi4_[c] \n Swi4_[n]_ipi_Swi4_[c]; x Swi6_[c]--Swi4_[c]')

        #rxncon = Rxncon('Cdc42_ppi_Ste20_[CRIB2]; ! Cdc42_[GnP]-{P}; x Ste20_[KD]--[CRIB2] \n Ste20_[KD]_ipi_Ste20_[CRIB2]')


        ##### print test #########

#         rxncon = Rxncon("""
#         Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; x Ste5_[MEKK]--Ste11
# Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; ! <Ste11^{M/50}>
# Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; K+ Hkr1_[TMD]--Sho1_[TMD]
# Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; K+ Msb2_[TMD]--Sho1_[TMD]
# Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; K+ Msb2_[CyT]--Sho1_[CyT]
# <Ste11^{M/50}>; and Opy2_[BDSte50]--Ste50_[RA]
# <Ste11^{M/50}>; and Ste11_[SAM]--Ste50_[SAM]



# A_ppi_C; K+ <bool>
#         <bool>; AND A--D; AND A--E
#         A_ppi_C; K+ <bool2>
#         <bool2>; AND B--F; AND B--G


#         Cdc24_[GEF]_GEF_Cdc42_[GnP]; ! <Cdc24^{M}>

#  <Cdc24^{M}>; or <Cdc24^{M/4}>
#  <Cdc24^{M/4}>; and Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
#  <Cdc24^{M/4}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
#  <Cdc24^{M}>; or <Cdc24^{M/F}>
#  <Cdc24^{M/F}>; and Cdc24_[AssocFar1]--Far1_[c]
#  <Cdc24^{M/F}>; and <Far1^{M}>
#  <Far1^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
#  <Far1^{M}>; and Far1_[nRING-H2]--Ste4_[AssocFar1]""")


        #rxncon = Rxncon(input_data)
        #print rxncon
        ###################################################################################
        rxncon.run_process()
        #print rxncon.complex_pool
        self.bngl_src = Bngl(
            rxncon.reaction_pool, rxncon.molecule_pool, rxncon.contingency_pool)
        # print bngl_src.get_src()


    def test_change(self):
        """
        Tests that molecules_pool is created and
        containe right number of molecules.
        rxn = Rxncon('C_p+_B_[C] \n A_ppi_B; ! B_[C]-{P}')
        rcont = rxn.reaction_pool['A_ppi_B']

        cont = Contingency('A_ppi_B', 'K+', get_state('A_[T666]-{P}'))
        # #print "rxn.contingency_pool: ", rxn.contingency_pool.get_required_contingencies()
        ComplexApplicator(rcont, []).apply_complexes()
        cap = ContingencyApplicator()
        cap.apply_on_container(rcont, cont)

        rxn.apply_contingencies(rcont)
        for reaction in rcont:
            reaction.run_reaction()



             rxn = Rxncon('C_p+_B_[C] \n A_ppi_B; ! B_[C]-{P}')
        rcont = rxn.reaction_pool['A_ppi_B']

        cont = Contingency('A_ppi_B', 'K+', get_state('A_[T666]-{P}'))
        # #print "rxn.contingency_pool: ", rxn.contingency_pool.get_required_contingencies()



        for rcont in rxn.reaction_pool:
            ComplexApplicator(rcont, []).apply_complexes()
            print dir(rcont)
            if rxn.reaction_pool['A_ppi_B'] == rcont:
                cap = ContingencyApplicator()
                cap.apply_on_container(rcont, cont)

                rxn.apply_contingencies(rcont)
                for reaction in rcont:
                    reaction.run_reaction()
            else:
                for reaction in rcont:
                    reaction.run_reaction()
        """
        # print "self.basic_cont: ", self.basic_cont
        print "bngl_src: ", self.bngl_src.get_src()
        pass
        # rxn = Rxncon('C_p+_B_[C] \n A_ppi_B; x B_[C]-{P}'
        # rxn.run_process()
        # rcont = rxn.reaction_pool['C_p+_B_[C]']

        # test_cont = rxn.reaction_pool['A_ppi_B']

        # for reaction in test_cont:

        # reaction.run_reaction()
        # print "reaction.substrat_complexes: ", reaction.substrat_complexes
        # cont = Contingency('C_p+_B_[C]', 'K+', get_state('A--B'))
        # cont_exc = Contingency('C_p+_B_[C]', '!', get_state('A--B'))
        # cont_exc2 = Contingency('C_p+_B_[C]', '!', get_state('B_[C]-{P}'))
        # cont_x = Contingency('C_p+_B_[C]', 'x', get_state('A--B'))
        # print "rxn.contingency_pool: ",
        # rxn.contingency_pool.get_required_contingencies()

        # print dir(get_state('A--B'))
        # print dir(get_state('A--B').components[0])
        # print get_state('A--B').components[0].name

        # for rcont in rxn.reaction_pool:
        #     ComplexApplicator(rcont, []).apply_complexes()
        # print dir(rcont)
        #     #

        #     if rxn.reaction_pool['C_p+_B_[C]'] == rcont:
        #         cap = ContingencyApplicator()
        #         ContingencyApplicator().apply_on_container(rcont, cont)

        #         rxn.apply_contingencies(rcont)
        #         for i, reaction in enumerate(rcont):
        # cap2 = ContingencyApplicator()
        # reaction_clone = reaction.clone()

        # print dir(reaction)

        # print reaction.product_complexes

        # if comp == get_state('A--B'):

        # m = Molecule("A")
        # new = BiologicalComplex()
        # new.molecules.append(m)
        # reaction.product_complexes.append(new)
        # cap.apply_on_reaction_product(reaction,cont_x)
        # cap.apply_on_reaction(reaction,cont_x)
        # rxn.apply_contingencies(rcont)
        #             reaction.run_reaction()
        #             component_names = [component.name for component in get_state('A--B').components]
        #             print component_names
        #             new_complex = []
        #             for comp in reaction.substrat_complexes:
        #                 if len(comp.molecules) == len(get_state('A--B').components):
        #                     print "reaction.product_complexes: ", reaction.product_complexes
        #                     print "comp: ", comp
        #                     print "comp.molecules: ", comp.molecules
        #                     print "HIER"

        # mol_index = comp.molecules.index(reaction.right_reactant)  # get the index of the molecule in the molecule List
        #                     mol = comp.molecules[mol_index].remove_bond(get_state('A--B'))
        #                     new = BiologicalComplex()
        #                     new.side = 'L'
        #                     mol.remove_bond(get_state('A--B'))
        #                     new.molecules.append(mol)
        # new_complex.append(new)
        #                     new_complex.append(new)
        #                     new = BiologicalComplex()
        #                     new.side = 'R'
        #                     for molecule in comp.molecules:
        #                         if mol.name != molecule.name and molecule.name in component_names:
        #                             if molecule.has_bond(get_state('A--B')):
        #                                 molecule.remove_bond(get_state('A--B'))
        #                             new.molecules.append(molecule)
        # new_complex.append(new)

        #                     new_complex.append(new)
        #                 else:
        #                     new_complex.append(comp)
        #             if new_complex:
        #                 reaction.product_complexes = new_complex
        #                 ContingencyApplicator().apply_on_reaction_product(reaction,cont_exc)
        #                 rxn.apply_contingencies(rcont)
        #                 reaction.run_reaction

        # for comp in reaction.product_complexes:

        #     if reaction.right_reactant in comp.molecules:
        #         print comp.molecules
        #         print comp.molecules[0]
        # print comp.molecules[1]
        # mol_index = comp.molecules.index(reaction.right_reactant)  # get the index of the molecule in the molecule List
        #         mol = comp.molecules[mol_index]
        #         new_complex = []
        #         for molecule in comp.molecules:
        #             if molecule.name != mol.name:
        #                 pass
        #         cap = ContingencyApplicator()
        #         cap.apply_on_complex(comp, cont_x)

        # new_complex.append(molecule)
        # reaction.product_complexes.append(new_complex)
        # print "dir(mol): ", dir(mol)
        # print "mol.name: ", mol.name
        # print "mol.binding_partners: ", mol.binding_partners
        # cap.apply_on_molecule(mol,cont_x)
        #mol.binding_partners = []
        # mol.remove_bond(get_state('A--B'))

        #reaction_clone = reaction.clone()

        # for comp in reaction.substrat_complexes:
        #     print comp
        #     cap.apply_on_complex(comp,cont_exc)

        #     cap.apply_on_complex(comp, cont_exc)

        #rcont[i] = reaction
        # rcont.add_reaction(reaction_clone)

        # rxn.apply_contingencies(rcont)
        # reaction.run_reaction()
        # cont_x = Contingency('C_p+_B_[C]', 'x', get_state('A--B'))
        # cont_exc = Contingency('C_p+_B_[C]', '!', get_state('A--B'))
        # cap.apply_on_reaction_product(reaction, cont_exc)
        # cap.apply_on_reaction(reaction, cont_exc)

        # reaction.run_reaction()
        # reaction_clone.run_reaction()
        #     else:
        #         rxn.apply_contingencies(rcont)
        #         for reaction in rcont:
        #             reaction.run_reaction()
        # initially container has one reaction
        # (changes after running the process because of OR and K+/K-)

        # for reaction in rcont:
        # reaction.run_reaction()

        # for reaction in rcont:
        # reaction.run_reaction()
        # rxn.run_process()
        # #
        # ComplexApplicator(self.rcont, []).apply_complexes()

        # self.bngl_src = Bngl(rxn.reaction_pool, rxn.molecule_pool, rxn.contingency_pool)
        # print "bngl_src: ", self.bngl_src.get_src()


# class x_exclamation_mark_Tests(TestCase):
#     """
#     Unit test for the new logic implementation of x and !
#     """

#     def setUP(self):

#         """
#         Prepares data for tests.
#         """
#         print "HIER"
#         self.basic_cont = Rxncon('A_ppi_B; ! A--C')
#         self.basic = Rxncon('A_ppi_B')

#     def test_change(self):
#         print "DA"
#         print self.basic
#         self.basic_cont.find_conflict()


if __name__ == '__main__':
    main()
