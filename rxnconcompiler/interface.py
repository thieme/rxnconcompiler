#!/usr/bin/env python

"""
Module rxnconCompiler_interface containes 
functions from Compiler used in the GUI.
"""

import argparse
import json
from rxncon import Rxncon
from compiler import Compiler
from bngl.bngl_output import BnglOutput
from bngl.bngl import Bngl

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


def get_bngl(inp, reaction_ids=None, max_stoich=4, file_name=None):
    """
    Returns BNGL code for given xls_tables.
    """
    comp = Compiler(inp)
    xls_tables = comp.xls_tables
    xls_tables = filter_reactions(xls_tables, reaction_ids)
    if not file_name:
        return Compiler(xls_tables).translate(True, True, True, True)
    f = open(file_name, 'w')
    f.write(Compiler(xls_tables).translate(True, True, True, True))
    f.close()

def get_rxncon(inp, file_name=None):
    """
    Returns data as rxncon string. 
    """
    if not file_name:
        return str(Rxncon(inp))
    f = open(file_name, 'w')
    f.write(str(Rxncon(inp)))
    f.close()

def get_json_reactions(inp, file_name=None):
    """Returns rxncon dict as a json string."""
    comp = Compiler(inp)
    reactions = json.dumps({'reaction_list': comp.xls_tables['reaction_list']}, indent=4, sort_keys=True)
    if file_name:
        f = open(file_name, 'w')
        f.write(reactions)
        f.close()
    return reactions    

def get_json_contingencies(inp, file_name=None):
    """Returns contingency list as json """
    comp = Compiler(inp)
    cont = json.dumps({'contingency_list': comp.xls_tables['contingency_list']}, indent=4, sort_keys=True)
    if file_name:
        f = open(file_name, 'w')
        f.write(cont)
        f.close()
    return cont

def get_json_definitions(inp, file_name=None):
    comp = Compiler(inp)
    definitions = json.dumps({'reaction_definition': comp.xls_tables['reaction_definition']}, indent=4, sort_keys=True)
    if file_name:
        f = open(file_name, 'w')
        f.write(definitions)
        f.close()
    return definitions

def get_json(inp, file_name=None):
    """Returns json format for rxncon"""
    comp = Compiler(inp)
    rxn = json.dumps(comp.xls_tables, indent=4, sort_keys=True)
    if file_name:
        f = open(file_name, 'w')
        f.write(rxn)
        f.close()
    return rxn    

    
def get_bngl_reactions(inp, reaction_ids=None):
    """
    Returns rules secion and parameters section.
    """
    # xls_tables
    comp = Compiler(inp)
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


        
def main():
    """
    Defines CLI for rulebased module.
    """
    #KR: cool, in particular that you dont need BioNetGen.
    #    do you have tests for main()?
    parser = argparse.ArgumentParser()
    parser.add_argument("rxncon_input", \
        help="Rxncon language input as xls file, json, txt, or string.")
    parser.add_argument("-o", "--output", \
        help="path to the output file")
    parser.add_argument("-s", "--max_stoich", default='4',\
        help="Value of max stoich variable in bngl.")
    parser.add_argument('--json', dest='mode', action='store_const', \
        const='json', default='bngl', \
        help='Indicate the output type as json (default: bngl).')
    parser.add_argument('--rxncon', dest='mode', action='store_const', \
        const='rxncon', default='bngl', \
        help='Indicate the output type as rxncon (default: bngl).')
    args = parser.parse_args()

    if args.rxncon_input:
        output_file = args.output or 'rxnconcompiler.output'        
        if args.mode == 'json':
            get_json(args.rxncon_input, output_file)
        elif args.mode == 'rxncon':
            get_rxncon(args.rxncon_input, output_file)
        elif args.mode == 'bngl':
            get_bngl(args.rxncon_input, None, args.max_stoich, output_file)

if __name__ == '__main__':
    main()


