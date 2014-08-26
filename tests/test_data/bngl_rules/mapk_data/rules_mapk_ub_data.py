#!/usr/bin/env python

"""
mapk_ub_data.py contains dictionary with all Ub+ reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_UB_DATA = {
# MODIFICATION
# Ub+ no contingencies
'SCF_Ub+_Tec1; ! Cdc4_[WD40]--Tec1_[CPD]; ! Cdc4_[SCF]--SCF_[Cdc4]': {
    'Rules':[
    'Cdc4(SCF!1).SCF(Cdc4!1) + Cdc4(WD40!1).Tec1(SCF~U,CPD!1) -> Cdc4(SCF!1).SCF(Cdc4!1) + Cdc4(WD40!1).Tec1(SCF~Ub,CPD!1)'],
    'Tags': [
    1, 'Ub+', 'SCF', 'Tec1', 'contingencies', '!', 'complicated']},

}

DATA = [MAPK_UB_DATA]
