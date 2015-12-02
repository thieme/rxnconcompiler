
import xlrd
import csv
import sys
import os
from rxnconcompiler.util.rxncon_errors import RxnconParserError
import rxnconcompiler.sbtab.sbtab_utils as sbtab_utils
import rxnconcompiler.sbtab.parser as sbtab_parser
import rxnconcompiler.parser.rxncon_parser as rxncon_parser


def get_files(inputdir):
        """
        Returns list of files (and only files) inside given input directory
        """
        if os.path.isfile(inputdir):
            return [os.path.split(inputdir)[-1]]

        if os.path.isdir(inputdir):
            files = [ f for f in os.listdir(inputdir) if os.path.isfile(os.path.join(inputdir,f)) and not
            f.startswith('.') and not f.startswith('#') ]
        #                                               is no directory                          is no libre office temp file
            return files
        else:
            print 'Error, can not open input directory(\''+inputdir+'\').'
            exit()

class DirCheck():
    def __init__(self, inputdir):
        self.inputdir = inputdir # info: may be path to dir, path to file or also xls_tables dict list
        self.filedir=""
        self.rxncon_detected = 0
        self.sbtab_detected = False
        self.rxncon_sbtab_detected = 0
        self.other_detected = False
        self.target_format=''
        self.parsable_to=''

        #print 'd initialised. inputdir= ', self.inputdir," delete in the end"

    def processing(self, filedir):
        if filedir.endswith('.txt'):# basti: nach dem letzten punkt mit split
            self.check_txt_File(filedir)

        elif filedir.endswith('.xls'):# basti: nach dem letzten punkt mit split
            # Read Excel Document
            self.check_xls_File(filedir)

        elif filedir.endswith('.ods'):# basti: nach dem letzten punkt mit split
            # Read Open / Libre Office Document
            print 'Found File(s) in .ods format. This format ist not supported. ' \
                  '\nPlease export to .xls or .txt format (Open/Libre Office and Excel can do this).\n' \
                  'If you want to translate from SBtab to rxncon you can also use .csv format.'

        elif filedir.endswith('.csv'):# basti: nach dem letzten punkt mit split
            # Read csv Table
            self.check_csv_File(filedir)
            if self.rxncon_detected>0:
                sys.exit('Found rxncon file in .csv Format. This is not supported, please export zu .xls or Quick Format in .txt')

        else:
            self.other_detected=True

    def check_directory_type(self):
        '''
        Checks whether input directory consists of SBtab, rxncon, both or other files
        '''


        # TODO: wird bei sbtab inputdir ueberprueft, ob jeder tabletype auch nur ein mal gefunden wurde? koennte man eventuell testen, nachdem ob_list erzeugt wurde
        self.files=get_files(self.inputdir)

        for filename in self.files:
            if os.path.isfile(self.inputdir):
                self.processing(self.inputdir)
            else:
                filedir= self.inputdir+'/'+filename
                self.processing(filedir)

            if filename.startswith('.'): # filename[0]
                #skips temp files
                continue



        if self.rxncon_detected==1:
            if self.sbtab_detected:
                raise RxnconParserError('Error, both SBtab and rxncon files detected in input directory! Please clean up the directory!')
            elif self.other_detected:
                raise RxnconParserError('Error, files of unknown format (neither SBtab nor rxncon) detected!') # basti: fkt da doppelt spaeter
            else:
                if self.rxncon_detected>1: # if >0 and not >1 --> ==1
                    raise RxnconParserError('Please specify path to single rxncon file')
                    #TODO: framework filepicker

        elif self.sbtab_detected:
            if self.other_detected:
                raise RxnconParserError('Error, files of unknown format (neither SBtab nor rxncon) detected!')
            elif self.rxncon_sbtab_detected > 1:
                raise RxnconParserError('Please specify path to single rxncon file')
                #TODO: framework filepicker
            elif self.rxncon_sbtab_detected==1:
                self.look_for_rxnconSBtab_files(self.inputdir)
            else:
                #print 'Directory of SBtab files detected. Starting parser.'
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
                self.rxncon_detected+=1
            else:
                self.other_detected=True



    def check_xls_File(self, filedir):
        '''
        Checks whether xls file is rxncon, SBtab or other file type
        '''

        sheet_number=0 #sheet we use to check the format
        xlsreader = xlrd.open_workbook(filedir)
        xls_sheet_names = xlsreader.sheet_names()

        for s in range(0,len(xls_sheet_names)):
            # if the first sheet has no content, try the first line of the next sheet
            try:
                sheet = xlsreader.sheet_by_index(sheet_number)
                first_line = sheet.row(0)
                break
            except IndexError:
                sheet_number+=1

        # TODO: Raise error is first line is not readable
        for cell in first_line:
            if '!!SBtab' in str(cell):
                self.sbtab_detected=True
                if 'rxncon' in str(cell):
                    self.rxncon_sbtab_detected+=1

        for sheet_name in xls_sheet_names:
            if '(III) Contingency list' in sheet_name and self.rxncon_sbtab_detected==0:
                self.rxncon_detected+=1

        if self.sbtab_detected==False and self.rxncon_detected==0 and self.rxncon_sbtab_detected==0:
            self.other_detected=True


    def check_ods_File(self, filedir):
        '''
        Checks whether ods file is rxncon, SBtab or other file type
        NOT SUPPORTED YET
        '''

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

    def file_or_dir(self, input):
        '''
        Checks whether inputstring is a directory or a file. Returns list of either the filename or all filenames
        :param input: Path
        :return: List of filename(s), path to file(s)
        '''
        if os.path.isfile(input):
            slash_index= [i for i, letter in enumerate(input) if letter == '/'] #find the occurences of the slash
            inputdir= input[0:max(slash_index)] # the string until the last slash is the inputdirectory
            inputfile = input[max(slash_index)+1:]
            self.files=[inputfile]
        elif os.path.isdir(input):
            self.files = get_files(input)
            inputdir= input

        return (inputdir)


    def look_for_SBtab_files(self, input):
        '''
        Checks whether all needed SBtab tables are inside given directory/document
        - ReactionList
        - ReactionID
        - ContingencyID
        - rxncon_Definition
        '''

        inputdir= self.file_or_dir(input)

        found_table_types=[]
        ob_list=[]
        for filename in self.files:
            #print 'Filename: ', filename, '            delete in look_for_SBtab_files()'
            ob_list.extend(sbtab_utils.build_SBtab_object(inputdir, filename))
        found_table_types= [ob.table_type for ob in ob_list]

        if 'ReactionID' in found_table_types and'ContingencyID' in found_table_types:
            self.parsable_to='rxncon'
            self.target_format= 'txt'

        if 'ReactionList' in found_table_types: #reaction definition
            self.target_format= 'xls'

        else:
            print 'Error: In order to translate the SBtab format to rxncon, you need tables with following TableTypes: \n' \
                  ' - ReactionID \n' \
                  ' - ContingencyID \n \n' \
                  'Only needed for export to xls format:\n ' \
                  '     - ReactionList(only for export to xls)'
            print 'Only the follwing TableTypes were found:'
            print found_table_types
            self.parsable_to=''

    def look_for_rxnconSBtab_files(self, input):
        '''
        Checks whether all needed tables are inside given new format rxncon file
        - rxnconReactionList
        - rxnconContingencyList
        - rxnconReactionDefinition
        -
        '''

        inputdir= self.file_or_dir(input)

        found_table_types=[]

        for filename in self.files:
            ob_list = sbtab_utils.build_SBtab_object(inputdir, filename)
            found_table_types= [ob.table_type for ob in ob_list]

        if 'rxnconReactionList' in found_table_types and 'rxnconContingencyList' in found_table_types:
            self.parsable_to='rxncon'
            self.target_format= 'txt'

        if 'rxnconReactionDefinition' in found_table_types:
            self.target_format= 'xls'

        else:
            print 'Error: In order to translate the new rxncon format to the old one, you need tables with following TableTypes:\n' \
                  ' - rxnconReactionList \n' \
                  ' - rxnconContingencyList \n \n' \
                  'Only needed for export to xls format: \n' \
                  '- rxnconReactionDefinition'

            print 'Only the follwing TableTypes were found:'
            print found_table_types
            self.parsable_to=''

    def controller(self):
        if isinstance(self.inputdir, dict):
            return self.inputdir # dict input
        elif os.path.exists(self.inputdir) and self.inputdir[-4:] == "json":
            return rxncon_parser.parse_rxncon(self.inputdir)
        elif not os.path.isfile(self.inputdir) and not os.path.isdir(self.inputdir):
            return rxncon_parser.parse_text(self.inputdir) #text input
        else:
            self.check_directory_type()
            if self.rxncon_detected and self.rxncon_sbtab_detected == 0 and not self.sbtab_detected and not self.other_detected: # old rxncon format
                return rxncon_parser.parse_rxncon(self.inputdir)
            if self.sbtab_detected and not self.other_detected :  # some sbtab input
                p= sbtab_parser.Parser(self.inputdir, self)
                if self.rxncon_sbtab_detected>0: # new rxncon input
                    if p.parsable_to=='rxncon':
                        p.parse_SBtab2rxncon()
                        return p.rxncon
                elif not self.rxncon_detected and not self.other_detected:
                    p.parse_SBtab2rxncon()
                    return p.rxncon


