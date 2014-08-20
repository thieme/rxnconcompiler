#!/usr/bin/env python

"""
mapk_cut_data.py contains dictionary with all CUT reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_CUT_DATA = {
# MODIFICATION
# AP no contingencies
'Yps1_CUT_Msb2_[HMH/CD]; k+ [NutrientDeprivation]': {
    'Rules':[
    'Yps1 + Msb2(HMHCD~U) -> Yps1 + Msb2(HMHCD~Truncated)'],
    'Tags': [
    1, 'CUT', 'Yps1', 'Msb2', 'contingencies', 'k+', 'input']},


}

DATA = [MAPK_CUT_DATA]
