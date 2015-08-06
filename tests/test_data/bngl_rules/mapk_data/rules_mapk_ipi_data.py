#!/usr/bin/env python

"""
mapk_ipi_data.py contains dictionary with all ipi reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_IPI_DATA = {
# ASOCIATION
# IPI no contingencies
'Swi4_[n]_ipi_Swi4_[c]; x Swi4_[c]--Swi6_[c]; x Slt2_[DB]--Swi4_[c]': {
    'Rules':[
    'Swi4(c,n) <-> Swi4(c!1,n!1)'],
    'Tags': [
    1, 'ipi', 'Swi4', 'contingencies', 'x']},


}

DATA = [MAPK_IPI_DATA]
