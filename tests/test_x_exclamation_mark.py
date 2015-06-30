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



        # rxncon = Rxncon("""
        #                 Kss1_[dockingSite]_ppi_Sst2_[MAPKSite]; ! <Kss1phos>; x <Sst2mod>
        #                 <Kss1phos>; OR  Kss1_[(T183)]-{P}; OR  Kss1_[(Y185)]-{P}
        #                 <Sst2mod>; AND Ste2_[Sst2Site]--Sst2_[Ste2Site]; AND Sst2_[(S539)]-{P}
        #                 Kss1_P+_Sst2_[(S539)]; ! Kss1_[dockingSite]--Sst2_[MAPKSite]
        #                 Kss1_P+_Sst2_[(S539)]; ! <Kss1phos>
        #                 """)

        #rxncon = Rxncon("""
        #               A_ppi_B; ! <AorC>
        #               <AorC>; AND A--C; AND A--D
        #               """)  # works

        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <complAB>
        #                 <complAB>; OR <complA>
        #                 <complAB>; OR <complB>
        #                 <complA>; AND A--E
        #                 <complA>; AND A--F
        #                 <complB>; OR A--C
        #                 <complB>; OR A--D
        #                 """)

        # rxncon = Rxncon("""
        #                  A_ppi_B; ! <complAB>
        #                  <complAB>; OR <complA>
        #                  <complA>; OR A--D
        #                  <complA>; OR B--C
        #                  <complA>; OR <complB>
        #                  <complA>; OR <complC>
        #                  <complB>; AND B--E
        #                  <complB>; AND B--F
        #                  <complC>; OR B--G
                         
        #                 """)
        #rxncon = Rxncon("""A_ppi_B""")
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <AorC>
        #                 <AorC>; OR A_[x]-{P}
        #                 <AorC>; OR B--C
        #                 <AorC>; OR A--D
        #                 <AorC>; OR B_[y]-{P}
        # #                 """)
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <III>
        #                 <III>; AND <II>
        #                 <III>; AND <I>
        #                 <I>; OR A--C
        #                 <I>; OR A--F
        #                 <II>; OR A--D
        #                 <II>; OR A--E
        #                 """)
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp>
        #                 <comp>; AND A--C
        #                 <comp>; AND <comp1>
        #                 <comp1>; OR A--D
        #                 <comp1>; OR A--E
        #                 """)
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp>
        #                 <comp>; OR A--C
        #                 <comp>; OR A--E
        #                 """)
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp>
        #                 <comp>; AND A--C
        #                 <comp>; AND <NOT>
        #                 <NOT>; NOT A-{P}
        #                 """)

        rxncon = Rxncon("""
                        <c2>; OR A--E
                        <c2>; OR A--F
                        <c1>; OR A--C
                        <c1>; OR A--D
                        A_ppi_B; ! <comp>
                        <comp>; AND <c1>
                        <comp>; AND <c2>
                        <comp>; AND A_[x]-{P}
                        A_ppi_C; ! <c2>
                        A_ppi_D; ! <comp1>
                        <comp1>; AND <c2>
                         """)

# expect:

# C, D
# C, not D, E
# not C, F, D
# not C, F, not D, E
        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <AorC> 
        #                 <AorC>; OR <complA>
        #                 <complA>; AND A_[x]-{P}
        #                 <complA>; AND A--D
        #                 <AorC>; OR <complB>
        #                 <complB>; AND B_[y]-{P}
        #                 <complB>; AND B--C
        #                 """)

        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <comp>
        #                 <comp>; or A-{P}
        #                 <comp>; or B-{P}
        #                 <comp>; or <compA>
        #                 <compA>; and A--C
        #                 <compA>; and A--D
        #                 <comp>; or <compB>
        #                 <compB>; and B--E
        #                 <compB>; and B--F
        #                 """)

        # we don't tell that A D E cannot exist as long as F is not bound ?
        # rxncon = Rxncon(""" A_ppi_B; ! <compA>
        #                 <compA>; or <compA1>
        #                 <compA>; or <compA2>
        #                 <compA>; or <compB>
        #                 <compB>; and B--T
        #                 <compB>; and B--Z
        #                 <compA1>; and A--C
        #                 <compA1>; and A--D
        #                 <compA2>; and A--E
        #                 <compA2>; and A--F """) 




       
        #rxncon = Rxncon('A_ppi_B; ! A-{P} \n A_ppi_B; x A-{P}; ! B-{P}')

        # rxncon = Rxncon("""
        #                 A_ppi_B; ! <MM> 
        #                 <MM>; AND B--E
        #                 <MM>; AND <MM2>
        #                 <MM2>; OR B_[x]-{P}
        #                 <MM2>; OR B_[y]-{P}""")  # Prob

        # rxncon = Rxncon("""
        #                A_ppi_B; ! <MM> 
        #                <MM>; AND B--E
        #                <MM>; AND <MM2>
        #                <MM2>; OR A--C
        #                <MM2>; OR A--D""")  # Prob

#                      #<AorC>; AND A_[x]-{P}; AND A_[y]-{P} 
        # rxncon = Rxncon("""
        #                A_ppi_B; ! <MM>
        #                <MM>; OR A--C
        #                <MM>; OR A--D
        #                """)
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


        #rxncon = Rxncon(input_data)
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
