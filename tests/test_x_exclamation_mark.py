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
        input_data = "/home/thiemese/projects/rxncon/rxncon-unix/web2py/applications/yeastmap/modules/rxncon/test/test_data/Tiger_et_al_TableS1_v3.xls"
        # self.xls_tables = parse_rxncon(input_data)
        #self.basic_cont = Rxncon('Z_P+_A_[Z] \n A_ppi_B; x A_[Z]-{P} \n X_p-_A_[Z]')

        #rxncon = Rxncon('A_ppi_B; ! A_[Z]-{P} \n C_ppi_B; ! A--B \n X_p-_A_[Z]')
        rxncon = Rxncon('Sln1_[HK(H576)]_PT_Sln1_[RR(D1144)] \n Sln1_[RR(D1144)]_PT_Ypd1_[(H64)] \n Ypd1_[(H64)]_PT_Ssk1_[RR(D544)]')
        #rxncon = Rxncon('Z_p+_A_[Z] \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A_[Z]')
        #rxncon = Rxncon("Z_P+_A_[Z] \n A_ppi_B; ! A_[Z]-{P} \n X_p-_A_[Z] \n X_[PD]_P+_Hog1_[(T174)] \n Hog1_[n]_ppi_Hot1_[m]; ! Hog1_[T174]-{P} \n Ptc1_[PD]_P-_Hog1_[(T174)]")
        #rxncon = Rxncon('Z_p+_A_[Z]; ! Z--A \n Z_ppi_A \n A_ppi_B; x A_[Z]-{P} \n X_p-_A_[Z]')
        #rxncon = Rxncon('Ypd1_[(H64)]_PT_Ssk1_[RR(D544)]; ! Ypd1--Ssk1 \n Ssk1_[RR]_ppi_Ssk2_[BDSsk1]; x Ssk1_[RRD544]-{P}; x Ssk1--Ssk22 \n Ssk1_[RR]_ppi_Ssk22; x Ssk1_[RRD544]-{P}; x Ssk1--Ssk2')
        #rxncon = Rxncon('Ypd1_[(H64)]_PT_Ssk1_[RR(D544)] \n Ssk1_[RR]_ppi_Ssk2_[BDSsk1]; x Ssk1_[RRD544]-{P} \n Ssk1_ppi_Ssk22; x Ssk1_[RRD544]-{P}')
        #rxncon = Rxncon('Ypd1_[(H64)]_PT_Ssk1_[RR(D544)]')
        #rxncon = Rxncon('A_p+_X1_[A]; k+ <S1S2> \n <S1S2>; AND X1--X2; AND X2--X3')
        #rxncon = Rxncon('Cdc42_ppi_Ste20; ! Cdc42_[GnP]-{P}; k+ Ste20_[KD]--[CRIB2] \n Ste20_[KD]_ipi_Ste20_[CRIB2]') # changed in master

        #rxncon = Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2 \n Ste20_[KD+CRIB]_ppi_Ste20_[KD+CRIB]; x Cdc42_[ED]--Ste20_[CRIB]')

        #rxncon = Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20]; k+ Ste20_[KD+CRIB]--Ste20_[KD+CRIB] \n Ste20_[KD+CRIB]_ppi_Ste20_[KD+CRIB]; x Cdc42_[ED]--Ste20_[CRIB] \n Ste20_[BR]_ppi_PIP2')

        # conflicted example x! mutual exclusive domains
        #rxncon =  Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20] \n Ste20_[CRIB]_ppi_Ste20_[CRIB]; x Cdc42_[ED]--Ste20_[CRIB] \n Ste20_[BR]_ppi_PIP2')
        #rxncon =  Rxncon('Cdc42_ppi_Ste20; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2 \n Ste20_[KD]_ppi_Ste20_[CRIB]; x Cdc42--Ste20 \n Ste20_[BR]_ppi_PIP2')

        # conflicted example in master branch
        #rxncon =  Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20]; k+ Ste20_[KD]--[CRIB2] \n Ste20_[KD]_ipi_Ste20_[CRIB2]; x Cdc42_[ED]--Ste20_[CRIB] \n Ste20_[BR]_ppi_PIP2')
        #rxncon =  Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20]; k+ Ste20_[KD]--Ste20_[CRIB2] \n Ste20_[KD]_ppi_Ste20_[CRIB2]; x Cdc42_[ED]--Ste20_[CRIB] \n Ste20_[BR]_ppi_PIP2')
        #rxncon =  Rxncon('Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20]; k+ Ste20_[CRIB]--Ste20_[CRIB] \n Ste20_[CRIB]_ppi_Ste20_[CRIB]; x Cdc42_[ED]--Ste20_[CRIB] \n Ste20_[BR]_ppi_PIP2')

        # works in master branch
        

        #rxncon = Rxncon(input_data)
        rxncon.run_process()
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
