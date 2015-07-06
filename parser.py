# File parser to convert from rxncon format to sbtab format and vice
# versa

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
                    formula_index=row.index('!SumFormula')
                    id_index = row.index('!SBOTerm')
                    print row #mw

                else:
                    reaction_list.append({
                        'Reaction': row[name_index].lower()}) #usw.
                    if colNrHeader != len(row):
                        print 'oh oh'
                    print row #mw

        #error catching
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
                
    print reaction_list
    return reaction_list



if __name__=="__main__":
    read_sbtab_csv('BIOMD0000000061_Reaction.csv')
    #print '--------------------------------------'
    #read_sbtab_csv('BIOMD0000000061_Compound.csv')
