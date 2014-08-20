#!/usr/bin/env python

"""
Collection of functions mostly for combiatorial operations.
get_dsr                 - creates DSR string (D - doamin, S - subdomain, R - residue)
create_all_combinations - creates all combinations of elements from a given list.
product                 - multiplication of matrices.
flatten                 - flatten a list of any depth.
get_permutations        - list of lists with combinations of elements from given lists.
"""

import re

def get_dsr(row, ab='A', with_delimiters=False):
    cmpnt = 'Component%s%%s' % ab
    if not with_delimiters:
        if row.has_key(cmpnt % '[DSR]'):
            return re.sub('[/\(\)]', '', row[cmpnt % '[DSR]']) if row[cmpnt % '[DSR]'] else 'bd'
        dsr = "%s%s%s" % (
                "%s" % row[cmpnt%'[Domain]'] if row[cmpnt%'[Domain]'] else '',
                "%s" % row[cmpnt%'[Subdomain]'] if row[cmpnt%'[Subdomain]'] else '',
                "%s" % row[cmpnt%'[Residue]'] if row[cmpnt%'[Residue]'] else '',
            )
        
        #dsr = 'bd0'+row['Component%s[Name]'%('A' if ab=='B' else 'B')]
        dsr = 'bd'
        dsr = re.sub('\W', '', dsr)
    elif row.has_key(cmpnt%'[DSR]'):
            return row[cmpnt%'[DSR]']
    else:
        dsr = "%s%s%s"%(
                "%s"%row[cmpnt%'[Domain]'] if row[cmpnt%'[Domain]'] else '',
                "/%s"%row[cmpnt%'[Subdomain]'] if row[cmpnt%'[Subdomain]'] else '',
                "(%s)"%row[cmpnt%'[Residue]'] if row[cmpnt%'[Residue]'] else '',
            )
    return dsr


def create_all_combinations(l):
    '''
    Return all possible comination of items from a given list.
    Only presence is important, not the order.
    >>> list(create_all_combinations([1,2,3]))
    [[3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]]
    '''
    for c in range(1, 2 ** len(l)):
        # Code Golf
        yield [l[i] for i, is_on in enumerate("".join([str((c >> y) & 1) for y in range(len(l) - 1, -1, -1)])) if is_on == '1']

def product(*args, **kwds):
    """
    copied from itertools
    Multiplying matrixes.
    """
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def flatten(x):
    """
    Copied from http://stackoverflow.com/questions/2158395/
    flatten-an-irregular-list-of-lists-in-python

    [1, 2, [3], [[[4]]]] ---> [1, 2, 3, 4]
    """
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

def get_permutations(input_list):
    """
    [(p,n),(p,n)] ---> [(p,p),(p,n),(n,p)]
    [(p,n),(p,n),(p,n)] ---> [(p,p,p),(p,n,n),(p,p,n) ...]
    """ 
    result = []
    prod = product([0, 1], repeat=len(input_list))
    prod = [x for x in prod]
    prod.remove(tuple([1] * len(input_list)))
    for comb in prod:
        temp = []
        for num, bit in enumerate(comb):
            temp.append(input_list[num][bit])
        result.append(temp)
    return result