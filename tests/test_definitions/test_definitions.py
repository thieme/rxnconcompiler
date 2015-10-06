#!/usr/bin/env python

"""
Unit Tests for definitions.py module.
"""

from unittest import main, TestCase

from rxnconcompiler.parser.rxncon_parser import parse_text
from rxnconcompiler.definitions.definitions import ReactionDefinitions
from rxnconcompiler.definitions.reaction_template import REACTION_TEMPLATE

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
        template = parse_text("A_ppi_B\nA_p+_C\nA_p-_B\n C_ap_D \n C_pt_D \n A_cut_D \n A_[x]_ipi_A_[y] \n A_trsc_B \n A_trsl_B \n A_deg_D\n A_produce_B \n A_consume_B")

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
        for key, value in self.definitions3.iteritems():
            if key == "deg":
                self.assertEqual(value['Category'], 'Synthesis/Degradation')
                self.assertEqual(value['Directionality'], 'unidirectional')
                self.assertEqual(value['ReactionTypeID'], '3,4')
                self.assertEqual(value['Reversibility'], 'irreversible')
                self.assertEqual(value['SourceState[Component]'], 'ComponentB')
                self.assertEqual(value['ProductState[Component]'], 'N/A')

            elif key == "p+":
                self.assertEqual(value['ReactionTypeID'], u'1.1.1.1',)
                self.assertEqual(value['Category'], u'Covalent Modification')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB',)
                self.assertEqual(value['SourceState[Component]'], u'N/A',)

                self.assertEqual(value['Reversibility'], u'irreversible',)
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "p-":
                self.assertEqual(value['ReactionTypeID'], u'1.1.2.1',)
                self.assertEqual(value['Category'], u'Covalent Modification',)

                self.assertEqual(value['ProductState[Component]'], u'N/A')
                self.assertEqual(value['SourceState[Component]'], u'ComponentB')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "ap":
                #### AP
                self.assertEqual(value['ReactionTypeID'], u'1.1.1.2')
                self.assertEqual(value['Category'], u'Covalent Modification')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB')
                self.assertEqual(value['SourceState[Component]'], u'N/A')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "pt":
                #### PT
                self.assertEqual(value['ReactionTypeID'], u'1.1.3.1')
                self.assertEqual(value['Category'], u'Covalent Modification')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB')
                self.assertEqual(value['SourceState[Component]'], u'ComponentA')

                self.assertEqual(value['Reversibility'], u'reversible')
                self.assertEqual(value['Directionality'], u'bidirectional')

            elif key == "cut":
                #### CUT
                self.assertEqual(value['ReactionTypeID'], "1.2.1.1")
                self.assertEqual(value['Category'], u'Covalent Modification')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB')
                self.assertEqual(value['SourceState[Component]'], u'N/A')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')
######## Association Reactions #####
            elif key == "ppi":
                #### ppi, i, bind
                self.assertEqual(value['ReactionTypeID'], u'2.1.1.1')
                self.assertEqual(value['Category'], u'Association')

                self.assertEqual(value['ProductState[Component]'], u'ComponentA')
                self.assertEqual(value['SourceState[Component]'], u'N/A')

                self.assertEqual(value['Reversibility'], u'reversible')
                self.assertEqual(value['Directionality'], u'nondirectional')

            elif key == "ipi":

                #### ipi
                self.assertEqual(value['ReactionTypeID'], u'2.1.1.2')
                self.assertEqual(value['Category'], u'Association')

                self.assertEqual(value['ProductState[Component]'], u'ComponentA')
                self.assertEqual(value['SourceState[Component]'], u'N/A')

                self.assertEqual(value['Reversibility'], u'reversible')
                self.assertEqual(value['Directionality'], u'nondirectional')

            elif key == "trsc":
                #### Transcription
                self.assertEqual(value['ReactionTypeID'], "3,1")
                self.assertEqual(value['Category'], u'Synthesis/Degradation')

                self.assertEqual(value['ProductState[Component]'], u'ComponentB-mRNA')
                self.assertEqual(value['SourceState[Component]'], u'N/A')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "trsl":
                #### Translation
                 self.assertEqual(value['ReactionTypeID'], "3,2")
                 self.assertEqual(value['Category'], u'Synthesis/Degradation')

                 self.assertEqual(value['ProductState[Component]'], u'ComponentB')
                 self.assertEqual(value['SourceState[Component]'], u'N/A')

                 self.assertEqual(value['Reversibility'], u'irreversible')
                 self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "deg":
                #### Degredation
                self.assertEqual(value['ReactionTypeID'], "3,4")
                self.assertEqual(value['Category'], u'Synthesis/Degradation')

                self.assertEqual(value['ProductState[Component]'], u'N/A')
                self.assertEqual(value['SourceState[Component]'], u'ComponentB')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "consume":
                self.assertEqual(value['ReactionTypeID'], "3,5")
                self.assertEqual(value['Category'], u'Synthesis/Degradation')

                self.assertEqual(value['ProductState[Component]'], u'N/A')
                self.assertEqual(value['SourceState[Component]'], u'ComponentB')

                self.assertEqual(value['Reversibility'], u'irreversible')
                self.assertEqual(value['Directionality'], u'unidirectional')

            elif key == "produce":
                 self.assertEqual(value['ReactionTypeID'], "3,3")
                 self.assertEqual(value['Category'], u'Synthesis/Degradation')

                 self.assertEqual(value['ProductState[Component]'], u'ComponentB')
                 self.assertEqual(value['SourceState[Component]'], u'N/A')

                 self.assertEqual(value['Reversibility'], u'irreversible')
                 self.assertEqual(value['Directionality'], u'unidirectional')


if __name__ == '__main__':
    main()

