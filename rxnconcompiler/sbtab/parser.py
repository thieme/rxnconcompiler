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

class Mapper(object):
    def __init__(self):
        self.mapping_dict={
                            #left : SBtab, right: rxncon
                                # Reaction List
                                '!ReactionID' : 'ReactionID',
                                '!ComponentA:Name' : 'ComponentA[Name]',
                                '!ComponentA:Domain' : 'ComponentA[Domain]',
                                '!ComponentA:Subdomain' : 'ComponentA[Subdomain]',
                                '!ComponentA:Residue' : 'ComponentA[Residue]',
                                '!Reaction' : 'ReactionType', # 'Reaction',
                                '!ComponentB:Name' : 'ComponentB[Name]',
                                '!ComponentB:Domain' : 'ComponentB[Domain]',
                                '!ComponentB:Subdomain' : 'ComponentB[Subdomain]',
                                '!ComponentB:Residue' : 'ComponentB[Residue]',
                                '!Quality' : 'Quality',
                                '!PubMedIdentifiers' : 'PubMedIdentifier(s)',
                                '!Comment': 'Comments',
                                # Contigency List
                                '!ContingencyID' : 'ContingencyID',
                                '!Target' : 'Target',
                                '!Contingency' : 'Contingency',
                                '!Modifier' : 'Modifier',
                                # Reaction definition
                                #'!Reaction' : 'Reaction',
                                '!Category:Type' : 'CategoryType',
                                '!Category' : 'Category',
                                '!SubclassID' : 'SubclassID',
                                '!Subclass' : 'Subclass',
                                '!ModifierOrBoundary' : 'Modifier or Boundary',
                                '!ReactionType:ID' : 'ReactionTypeID',
                                '!ReactionType' : 'ReactionType',
                                '!Reaction:Name' : 'ReactionName',
                                '!Reversibility' : 'Reversibility',
                                '!Directionality' : 'Directionality',
                                '!SourceState:Component' : 'SourceState[Component]',
                                '!SourceState:Modification' : 'SourceState[Modification]',
                                '!ProductState:Component' : 'ProductState[Component]',
                                '!ProductState:Modification' : 'ProductState[Modification]',
                                '!coSubstrates' : 'coSubstrate(s)',
                                '!coProducts' : 'coProduct(s)'
                        }

    def update_mapping_dict(self, tableType):
        if 'reaction_list' in tableType:
            self.mapping_dict['!Reaction']= 'ReactionType'
            self.mapping_dict['!Comment']='Comments'
        else:
            self.mapping_dict['!Reaction']= 'Reaction'
            if 'contingency_list' in tableType:
                self.mapping_dict['!Comment']='Comment'

class Commandline(object):
    def __init__(self):
        self.inputdir= ''
        self.outputformat='xls'


    def hello(self):
        '''
        Introduces parser to user and reads input directory from comment line
        '''
        print 'You are using rxncon SBtab parser.' \
              'It helps you to translate network data from rxncon format to SBtab format and vice versa.' \
        #      'If you want to parse a rxncon file to a SBtab file, the following input filetypes are supported:' \
        #       ' - .txt' \
        #       ' - .xls'
        # print 'If you want to parse a SBtab file to a rxncon file, these input filetypes are supported:' \
        #       ' - .xls' \
        #       ' - .csv'
        print ''
        inputdir = raw_input('Please enter the path to the directory containing your network files: \n') # only works in python 2.x, for python3 would be input()

        self.inputdir=inputdir

    def outputformat_formating(self, possibilities, default):
        self.outputformat= raw_input('Please enter the output format. Possible are .{0} (default= .{1}):\n'.format(" & .".join(possibilities), default))
        if self.outputformat=='':
            self.outputformat='{0}'.format(default)
        else:
            #self.outputformat = self.outputformat[-3:] # basti: nach dem letzten punkt mit split
            self.outputformat = self.outputformat.split('.')[-1]

    def read_outputformat(self, parsable_to):
        if parsable_to=='rxncon':
            self.outputformat_formating(["txt","xls"], "txt")
            # self.outputformat= raw_input('Please enter the output format. Possible are .txt & .xls (default= .txt):\n')
            # if self.outputformat=='':
            #     self.outputformat='txt'https://www.fairphone.com/
            # else:
            #     self.outputformat = self.outputformat[-3:]

        elif parsable_to=='sbtab':
            self.outputformat_formating(["csv","xls"], "csv")
            # self.outputformat= raw_input('Please enter the output format. Possible are .csv & .xls (default= .csv):\n')
            # if self.outputformat=='':
            #     self.outputformat='csv'
            # else:
            #     self.outputformat = self.outputformat[-3:]

class DirCheck(object):
    def __init__(self, inputdir):
        self.inputdir = inputdir
        self.rxncon_detected = False
        self.sbtab_detected = False
        self.other_detected = False
        self.target_format=''
        self.parsable_to=''

    def check_directory_type(self):
        '''
        Checks whether input directory consists of SBtab, rxncon, both or other files
        '''
        print self.inputdir , '      delete this print in the end, check_directory_type()'

        files=get_files(self.inputdir)

        for filename in files:
            filedir= self.inputdir+'/'+filename

            if filename.startswith('.'): # filename[0]
                #skips temp files
                continue

            if filename.endswith('.txt'):# basti: nach dem letzten punkt mit split
                self.check_txt_File(filedir)

            elif filename.endswith('.xls'):# basti: nach dem letzten punkt mit split
                # Read Excel Document
                self.check_xls_File(filedir)

            elif filename.endswith('.ods'):# basti: nach dem letzten punkt mit split
                # Read Open / Libre Office Document
                print 'Found File(s) in .ods format. This format ist not supported. ' \
                      '\nPlease export to .xls or .txt format (Open/Libre Office and Excel can do this).\n' \
                      'If you want to translate from SBtab to rxncon you can also use .csv format.'
                #sbtab_detected, rxncon_detected, other_detected = check_ods_File(filedir, sbtab_detected, rxncon_detected, other_detected)

            elif filename.endswith('.csv'):# basti: nach dem letzten punkt mit split
                # Read csv Table
                self.check_csv_File(filedir)
                if self.rxncon_detected:
                    sys.exit('Found rxncon file in .csv Format. This is not supported, please export zu .xls or Quick Format in .txt')

            else:
                self.other_detected=True

        if self.rxncon_detected==True:
            if self.sbtab_detected==True:
                print 'Error, both SBtab and rxncon files detected in input directory! Please clean up the directory!'
            elif self.other_detected==True:
                print 'Error, files of unknown format (neither SBtab nor rxncon) detected!' # basti: fkt da doppelt spaeter
            else:
                print 'Directory of rxncon files detected. Starting parser.'
                self.look_for_rxncon_files()

        elif self.sbtab_detected==True:
            if self.other_detected==True:
                print 'Error, files of unknown format (neither SBtab nor rxncon) detected!'
            else:
                print 'Directory of SBtab files detected. Starting parser.'
                self.look_for_SBtab_files(self.inputdir)
                if self.target_format:
                    if self.target_format=='txt':
                        print "Warning: You can export the files in current directory only to rxncon quick format (.txt)." \
                              "         Not all needed Files for xls export are found." \
                              "         If you still choose xls export, the program will crash."


    def check_txt_File(self, filedir):
        '''
        Checks whether txt file is rxncon, SBtab or other file type
        '''
        with open(filedir, 'r') as f:
            first_line= f.readline().strip()
            if 'SBtab' in first_line:
                self.sbtab_detected=True
            elif 'rxncon' in first_line:
                # sollte im rxncon header fuer txt files vorkommen, gibt es bisher nicht
                self.rxncon_detected=True
            else:
                self.other_detected=True



    def check_xls_File(self, filedir):
        '''
        Checks whether xls file is rxncon, SBtab or other file type
        '''

        xlsreader = xlrd.open_workbook(filedir)
        xls_sheet_names = xlsreader.sheet_names()
        first_sheet = xlsreader.sheet_by_index(0)

        first_line = first_sheet.row(0)
        for cell in first_line:
            if '!!SBtab' in str(cell):
                self.sbtab_detected=True

        for sheet_name in xls_sheet_names:
            if ('(III) Contingency list' in sheet_name or 'Contingency List' in sheet_name or 'contingency list' in sheet_name) and not 'ContingencyID' in sheet_name:
                self.rxncon_detected=True

        if self.sbtab_detected==False and self.rxncon_detected==False:
            self.other_detected=True


    def check_ods_File(self, filedir):
        '''
        Checks whether ods file is rxncon, SBtab or other file type
        NOT SUPPORTED YET
        '''
        #sbtab_detected, rxncon_detected, other_detected = check_ods_File(filedir, sbtab_detected, rxncon_detected, other_detected)
        #return sbtab_detected, rxncon_detected, other_detected

        pass

    def check_csv_File(self, filedir):
        '''
        Checks whether csv file is rxncon, SBtab or other file type
        '''
        # cant be rxncon file then
        with open(filedir, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
            try:
                first_line = csvfile.readline().strip()
                if 'SBtab' in first_line:
                    self.sbtab_detected=True
                else:
                    self.other_detected=True

            #error catching
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filedir, csvreader.line_num, e))


    def look_for_SBtab_files(self, inputdir):
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

        if 'ReactionID' in found_table_types and'ContingencyID' in found_table_types:
            self.parsable_to='rxncon'
            self.target_format= 'txt'

        if 'ReactionList' in found_table_types and 'Gene' in found_table_types:
            self.target_format= 'xls'

        else:
            print 'Error: In order to translate the SBtab format to rxncon, you need tables with following TableTypes:' \
                  ' - ReactionID' \
                  ' - ContingencyID' \
                  'Only needed for export to xls format: ' \
                  '     - Gene (only for export to xls)' \
                  '     - ReactionList(only for export to xls)'
            print 'Only the follwing TableTypes were found:'
            print found_table_types
            self.parsable_to=''

    def look_for_rxncon_files(self):
        '''
        Checks weather all needed rxncon files/sheets are given inside input directory:
        - (I) Reaction List
        - (III) Contingency List
        - (IV) Reaction definition
        '''

        files = get_files(self.inputdir)
        found_tables=[]
        # basti
        #found_tables = [table for filename in files for table in build_rxncon_dict(self.inputdir, filename)]
        for filename in files:
            d= build_rxncon_dict(self.inputdir, filename)
            #found_tables = [table for table in d]
            for table in d.keys():
                found_tables.append(table)

        if 'reaction_definition' in found_tables and 'contingency_list' in found_tables and 'reaction_list' in found_tables:
            self.parsable_to='sbtab'

        else:
            print 'Error: In order to translate the rxncon format to SBtab, you need the following tables:' \
                  ' - reaction_definition' \
                  ' - contingency_list' \
                  ' - reaction_list' \
                  'Only the following tables were found: '
            print found_tables

class Parser(Commandline):

    def __init__(self, parsable_to, inputdir, target_format):
        super(Parser, self).__init__()
        self.parsable_to=parsable_to
        self.inputdir=inputdir
        self.target_format = target_format
        self.gene_list=None

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

    def parse_SBtab2rxncon(self):
        '''
        Main function for parsing SBtab --> rxncon Format. Creates rxncon object
        '''
        files = get_files(self.inputdir)
        self.read_outputformat(self.parsable_to) #reactivate
        print self.outputformat
        if self.outputformat!='txt' and self.outputformat!='xls':
            print 'Error, the format ',self.outputformat,' is not supported.'

        self.ob_list=[] # List of dictionaries
        reaction_def_found=False
        for filename in files:
            ob= build_SBtab_object(self.inputdir, filename)
            self.ob_list.append({'object':ob, 'type':ob.table_type, 'filename':filename })
            if ob.table_type=='ReactionList' and ob.table_name=='Reaction definitions':
                reaction_def_found=True
                print 'Custom reaction definition file detected in: ' + filename

        if not reaction_def_found:
            print 'No reaction definition file found. Using default.'
            reaction_definition = DEFAULT_DEFINITION
        else:
            reaction_definition=self.build_reaction_definition(self.ob_list)

        if self.outputformat=='xls' and self.target_format=='xls':
            self.gene_list=self.build_gene_list(self.ob_list)

        self.rxncon = self.build_rxncon(self.ob_list, reaction_definition) #rxncon object

    def build_rxncon(self, ob_list, reaction_definition):
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
                #
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
                            'Reaction[Full]': self.build_full(row,indexes_dict)
                        })
                reaction_list.pop(0)

        return Rxncon(dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition), parsed_xls=True) #build rxncon object

    def build_full(self, row,d):
        '''
        Creates Full Reaction String from given SBtab reaction row and a dictionary, that tells in which column is what.
        Template: ComponentA_[Domain/Subdomain(Residue)]_reaction_ComponentB_[Domain/Subdomain(Residue)]
        '''

        def component(comp):
            out=''
            out+=row[d['c%sn'%comp]]

            if row[d['c%sd'%comp]]:
                out+='_['+row[d['c%sd'%comp]]
                if row[d['c%ss'%comp]]:
                    out+='/'+row[d['c%ss'%comp]]
                if row[d['c%sr'%comp]]:
                    out+='('+row[d['c%sr'%comp]]+')'
                out+=']'
            elif row[d['c%ss'%comp]]:
                out+='_['+row[d['c%ss'%comp]]  # if no dom%sin but only subdom%sin is given, the subdom%sin becomes dom%sin. is th%st correct?
                if row[d['c%sr'%comp]]:
                    out+='('+row[d['c%sr'%comp]]+')'
                out+=']'
            elif row[d['c%sr'%comp]]:
                out+='_[(' + row[d['c%sr'%comp]] + ')]'

            return out

        out = component("a")
        out+='_'+row[d['rea']]+'_'
        out+= component("b")
        # Reaction B
        # out+=row[d['cbn']]
        # if row[d['cbd']]:
        #     out+='_['+row[d['cbd']]
        #     if row[d['cbs']]:
        #         out+='/'+row[d['cbs']]
        #     outif row[d['cbr']]:
        #         out+='('+row[d['cbr']]+')'
        #     out+=']'
        # elif row[d['cbs']]:
        #     out+='_['+row[d['cbs']]  # if no domain but only subdomain is given, the subdomain becomes domain. is that correct?
        #     if row[d['cbr']]:
        #         out+='('+row[d['cbr']]+')'
        #     out+=']'
        # elif row[d['cbr']]:
        #     out+='_[(' + row[d['cbr']] + ')]'

        return out

    def build_gene_list(self, ob_list):
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
                gene_list=[{
                        'Gene': row[gene_col_index],
                        'Name': row[name_col_index],
                        'LocusName': row[locus_col_index]
                    } for row in ob['object'].getRows()]

        return gene_list

    def build_reaction_definition(self, ob_list):
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

    def parse_rxncon2SBtab(self):
        '''
        Main function for parsing rxncon--> SBtab Format
        '''

        def build_value_rows(tableType, columns, length):
            ''' Builds XXXX of XXX of values and maps it to the SBtab columns
            '''

            #print 'print self.d[\''+tableType+'\'][1].keys() :\n ', self.d[tableType][1].keys()
            #self.read_outputformat(self.parsable_to)
            m = Mapper()
            m.update_mapping_dict(tableType)
            for i in range(0,length): # for all items in e.g. reaction_list
                        values=[]
                        for col in columns:
                            values.append(self.d[tableType][i][m.mapping_dict[col]])
                        value_rows.append(values)
            return value_rows

        files = get_files(self.inputdir)
        #self.read_outputformat(self.parsable_to) reactivate

        # if self.outputformat=='':
        #     self.outputformat='csv'
        # else:
        #     self.outputformat = self.outputformat[-3:]
        # if self.outputformat!='csv' and self.outputformat!='xls' and self.outputformat!='txv' and self.outputformat!='ods':
        #     print 'Error, the format ',self.outputformat,' is not supported.'

        for file in files:
            filedir=self.inputdir+'/'+file
            #################################################
            #xls_tables= parse_xls(filedir)
            #print xls_tables
            #################################################
            self.d= build_rxncon_dict(self.inputdir,file) #dict with 3 values, that are itself lists of dicts
            for key in self.d:#.keys():
                tableType=''
                tableName=''
                value_rows=[] #each list item is a list with the values of a row for easier delimiter organisation

                if 'reaction_list' in key:
                    tableType='ReactionID'
                    tableName='Reaction list'
                    filename='filename1'

                    columns= ['!ReactionID','!ComponentA:Name','!ComponentA:Domain','!ComponentA:Subdomain','!ComponentA:Residue','!Reaction','!ComponentB:Name','!ComponentB:Domain','!ComponentB:Subdomain','!ComponentB:Residue','!Quality','!PubMedIdentifiers','!Comment']
                    value_rows=build_value_rows(key, columns, len(self.d[key])) #each list item is a list with the values of a row for easier delimiter organisation

                elif 'contingency_list' in key:
                    tableType='ContingencyID'
                    tableName='Contingency list'
                    filename='filename2'
                    columns= ['!ContingencyID' ,'!Target' ,'!Contingency' ,'!Modifier' ,'!PubMedIdentifiers' ,'!Quality' ,'!Comment']
                    value_rows=build_value_rows(key, columns, len(self.d[key])) #each list item is a list with the values of a row for easier delimiter organisation

                elif 'reaction_definition' in key:
                    tableType='ReactionList'
                    tableName='Reactions definitions'
                    filename='filename3'
                    columns=['!Reaction','!Category:Type','!Category','!SubclassID','!Subclass','!ModifierOrBoundary','!ReactionType:ID','!ReactionType','!Reaction:Name','!Reversibility','!Directionality','!SourceState:Component','!SourceState:Modification','!ProductState:Component','!ProductState:Modification','!coSubstrates','!coProducts','!Comment']
                    value_rows=build_value_rows(key, columns, len(self.d[key])) #each list item is a list with the values of a row for easier delimiter organisation

                header_row='!!SBtab !!SBtabVersion=\'0.8\' TableType="'+ tableType +'" TableName="'+tableName#+'\n'

                print 'ist:'
                print header_row
                for col in columns:
                        #print col+ '\t', # using tabs as delimeters
                        print col+ ',', # using comma as delimeters
                print ''
                for row in value_rows[0:2]:
                    for value in row:
                        print str(value)+',',
                    print ''

                print ''
                print '-----------------------------'
                print ''

                #print len(columns), columns
                #print len(value_rows[1]), value_rows[1]
                #sbtab= createDataset(header_row, columns, value_rows, filename)
                #print sbtab
                #print 'inputdir: ', inputdir
                #print 'filedir: ',filedir
                print 'soll:'
                #f= open('sbtab_files/tiger_files_csv_cut/Tiger_et_al_TableS1_SBtab_ReactionID.csv', 'r')
                f= open('rxncon_files/rxncon_xls/sps_cut/reduced_cols/sbtab_format/ContingencyID.csv', 'r')
                #f=open(filedir, 'r')
                ff= f.read()
                print ff[0:400]    #das hier will ich lesen
                print '####################################'

                #fff = tablibIO.importSetNew(ff,filedir)
                #ffff = SBtab.SBtabTable(fff,filedir)
                #fff = tablibIO.importSetNew(ff,'sbtab_files/tiger_files_csv_cut/Tiger_et_al_TableS1_SBtab_ReactionID.csv')
                #ffff = SBtab.SBtabTable(fff,'sbtab_files/tiger_files_csv_cut/Tiger_et_al_TableS1_SBtab_ReactionID.csv')
                fff = tablibIO.importSetNew(ff,'rxncon_files/rxncon_xls/sps_cut/reduced_cols/sbtab_format/ContingencyID.csv')
                ffff = SBtab.SBtabTable(fff,'rxncon_files/rxncon_xls/sps_cut/reduced_cols/sbtab_format/ContingencyID.csv')
                ffff.update()



                #ffff.writeSBtab('csv',filedir+'/output/test')   #das schreiben sollte in eine eigene funktion so wie write_sbtab_xls oder so
                #ffff.writeSBtab('csv')


class SBtabWriter(object):
    def __init__(self):
        pass

    def write_sbtab_xls(inputdir, sbtab, filename):
        '''
        Gets sbtab object and saves it as a xls file
        '''
        outputname= '_output'
        output_directory='output_parser'
        if not os.path.exists(inputdir+'/'+output_directory):
            os.mkdir(inputdir+'/'+output_directory)

        sbtab.writeSBtab('csv',inputdir+output_directory+'/'+filename+outputname)

class RxnconWriter(object):
    def __init__(self, rxncon, outputformat, target_format, inputdir, gene_list):
        self.rxncon = rxncon
        self.outputformat = outputformat
        self.target_format= target_format
        self.inputdir = inputdir
        self.gene_list= gene_list

    def write(self):
        if self.outputformat=='txt' and (self.target_format=='txt' or self.target_format=='xls'):
            self.write_rxncon_txt(self.inputdir, self.rxncon)
        elif self.outputformat=='xls' and self.target_format=='xls':
            self.write_rxncon_xls(self.inputdir, self.rxncon, self.gene_list)

    def write_rxncon_txt(self, inputdir, rxncon):
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

    def write_rxncon_xls(self, inputdir, rxncon, gene_list):
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

        #def column_gen(self, sheet, cols_r, size ):  basti
        #    for c in cols_r:
        #        sheet.set_column(c+':'+c, size)
        #    return sheet

        #column_gen(r_sheet, small_cols_r, 15)
        #column_gen(r_sheet, medium_cols_r, 23)


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
            # over each row
            r_sheet.write('A'+str(i+1), str(i))
            #r_sheet.write('B'+str(i+1),reaction_list[i-1]['Reaction[Full]'])
            #rxn_form='{=L2&if(and(M2="",N2="",O2=""),"","_["&M2&if(N2="","","/"&N2)&if(O2="","]","("&O2&")]"))&"_"&I2&"_"&Q2&if(and(R2="",S2="",T2=""),"","_["&R2&if(S2="","","/"&S2)&if(T2="","]","("&T2&")]"))}'
            rxn_form='{=L'+str(i+1)+'&if(and(M'+str(i+1)+'="",N'+str(i+1)+'="",O'+str(i+1)+'=""),"","_["&M'+str(i+1)+'&if(N'+str(i+1)+'="","","/"&N'+str(i+1)+')&if(O'+str(i+1)+'="","]","("&O'+str(i+1)+'&")]"))&"_"&I'+str(i+1)+'&"_"&Q'+str(i+1)+'&if(and(R'+str(i+1)+'="",S'+str(i+1)+'="",T'+str(i+1)+'=""),"","_["&R'+str(i+1)+'&if(S'+str(i+1)+'="","","/"&S'+str(i+1)+')&if(T'+str(i+1)+'="","]","("&T'+str(i+1)+'&")]"))}'
            r_sheet.write_formula('B'+str(i+1),rxn_form)
            ss_form='{=if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="N/A","N/A",if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="ComponentB, ComponentB","ComponentB"&left(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH),find(",",vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH))-1)&", ComponentB"&right(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH),len(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH))-find(",",vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH))-1),if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH)="N/A",if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="ComponentB",Q'+str(i+1)+',"Error"),if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="ComponentA",L'+str(i+1)+'&if(and(M'+str(i+1)+'="",N'+str(i+1)+'="",O'+str(i+1)+'=""),"","_["&M'+str(i+1)+'&if(N'+str(i+1)+'="","","/"&N'+str(i+1)+')&if(O'+str(i+1)+'="","]","("&O'+str(i+1)+'&")]")),if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="ComponentB",Q'+str(i+1)+'&if(and(R'+str(i+1)+'="",S'+str(i+1)+'="",T'+str(i+1)+'=""),"","_["&R'+str(i+1)+'&if(S'+str(i+1)+'="","","/"&S'+str(i+1)+')&if(T'+str(i+1)+'="","]","("&T'+str(i+1)+'&")]")),if(vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,5,FALSCH)="ComponentA, ComponentB","","Error")))&vlookup(I'+str(i+1)+',"(IV) Reaction definition"!$H:$Q,6,FALSCH))))}'
            r_sheet.write_formula('C'+str(i+1),ss_form)
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

        #for i in range(len(headers_c)): basti
            #c_sheet.write(alfa[i]+'1', headers_c[i])

        #write content
        contingency_list= rxncon.xls_tables['contingency_list']
        number_reactions_c = len(contingency_list)

        for i in range(1,number_reactions_c+1):  # basti: mapping
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

        for c in small_cols_rd:  # see function column_gen
            rd_sheet.set_column(c+':'+c,15)
        for c in medium_cols_rd:
            rd_sheet.set_column(c+':'+c,23)
        for c in big_cols_rd:
            rd_sheet.set_column(c+':'+c,33)
        #write headers
        headers_rd= ['Reaction', 'CategoryType', 'Category', 'SubclassID', 'Subclass', 'Modifier or Boundary', 'ReactionTypeID', 'ReactionType', 'ReactionName', 'Reversibility', 'Directionality', 'SourceState[Component]', 'SourceState[Modification]', 'ProductState[Component]', 'ProductState[Modification]', 'coSubstrate(s)', 'coProduct(s)', 'Comments']
        for c in alfa[0:len(headers_rd)]: # basti: duplication
            rd_sheet.write(c+'1', headers_rd[alfa.index(c)])

        #write content
        reaction_definition_list= rxncon.xls_tables['reaction_definition']
        number_reactions_rd = len(reaction_definition_list)

        for i in range(1,number_reactions_rd+1): # basti; mapping
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

    # contingency definitions sheet # basti: kann weck
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

    # ORF sheet  # basti: weck
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
        print 'Successfully wrote rxncon xls format to '+inputdir+'/'+output_directory+'/'+outputname




if __name__=="__main__":

    c=Commandline()
    #c.hello()
    c.inputdir='rxncon_files/rxncon_xls/sps_cut'
    #c.inputdir='sbtab_files/tiger_files_csv_cut'

    d=DirCheck(c.inputdir)
    d.check_directory_type()


    p=Parser(d.parsable_to, d.inputdir, d.target_format)

    print p.target_format

    if d.parsable_to=='rxncon':
        p.parse_SBtab2rxncon()
        w=RxnconWriter(p.rxncon, p.outputformat, p.target_format, p.inputdir, p.gene_list)

    elif d.parsable_to=='sbtab':
        p.parse_rxncon2SBtab()
        w= SBtabWriter()

    #w.write()


    #'to be' usage:
    #inputdir= hello()
    #check_directory_type(inputdir)


    #check_directory_type('sbtab_files/example_files(sbtab)_csv')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_ods')
    #print '------------------------'
    #check_directory_type('sbtab_files/example_files(sbtab)_xls')
    #print '------------------------'
    #check_directory_type('sbtab_files/tiger_files_csv_cut')
    #print '------------------------'
    #check_directory_type('sbtab_files/tiger_files_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_xls')
    # print '------------------------'
    # check_directory_type('rxncon_files/rxncon_txt')

    #read rxncon input:
    #parse_rxncon2SBtab('rxncon_files/rxncon_xls/rxncon_simple_example-1.xls')
    #check_directory_type('rxncon_files/rxncon_xls/sps')
    #print '------------------------'#check_directory_type('rxncon_files/rxncon_xls/simple_xls')
    #print '------------------------'
    #check_directory_type('rxncon_files/rxncon_txt/test_txt')
    #print '------------------------'
    #check_directory_type('rxncon_files/rxncon_txt/tiger_own_output_txt')
    #print '------------------------'
