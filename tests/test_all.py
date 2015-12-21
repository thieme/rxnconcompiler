#!/usr/bin/env python

"""
All tests for rxncon modules.
"""

from unittest import main, TestCase
# test tree
from test_tree.test_tree import TestTree
#
from test_rxncon import RxnconTests
from test_compiler import CompilerTests
from test_interface import InterfaceTests, CliTests

# test_acceptance
# DATA_SETS for testing can be changed in the test files
#from test_acceptance.test_bionetgen_acceptance import BioNetGenTests  # requires BioNetGen and Perl
from test_acceptance.test_bngl_sections_acceptance import MoleculesTests
from test_acceptance.test_rules_acceptance import RuleAcceptanceTests

# test_biological_complex
from test_biological_complex.test_biological_complex import BiologicalComplexTests, AlternativeComplexesTests
from test_biological_complex.test_complex_applicator import ComplexApplicatorTests
from test_biological_complex.test_complex_builder import BiologicalComplexBuilderTests

# test_bngl
from test_bngl.test_bngl import BnglTests
from test_bngl.test_bngl_output import BnglTranslatorTests, BnglOutputTests
from test_bngl.test_requirements import RequirementsGeneratorTests, RequirementsFactoryTests

# test_contingency
from test_contingency.test_contingency import ContingencyTests, BooleanContingencyTests, \
	ComplexContingencyTests
from test_contingency.test_contingency_applicator import ContingencyApplicatorTests
from test_contingency.test_contingency_factory import ContingencyFactoryTests, \
	ContingencyApoptosisTests, ContingencyMAPKTests, ContingencyWrapperTests, \
	ComplexTests

# test_definitions
from test_definitions.test_definitions import ReactionDefinitionTests

# test_molecule
from test_molecule.test_domain_factory import DomainFactoryTests, DomainAcceptanceTests
from test_molecule.test_molecule import MoleculeTests
from test_molecule.test_state import StateFactoryTests, StateTests

# test_parser
from test_parser.test_rxncon_parser import RxnconTextParserTests, RxnconXlsParserTests, RxnconParserTests, RxnconParserConingencyManipulationTests

# test_reaction
from test_reaction.test_rate import RateTests
from test_reaction.test_reaction import ReactionTests
from test_reaction.test_reaction_container import ReactionContainerTests
from test_reaction.test_reaction_factory import ReactionFactoryTests

# test_util
from test_util.test_util import UtilTests

# test_SBtab
from test_sbtab.test_sbtab_parser import DirCheckTest
#from test_sbtab.test_sbtab_parser import DataManipulationTest
from test_sbtab.test_sbtab_parser import ParserTest



if __name__ == '__main__':
    main()