#!/usr/bin/env python

"""
rules_mapk_bind_data.py contains dictionary with BIND reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_BIND_DATA = {
# ASSOCCIATION
# BIND no contingencies
'Hot1_BIND_Hot1Site': {
    'Rules':[
    'Hot1(AssocHot1Site) + Hot1Site(AssocHot1) <-> Hot1(AssocHot1Site!1).Hot1Site(AssocHot1!1)'],
    'Tags': [
    1, 'BIND', 'Hot1', 'Hot1Site', 'no contingencies']},

'Rlm1_BIND_Rlm1Site': {
    'Rules':[
    'Rlm1(AssocRlm1Site) + Rlm1Site(AssocRlm1) <-> Rlm1(AssocRlm1Site!1).Rlm1Site(AssocRlm1!1)'],
    'Tags': [
    1, 'BIND', 'Rlm1', 'Rlm1Site', 'no contingencies']},

'Smp1_BIND_Smp1Site': {
    'Rules':[
    'Smp1(AssocSmp1Site) + Smp1Site(AssocSmp1) <-> Smp1(AssocSmp1Site!1).Smp1Site(AssocSmp1!1)'],
    'Tags': [
    1, 'BIND', 'Smp1', 'Smp1Site', 'no contingencies']},

'Ste12_[n/HTH]_BIND_PRE': {
    'Rules':[
    'Ste12(nHTH) + PRE(AssocSte12) <-> PRE(AssocSte12!1).Ste12(nHTH!1)'],
    'Tags': [
    1, 'BIND', 'Ste12', 'PRE', 'no contingencies']},

'Sko1_[bZIP]_BIND_CRE': {
    'Rules':[
    'Sko1(bZIP) + CRE(AssocSko1) <-> CRE(AssocSko1!1).Sko1(bZIP!1)'],
    'Tags': [
    1, 'BIND', 'Sko1', 'CRE', 'no contingencies']},

'Tec1_[n/TEA]_BIND_TCS': {
    'Rules':[
    'Tec1(nTEA) + TCS(AssocTec1) <-> TCS(AssocTec1!1).Tec1(nTEA!1)'],
    'Tags': [
    1, 'BIND', 'Tec1', 'TCS', 'no contingencies']},

# BIND contingencies
'Swi4_BIND_SCBFKS2; ! Slt2_[DB]--Swi4_[c]; x Swi4_[n]--Swi4_[c]': {
    'Rules':[
    'Slt2(DB!1).Swi4(AssocSCBFKS2,c!1,n) + SCBFKS2(AssocSwi4) <-> SCBFKS2(AssocSwi4!1).Slt2(DB!2).Swi4(AssocSCBFKS2!1,c!2,n)'],
    'Tags': [
    1, 'BIND', 'Swi4', 'SCBFKS2', 'contingencies', 'complicated']},

'Swi4_BIND_SCBG1; x Slt2_[DB]--Swi4_[c]; x Swi4_[n]--Swi4_[c]': {
    'Rules':[
    'Swi4(AssocSCBG1,c,n) + SCBG1(AssocSwi4) <-> SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c,n)'],
    'Tags': [
    1, 'BIND', 'Swi4', 'SCBG1', 'contingencies', 'complicated']},

}

DATA = [MAPK_BIND_DATA]