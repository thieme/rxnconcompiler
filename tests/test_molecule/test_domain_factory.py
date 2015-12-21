#!/usr/bin/env python

"""
Unit Tests for domain_factory.py module.

Acceptance Tests for domain naming feature.
Test entire rule examples (also updainting 
modification domains and warnings).
"""

from unittest import main, TestCase

from rxnconcompiler.compiler import Compiler
from rxnconcompiler.molecule.domain_factory import DomainFactory, Domain

DOMAINS_ASSOSIATION = """A_BIND_DNA
A_ppi_C; ! A--DNA"""

DOMAINS_MODIFICATION = """X_P+_A
A_ppi_B; ! A-{P}
"""
class DomainFactoryTests(TestCase):
    """Tests for DomainFactoryTests"""
    def setUp(self):
        """
        Sets DomainFactory objest.
        """
        self.df = DomainFactory()

    def test_association_domain_from_str(self):
        """
        Tests whether correct association domain name is returned given a string.
        """
        result = self.df.get_association_domain_from_str('X--Y', 'A')
        self.assertEqual(result.name, 'AssocY')
        result = self.df.get_association_domain_from_str('X_[xxx]--Y_[yyy]', 'A')
        self.assertEqual(result.name, 'xxx')

    def test_association_domain_from_dict(self):
        """
        Tests whether correct association domain name is returned given a dict.
        (A row from xls_tables).
        """
        pass
            
    def test_modification_domain_from_str(self):
        """ 
        Tests whether correct modification domain name is return given a string.
        """
        result = self.df.get_modification_domain_from_str('A-{P}')
        self.assertEqual(result.name, 'bd')
        result = self.df.get_modification_domain_from_str('A_[XxX]-{P}')
        self.assertEqual(result.name, 'XxX')

    def test_modification_domain_from_dict(self):
        """ 
        Tests whether correct modification domain name is return given a dictionary.
        (a row from xls_tables).
        """
        pass

    def test_localisation_domain(self):
        """
        Should return loc.
        """
        loc_dom = self.df.get_localisation_domain()
        self.assertEqual(loc_dom.name, 'loc')

    def test_domain_object_dsr(self):
        dsr = "d/s(r)"
        domain = Domain(dsr)
        self.assertEqual(domain.main,"d")
        self.assertEqual(domain.sub,"s")
        self.assertEqual(domain.residue,"r")
        self.assertEqual(domain.name, "dsr")
        self.assertEqual(domain.raw_name, dsr)

    def test_domain_object_set_domain_info(self):
        domain = Domain("")
        domain.set_domain_info("d","s","r")
        self.assertEqual(domain.main,"d")
        self.assertEqual(domain.sub,"s")
        self.assertEqual(domain.residue,"r")
        self.assertEqual(domain.name, "dsr")
        self.assertEqual(domain.raw_name, "d/s(r)")


        
class DomainAcceptanceTests(TestCase):
    """Establishes default domains naming in rxncon."""
    
    def test_association(self):
        """
        Default domain is name of the binding partner. 
        Uper and lower case preserved as it is.
        """
        bngl = Compiler(DOMAINS_ASSOSIATION).translate()
        #print "bngl: ", bngl
        #rule = "A(AssocDNA) + DNA(AssocA) <-> A(AssocDNA!1).DNA(AssocA!1)"
        rule1 = "A(AssocDNA) + DNA(AssocA) -> A(AssocDNA!1).DNA(AssocA!1)"
        rule2 = "A(AssocC!2,AssocDNA!1).C(AssocA!2).DNA(AssocA!1) -> A(AssocC,AssocDNA) + C(AssocA) + DNA(AssocA)"
        rule3 = "A(AssocC,AssocDNA!1).DNA(AssocA!1) -> A(AssocC,AssocDNA) + DNA(AssocA)"
        self.assertIn(rule1, bngl)
        self.assertIn(rule2, bngl)
        self.assertIn(rule3, bngl)

    def test_modification(self):
        """
        Problem: default domain created in a reaction 
        is not identical with default domain used in contingencies.
        Solution: rxncon recognises that default 
        A_[bd]-{P} can match A-[anything]-{P}.
        
        1. rxncon searches through the present product states.
        2. It exchanges bd with other domain name 
           (to avoid errors while runing BioNetGen)selfself.
        3. If there are no reaction that produces A-{P} - generates WARNING. 
        4. When there are two such reactions: 
           takes the first one as a default and generates WARNING.
        """
        # one phosphorylation reaction - should be OK.
        bngl = Compiler(DOMAINS_MODIFICATION).translate()
        rule = "A(X~P,AssocB) + B(AssocA) <-> A(X~P,AssocB!1).B(AssocA!1)"
        #self.assertIn(rule, bngl)
        self.assertNotIn('WARNING', bngl)
        
        # two phosphorylation reactions.
        inp ='X_P+_A\nA_ppi_B; ! A-{P}\nY_P+_A'
        bngl = Compiler(inp).translate()
        #self.assertIn(rule, bngl)
        self.assertIn('WARNING', bngl)

        # no phosphorylation reaction.
        bngl = Compiler("A_ppi_B; ! A-{P}").translate()
        rule = "A(bd~P,AssocB) + B(AssocA) <-> A(bd~P,AssocB!1).B(A!1)"
        #self.assertIn(rule, bngl)
        self.assertIn('WARNING', bngl)
        
    def test_relocalization(self):
        """
        Relocalisation: loc domain.
        """ 
        pass

            

if __name__ == '__main__':
    main()