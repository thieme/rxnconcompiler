#!/usr/bin/env python

"""
Class Compiler: translates any rxncon language input 
                (json, string, dict, xls, txt) into BNGL.
"""

from parser.rxncon_parser import parse_rxncon
from rxncon import Rxncon
from bngl.bngl import Bngl

class Compiler:
    """
    Compiler object translates given rxncon input (xls file or quick text)
    into BioNetGen source code (BNGL file).

    TODO: rename to RxnconCompiler (Copiler not specific)
    TODO: add functions for translation into other formats
    TODO: apply filters
    TODO: write any output write_bngl ---> write_output
    """
    def __init__(self, input_data):
        """
        Keeps single xls object.
        """
        self.xls_tables = parse_rxncon(input_data)

    def translate(self, add_translation=False, add_missing_reactions=False, add_complexes=True, add_contingencies=True): 
        """
        Translates Rxncon data into bngl string.
        Uses Rxncon and Bngl objects.
        """
        rxncon = Rxncon(self.xls_tables)
        rxncon.run_process(add_translation, add_missing_reactions, add_complexes, add_contingencies)
        bngl = Bngl(rxncon.reaction_pool, \
            rxncon.molecule_pool, rxncon.contingency_pool, rxncon.war)
        bngl_src = bngl.get_src()
        return bngl_src

    def write_bngl(self, bngl_src, output_path):
        """
        Writes bngl string to file.
        """
        output_file = open(output_path, 'w')
        output_file.write(bngl_src)
