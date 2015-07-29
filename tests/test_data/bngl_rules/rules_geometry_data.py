#!/usr/bin/env python

"""
rule_geometry_data.py contains dictionaries with examples of rules with 
with boolean contingencies that define geometry of a complex.
(e.g. <C1>; 1--2 Ste7--Ste11). 

One dict represents single system, that should run in BioNetGen.
{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

GEOMETRY = {
"""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Comp>
<Comp>; OR <C1>; OR <C2>
<C1>; 1--2 Ste7--Ste11
<C2>; 1--2 Ste5_[MEKK]--Ste11; 3--4 Ste5_[MEK]--Ste7; 1--3 Ste5_[BDSte5]--Ste5_[BDSte5]""": {
    'Rules':[
    'Ste11(AssocSte7!1).Ste7(ALS359~U,AssocSte11!1) -> Ste11(AssocSte7!1).Ste7(ALS359~P,AssocSte11!1)',
    'Ste11(AssocSte5!3,AssocSte7).Ste5(BDSte5!2,MEKK!3).Ste5(BDSte5!2,MEK!1).Ste7(ALS359~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!3,AssocSte7).Ste5(BDSte5!2,MEKK!3).Ste5(BDSte5!2,MEK!1).Ste7(ALS359~P,AssocSte11,AssocSte5!1)'],
    'Tags': [
    1, 'P+', 'contingencies', '!', 'bool', 'defined geometry']},

'Ste7_ppi_Ste11': {
    'Rules':[
    'Ste7(AssocSte11) + Ste11(AssocSte7) <-> Ste11(AssocSte7!1).Ste7(AssocSte11!1)'],
    'Tags': [
    1, 'ppi', 'Ste7', 'Ste11', 'no contingencies']},

'Ste5_[MEKK]_ppi_Ste11': {
    'Rules':[
    'Ste5(MEKK) + Ste11(AssocSte5) <-> Ste11(AssocSte5!1).Ste5(MEKK!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste11', 'no contingencies']},

'Ste5_[MEK]_ppi_Ste7': {
    'Rules':[
    'Ste5(MEK) + Ste7(AssocSte5) <-> Ste5(MEK!1).Ste7(AssocSte5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste7', 'no contingencies']},

'Ste5_[BDSte5]_ppi_Ste5_[BDSte5]': {
    'Rules':[
    'Ste5(BDSte5) + Ste5(BDSte5) <-> Ste5(BDSte5!1).Ste5(BDSte5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'no contingencies', 'homodimer']}
}

DATA = [GEOMETRY]
