#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all DEG reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_DEG_DATA = {
# DEGRADATION / SYNTHESIS
# DEG
'Bar1_[PepD]_DEG_MFalpha_[(L6-K7)]': {
    'Rules':[
    'Bar1 + MFalpha -> Bar1'],
    'Tags': [
    1, 'DEG', 'Bar1', 'MFalpha', 'no contingencies']},
}

DATA = [MAPK_DEG_DATA]
