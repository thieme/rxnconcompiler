#!/usr/bin/env python

"""
Unit tests for bngl_output.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.molecule.state import get_state
from rxnconcompiler.rxncon import Rxncon
from rxnconcompiler.bngl.rule import Rule
from rxnconcompiler.bngl.rule_factory import RuleFactory
from rxnconcompiler.bngl.bngl_output import BnglOutput, BnglTranslator


Ste11 = """Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste11-7>
<Ste11-7>; OR Ste7--Ste11; OR <Ste7-5-5-11>
<Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]"""

class BnglTranslatorTests(TestCase):
    """
    Unit Tests for BnglTranslator (rule_output.py)
    """
    def setUp(self):
        rxncon = Rxncon(Ste11)
        rxncon.run_process()
        self.rections = rxncon.reaction_pool['Ste11_[KD]_P+_Ste7_[(ALS359)]']
        self.translator = BnglTranslator()

    def test_complex_str(self):
        """
        Tests that BnglTranslator returns corect complex string 
        from BiologicalComplex object.
        """
        product = self.rections[0].product_complexes[0]
        self.assertEqual(self.translator.get_complex_str(product), "Ste11(AssocSte7!1).Ste7(ALS359~P,AssocSte11!1)")
        product = self.rections[1].product_complexes[0]
        #self.assertEqual(self.translator.get_complex_str(product), "Ste11(AssocSte5!3,AssocSte7).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte5!1)")
        self.assertEqual(self.translator.get_complex_str(product), "Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte11,AssocSte5!1)")
                                                                   
    def test_rule_str(self):
        """
        Tests that BnglTranslator returns correct rule string from Rule object.
        for this reaction the tree looks like

                Ste7 (cid:1)
                /   \
    (cid:2) Ste11   Ste5 (cid:3)
                    /   \
        (cid:4) Ste11   Ste5 (cid:5)

        Hence we have two different Ste11 considering here
            Ste11 with cid: 2 for the first rule
            Ste11 with cid: 4 for the second rule
        """
        rule = Rule(self.rections[0])
        expected = "Ste11(AssocSte7!1).Ste7(ALS359~U,AssocSte11!1) -> Ste11(AssocSte7!1).Ste7(ALS359~P,AssocSte11!1)    k1\n"
        result = self.translator.get_rule_str(rule)
        self.assertEqual(expected, result)

        rule = Rule(self.rections[1])
        expected = "Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte11,AssocSte5!1)    k1\n"
        result = self.translator.get_rule_str(rule)
        self.assertEqual(expected, result)

    def test_get_binding_domain(self):
        """"""
        bt = BnglTranslator()
        state = get_state(' Ste5_[Ste11]--Ste11_[Ste5]')
        self.assertEqual(bt.get_binding_domain('Ste5', state, None), 'Ste11')


class BnglOutputTests(TestCase):
    """
    Unit Tests for BnglOutput class (rule_output.py).
    """
    def setUp(self):
        rxncon = Rxncon(Ste11)
        rxncon.run_process()
        rule_factory = RuleFactory(rxncon.reaction_pool, rxncon.contingency_pool)
        self.output = BnglOutput(rule_factory.rule_pool, rxncon.molecule_pool)

    def test_molecules_section(self):
        self.output.create_molecule_type_section()
        result = self.output.molecules_txt
        expected = """begin molecule types
Ste11
Ste7(ALS359~U~P)
end molecule types\n\n"""
        self.assertEqual(result, expected)


    def test_species_section(self):
        self.output.create_seed_species_section()
        result = self.output.species_txt
        expected = """begin seed species
Ste11                                                                                      100
Ste7(ALS359~U)                                                                             100
end seed species\n\n"""
        self.assertEqual(result, expected)
        



if __name__ == '__main__':
    main()