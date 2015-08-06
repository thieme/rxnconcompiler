#!/usr/bin/env python

"""
Unit Tests for definitions.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text
from rxnconcompiler.definitions.definitions import ReactionDefinitions


class ReactionDefinitionTests(TestCase):
    """
    Unit Tests for ReactionDeffinition class.
    """

    def setUp(self):
        """
        Prepares data for testing.
        """
        table = parse_text('A_ppi_B\nA_ppi_C\nX_P+_B')
        self.definitions = ReactionDefinitions(table)

    def test_categories_dict(self):
        """
        Tests correct creation of categories_dict 
        from the default_definition.py 
        (default_definition.py is used when quick input is used).
        dict looks like {'Covalent Modification': 'p+', 'p-', ...'} 
        """
        cat_dict = self.definitions.categories_dict
        self.assertEqual(len(cat_dict.keys()), 4)
        self.assertIn('Covalent Modification', cat_dict.keys())
        self.assertIn('p+', cat_dict['Covalent Modification'])
        self.assertIn('ppi', cat_dict['Association'])


if __name__ == '__main__':
    main()

