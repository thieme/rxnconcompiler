# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015


import SBtab
import os
import tablib
import tablibIO


def isequal(a, b):
    '''
    Compares two strings case insensitively
    '''
    try:
        return a.lower() == b.lower()
    except AttributeError:
        return a == b

def look_for_SBtab_files(inputdir):
    '''
    Checks whether alle needed SBtab files are inside given Directory:
    - ReactionList
    - ContingencyID
    - rxncon_Definition
    - Gene
    '''
    
    for filename in os.listdir(inputdir):

        table_file = open(inputdir+'/'+filename,'r')
        table = table_file.read()
        tablib_table = tablibIO.importSetNew(table,filename)
        ob = SBtab.SBtabTable(tablib_table,filename)
        
        print ob.table_type
    



def get_info(ob):
    '''
    Function that gives some Information about given Object and current working enviroment
    '''
    print 'Print: '
    print ob
    print '\nType: '
    print type(ob)
    print'\nDir: '
    print dir(ob)
    #print getattr(ob)
    #print hasattr(ob)
    print '\nGlobals: '
    print globals()
    print '\nLocals: '
    print locals()
    print '\nCallable: '
    print callable(ob)

def get_SBtab_info(ob):
    '''
    Uses SBtab methods to print out some Information about input SBtabTable instance
    '''

    print 'Columns:\t', ob.columns
    print 'Header_row: \t', ob.header_row
    #print ob.sbtab_list
    #print ob.table
    print 'TableType:\t', ob.table_type


if __name__=="__main__":
    #read_sbtab_csv('BIOMD0000000061_Reaction.csv')
    #print '--------------------------------------'
    #read_sbtab_csv('BIOMD0000000061_Compound.csv')
    #ob = SBtabTools.openSBtab('tiger_files/Tiger_et_al_TableS1_SBtab_Reaction.csv')
    #print os.listdir('tiger_files')
    #look_for_SBtab_files('tiger_files/Tiger_et_al_TableS1_SBtab_Reaction.csv')
    look_for_SBtab_files('example_files')
    print '------------------------'
    look_for_SBtab_files('tiger_files')
    
    #print ob
