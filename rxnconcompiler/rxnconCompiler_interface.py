#!/usr/bin/env python

"""
Module rxnconCompiler_interface containes 
functions from Compiler used in the GUI.
"""

from rulebased import Compiler, Rxncon, Bngl
from bngl.bngl_output import BnglOutput

def parse(rxncon_input):
    """
    returns dict
    gets xls/txt/dict
    """
    comp = Compiler(rxncon_input)
    return comp.xls_tables

def filter_reactions(xls_tables, id_list=None):
    """
    Filters reactions in xls_tables (xls_tables[reaction_list])
    if id_list empty returns whole xls_tables,
    else xls_tables[reaction_list] containsindicated reactions.
    """
    comp = Compiler(xls_tables)
    xls_tables = comp.xls_tables
    if not id_list:
        return xls_tables
    temp = []
    id_list = [str(rid) for rid in id_list]
    for reaction in xls_tables['reaction_list']:
        if str(reaction['ReactionID']) in id_list:
            temp.append(reaction)
    new_xls = {}
    new_xls['reaction_list'] = temp
    new_xls['reaction_definition'] = xls_tables['reaction_definition']
    new_xls['contingency_list'] = xls_tables['contingency_list']
    return new_xls


def get_src(xls_tables, reaction_ids=None, max_stoich=4):
    """
    Returns BNGL code for given xls_tables.
    """
    comp = Compiler(xls_tables)
    xls_tables = comp.xls_tables
    xls_tables = filter_reactions(xls_tables, reaction_ids)
    return Compiler(xls_tables).translate(True, True, True, True)


def get_reactions(xls_tables, reaction_ids=None):
    """
    Returnd rules secion and parameters section.
    """
    # xls_tables
    comp = Compiler(xls_tables)
    xls_tables = comp.xls_tables
    xls_tables = filter_reactions(xls_tables, reaction_ids)
    # Rxncon
    rxncon = Rxncon(xls_tables)
    rxncon.run_process(True, True, True, True)
    # Bngl
    bngl = Bngl(rxncon.reaction_pool, \
            rxncon.molecule_pool, rxncon.contingency_pool, rxncon.war)
    # BnglOutput
    output = BnglOutput(bngl.rule_pool, bngl.molecule_pool, bngl.warnings)
    output.create_sections_txt()
    return output.parameters_txt, output.rules_txt