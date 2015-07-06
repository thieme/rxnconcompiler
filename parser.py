# File parser to convert from rxncon format to sbtab format and vice
# versa

type_identifier = "TableType"

def parse_csv(filename):
    '''
    http://www.decalage.info/python/configparser
    '''
    #filename = 'BIOMD0000000061_Reaction.csv' #mw

    with open(filename, 'r') as f:
        first_line= f.readline().strip()
        type_pos_begin= (first_line.find(type_identifier))+11
        type_pos_end= first_line.find(' ', type_pos_begin)-1
        tableType=first_line[type_pos_begin:type_pos_end]
        
        print tableType
#    for line in f:
        




if __name__=="__main__":
        parse_csv('BIOMD0000000061_Reaction.csv')
