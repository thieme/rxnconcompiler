# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015


import SBtab
import os
import tablibIO
import tablib
import csv
import xlrd
import xlsxwriter
import sys
import re
from rxnconcompiler.parser.rxncon_parser import parse_rxncon
from rxnconcompiler.parser.rxncon_parser import parse_xls
from rxnconcompiler.definitions.default_definition import DEFAULT_DEFINITION # default definition tabelle machen
from rxnconcompiler.rxncon import Rxncon
#from SBtabTools import createDataset

def get_files(inputdir):
    """
    Returns list of files (and only files) inside given input directory
    """
    if os.path.isdir(inputdir):
        files = [ f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir,f)) and not f.startswith('.') ]
    #                                               is no directory                          is no libre office temp file
        return files
    else:
        print 'Error, can not open input directory(\''+inputdir+'\').'
        exit()




def check_directory_type(inputdir):
    '''
    Checks whether input directory consists of SBtab, rxncon, both or other files
    '''
    print inputdir, '      delete this print in the end, check_directory_type()'

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
            print 'Error, both SBtab and rxncon files detected in input directory! Please clean up the directory!'
        elif other_detected==True:
            print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
        else:
            print 'Directory of rxncon files detected. Starting parser.'
            if look_for_rxncon_files(inputdir):
                parse_rxncon2SBtab(inputdir)
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
        if ('(III) Contingency list' in sheet_name or 'Contingency List' in sheet_name or 'contingency list' in sheet_name) and not 'ContingencyID' in sheet_name:
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

    for filename in files:
        #print 'Filename: ', filename
        ob= build_SBtab_object(inputdir, filename)
        found_table_types.append(ob.table_type)

    if 'ReactionList' in found_table_types and 'ReactionID' in found_table_types and'ContingencyID' in found_table_types and 'Gene' in found_table_types:
        return 'xls'

    elif 'ReactionID' in found_table_types and'ContingencyID' in found_table_types:
        return 'txt'
    else:
        print 'Error: In order to translate the SBtab format to rxncon, you need tables with following TableTypes:' \
              ' - ReactionID' \
              ' - ContingencyID' \
              'Only needed for export to xls format: ' \
              '     - Gene (only for export to xls)' \
              '     - ReactionList(only for export to xls)'
        print 'Only the follwing TableTypes were found:'
        print found_table_types

def look_for_rxncon_files(inputdir):
    '''
    Checks weather all needed rxncon files/sheets are given inside input directory:
    - (I) Reaction List
    - (III) Contingency List
    - (IV) Reaction definition
    '''

    files = get_files(inputdir)
    found_tables=[]

    for filename in files:
        d= build_rxncon_dict(inputdir, filename)
        for table in d.keys():
            found_tables.append(table)

    if 'reaction_definition' in found_tables and 'contingency_list' in found_tables and 'reaction_list' in found_tables:
        return True

    else:
        print 'Error: In order to translate the rxncon format to SBtab, you need the following tables:' \
              ' - reaction_definition' \
              ' - contingency_list' \
              ' - reaction_list' \
              'Only the following tables were found: '
        print found_tables
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

def build_rxncon_dict(inputdir, filename):
    d = parse_rxncon(inputdir+'/'+filename)
    return d


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
    Main function for parsing SBtab --> rxncon Format
    '''
    files = get_files(inputdir)
    output_format='xls' #delete
    #reactivate :
    # output_format= raw_input('Please enter the output format. Possible are .txt & .xls (default= .txt):\n')
    if output_format=='':
        output_format='txt'
    else:
        output_format = output_format[-3:]
    if output_format!='txt' and output_format!='xls':
        print 'Error, the format ',output_format,' is not supported.'

    ob_list=[] # List of dictionaries
    reaction_def_found=False
    for filename in files:
        ob= build_SBtab_object(inputdir, filename)
        ob_list.append({'object':ob, 'type':ob.table_type, 'filename':filename })
        if ob.table_type=='ReactionList' and ob.table_name=='Reaction definitions':
            reaction_def_found=True
            print 'Custom reaction definition file detected in: ' + filename

    if not reaction_def_found:
        print 'No reaction definition file found. Using default.'
        reaction_definition = DEFAULT_DEFINITION
    else:
        reaction_definition=build_reaction_definition(ob_list)

    rxncon = build_rxncon(ob_list, reaction_definition)

    if output_format=='txt':
        write_rxncon_txt(inputdir,rxncon)

    elif output_format=='xls':
        gene_list=build_gene_list(ob_list)
        write_rxncon_xls(inputdir, rxncon, gene_list)


def build_rxncon(ob_list, reaction_definition):
    '''
    Creates rxncon object from given SBtab files
    '''
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
            #     if check_full_rxns(build_full(row,indexes_dict),contingency_list):
            #     ich glaube dieser Check, den Sebastian sich gewuenscht hat macht gar keinen sinn. Es kann auch sein
            #     , dass eine reaction in reactionID existiert, die in ContigencyID gar nicht vorkommt.  oder?
            #         reaction_list.append({
            #             'ReactionType': row[indexes_dict['rea']],
            #             'ComponentA[Name]': row[indexes_dict['can']],
            #             'ComponentA[Domain]': row[indexes_dict['cad']],
            #             'ComponentA[Subdomain]': row[indexes_dict['cas']],
            #             'ComponentA[Residue]': row[indexes_dict['car']],
            #             'ComponentB[Name]': row[indexes_dict['cbn']],
            #             'ComponentB[Domain]': row[indexes_dict['cbd']],
            #             'ComponentB[Subdomain]': row[indexes_dict['cbs']],
            #             'ComponentB[Residue]': row[indexes_dict['cbr']],
            #             'Reaction[Full]': build_full(row,indexes_dict)
            #         })
            #     else:
            #         print 'Was not able to parse the following input row correctly:'
            #         print row
            #         exit()
            # reaction_list.pop(0)
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

    return Rxncon(dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition), parsed_xls=True) #build rxncon object

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

def check_full_rxns(full_reaction, dictionary_list):
    '''
    Checks whether all targets match a full reaction. Validation of Full Reaction creation function
    '''
    for d in dictionary_list:
        if full_reaction.lower().strip() == d['Target'].lower().strip():
            return True
        #else:
         #   print 'missmatch'
          #  print full_reaction, d['Target']

def build_gene_list(ob_list):
    '''
    Creates gene list from given SBtab file
    '''
    for ob in ob_list:
        if ob['type']=='Gene':
        # Find column indexes for !Target, !Contingency and !Modifier columns
            gene_col_index= ob['object'].columns.index('!Gene')
            name_col_index= ob['object'].columns.index('!Name')
            locus_col_index= ob['object'].columns.index('!LocusName')

            # Save the data of these three columns to lists
            gene_list=[{}]
            for row in ob['object'].getRows():
                gene_list.append({
                    'Gene': row[gene_col_index],
                    'Name': row[name_col_index],
                    'LocusName': row[locus_col_index]
                })
            gene_list.pop(0)
    return gene_list

def build_reaction_definition(ob_list):
    '''
    Creates Reaction definition dictionary, from given table
    '''
    for ob in ob_list:
        if ob['type']=='ReactionList':
            indexes_dict={
                'r': ob['object'].columns.index('!Reaction'),
                'ct': ob['object'].columns.index('!Category:Type'),
                'c': ob['object'].columns.index('!Category'),
                'si': ob['object'].columns.index('!SubclassID'),
                's': ob['object'].columns.index('!Subclass'),
                'm': ob['object'].columns.index('!ModifierOrBoundary'),
                'rti': ob['object'].columns.index('!ReactionType:ID'),
                'rt': ob['object'].columns.index('!ReactionType'),
                'rn': ob['object'].columns.index('!Reaction:Name'),
                'rev': ob['object'].columns.index('!Reversibility'),
                'd': ob['object'].columns.index('!Directionality'),
                'ssc': ob['object'].columns.index('!SourceState:Component'),
                'ssm': ob['object'].columns.index('!SourceState:Modification'),
                'psc': ob['object'].columns.index('!ProductState:Component'),
                'psm': ob['object'].columns.index('!ProductState:Modification'),
                'cs': ob['object'].columns.index('!coSubstrates'),
                'cp': ob['object'].columns.index('!coProducts'),
                'co': ob['object'].columns.index('!Comment')
                }
            reaction_definition_list=[{}]
            for row in ob['object'].getRows():
            # reaction_list.pop(0)
                reaction_definition_list.append({
                    'Reaction' : unicode(row[indexes_dict['r']]),
                    'CategoryType' : unicode(row[indexes_dict['ct']]),
                    'Category' : unicode(row[indexes_dict['c']]),
                    'SubclassID' : unicode(row[indexes_dict['si']]),
                    'Subclass' : unicode(row[indexes_dict['s']]),
                    'Modifier or Boundary' : unicode(row[indexes_dict['m']]),
                    'ReactionTypeID' : unicode(row[indexes_dict['rti']]),
                    'ReactionType' : unicode(row[indexes_dict['rt']]),
                    'ReactionName' : unicode(row[indexes_dict['rn']]),
                    'Reversibility' : unicode(row[indexes_dict['rev']]),
                    'Directionality' : unicode(row[indexes_dict['d']]),
                    'SourceState[Component]' : unicode(row[indexes_dict['ssc']]),
                    'SourceState[Modification]' : unicode(row[indexes_dict['ssm']]),
                    'ProductState[Component]' : unicode(row[indexes_dict['psc']]),
                    'ProductState[Modification]' : unicode(row[indexes_dict['psm']]),
                    'coSubstrate(s)' : unicode(row[indexes_dict['cs']]),
                    'coProduct(s)' : unicode(row[indexes_dict['cp']]),
                    'Comments' : unicode(row[indexes_dict['co']])
                    })
            reaction_definition_list.pop(0)
        return reaction_definition_list

def parse_rxncon2SBtab(inputdir):
    '''
    Main function for parsing rxncon--> SBtab Format
    '''
    files = get_files(inputdir)
    output_format='xls' #delete
    #reactivate :
    # output_format= raw_input('Please enter the output format. Possible are .csv, .xls, .tsv, .ods (default= .csv):\n')
    if output_format=='':
        output_format='csv'
    else:
        output_format = output_format[-3:]
    if output_format!='csv' and output_format!='xls' and output_format!='txv' and output_format!='ods':
        print 'Error, the format ',output_format,' is not supported.'




    for file in files:
        filedir=inputdir+'/'+file
        #################################################
        #xls_tables= parse_xls(filedir)
        #print xls_tables
        #################################################
        d= build_rxncon_dict(inputdir,file)
        for key in d.keys():
            #print key
            #print d[key][1]

            tableType=''
            tableName=''
            if 'reaction_list' in key:
                tableType='ReactionID'
                tableName='Reaction list'
                filename='filename1'

                header_row='!!SBtab !!SBtabVersion=\'0.8\' TableType="'+ tableType +'" TableName="'+tableName+'"'
                big=header_row+'\n'
                #columns=d[key][1].keys()
                columns= ['!ReactionID','!ComponentA:Name','!ComponentA:Domain','!ComponentA:Subdomain','!ComponentA:Residue','!Reaction','!ComponentB:Name','!ComponentB:Domain','!ComponentB:Subdomain','!ComponentB:Residue','!Quality','!PubMedIdentifiers','!Comment']
                value_rows=[]
                #print d[key][1].values()
                for row in d[key]:
                    value_rows.append(row.values())

                for col in columns:
                    big= big + col+ ' '

            elif 'contingency_list' in key:
                tableType='ContingencyID'
                tableName='Contingency list'
                filename='filename2'

                header_row='!!SBtab !!SBtabVersion=\'0.8\' TableType="'+ tableType +'" TableName="'+tableName+'"'
                big=header_row+'\n'
            elif 'reaction_definition' in key:
                tableType='ReactionList'
                tableName='Reactions definitions'
                filename='filename3'

                header_row='!!SBtab !!SBtabVersion=\'0.8\' TableType="'+ tableType +'" TableName="'+tableName+'"'
                big=header_row+'\n'

            print '####################################'
            print 'ist:'
            print big
            print ''
            #print len(columns), columns
            #print len(value_rows[1]), value_rows[1]
            #sbtab= createDataset(header_row, columns, value_rows, filename)
            #print sbtab
            print filedir
            print '\nsoll:'
            f= open('sbtab_files/tiger_files_csv_cut/Tiger_et_al_TableS1_SBtab_ReactionID.csv', 'r')
            ff= f.read()
            print ff[0:400]

            fff = tablibIO.importSetNew(ff,filedir)
            ffff = SBtab.SBtabTable(fff,filedir)
            ffff.update()

            #ffff.writeSBtab('csv',filedir, 'test_output')
            ffff.writeSBtab('csvr   ')



def write_rxncon_txt(inputdir, rxncon):
    '''
    Gets rxncon Object and saves it as a txt file
    '''
    outputname= 'output'+'.txt'
    output_directory='output_parser'

    if not os.path.exists(inputdir+'/'+output_directory):
        os.mkdir(inputdir+'/'+output_directory)


    f = open(inputdir+'/'+output_directory+'/'+outputname, "w")
    f.write('# rxncon_version=dynamische get methode\trxncon_format=quick\n')
    f.write(str(rxncon))

    # Close opened file
    f.close()
    print 'Successfully wrote rxncon quick format to '+inputdir+'/'+output_directory+'/'+outputname

def write_rxncon_xls_tablib(inputdir, rxncon):
    '''
    Writes rxncon Object to xls File using Tablib library
    Work was paused because tablib can't set column width
    '''
    outputname= 'output'+'.xls'
    output_directory='output_parser'

    data_R= tablib.Dataset() # (I) Reaction list
    data_R.title= '(I) Reaction list'
    #data_R.headers=['ReactionID'] #''', 'Reaction[Full]', 'SourceState', 'ProductState', 'coSubstrate(s)', 'coProduct(s)',
                    # 'ComponentA[ID]', 'ComponentA[Species]', 'ReactionType', 'ComponentB[ID]', 'ComponentB[Species]',
                    # 'ComponentA[Name]', 'ComponentA[Domain]', 'ComponentA[Subdomain]', 'ComponentA[Residue]','Reaction',
                    # 'ComponentB[Name]', 'ComponentB[Domain]', 'ComponentB[Subdomain]', 'ComponentB[Residue]', 'Quality',
                    # 'PubMedIdentifier(s)', 'Comments']
    data_R.append(['ReactionID', 'Reaction[Full]', 'SourceState', 'ProductState', 'coSubstrate(s)', 'coProduct(s)',
                    'ComponentA[ID]', 'ComponentA[Species]', 'ReactionType', 'ComponentB[ID]', 'ComponentB[Species]',
                    'ComponentA[Name]', 'ComponentA[Domain]', 'ComponentA[Subdomain]', 'ComponentA[Residue]','Reaction',
                    'ComponentB[Name]', 'ComponentB[Domain]', 'ComponentB[Subdomain]', 'ComponentB[Residue]', 'Quality',
                    'PubMedIdentifier(s)', 'Comments'])

    #data_R.append(['teeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeest'])

    data_M = tablib.Dataset() # (II) Metabolic Reaction list
    data_M.title= '(II) Metabolic Reaction list'
    data_M.append(['To be implemented'])

    data_C= tablib.Dataset() # (III) Contingency list
    data_C.title='(III) Contingency list'
    data_Rd= tablib.Dataset() # (IV) Reaction definition
    data_Rd.title= '(IV) Reaction definition'
    data_Cd= tablib.Dataset() # (V) Contingency Definitions
    data_Cd.title= '(V) Contingency Definitions'
    data_Cd.headers=['','Contingency','']
    data_Cd.append(['Contingencies', '!', 'Absolutely required'])


    book=tablib.Databook((data_R, data_M, data_C, data_Rd, data_Cd))


    if not os.path.exists(inputdir+'/'+output_directory):
        os.mkdir(inputdir+'/'+output_directory)

    with open(inputdir+'/'+output_directory+'/'+outputname,'wb') as f:
        f.write(book.xls)

def write_rxncon_xls(inputdir, rxncon, gene_list):
    '''
    Writes rxncon Object to xls File using XlsxWriter library
    '''
    outputname= 'output'+'.xls'
    output_directory='output_parser'

    if not os.path.exists(inputdir+'/'+output_directory):
        os.mkdir(inputdir+'/'+output_directory)

    # define an alphabet for later lookup (indexing of columns)
    alfa = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


    workbook = xlsxwriter.Workbook(inputdir+'/'+output_directory+'/'+outputname)
# reaction List sheet
    r_sheet= workbook.add_worksheet('(I) Reaction list')
    # set colums widths
    small_cols_r =['A','C','E','F','I','J','P','U']
    medium_cols_r=['D','G','L','M','N','O','Q','R','S','T','V']
    big_cols_r=['B','H','K','W']
    for c in small_cols_r:
        r_sheet.set_column(c+':'+c,15)
    for c in medium_cols_r:
        r_sheet.set_column(c+':'+c,23)
    for c in big_cols_r:
        r_sheet.set_column(c+':'+c,33)
    #write headers
    headers_r= ['ReactionID', 'Reaction[Full]', 'SourceState', 'ProductState', 'coSubstrate(s)', 'coProduct(s)',
                    'ComponentA[ID]', 'ComponentA[Species]', 'ReactionType', 'ComponentB[ID]', 'ComponentB[Species]',
                    'ComponentA[Name]', 'ComponentA[Domain]', 'ComponentA[Subdomain]', 'ComponentA[Residue]','Reaction',
                    'ComponentB[Name]', 'ComponentB[Domain]', 'ComponentB[Subdomain]', 'ComponentB[Residue]', 'Quality',
                    'PubMedIdentifier(s)', 'Comments']
    for c in alfa[0:len(headers_r)]:
        r_sheet.write(c+'1', headers_r[alfa.index(c)])

    #write content
    reaction_list= rxncon.xls_tables['reaction_list']
    number_reactions_r = len(reaction_list)

    for i in range(1,number_reactions_r+1):
        r_sheet.write('A'+str(i+1), str(i))
        r_sheet.write('B'+str(i+1),reaction_list[i-1]['Reaction[Full]'])
        # no source state information given
        # no product state information given
        # no co substrates given (in example file done with references)
        # no coproducts given (in example file done with references)
        r_sheet.write('G'+str(i+1),reaction_list[i-1]['ComponentA[Name]']) #is that correct? because header says ID not name
        # no species information given
        r_sheet.write('I'+str(i+1),reaction_list[i-1]['ReactionType'])
        r_sheet.write('J'+str(i+1),reaction_list[i-1]['ComponentB[Name]'])#is that correct? because header says ID not name
        # no species information given
        r_sheet.write('L'+str(i+1),reaction_list[i-1]['ComponentA[Name]'])
        r_sheet.write('M'+str(i+1),reaction_list[i-1]['ComponentA[Domain]'])
        r_sheet.write('N'+str(i+1),reaction_list[i-1]['ComponentA[Subdomain]'])
        r_sheet.write('O'+str(i+1),reaction_list[i-1]['ComponentA[Residue]'])
        r_sheet.write('P'+str(i+1),reaction_list[i-1]['ReactionType'])
        r_sheet.write('Q'+str(i+1),reaction_list[i-1]['ComponentB[Name]'])
        r_sheet.write('R'+str(i+1),reaction_list[i-1]['ComponentB[Domain]'])
        r_sheet.write('S'+str(i+1),reaction_list[i-1]['ComponentB[Subdomain]'])
        r_sheet.write('T'+str(i+1),reaction_list[i-1]['ComponentB[Residue]'])
        # no quality given
        # no PubMedIdentigfiers given
        # no comments given

# metabolic reaction list sheet
    m_sheet= workbook.add_worksheet('(II) Metabolic reaction list')
    m_sheet.set_column('A:A',25)
    m_sheet.write('A1', 'to be implemented')

# contigency list sheet
    c_sheet= workbook.add_worksheet('(III) Contingency list')
    # set colums widths
    medium_cols_c =['A','C','H']
    big_cols_c=['B','D','E','F','G']

    for c in medium_cols_c:
        c_sheet.set_column(c+':'+c,23)
    for c in big_cols_c:
        c_sheet.set_column(c+':'+c,33)
    #write headers
    headers_c= ['ContingencyID', 'Target', 'Contingency', 'Modifier', 'PubMedIdentifier(s)', 'Quality', 'Comment', '']
    for c in alfa[0:len(headers_c)]:
        c_sheet.write(c+'1', headers_c[alfa.index(c)])

    #write content
    contingency_list= rxncon.xls_tables['contingency_list']
    number_reactions_c = len(contingency_list)

    for i in range(1,number_reactions_c+1):
        c_sheet.write('A'+str(i+1),contingency_list[i-1]['ContingencyID'])
        c_sheet.write('B'+str(i+1),contingency_list[i-1]['Target'])
        c_sheet.write('C'+str(i+1),contingency_list[i-1]['Contingency'])
        c_sheet.write('D'+str(i+1),contingency_list[i-1]['Modifier'])
        # no pubmed IDs given
        # no quality given
        # no comments given

# reaction defintion sheet
    rd_sheet= workbook.add_worksheet('(IV) Reaction Definitions')

    # set colums widths
    small_cols_rd =['A','D','H','P','Q']
    medium_cols_rd =['B','F','G','J','K','R']
    big_cols_rd=['C','E','I','L','M','N','O']

    for c in small_cols_rd:
        rd_sheet.set_column(c+':'+c,15)
    for c in medium_cols_rd:
        rd_sheet.set_column(c+':'+c,23)
    for c in big_cols_rd:
        rd_sheet.set_column(c+':'+c,33)
    #write headers
    headers_rd= ['Reaction', 'CategoryType', 'Category', 'SubclassID', 'Subclass', 'Modifier or Boundary', 'ReactionTypeID', 'ReactionType', 'ReactionName', 'Reversibility', 'Directionality', 'SourceState[Component]', 'SourceState[Modification]', 'ProductState[Component]', 'ProductState[Modification]', 'coSubstrate(s)', 'coProduct(s)', 'Comments']
    for c in alfa[0:len(headers_rd)]:
        rd_sheet.write(c+'1', headers_rd[alfa.index(c)])

    #write content
    reaction_definition_list= rxncon.xls_tables['reaction_definition']
    number_reactions_rd = len(reaction_definition_list)

    for i in range(1,number_reactions_rd+1):
        rd_sheet.write('A'+str(i+1),reaction_definition_list[i-1]['Reaction'])
        rd_sheet.write('B'+str(i+1),reaction_definition_list[i-1]['CategoryType'])
        rd_sheet.write('C'+str(i+1),reaction_definition_list[i-1]['Category'])
        rd_sheet.write('D'+str(i+1),reaction_definition_list[i-1]['SubclassID'])
        rd_sheet.write('E'+str(i+1),reaction_definition_list[i-1]['Subclass'])
        rd_sheet.write('F'+str(i+1),reaction_definition_list[i-1]['Modifier or Boundary'])
        rd_sheet.write('G'+str(i+1),reaction_definition_list[i-1]['ReactionTypeID'])
        rd_sheet.write('H'+str(i+1),reaction_definition_list[i-1]['ReactionType'])
        rd_sheet.write('I'+str(i+1),reaction_definition_list[i-1]['ReactionName'])
        rd_sheet.write('J'+str(i+1),reaction_definition_list[i-1]['Reversibility'])
        rd_sheet.write('K'+str(i+1),reaction_definition_list[i-1]['Directionality'])
        rd_sheet.write('L'+str(i+1),reaction_definition_list[i-1]['SourceState[Component]'])
        rd_sheet.write('M'+str(i+1),reaction_definition_list[i-1]['SourceState[Modification]'])
        rd_sheet.write('N'+str(i+1),reaction_definition_list[i-1]['ProductState[Component]'])
        rd_sheet.write('O'+str(i+1),reaction_definition_list[i-1]['ProductState[Modification]'])
        rd_sheet.write('P'+str(i+1),reaction_definition_list[i-1]['coSubstrate(s)'])
        rd_sheet.write('Q'+str(i+1),reaction_definition_list[i-1]['coProduct(s)'])
        rd_sheet.write('R'+str(i+1),reaction_definition_list[i-1]['Comments'])

# contingency definitions sheet
    # just going to print the default
    cd_sheet= workbook.add_worksheet('(V) Contingency Definitions')
    cd_sheet.set_column('A:A',23)
    cd_sheet.set_column('B:B',15)
    cd_sheet.set_column('C:C',70)

    cd_sheet.write('B1', 'Contingency')
    cd_sheet.write('A2', 'Contingencies:')
    conts=['!','K+','0', 'K-','x', '?']
    conts_meanings=['Absolutely required','Positive effector','No effect', 'Negative effector', 'Absolutely inhibitory', 'Unknown']
    for cont in conts:
        cd_sheet.write('B'+str(conts.index(cont)+2),cont)
        cd_sheet.write('C'+str(conts.index(cont)+2),conts_meanings[conts.index(cont)])
    cd_sheet.write('A8','Boolean operators')
    cd_sheet.write('B8','AND')
    cd_sheet.write('B9','OR')
    cd_sheet.write('C8','Used when several states are required for a certain effect (Intersection of states)')
    cd_sheet.write('C9','Used when severak states can give an effect individually (Union of states)')

# ORF sheet
    #ich baller hier alle gene rein, keine ahung welche orf und welche non orf sind
    o_sheet= workbook.add_worksheet('(VI) ORF IDs')
    o_sheet.set_column('A:A',15)
    o_sheet.set_column('B:B',15)
    o_sheet.set_column('C:C',15)
    o_sheet.set_column('D:D',15)

     #write content
    number_reactions_o = len(gene_list)

    for i in range(0,number_reactions_o-1):
        o_sheet.write('A'+str(i+1),gene_list[i]['LocusName'])
        o_sheet.write('B'+str(i+1),gene_list[i]['Name'])
        o_sheet.write('C'+str(i+1),gene_list[i]['LocusName']) #again?
        o_sheet.write('D'+str(i+1),gene_list[i]['Gene'])

# non orf ids sheet
    n_sheet= workbook.add_worksheet('(VII) Non ORF IDs') #wird das benoetigt?

    workbook.close()


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
    #inputdir= hello()
    #check_directory_type(inputdir)


    #check_directory_type('sbtab_files/example_files(sbtab)_csv')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_ods')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_xls')
    #print '------------------------'
    #check_directory_type('sbtab_files/tiger_files_csv')
    #print '------------------------'
    #check_directory_type('sbtab_files/tiger_files_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_txt')

    #read rxncon input:
    #parse_rxncon2SBtab('rxncon_files/rxncon_xls/rxncon_simple_example-1.xls')
    check_directory_type('rxncon_files/rxncon_xls/simple_xls')
    #print '------------------------'
    #check_directory_type('rxncon_files/rxncon_txt/test_txt')
    #print '------------------------'
    #check_directory_type('rxncon_files/rxncon_txt/tiger_own_output_txt')
    #print '------------------------'
