# File parser to convert from rxncon format to sbtab format and vice
# versa
# Mathias Wajnberg July 2015
#
# Mapping:
#| sbtab       | -->  | rxncon              |
#|_____________|______|_____________________|
#| !Name       |      | Reaction            |
#| !SumFormula |      | makes up components |
#| !SBOTerm    |      | ReactionID          |



type_identifier = "TableType"
import csv

def read_sbtab_csv(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''
    
    reaction_list=[]

    type_identifier = "TableType"

    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            #get Table Type
            first_line= csvfile.readline().strip()
            type_pos_begin= (first_line.find(type_identifier))+11
            type_pos_end= first_line.find(' ', type_pos_begin)-1
            tableType=first_line[type_pos_begin:type_pos_end] #e.g. Reaction, Compound etc.
            
            for row in csvreader:
                if row[0][0]=='!':
                    colNrHeader= len(row)
                    name_index=row.index('!Name')
                    id_index = row.index('!SBOTerm')
                    formula_index=row.index('!SumFormula')
                    #componentA, componentB = getComponents(row[formula_index])
                    print row #mw

                else:
                    reaction_list.append({
                        'Reaction': row[name_index].lower(),
                        'ReactionID': row[id_index]
                    }) #usw.
                    if colNrHeader != len(row):
                        print 'oh oh'
                    print row #mw

        #error catching
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
                
    print reaction_list
    return reaction_list

def getComponents(formula):
    """Read Component names from Sum Formula of a Reaction in sbtab
    format"""
    arrow_pos = formula.find('<=>')
    left=formula[0:arrow_pos-1]
    right=formula[arrow_pos+4:]

    no_comps_l= left.count('+')+1
    no_comps_r= right.count('+')+1

    comps_l=[]
    comps_r=[]



if __name__=="__main__":
    read_sbtab_csv('BIOMD0000000061_Reaction.csv')
    #print '--------------------------------------'
    #read_sbtab_csv('BIOMD0000000061_Compound.csv')
