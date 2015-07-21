# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015


import SBtab
import os
import tablib
import tablibIO
import csv


def isequal(a, b):
    '''
    Compares two strings case insensitively
    '''
    try:
        return a.lower() == b.lower()
    except AttributeError:
        return a == b

def get_files(inputdir):
    '''
    Returns list of files (and only files) inside given input directory
    '''

    files = [ f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir,f)) ]

    return files


def check_directory_type(inputdir):
    '''
    Checks whether input directory consists of SBtab, rxncon, both or other files
    '''
    rxncon_detected = False
    sbtab_detected = False
    other_files = False

    files=get_files(inputdir)

    for filename in files:

        if filename.endswith('.txt'):
            with open(filename, 'r') as f:
                first_line= f.readline().strip()
                if 'SBtab' in first_line:
                    sbtab_detected=True

                    #Den Fall abfangen ob text oder xls /  ods ist. Wenn txt dann nach dem header suchen, den es noch nicht
                    #gibt. ich werde den festelgen (sowas wie # rxncon_version = dings oder so)
                    #wenn es xls / ods ist gucken wie die Reiter in dem File heissen. Wenn 'Contingency list' vorkommt ist es
                    #rxncon

                elif 'rxncon' in first_line:
                    # sollte im rxncon header fuer txt files vorkommen, gibt es bisher nicht
                    rxncon_detected=True
                else:
                    other_files=True

        elif filename.endswith('.xls'):
            pass

        elif filename.endswith('.ods'):
            pass

        elif filename.endswith('.csv'):
            with open(inputdir+'/'+filename, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                try:
                    first_line = csvfile.readline().strip()
                    if 'SBtab' in first_line:
                        sbtab_detected=True
                    else:
                        sys.exit('Can not handel input file %s.\nInput files must be either in SBtab or rxncon format.' % (filename))

                #error catching
                except csv.Error as e:
                    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

        else:
            other_files=True


    if rxncon_detected==True:
        if sbtab_detected==True:
            print 'Error, both SBtab and rxncon files detected in input directory!'
        elif other_files==True:
            print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
        else:
            print 'Directory of rxncon files detected. Starting parser.'
            #look_for_rxncon_files, starte rxcon to sbtab parsing
    elif sbtab_detected==True:
        if other_files==True:
            print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
        else:
            print 'Directory of SBtab files detected. Starting parser.'
            look_for_SBtab_files(inputdir)



def look_for_SBtab_files(inputdir):
    '''
    Checks whether alle needed SBtab files are inside given Directory:
    - ReactionList
    - ContingencyID
    - rxncon_Definition
    - Gene
    '''

    files = get_files(inputdir)

    for filename in files:

        #print 'Filename: ', filename

        table_file = open(inputdir+'/'+filename,'r')
        table = table_file.read()
        tablib_table = tablibIO.importSetNew(table,filename)
        ob = SBtab.SBtabTable(tablib_table,filename)

        print ob.table_type

        #print '##########################'
        #get_info(ob)




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
    check_directory_type('example_files')
    print '------------------------'
    check_directory_type('tiger_files')

    #print ob
