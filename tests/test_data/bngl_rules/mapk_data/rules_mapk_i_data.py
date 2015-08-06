#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all i (interacion) reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_I_DATA = {
# ASOCCIATION
# i no contingencies
'Pkc1_i_PS': {
    # TODO: is the alphabetical order right here?
    'Rules':[
    'Pkc1(AssocPS) + PS(AssocPkc1) <-> PS(AssocPkc1!1).Pkc1(AssocPS!1)'],
    'Tags': [
    1, 'i', 'Pkc1', 'PS', 'no contingencies', 'todo']},

'Pkh1_i_PHS': {
    'Rules':[
    'Pkh1(AssocPHS) + PHS(AssocPkh1) <-> PHS(AssocPkh1!1).Pkh1(AssocPHS!1)'],
    'Tags': [
    1, 'i', 'Pkh1', 'PHS', 'no contingencies']},

'Pkh2_i_PHS': {
    'Rules':[
    'Pkh2(AssocPHS) + PHS(AssocPkh2) <-> PHS(AssocPkh2!1).Pkh2(AssocPHS!1)'],
    'Tags': [
    1, 'i', 'Pkh2', 'PHS', 'no contingencies']},

'Ste20_[BR]_i_PIP2': {
    'Rules':[
    'Ste20(BR) + PIP2(AssocSte20) <-> PIP2(AssocSte20!1).Ste20(BR!1)'],
    'Tags': [
    1, 'i', 'Ste20', 'PIP2', 'no contingencies']},
}

DATA = [MAPK_I_DATA]
