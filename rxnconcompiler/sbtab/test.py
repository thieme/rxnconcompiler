
'''
This script tests the sbtab to rxncon (and vice versa) parser and translator
'''

from rxnconcompiler.parser.rxncon_parser import *
from rxnconcompiler.sbtab.parser import *


if __name__=="__main__":
    xls_tables= parse_xls('sbtab_files/tiger_files_csv_cut/output_parser/output.xls')
    print xls_tables
    obj1= Rxncon(xls_tables)

    p=SBtabParser('rxncon', 'sbtab_files/tiger_files_csv_cut/', 'xls')
    p.parse_SBtab2rxncon()
    obj2= p.rxncon

    print obj1
    print obj2
    
