import os

import rxnconcompiler.sbtab.tablibIO as tablibIO
import rxnconcompiler.sbtab.SBtab as SBtab


def build_SBtab_object(inputdir, filename):
    '''
    Gets input directory and filename of SBtab formatted File and creates Object from this using SBtab Library.
    If file contents multiple sheets, multiple objects get returned
    '''
    if os.path.isfile(inputdir):
        table_file = open(inputdir, 'r')
    else:
        table_file = open(inputdir + '/' + filename, 'r')
    table = table_file.read()
    if filename[-3:] == 'xls':
        tablib_table = tablibIO.haveXLS(table, True, False)
        ob_list = [SBtab.SBtabTable(dataset, filename) for dataset in tablib_table._datasets]
        return ob_list
    else:
        tablib_table = tablibIO.importSetNew(table, filename)
        ob = SBtab.SBtabTable(tablib_table, filename)
        return [ob]


def build_rxncon_dict(inputdir, filename):
    d = parse_rxncon(inputdir + '/' + filename)
    return d
