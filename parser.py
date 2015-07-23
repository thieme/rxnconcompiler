# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015


import SBtab
import os
#import tablib
import tablibIO
import csv
import xlrd
import sys
import re

def get_files(inputdir):
    """
    Returns list of files (and only files) inside given input directory
    """
    files = [ f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir,f)) ]

    return files


def check_directory_type(inputdir):
    '''
    Checks whether input directory consists of SBtab, rxncon, both or other files
    '''
    print inputdir

    rxncon_detected = False
    sbtab_detected = False
    other_detected = False

    files=get_files(inputdir)

    for filename in files:
        filedir= inputdir+'/'+filename

        if filename.startswith('.'):
            #skips temp files
            continue

        if filename.endswith('.txt'):
            sbtab_detected, rxncon_detected, other_detected = check_txt_File(filedir, sbtab_detected, rxncon_detected, other_detected)

        elif filename.endswith('.xls'):
            # Read Excel Document
            sbtab_detected, rxncon_detected, other_detected = check_xls_File(filedir, sbtab_detected, rxncon_detected, other_detected)

        elif filename.endswith('.ods'):
            # Read Open / Libre Office Document
            print 'Found File(s) in .ods format. This format ist not supported. Please use .xls or .txt format.\n' \
                  'If you want to translate from SBtab to rxncon you can also use .csv format.'
            #sbtab_detected, rxncon_detected, other_detected = check_ods_File(filedir, sbtab_detected, rxncon_detected, other_detected)

        elif filename.endswith('.csv'):
            # Read csv Table
            sbtab_detected, rxncon_detected, other_detected = check_csv_File(filedir, sbtab_detected, rxncon_detected, other_detected)
            if rxncon_detected:
                sys.exit('Found rxncon file in .csv Format. This is not supported, please export zu .xls or Quick Format in .txt')

        else:
            other_detected=True


    if rxncon_detected==True:
        if sbtab_detected==True:
            print 'Error, both SBtab and rxncon files detected in input directory!'
        elif other_detected==True:
            print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
        else:
            print 'Directory of rxncon files detected. Starting parser.'
            #look_for_rxncon_files, starte rxcon to sbtab parsing
    elif sbtab_detected==True:
        if other_detected==True:
            print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
        else:
            print 'Directory of SBtab files detected. Starting parser.'
            if look_for_SBtab_files(inputdir):
                parse_SBtab2rxncon(inputdir)

def check_txt_File(filedir, sbtab_detected, rxncon_detected, other_detected):
    '''
    Checks whether txt file is rxncon, SBtab or other file type
    '''
    with open(filedir, 'r') as f:
                first_line= f.readline().strip()
                if 'SBtab' in first_line:
                    sbtab_detected=True
                elif 'rxncon' in first_line:
                    # sollte im rxncon header fuer txt files vorkommen, gibt es bisher nicht
                    rxncon_detected=True
                else:
                    other_detected=True

    return sbtab_detected, rxncon_detected, other_detected

def check_xls_File(filedir, sbtab_detected, rxncon_detected, other_detected):
    '''
    Checks whether xls file is rxncon, SBtab or other file type
    '''
    xlsreader = xlrd.open_workbook(filedir)
    xls_sheet_names = xlsreader.sheet_names()
    first_sheet = xlsreader.sheet_by_index(0)

    first_line = first_sheet.row(0)
    for cell in first_line:
        if '!!SBtab' in str(cell):
            sbtab_detected=True

    for sheet_name in xls_sheet_names:
        if 'Contingency' in sheet_name or 'contingency' in sheet_name:
            rxncon_detected=True

    if sbtab_detected==False and rxncon_detected==False:
        other_detected=True

    return sbtab_detected, rxncon_detected, other_detected

def check_ods_File(filedir, sbtab_detected, rxncon_detected, other_detected):
    '''
    Checks whether ods file is rxncon, SBtab or other file type
    '''
    return sbtab_detected, rxncon_detected, other_detected

def check_csv_File(filedir, sbtab_detected, rxncon_detected, other_detected):
    '''
    Checks whether csv file is rxncon, SBtab or other file type
    '''
    # cant be rxncon file then
    with open(filedir, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            first_line = csvfile.readline().strip()
            if 'SBtab' in first_line:
                sbtab_detected=True
            else:
                other_detected=True

        #error catching
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filedir, csvreader.line_num, e))

    return sbtab_detected, rxncon_detected, other_detected

def look_for_SBtab_files(inputdir):
    '''
    Checks whether all needed SBtab tables are inside given directory/document
    - ReactionList
    - ContingencyID
    - rxncon_Definition
    - Gene
    '''

    files = get_files(inputdir)
    found_table_types=[]
    rxncon_def_found=False

    for filename in files:
        #print 'Filename: ', filename
        ob= build_SBtab_object(inputdir, filename)
        found_table_types.append(ob.table_type)

        #print '##########################'
        #get_info(ob)

        #print files

        p = re.compile('rxncon_Definition.*') # every file with that name, no matter what file format
        m = p.match(filename)
        if m:
            rxncon_def_found=True



    if 'ReactionList' in found_table_types and 'ContingencyID' in found_table_types and 'Gene' in found_table_types:
        if rxncon_def_found and 'Definition' in found_table_types:
            return True
        else:
            print 'Error: In order to translate the SBtab Format to rxncon you need the "rxncon_Definition" File inside this directory' \
                  'you can download it here:'
            print 'www.rxncon.org'
            return False
    else:
        print 'Error: In order to translate the SBtab Format to rxncon you need tables with following TableTypes:' \
              ' - ReactionList' \
              ' - ContingencyID' \
              ' - Gene' \
              ' - Definition (inside "rxncon_Definition" File)'
        return False

def build_SBtab_object(inputdir, filename):
    '''
    Gets input directory and filename of SBtab formatted File and creates Object from this using SBtab Library
    '''
    table_file = open(inputdir+'/'+filename,'r')
    table = table_file.read()
    tablib_table = tablibIO.importSetNew(table,filename)
    ob = SBtab.SBtabTable(tablib_table,filename)
    return ob


def look_for_rxncon_sheets(inputdir):
    '''
    Checks whether all needed sheets are inside given rxcon File in given directory:
    - Reaction List
    - Contingency List
    - Reaction definition
    '''
    pass




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

def parse_SBtab2rxncon(inputdir):
    '''
    Main function for parsin SBtab --> rxncon Format
    '''
    files = get_files(inputdir)
    ob_list=[]

    for filename in files:
        #print 'Filename: ', filename
        ob= build_SBtab_object(inputdir, filename)
        ob_list.append(ob)

        #print '##########################'
        #get_info(ob)

if __name__=="__main__":
    #read_sbtab_csv('BIOMD0000000061_Reaction.csv')
    #print '--------------------------------------'
    #read_sbtab_csv('BIOMD0000000061_Compound.csv')
    #ob = SBtabTools.openSBtab('tiger_files/Tiger_et_al_TableS1_SBtab_Reaction.csv')
    #print os.listdir('tiger_files')
    #look_for_SBtab_files('tiger_files/Tiger_et_al_TableS1_SBtab_Reaction.csv')
    # check_directory_type('sbtab_files/example_files(sbtab)_csv')
    # print '------------------------'
    # check_directory_type('sbtab_files/example_files(sbtab)_ods')
    # print '------------------------'
    # check_directory_type('sbtab_files/example_files(sbtab)_xls')
    # print '------------------------'
    check_directory_type('sbtab_files/tiger_files_csv')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_txt')

