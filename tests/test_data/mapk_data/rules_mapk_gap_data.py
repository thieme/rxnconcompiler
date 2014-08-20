#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all GAP reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

# Sst2_[RGS]_GAP_Gpa1_[GnP]; k+ Gpa1_[BDRec]--Ste2_[CyT]; k+ Ste2_[CyT]--Sst2_[nDEP]

MAPK_GAP_DATA = {
# COVALENT MODIFICATION
# gap no contingencies
'Bag7_GAP_Rho1_[GnP]': {
    'Rules':[
    'Bag7 + Rho1(GnP~P) -> Bag7 + Rho1(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Bag7', 'Rho1', 'no contingencies']},

'Bem2_GAP_Rho1_[GnP]': {
    'Rules':[
    'Bem2 + Rho1(GnP~P) -> Bem2 + Rho1(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Bem2', 'Rho1', 'no contingencies']},

'Bem3_GAP_Cdc42_[GnP]': {
    'Rules':[
    'Bem3 + Cdc42(GnP~P) -> Bem3 + Cdc42(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Bem3', 'Cdc42', 'no contingencies']},

'Lrg1_[GAP]_GAP_Rho1_[GnP]': {
    'Rules':[
    'Lrg1 + Rho1(GnP~P) -> Lrg1 + Rho1(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Lrg1', 'Rho1', 'no contingencies']},

'Rga1_GAP_Cdc42_[GnP]': {
    'Rules':[
    'Rga1 + Cdc42(GnP~P) -> Rga1 + Cdc42(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Rga1', 'Cdc42', 'no contingencies']},

'Rga2_GAP_Cdc42_[GnP]': {
    'Rules':[
    'Rga2 + Cdc42(GnP~P) -> Rga2 + Cdc42(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Rga2', 'Cdc42', 'no contingencies']},

'Sac7_[GAP]_GAP_Rho1_[GnP]': {
    'Rules':[
    'Sac7 + Rho1(GnP~P) -> Sac7 + Rho1(GnP~U)'],
    'Tags': [
    1, 'GAP', 'Sac7', 'Rho1', 'no contingencies']},

'Sst2_[RGS]_GAP_Gpa1_[GnP]; k+ Gpa1_[BDRec]--Ste2_[CyT]; k+ Ste2_[CyT]--Sst2_[nDEP]': {
    'Rules':[
    'Sst2(nDEP!1).Ste2(CyT!1) + Gpa1(GnP~P,BDRec!1).Ste2(CyT!1) -> Sst2(nDEP!1).Ste2(CyT!1) + Gpa1(GnP~U,BDRec!1).Ste2(CyT!1)',
    'Sst2(nDEP!1).Ste2(CyT!1) + Gpa1(GnP~P,BDRec) -> Sst2(nDEP!1).Ste2(CyT!1) + Gpa1(GnP~U,BDRec)',
    'Sst2(nDEP) + Gpa1(GnP~P,BDRec!1).Ste2(CyT!1) -> Sst2(nDEP) + Gpa1(GnP~U,BDRec!1).Ste2(CyT!1)',
    'Sst2(nDEP) + Gpa1(GnP~P,BDRec) -> Sst2(nDEP) + Gpa1(GnP~U,BDRec)'],
    'Tags': [
    1, 'GAP', 'Sst2', 'Gpa1', 'contingencies', 'K+', 'complicated']},
}


DATA = [MAPK_GAP_DATA]
