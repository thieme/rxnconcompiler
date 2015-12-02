# File parser for parsing SBtab files and reformatting the data to fir internal Rxncon format representation
# Mathias Wajnberg July 2015 - December 2015
__author__ = 'Mathias Wajnberg'

from rxnconcompiler.definitions.default_definition import DEFAULT_DEFINITION # default definition tabelle machen
from rxnconcompiler.definitions.reaction_template import REACTION_TEMPLATE # default def for new format
from rxnconcompiler.util.rxncon_errors import RxnconParserError
import sbtab_utils



class Mapper(object):
    #Basti: wird das immernoch gebraucht?
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
        self.inputfile=''
        self.outputformat='xls'
        self.files=[] # needed ?


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
        self.inputdir = raw_input('Please enter the path to the directory containing your network files: \n') # only works in python 2.x, for python3 would be input()
        self.files=get_files(self.inputdir)


    def outputformat_formating(self, possibilities, default):
        self.outputformat= raw_input('Please enter the output format. Possible are .{0} (default= .{1}):\n'.format(" & .".join(possibilities), default))
        if self.outputformat=='':
            self.outputformat='{0}'.format(default)
        else:
            self.outputformat = self.outputformat.split('.')[-1]

    def read_outputformat(self, parsable_to):
        if parsable_to=='rxncon':
            self.outputformat_formating(["txt","xls"], "txt")
            # self.outputformat= raw_input('Please enter the output format. Possible are .txt & .xls (default= .txt):\n')
            # if self.outputformat=='':
            #     self.outputformat='txt'
            # else:
            #     self.outputformat = self.outputformat[-3:]

class Parser(Commandline):

    def __init__(self, inputdir, d=None):
        super(Parser, self).__init__()
        if d==None:
            import rxnconcompiler.parser.parsing_controller as controller
            self.d=controller.DirCheck(inputdir)
            self.d.check_directory_type()
        else:
            self.d=d
        self.parsable_to=self.d.parsable_to
        self.inputdir=inputdir
        self.target_format = self.d.target_format
        self.ob_list=[]

    def get_info(ob):
        '''
        Function that gives some Information about given Object and current working environment
        '''
        print 'Print: '
        print ob
        print '\nType: '
        print type(ob)
        print'\nDir: '
        print dir(ob)
        print '\nLocals: '
        print locals()
        print '\nCallable: '
        print callable(ob)
        print ''

    def build_ob_list(self):
        for filename in self.d.files:
            ob= sbtab_utils.build_SBtab_object(self.inputdir, filename) # if file has multiple
            # sheets, ob already is the ob list. and this for loop only has one step. This is why
            #  the following nested for loop does not have to much bad influence on the runtime
            if type(ob)==list:
                for index in range(0,len(ob)):
                    self.ob_list.append({'object':ob[index], 'type':ob[index].table_type,
                                         'filename':filename })
            else:
                self.ob_list.append({'object':ob[0], 'type':ob[0].table_type, 'filename':filename })

    def parse_SBtab2rxncon(self):
        '''
        Main function for translating SBtab --> rxncon Format. Creates rxncon object
        '''
        reaction_def_found=False

        #self.read_outputformat(self.parsable_to) #reactivate
        #print self.outputformat
        if self.outputformat!='txt' and self.outputformat!='xls':
            raise RxnconParserError('Error, the format '+self.outputformat+' is not supported.')

        self.build_ob_list()

        for ob_ele in self.ob_list:
            if (ob_ele["type"]=='ReactionList' and ob_ele['object'].table_name=='Reaction definitions') or ob_ele["type"]=='rxnconReactionDefinition':
                    reaction_def_found=True
            if not reaction_def_found:
                reaction_definition= DEFAULT_DEFINITION
                if self.d.rxncon_sbtab_detected>0:
                    reaction_template = REACTION_TEMPLATE  # needs to be updated into reaction_definition
            else:
                reaction_definition=self.build_reaction_definition()

        self.rxncon = self.build_rxncon(self.ob_list, reaction_definition) #rxncon object

        # rxncon object generation for writing must happen in separate file (writer.py or so) because of cyclic imports
        # parser MUST NOT import rxncon, because it is imported into parsing controller and parsing controller is imported intp rxncon

    def build_contingency_list(self,ob):
    # Find column indexes for !Target, !Contingency and !Modifier columns
        targ_col_index= ob['object'].columns.index('!Target')
        cont_col_index= ob['object'].columns.index('!Contingency')
        modi_col_index= ob['object'].columns.index('!Modifier')
        if '!UID:Contingency' in ob['object'].columns_dict:
            # new rxncon inout
            id_col_index= ob['object'].columns.index('!UID:Contingency')
        else:
            # standard sbtab
            id_col_index= ob['object'].columns.index('!ContingencyID')

        # Save the data of these three columns to lists
        contingency_list=[{}]
        for row in ob['object'].getRows():
            if row[id_col_index]!='':
                contingency_list.append({
                    'ContingencyID': row[id_col_index],
                    'Target': row[targ_col_index],
                    'Contingency': row[cont_col_index],
                    'Modifier': row[modi_col_index]
                })
        contingency_list.pop(0)
        return contingency_list

    def build_rxncon(self, ob_list, reaction_definition):
        '''
        Creates rxncon object from given SBtab files
        '''

        for ob in ob_list:
            if ob['type'] in['ContingencyID','rxnconContingencyList']:
                # nearly same in both old rxncon input and new rxncon SBtab hybrid input
                    contingency_list= self.build_contingency_list(ob)

            if self.d.rxncon_sbtab_detected==0:
                #Basti: Versuch den inhalt hier und den im else Fall ein bisschen mehr zusammen zu fuehren. Wenn ich das
                #Basti: richtig sehe ist der einzige unterschied im indexes_dict das im else case noch weitere Spalten sind
                #Basti: das kann manabfangen in dem meine eine Funktion drum baut
                # standart sbtab format
                if ob['type']=='ReactionID':
                # standard SBtab Format, the reaction_list here is called
                # ReactionID, as Reaction List was allready picked in SBtab
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
                    #Basti: extra Funktion
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
                                'Reaction[Full]': self.build_full(row,indexes_dict)
                            })
                    reaction_list.pop(0)
            else:
                # new rxncon format
                if ob['type']=='rxnconReactionList':
                    # Find column indexes for !ComponentA:Name, !ComponentA:Domain, !ComponentA:Subdomain, !ComponentA:Residue, !Reaction, !ComponentB:Name, !ComponentB:Domain, !ComponentB:Subdomain, !ComponentB:Residue
                    indexes_dict={
                        'uid': ob['object'].columns.index('!UID:Reaction'),
                        'ss' : ob['object'].columns.index('!SourceState'),
                        'ps' : ob['object'].columns.index('!ProductState'),

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
                    #Basti: extra Funktion
                    reaction_list=[{}]
                    for i,row in enumerate(ob['object'].getRows()):
                        r_def= [reaction for reaction in reaction_definition if row[indexes_dict['rea']].lower() == reaction['UID:Reaction'].lower()][0]
                        # using reaction as foreign key on reaction definition UID:Reaction to get the ReactionTypeID
                        reaction_list.append({
                                'ReactionID' : i+1,
                                'UID:Reaction' : r_def['UID:Reaction'].lower(),
                                'ReactionType:ID' : r_def['ReactionType:ID'],

                                'SourceState' : row[indexes_dict['ss']],
                                'ProductState' : row[indexes_dict['ps']],

                                'ComponentA[Name]': row[indexes_dict['can']],
                                'ComponentA[Domain]': row[indexes_dict['cad']],
                                'ComponentA[Subdomain]': row[indexes_dict['cas']],
                                'ComponentA[Residue]': row[indexes_dict['car']],
                                'ComponentA[DSR]': '{0}/{1}({2})'.format(row[indexes_dict['cad']],row[indexes_dict['cas']],row[indexes_dict['car']]),
                                'ComponentB[Name]': row[indexes_dict['cbn']],
                                'ComponentB[Domain]': row[indexes_dict['cbd']],
                                'ComponentB[Subdomain]': row[indexes_dict['cbs']],
                                'ComponentB[Residue]': row[indexes_dict['cbr']],
                                'ComponentB[DSR]': '{0}/{1}({2})'.format(row[indexes_dict['cbd']],row[indexes_dict['cbs']],row[indexes_dict['cbr']]),

                                'Reaction[Full]': self.build_full(row,indexes_dict)
                            })
                    reaction_list.pop(0)
        # for ob in ob_list loop ends

        #return Rxncon(dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition), parsed_xls=True) #build rxncon object
        return dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition) #build rxncon dict


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
                out+='_['+row[d['c%ss'%comp]]
                if row[d['c%sr'%comp]]:
                    out+='('+row[d['c%sr'%comp]]+')'
                out+=']'
            elif row[d['c%sr'%comp]]:
                out+='_[(' + row[d['c%sr'%comp]] + ')]'

            return out

        out = component("a")
        out+='_'+row[d['rea']]+'_'
        out+= component("b")

        return out


    def build_reaction_definition(self):
        '''
        Creates Reaction definition dictionary, from given table
        '''

        for ob in self.ob_list:
            reaction_definition_list=[]
            if ob['type'] == 'ReactionList':
                if self.d.rxncon_sbtab_detected ==0:
                # standart sbtab format
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
                    return reaction_definition_list

            elif ob['type']== 'rxnconReactionDefinition':
                # new rxncon sbtab hybrid format
                    reactionTypeID2def = dict([(row['ReactionType:ID'], row) for row in REACTION_TEMPLATE])
                    indexes_dict={
                        'r': ob['object'].columns.index('!UID:Reaction'),
                        'm': ob['object'].columns.index('!ModifierBoundary'),
                        'rtn': ob['object'].columns.index('!ReactionType:Name'),
                        'rti': ob['object'].columns.index('!ReactionType:ID'),
                        'rn': ob['object'].columns.index('!Reaction:Name'),
                        'cs': ob['object'].columns.index('!coSubstrates'),
                        'cp': ob['object'].columns.index('!coProducts'),
                        'co': ob['object'].columns.index('!Comment')
                        }

                    for row in ob['object'].getRows():
                    # reaction_list.pop(0)
                        reaction_definition_list.append({
                            'UID:Reaction' : unicode(row[indexes_dict['r']]),
                            'ModifierBoundary' : unicode(row[indexes_dict['m']]),
                            'ReactionType:ID' : unicode(row[indexes_dict['rti']]),
                            'ReactionType:Name' : unicode(row[indexes_dict['rtn']]),
                            'Reaction:Name' : unicode(row[indexes_dict['rn']]),
                            'coSubstrate(s)' : unicode(row[indexes_dict['cs']]),
                            'coProduct(s)' : unicode(row[indexes_dict['cp']]),
                            'Comment' : unicode(row[indexes_dict['co']])
                            })
                        reaction_definition_list[-1].update(reactionTypeID2def[row[indexes_dict['rti']]])


                    return reaction_definition_list


if __name__=="__main__":

    c=Commandline()
    #c.hello()
    #c.inputdir='rxncon_files/rxncon_xls/sps_cut'   # sbtab file export, old rxncon
    #c.inputdir ='rxncon_files/rxncon_xls/multi'   # multiple old rxncon
    #c.inputdir='rxncon_sbtab_files'   # new rxncon input format
    #c.inputdir='rxncon_sbtab_files/noCompa'   # new rxncon input format without compartment
    c.inputdir='rxncon_sbtab_files/' # 19.10.15 new rxncon input
    #c.inputdir='sbtab_files/tiger_files_csv_cut'


    p=Parser(c.inputdir)

    print p.target_format

    if p.d.parsable_to=='rxncon':
        p.parse_SBtab2rxncon()


