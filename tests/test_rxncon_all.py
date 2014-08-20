#!/usr/bin/env python

"""
All tests for rxncon modules.
"""

from unittest import main, TestCase

# Unit Tests
from test_biological_complex import BiologicalComplexTests, AlternativeComplexesTests
from test_bngl_output import BnglTranslatorTests, BnglOutputTests
from test_contingency import ContingencyTests, BooleanContingencyTests, \
	ComplexContingencyTests
from test_contingency_factory import ContingencyFactoryTests, \
	ContingencyApoptosisTests, ContingencyMAPKTests, ContingencyWrapperTests, \
	ComplexTests
from test_definitions import ReactionDefinitionTests
from test_domain_factory import DomainFactoryTests, DomainAcceptanceTests
from test_molecule import MoleculeTests
from test_rate import RateTests
from test_reaction import ReactionTests
from test_reaction_container import ReactionContainerTests
from test_reaction_factory import ReactionFactoryTests
from test_rulebased import RxnconTests, CompilerTests, BnglTests
from test_rxncon_parser import RxnconTextParserTests, RxnconXlsParserTests
from test_state import StateFactoryTests, StateTests
from test_util import UtilTests

# Acceptance Tests
# DATA_SETS for testing can be changed in the files
#from test_bionetgen_acceptance import BioNetGenTests  # requires BioNetGen and Perl
from test_bngl_sections_acceptance import MoleculesTests
from test_rules_acceptance import RuleAcceptanceTests
from test_interface import RxnconCompilerInterfaceTests



if __name__ == '__main__':
    main()