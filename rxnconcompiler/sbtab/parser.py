# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015


import SBtab
import os
import tablibIO
import csv
import xlrd
import sys
import re
from rxnconcompiler.parser.rxncon_parser import parse_xls
from rxnconcompiler.definitions.default_definition import DEFAULT_DEFINITION # default definition tabelle machen
from rxnconcompiler.rxncon import Rxncon

def get_files(inputdir):
    """
    Returns list of files (and only files) inside given input directory
    """
    files = [ f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir,f)) and not f.startswith('.') ]
    #                                            is no directory                          is no libre office temp file
    return files


def check_directory_type(inputdir):
    '''
    Checks whether input directory consists of SBtab, rxncon, both or other files
    '''
    #print inputdir, '      delete this print in the end, check_directory_type()'

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
            print 'Found File(s) in .ods format. This format ist not supported. ' \
                  '\nPlease export to .xls or .txt format (Open/Libre Office can do this).\n' \
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
                if look_for_SBtab_files(inputdir)=='txt':
                    print "Warning: You can export the files in current directory only to rxncon quick format (.txt)." \
                          "         Not all needed Files for xls export are found." \
                          "         If you still choose xls export, the program will crash."
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
    NOT SUPPORTED YET
    '''
    #sbtab_detected, rxncon_detected, other_detected = check_ods_File(filedir, sbtab_detected, rxncon_detected, other_detected)
    #return sbtab_detected, rxncon_detected, other_detected

    pass

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
    - ReactionID
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


        p = re.compile('rxncon_definition.*') # every file with that name, no matter what file format
        # achtung: es gibt ein mal eine sbatb seitige rxncon_definition datei und eine rxcon seitige.
        # wenn die rxncon seitige fehlt, wird die default erstellt und verwendet
        # keine ahnung wozu die sbtab seitige sein soll...
        m = p.match(filename)
        if m:
            rxncon_def_found=True
            print "rxncon_Definition file detected."



    if 'ReactionList' in found_table_types and 'ReactionID' in found_table_types and'ContingencyID' in found_table_types and 'Gene' in found_table_types:
        #not needed anymore, rxncon_definition gets createdget created
        #if rxncon_def_found and 'Definition' in found_table_types:
        return 'xls'
        #else:
            #print 'Error: In order to translate the SBtab Format to rxncon you need the "rxncon_Definition" File inside this directory' \
                  #'you can download it here:'
            #print 'www.rxncon.org'
            #return False
    elif 'ReactionID' in found_table_types and'ContingencyID' in found_table_types:
        return 'txt'
    else:
        print 'Error: In order to translate the SBtab Format to rxncon you need tables with following TableTypes:' \
              ' - ReactionList(only for export to xls)' \
              ' - ReactionID' \
              ' - ContingencyID' \
              ' - Gene(only for export to xls)' \


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
    #print '\nGlobals: '
    #print globals()
    print '\nLocals: '
    print locals()
    print '\nCallable: '
    print callable(ob)
    print ''

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
    #output_format='' #delete
    #reactivate :
    output_format= raw_input('Please enter the output format. Possible are .txt & .xls (default= .txt):\n')
    if output_format=='':
        output_format='txt'
    else:
        output_format = output_format[-3:]
    if output_format!='txt' and output_format!='xls':
        print 'Error, the format ',output_format,' is not supported.'

    reaction_def_found=False
    if 'reaction_definition' in files:
        reaction_def_found=True

    ob_list=[] # List of dictionaries
    for filename in files:
        #print 'Filename: ', filename
        ob= build_SBtab_object(inputdir, filename)
        ob_list.append({'object':ob, 'type':ob.table_type, 'filename':filename })

        #print '##########################'
    #get_info(ob)

    if output_format=='xls':
        print 'Sorry, this functionality is not yet implemented. Exporting to txt now.'
        output_format='txt'

    if output_format=='txt':
        for ob in ob_list:
            if ob['type']=='ContingencyID':
                # Find column indexes for !Target, !Contingency and !Modifier columns
                targ_col_index= ob['object'].columns.index('!Target')
                cont_col_index= ob['object'].columns.index('!Contingency')
                modi_col_index= ob['object'].columns.index('!Modifier')
                
                # Save the data of these three columns to lists
                contingency_id=0
                contingency_list=[{}]
                for row in ob['object'].getRows():
                    contingency_list.append({
                        'ContingencyID': contingency_id,
                        'Target': row[targ_col_index],
                        'Contingency': row[cont_col_index],
                        'Modifier': row[modi_col_index]
                    })
                    contingency_id += 1
                contingency_list.pop(0)

            elif ob['type']=='ReactionID':
                # Find column indexes for !ComponentA:Name, !ComponentA:Domain, !ComponentA:Subdomain, !ComponentA:Residue, !Reaction, !ComponentB:Name, !ComponentB:Domain, !ComponentB:Subdomain, !ComponentB:Residue
                indexes_dict={
                    'can': ob['object'].columns.index('!ComponentA:Name'),
                    'cad': ob['object'].columns.index('!ComponentA:Domain'),
                    'cas': ob['object'].columns.index('!ComponentA:Subdomain'),
                    'car': ob['object'].columns.index('!ComponentA:Residue'),

                    'rea': ob['object'].columns.index('!Reaction'),

                    'cbn': ob['object'].columns.index('!ComponentB:Name'),
                    'cbd': ob['object'].columns.index('!ComponentB:Domain'),
                    'cbs': ob['object'].columns.index('!ComponentB:Subdomain'),
                    'cbr': ob['object'].columns.index('!ComponentB:Residue')
                }

                # Save the data of these three columns to list of dictionaries
                reaction_list=[{}]

                for row in ob['object'].getRows():
                    reaction_list.append({
                        'ReactionType': row[indexes_dict['rea']],
                        'ComponentA[Name]': row[indexes_dict['can']],
                        'ComponentA[Domain]': row[indexes_dict['cad']],
                        'ComponentA[Subdomain]': row[indexes_dict['cas']],
                        'ComponentA[Residue]': row[indexes_dict['car']],
                        'ComponentB[Name]': row[indexes_dict['cbn']],
                        'ComponentB[Domain]': row[indexes_dict['cbd']],
                        'ComponentB[Subdomain]': row[indexes_dict['cbs']],
                        'ComponentB[Residue]': row[indexes_dict['cbr']],
                        'Reaction[Full]': build_full(row,indexes_dict)
                    })
                reaction_list.pop(0)
            if not reaction_def_found:
                reaction_definition = DEFAULT_DEFINITION
            else:
                # build reaction definition
                pass

        #rxncon = Rxncon(dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition), parsed_xls=True) #build rxncon object
        rxncon = Rxncon(dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition))


        # write contents to txt File
        write_rxncon_txt(inputdir,rxncon)


def build_full(row,d):
    '''
    Creates Full Reaction String from given SBtab reaction row and a dictionary, that tells in which column is what.
    Template: ComponentA_[Domain/Subdomain(Residue)]_reaction_ComponentB_[Domain/Subdomain(Residue)]
    '''
    out=''
    out+=row[d['can']]

    if row[d['cad']]:
        out+='_['+row[d['cad']]
        if row[d['cas']]:
            out+='/'+row[d['cas']]
        if row[d['car']]:
            out+='('+row[d['car']]+')'
        out+=']'
    elif row[d['cas']]:
        out+='_['+row[d['cas']]  # if no domain but only subdomain is given, the subdomain becomes domain. is that correct?
        if row[d['car']]:
            out+='('+row[d['car']]+')'
        out+=']'
    elif row[d['car']]:
        out+='_[(' + row[d['car']] + ')]'

    out+='_'+row[d['rea']]+'_'

    # Reaction B
    out+=row[d['cbn']]
    if row[d['cbd']]:
        out+='_['+row[d['cbd']]
        if row[d['cbs']]:
            out+='/'+row[d['cbs']]
        if row[d['cbr']]:
            out+='('+row[d['cbr']]+')'
        out+=']'
    elif row[d['cbs']]:
        out+='_['+row[d['cbs']]  # if no domain but only subdomain is given, the subdomain becomes domain. is that correct?
        if row[d['cbr']]:
            out+='('+row[d['cbr']]+')'
        out+=']'
    elif row[d['cbr']]:
        out+='_[(' + row[d['cbr']] + ')]'

    return out

# def magic(liste von targets, liste von full rxns):
#     '''
#     Checks whether all targets match a full reaction. Validation of Full Reaction creation function
#     '''

def parse_rxncon2SBtab(inputdir):
    xls_tables= parse_xls(inputdir)
    pass

def write_rxncon_txt(inputdir, rxncon):
    '''
    Gets rxncon Object and saves it as a txt file
    '''
    outputname= 'output'+'.txt'
    output_directory='output_parser'

    if not os.path.exists(inputdir+'/'+output_directory):
        os.mkdir(inputdir+'/'+output_directory)
    f = open(inputdir+'/'+output_directory+'/'+outputname, "w")
    f.write('# rxncon_version=12345\trxncon_format=quick\n')
    f.write(str(rxncon))

    # Close opened file
    f.close()

    print 'Succes! Saved File in:', inputdir+'/'+output_directory+'/'+outputname

def hello():
    '''
    Introduces parser to user and reads input directory from comment line
    '''
    print 'You are using rxncon SBtab parser.' \
          'If you want to parse a rxncon file to a SBtab file, the following input filetypes are supported:' \
          ' - .txt' \
          ' - .xls'
    print 'If you want to parse a SBtab file to a rxncon file, these input filetypes are supported:' \
          ' - .xls' \
          ' - .csv'
    print ''
    inputdir = raw_input('Please enter the path to the directory containing your network files: \n') # only works in python 2.x, for python3 would be input()

    return inputdir


if __name__=="__main__":

    #'to be' usage:
    inputdir= hello()
    check_directory_type(inputdir)


    #check_directory_type('sbtab_files/example_files(sbtab)_csv')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_ods')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_xls')
    #print '------------------------'
    #check_directory_type('sbtab_files/tiger_files_csv')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_txt')

    #read rxncon input:
    #parse_rxncon2SBtab('rxncon_files/rxncon_xls/rxncon_simple_example-1.xls')
