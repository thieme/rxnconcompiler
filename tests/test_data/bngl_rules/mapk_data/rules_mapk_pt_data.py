#!/usr/bin/env python

"""
mapk_pt_data.py contains dictionary with all PT (phosphotransfer) reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_PT_DATA = {
# MODIFICATION
# PT no contingencies
'Sln1_[HK(H576)]_PT_Sln1_[RR(D1144)]': {
    'Rules':[
    'Sln1(HKH576~P) + Sln1(RRD1144~U) <-> Sln1(HKH576~U) + Sln1(RRD1144~P)'],
    'Tags': [
    1, 'Sln1', 'PT', 'no contingencies']},

'Sln1_[RR(D1144)]_PT_Ypd1_[(H64)]': {
    'Rules':[
    'Sln1(RRD1144~P) + Ypd1(H64~U) <-> Sln1(RRD1144~U) + Ypd1(H64~P)'],
    'Tags': [
    1, 'Sln1', 'Ypd1', 'PT', 'no contingencies']},

# PT contingencies
'Ypd1_[(H64)]_PT_Ssk1_[RR(D544)]; ! Ssk1_[RR]--Ypd1_[AssocSsk1]': {
    'Rules':[
    'Ssk1(RRD544~U,RR!1).Ypd1(H64~P,AssocSsk1!1) <-> Ssk1(RRD544~P,RR!1).Ypd1(H64~U,AssocSsk1!1)'],
    'Tags': [
    1, 'Ypd1', 'Ssk1', 'PT', 'contingencies', '!', 'ask MK']},
}

DATA = [MAPK_PT_DATA]
