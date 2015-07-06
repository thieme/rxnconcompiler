# File parser to convert from rxncon format to sbtab format and vice
# versa

type_identifier = "TableType"
import csv

def parse_csv(filename):
    '''
    https://docs.python.org/2/library/csv.html
    '''

    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        try:
            for row in csvreader:
                print row

        #error catching
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
                




if __name__=="__main__":
    parse_csv('BIOMD0000000061_Reaction.csv')
    print '--------------------------------------'
    parse_csv('BIOMD0000000061_Compound.csv')
