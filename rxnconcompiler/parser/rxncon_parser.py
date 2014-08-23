#!/usr/bin/env python

"""
Module rxncon_parser.py.

Parses rxncon input data from xls file or string (quick).
Returns rxncon json dictionary.

Contains functions

parse_text  
parse_xls
parse_rxncon - recognise input, can parse:
               xls, string, string from file, 
               dict (recognises that input is already parsed).
"""

import sys
import os
import os.path
#sys.path.append(os.sep.join(os.getcwd().split(os.sep)[:-1]))
sys.path.append(os.sep.join(__file__.split(os.sep)[:-2]))
import xlrd
from util.rxncon_errors import RxnconParserError
from definitions.default_definition import DEFAULT_DEFINITION


def parse_rxncon(rxncon_input):
    """Recognizes input and uses text or xls parser. Returns xls_tables (dict)."""
    # already parsed:
    if type(rxncon_input) == dict:
        return rxncon_input

    # xls
    elif rxncon_input[-4:] in ['.ods', '.xls', '.xlsx']:
        return parse_xls(rxncon_input)

    # quick from file
    elif os.path.exists(rxncon_input):
        f = open(rxncon_input)
        quick_str = f.read().strip()
        return parse_text(quick_str)
        
    # quick from string
    else:
        return parse_text(rxncon_input)
        

def parse_text(rxncon_text):
    """Parses quick format and returns xls_tables dict."""
    reaction_definition = DEFAULT_DEFINITION #pickle.load(open(reaction_definition_filename, 'r'))
    reaction2def = dict([(row['Reaction'].lower(), row) for row in reaction_definition])
    lines = rxncon_text.split("\n")
    reaction_list = []
    contingency_list = []
    contingency_id = 0
    reaction_id = 0
    for line in lines:
        line = line.strip()
        if line.startswith('#') or not line:
            continue  # filter comments and empty lines
        split_line = line.split(';')

        try:
            if line[0] in '!xk':
                for cont in split_line:
                    cont = cont.strip()
                    split_cont = cont.split()
                    contingency_list.append({
                        'ContingencyID': contingency_id,
                        'Target': '',
                        'Contingency': split_cont[0],
                        'Modifier': split_cont[1]
                        })
                    contingency_id += 1
                continue
        except:
            raise RxnconParserError('Error in line:<br/>\n%s<br/>\n%s' % (line, sys.exc_info()[1])) 

        reaction_full = split_line[0].strip()

        r_def = None
        for r_name in reaction2def.keys():
            if '_%s_' % r_name in reaction_full.lower():
                r_def = reaction2def[r_name]
                break
        else: #indent
            
            if not reaction_full[0] in '<[{':
                raise RxnconParserError('unknown reaction type in %s' % reaction_full)

        if r_def:
            start = reaction_full.lower().find('_%s_' % r_def['Reaction'].lower())
            reaction_components = reaction_full.split(reaction_full[start:start + len(r_def['Reaction']) + 2])
            comp_name2index = dict(ComponentA=0, ComponentB=1)
            source_state = 'N/A'
            if r_def['SourceState[Component]'] != 'N/A':
                components = [c.strip() for c in r_def['SourceState[Component]'].split(',')]
                modificats = [c.strip() for c in r_def['SourceState[Modification]'].split(',')]
                for index in range(len(components)):
                    if modificats[index] != 'N/A':  # avoid adding N/A to the state name
                        source_state = reaction_components[comp_name2index[components[index]]] + modificats[index]
                    else:
                        source_state = reaction_components[comp_name2index[components[index]]]
            product_state = 'N/A'
            if r_def['ProductState[Component]'] != 'N/A':
                components = [c.strip() for c in r_def['ProductState[Component]'].split(',')]
                modificats = []
                modificats = [c.strip() for c in r_def['ProductState[Modification]'].split(',')]
                for index in range(len(components)):
                    if modificats[index] != 'N/A':  # avoid adding N/A to the state name
                        modification = modificats[index] if '--Component' not in modificats[index] \
                                                         else '--' + reaction_components[1]
                    else:
                        modification = ''
                    if 'mRNA' in components[index]:
                        components[index] = components[index][:-5]
                        modification = 'mRNA'
                    #!!! 
                    # changed the following line to satisfy test_rxncon_parser and 
                    # to fix test_sbgner. However, not sure whether this will break 
                    # any functionality elsewhere. Tests say no at least.
                    # (2012/12/10)
                    #product_state = reaction_components[0].split('_')[0] + modification
                    if components[index] == 'ComponentA':
                        product_state = reaction_components[0] + modification
                    else:
                        product_state = reaction_components[1] + modification
                    

            component_a = reaction_components[0]
            # split up dsr into its components
            # [Domain/Subdomain(Residue)]
            import re
            dsrA = reaction_components[0].split('_')[1][1:-1] if '_' in reaction_components[0] else ''
            matchA = re.match('(\w*)/?(\w*)\(?(\w*)\)?',dsrA)
            dsrB = reaction_components[1].split('_')[1][1:-1] if '_' in reaction_components[1] else ''
            matchB = re.match('(\w*)/?(\w*)\(?(\w*)\)?',dsrB)
            # here we have inconsistency in xls we have separate keys for Domain, Subdomain and Residue
            reaction_list.append({
                'ReactionID': reaction_id,
                'ReactionType': r_def['Reaction'].lower(),
                'Reaction': r_def['Reaction'].lower(),
                'Reaction[Full]': reaction_full,
                'SourceState': source_state,
                'ProductState': product_state,
                'ComponentA[Name]': reaction_components[0].split('_')[0],
                'ComponentA[DSR]': dsrA,
                'ComponentA[Domain]': matchA.group(1),
                'ComponentA[Subdomain]': matchA.group(2),
                'ComponentA[Residue]': matchA.group(3),
                'ComponentB[Name]': reaction_components[1].split('_')[0],
                'ComponentB[DSR]': dsrB,
                'ComponentB[Domain]': matchB.group(1),
                'ComponentB[Subdomain]': matchB.group(2),
                'ComponentB[Residue]': matchB.group(3),
                })
            reaction_id += 0
        try:
            if len(split_line) > 1:  # contingencies present
                for cont in split_line[1:]:
                    cont = cont.strip()
                    split_cont = cont.split()
                    contingency_list.append({
                        'ContingencyID': contingency_id,
                        'Target': reaction_full,
                        'Contingency': split_cont[0],
                        'Modifier': split_cont[1]
                        })
                    contingency_id += 1
        except:
            raise RxnconParserError('Error in line:<br/>\n%s<br/>\n%s' % (line, sys.exc_info()[1]))
    return dict(reaction_list=reaction_list, contingency_list=contingency_list, reaction_definition=reaction_definition)


def parse_xls(file_path):
    try:
        xl = readexcel(file_path)
    except:
        raise RxnconParserError('Error reading the Excel file: %s %s'%(sys.exc_info()[0],sys.exc_info()[1] ))
    sheetnames = xl.worksheets()
    if '(IV) Reaction definition' in sheetnames:
        xls_talbes = dict(
                reaction_list = list(xl.getiter('(I) Reaction list')),
                contingency_list = list(xl.getiter('(III) Contingency list')),
                reaction_definition = list(xl.getiter('(IV) Reaction definition'))
                )
    else:
        xls_talbes = dict(
                reaction_list = list(xl.getiter(sheetnames[0])),
                contingency_list = list(xl.getiter(sheetnames[1])),
                reaction_definition = list(xl.getiter(sheetnames[2])),
                )
    return xls_talbes



class readexcel(object):
    """ Simple OS Independent Class for Extracting Data from Excel Files 
        the using xlrd module found at http://www.lexicon.net/sjmachin/xlrd.htm
        
        Versions of Excel supported: 2004, 2002, XP, 2000, 97, 95, 5, 4, 3
        xlrd version tested: 0.5.2
        
        Data is extracted by creating a iterator object which can be used to 
        return data one row at a time. The default extraction method assumes 
        that the worksheet is in tabular format with the first nonblank row
        containing variable names and all subsequent rows containing values.
        This method returns a dictionary which uses the variables names as keys
        for each piece of data in the row.  Data can also be extracted with 
        each row represented by a list.
        
        Extracted data is represented fairly logically. By default dates are
        returned as strings in "yyyy/mm/dd" format or "yyyy/mm/dd hh:mm:ss",
        as appropriate.  However, dates can be return as a tuple containing
        (Year, Month, Day, Hour, Min, Second) which is appropriate for usage
        with mxDateTime or DateTime.  Numbers are returned as either INT or 
        FLOAT, whichever is needed to support the data.  Text, booleans, and
        error codes are also returned as appropriate representations.
        
        Quick Example:
        xl = readexcel('testdata.xls')
        sheetnames = xl.worksheets()
        for sheet in sheetnames:
            print sheet
            for row in xl.getiter(sheet):
                # Do Something here
        """ 
    def __init__(self, filename):
        """ Returns a readexcel object of the specified filename - this may
        take a little while because the file must be parsed into memory """
        if not os.path.isfile(filename):
            raise NameError, "%s is not a valid filename" % filename
        self.__filename__ = filename
        self.__book__ = xlrd.open_workbook(filename)
        self.__sheets__ = {}
        self.__sheetnames__ = []
        for i in self.__book__.sheet_names():
            uniquevars = []
            firstrow = 0
            sheet = self.__book__.sheet_by_name(i)
            for row in range(sheet.nrows):
                types,values = sheet.row_types(row),sheet.row_values(row)
                nonblank = False
                for j in values:
                    if j != '':
                        nonblank=True
                        break
                if nonblank:
                    # Generate a listing of Unique Variable Names for Use as
                    # Dictionary Keys In Extraction. Duplicate Names will
                    # be replaced with "F#"
                    variables = self.__formatrow__(types,values,False)
                    unknown = 1
                    while variables:
                        var = variables.pop(0)
                        if var in uniquevars or var == '':
                            var = 'F' + str(unknown)
                            unknown += 1
                        uniquevars.append(str(var))
                    firstrow = row + 1
                    break
            self.__sheetnames__.append(i)
            self.__sheets__.setdefault(i,{}).__setitem__('rows',sheet.nrows)
            self.__sheets__.setdefault(i,{}).__setitem__('cols',sheet.ncols)
            self.__sheets__.setdefault(i,{}).__setitem__('firstrow',firstrow)
            self.__sheets__.setdefault(i,{}).__setitem__('variables',uniquevars[:])
    def getiter(self, sheetname, returnlist=False, returntupledate=False):
        """ Return an generator object which yields the lines of a worksheet;
        Default returns a dictionary, specifing returnlist=True causes lists
        to be returned.  Calling returntupledate=True causes dates to returned
        as tuples of (Year, Month, Day, Hour, Min, Second) instead of as a
        string """
        if sheetname not in self.__sheets__.keys():
            raise NameError, "%s is not present in %s" % (sheetname,\
                                                          self.__filename__)
        if returnlist:
            return __iterlist__(self, sheetname, returntupledate)
        else:
            return __iterdict__(self, sheetname, returntupledate)
    def worksheets(self):
        """ Returns a list of the Worksheets in the Excel File """
        return self.__sheetnames__
    def nrows(self, worksheet):
        """ Return the number of rows in a worksheet """
        return self.__sheets__[worksheet]['rows']
    def ncols(self, worksheet):
        """ Return the number of columns in a worksheet """
        return self.__sheets__[worksheet]['cols']
    def variables(self,worksheet):
        """ Returns a list of Column Names in the file,
            assuming a tabular format of course. """
        return self.__sheets__[worksheet]['variables']
    def __formatrow__(self, types, values, wanttupledate):
        """ Internal function used to clean up the incoming excel data """
        ##  Data Type Codes:
        ##  EMPTY 0
        ##  TEXT 1 a Unicode string 
        ##  NUMBER 2 float 
        ##  DATE 3 float 
        ##  BOOLEAN 4 int; 1 means TRUE, 0 means FALSE 
        ##  ERROR 5 
        returnrow = []
        for i in range(len(types)):
            type,value = types[i],values[i]
            if type == 2:
                if value == int(value):
                    value = int(value)
            elif type == 3:
                datetuple = xlrd.xldate_as_tuple(value, self.__book__.datemode)
                if wanttupledate:
                    value = datetuple
                else:
                    # time only no date component
                    if datetuple[0] == 0 and datetuple[1] == 0 and \
                       datetuple[2] == 0: 
                        value = "%02d:%02d:%02d" % datetuple[3:]
                    # date only, no time
                    elif datetuple[3] == 0 and datetuple[4] == 0 and \
                         datetuple[5] == 0:
                        value = "%04d/%02d/%02d" % datetuple[:3]
                    else: # full date
                        value = "%04d/%02d/%02d %02d:%02d:%02d" % datetuple
            elif type == 5:
                value = xlrd.error_text_from_code[value]
            returnrow.append(value)
        return returnrow

def __iterlist__(excel, sheetname, tupledate):
    """ Function Used To create the List Iterator """
    sheet = excel.__book__.sheet_by_name(sheetname)
    for row in range(excel.__sheets__[sheetname]['rows']):
        types,values = sheet.row_types(row),sheet.row_values(row)
        yield excel.__formatrow__(types, values, tupledate)

def __iterdict__(excel, sheetname, tupledate):
    """ Function Used To create the Dictionary Iterator """
    sheet = excel.__book__.sheet_by_name(sheetname)
    for row in range(excel.__sheets__[sheetname]['firstrow'],\
                     excel.__sheets__[sheetname]['rows']):
        types,values = sheet.row_types(row),sheet.row_values(row)
        formattedrow = excel.__formatrow__(types, values, tupledate)
        # Pad a Short Row With Blanks if Needed
        for i in range(len(formattedrow),\
                       len(excel.__sheets__[sheetname]['variables'])):
            formattedrow.append('')
        yield dict(zip(excel.__sheets__[sheetname]['variables'],formattedrow))