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
        table3 = parse_text('A_ppi_B\nA_ppi_C\nX_P+_B\nA_DEG_D\n')
        self.definitions3 = ReactionDefinitions(table3)
        template = parse_text("A_ppi_B\nA_p+_C\nA_p-_B\n C_ap_D")

    def test_categories_dict(self):
        """
        Tests correct creation of categories_dict 
        from the default_definition.py 
        (default_definition.py is used when quick input is used).
        dict looks like {'Covalent Modification': 'p+', 'p-', ...'} 
        """
        cat_dict = self.definitions3.categories_dict
        self.assertEqual(len(cat_dict.keys()), 3)
        self.assertIn('Covalent Modification', cat_dict.keys())
        self.assertIn('Association', cat_dict.keys())
        self.assertIn('Synthesis/Degradation', cat_dict.keys())
        self.assertIn('p+', cat_dict['Covalent Modification'])
        self.assertIn('ppi', cat_dict['Association'])
        self.assertIn('deg', cat_dict['Synthesis/Degradation'])

    def test_template_information(self):
        for key, value in self.definitions3:
            if key == "deg":
                self.assertEqual(value['Category'], 'Synthesis/Degradation')
                self.assertEqual(value['Directionality'], 'undirectional')
                self.assertEqual(value['ReactionTypeID'], '3,4')
                self.assertEqual(value['Reversibility'], 'irreversible')
                self.assertEqual(value['SourceState[Component]'], 'ComponentB')
                self.assertEqual(value['ProductState[Component]'], 'N/A')
            elif key == "p+":
                self.assertEqual(value['ReactionTypeID'], u'1.1.1.1',)
                self.assertEqual(value['Category'], u'Covalent Modification')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB',)
                self.assertEqual(value['SourceState[Component]'], u'N/A',)

                #'ProductState[Modification]': u'-{P}',
                #'SourceState[Modification]': u'N/A',
                self.assertEqual(value['Reversibility'], u'irreversible',)
                self.assertEqual(value['Directionality'], u'unidirectional')
            elif key == "p-":
                self.assertEqual(value['ReactionTypeID'], u'1.1.2.1',)
                self.assertEqual(value['Category'], u'Covalent Modification',)

                self.assertEqual(value['ProductState[Component]'], u'N/A')
                self.assertEqual(value['SourceState[Component]'], u'ComponentB')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

#
# {
# #### AP
#     'ReactionTypeID': u'1.1.1.2',
#     'Category': u'Covalent Modification',
#
#     'ProductState[Component]': u'ComponentB',
#     'SourceState[Component]': u'N/A',
#
#     'Reversibility': u'irreversible',
#     'Directionality': u'unidirectional'
#
# # 'ProductState[Modification]': u'-{P}',
#
#
#  #'SourceState[Modification]': u'N/A'
#  },
#
# {
# #### PT
# 'ReactionTypeID': u'1.1.3.1',
# 'Category': u'Covalent Modification',
#
#  'ProductState[Component]': u'ComponentB',
# 'SourceState[Component]': u'ComponentA',
#
#  'Reversibility': u'reversible',
#  'Directionality': u'bidirectional'
#  #'ProductState[Modification]': u'-{P}',
#
#  #'SourceState[Modification]': u'-{P}'
# },
#
#
# {
# #### CUT
#  'ReactionTypeID': "1.2.1.1",
#  'Category': u'Covalent Modification',
#
#  'ProductState[Component]': u'ComponentB',
#  'SourceState[Component]': u'N/A',
#
#  'Reversibility': u'irreversible',
#  'Directionality': u'unidirectional'
#  #'ProductState[Modification]': u'-{Truncated}',
#  #'SourceState[Modification]': u'N/A'},
# },
#
# ######## Association Reactions #####
# {
# #### ppi, i, bind
# 'ReactionTypeID': u'2.1.1.1',
# 'Category': u'Association',
#
# 'ProductState[Component]': u'ComponentA',
# 'SourceState[Component]': u'N/A',
#
# 'Reversibility': u'reversible',
# 'Directionality': u'nondirectional',
#
#
#  #'ProductState[Modification]': u'--ComponentB',
#  #'SourceState[Modification]': u'N/A'},
#
# },
#
# {
# #### ipi
# 'ReactionTypeID': u'2.1.1.2',
# 'Category': u'Association',
#
# 'ProductState[Component]': u'ComponentA',
# 'SourceState[Component]': u'N/A',
#
# 'Reversibility': u'reversible',
# 'Directionality': u'nondirectional',
#  #'ProductState[Modification]': u'--ComponentB',
#  #'SourceState[Modification]': u'N/A'},
#
# },
# {
# #### Transcription
#     'ReactionTypeID': "3,1",
#     'Category': u'Synthesis/Degradation',
#
#     'ProductState[Component]': u'ComponentB-mRNA',
#     'SourceState[Component]': u'N/A',
#
#     'Reversibility': u'irreversible',
#     'Directionality': u'unidirectional',
#
# # 'ProductState[Modification]': u'N/A',
# #'SourceState[Modification]': u'N/A'
# },
#     {
# #### Translation
#  'ReactionTypeID': "3,2",
#  'Category': u'Synthesis/Degradation',
#
#  'ProductState[Component]': u'ComponentB',
#  'SourceState[Component]': u'N/A',
#
#  'Reversibility': u'irreversible',
#  'Directionality': u'unidirectional',
# # 'ProductState[Modification]': u'N/A',
#  #'SourceState[Modification]': u'N/A'},
#
#     },
# {
# #### Degredation
# 'ReactionTypeID': "3,4",
# 'Category': u'Synthesis/Degradation',
#
#  'ProductState[Component]': u'N/A',
# 'SourceState[Component]': u'ComponentB',
#
#  'Reversibility': u'irreversible',
#  'Directionality': u'unidirectional',
#  #'ProductState[Modification]': u'N/A',
# # 'SourceState[Modification]': u'N/A'
# },
#
# {
# #has to be changed
#     'ReactionTypeID': "3,5",
# 'Category': u'Synthesis/Degradation',
#
#  'ProductState[Component]': u'N/A',
# 'SourceState[Component]': u'ComponentB',
#
#  'Reversibility': u'irreversible',
# 'Directionality': u'unidirectional',
#  #'ProductState[Modification]': u'N/A',
#  # 'SourceState[Modification]': u'N/A'
# },
#     {
# #has to be changed
#  'ReactionTypeID': "3,3",
#  'Category': u'Synthesis/Degradation',
#
#  'ProductState[Component]': u'ComponentB',
#  'SourceState[Component]': u'N/A',
#
#  'Reversibility': u'irreversible',
#  'Directionality': u'unidirectional',
#
#
# # 'ProductState[Modification]': u'N/A',
#
#
#  #'SourceState[Modification]': u'N/A'
#     },

if __name__ == '__main__':
    main()

