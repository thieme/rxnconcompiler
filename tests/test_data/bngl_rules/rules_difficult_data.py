#!/usr/bin/env python

# TODO: add ppi reactions

"""
rule_difficult_data.py contains dictionaries with examples of reactions
that produced eror in some point and are not included in other tests.
(e.g. <C1>; 1--2 Ste7--Ste11). 

One dict represents single system, that should run in BioNetGen.
{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""


DEGRADATION = {
'Kin_P+_X': {
    'Rules': [
    'Kin + X(Kin~U) -> Kin + X(Kin~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']},

'ins_ppi_IR': {
    'Rules':[
    'ins(IR) + IR(ins) <-> IR(ins!1).ins(IR!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

'a_ppi_IR': {
    'Rules':[
    'a(IR) + IR(a) <-> IR(a!1).a(IR!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

'X_DEG_ins; ! X_[Kin]-{P}; ! ins--IR': {
    'Rules':[
    'X(Kin~P) + IR(ins!1).ins(IR!1) -> X(Kin~P) + IR(ins)'],
    'Tags': [
    1, 'DEG', 'no contingencies']},
}

# This is not possible now
JANINA = {"""A_ppi_B
A_ppi_C
A_ppi_D
A_P+_E; ! <bool>
<bool>; OR <1+2>; OR <2+3>; OR <1+3>
<1+2>; ! A--B
<1+2>; ! A--C
<1+2>; x A--D
<2+3>; ! A--C
<2+3>; ! A--D
<2+3>; x A--B
<1+3>; ! A--B
<1+3>; ! A--D
<1+3>; x A--C""": { 
    'Rules': [
    'Kin + X(Kin~U) -> Kin + X(Kin~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']}
}

JANINA2 = {
"""Fus3_ppi_Ste7; k- <C>
<C>; AND Ste5--Ste7; AND Ste5--Ste11""": { 
    'Rules': [
    'Kin + X(Kin~U) -> Kin + X(Kin~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']}
}


BOOL_EXAMPLE = {
# required for <bool>
'''Cdc4_[WD40]_ppi_Tec1_[CPD]''': {
    'Rules': [
    'Cdc4(WD40) + Tec1(CPD) <-> Cdc4(WD40!1).Tec1(CPD!1)'],
    'Tags': [
    1, 'ppi', 'Cdc4', 'Tec1', 'no contingencies']},

# required for <bool>
'''Cdc4_[SCF]_ppi_SCF_[Cdc4]''': {
    'Rules': [
    'Cdc4(SCF) + SCF(Cdc4) <-> Cdc4(SCF!1).SCF(Cdc4!1)'],
    'Tags': [
    1, 'ppi', 'Cdc4', 'SCF', 'no contingencies']},

# required for <bool2>
'''Ste5_[MEK]_ppi_Ste7_[Ste5]''': {
    'Rules': [
    'Ste5(MEK) + Ste7(Ste5) <-> Ste5(MEK!1).Ste7(Ste5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste7', 'no contingencies']},

# required for <bool2>
'''Fus3_[CD]_ppi_Ste7_[BDMAPK]''': {
    'Rules': [
    'Fus3(CD) + Ste7(BDMAPK) <-> Fus3(CD!1).Ste7(BDMAPK!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ste7', 'no contingencies']},

'''SCF_Ub+_Tec1; ! <bool>
<bool>; AND Cdc4_[WD40]--Tec1_[CPD]; AND Cdc4_[SCF]--SCF_[Cdc4]''': {
    'Rules': [
    'Cdc4(SCF!2,WD40!1).SCF(Cdc4!2).Tec1(SCF~U,CPD!1) -> Cdc4(SCF!2,WD40!1).SCF(Cdc4!2).Tec1(SCF~Ub,CPD!1)'],
    'Tags': [
    1, 'Ub+', 'SCF', 'Tec1', 'contingencies', 'bool']},

'''Fus3_ppi_Ste5_[Unlock]; ! <bool2> 
<bool2>; AND Ste5_[MEK]--Ste7_[Ste5]; AND Fus3_[CD]--Ste7_[BDMAPK]''': {
    'Rules':[
    'Fus3(AssocSte5,CD!2).Ste5(MEK!1,Unlock).Ste7(BDMAPK!2,Ste5!1) <-> Fus3(AssocSte5!3,CD!2).Ste5(MEK!1,Unlock!3).Ste7(BDMAPK!2,Ste5!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ptp3', 'contingencies', '!', 'difficault']},

'''A_ppi_B; ! <AorC> 
<AorC>; OR A_[x]-{P}; OR B_[y]-{P}; OR A--C; OR B--D; OR B_[z]-{P}''': {
    'Rules': [
        'A(x~P,AssocB) + B(AssocA) <-> A(x~P,AssocB!1).B(AssocA!1)',
        'A(x~U,AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <-> A(x~U,AssocB!2,AssocC!1).B(AssocA!2).C(AssocA!1)',
        'A(x~U,AssocB,AssocC) + B(y~P,AssocA) <-> A(x~U,AssocB!1,AssocC).B(y~P,AssocA!1)',
        'A(x~U,AssocB,AssocC) + B(y~U,AssocA,AssocD!1).D(AssocB!1) <-> A(x~U,AssocB!2,AssocC).B(y~U,AssocA!2,AssocD!1).D(AssocB!1)',],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']},

'''A_ppi_B; ! <AorC> \n <AorC>; OR A--C; OR B--D''': {
    'Rules': [
        'A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <-> A(AssocB!2,AssocC!1).B(AssocA!2).C(AssocA!1)',
        'A(AssocB,AssocC) + B(AssocA,AssocD!1).D(AssocB!1) <-> A(AssocB!2,AssocC).B(AssocA!2,AssocD!1).D(AssocB!1)'],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']},

"""Ste11_[KD]_P+_Ste7_[(ALS359)]; ! <Ste7-5-5-11>
<Ste7-5-5-11>; AND Ste5_[MEKK]--Ste11; AND Ste5_[MEK]--Ste7; AND Ste5_[BDSte5]--Ste5_[BDSte5]""": {
    'Rules': [
        'Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~U,AssocSte5!1) -> Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte5!1)'],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']},

'''Ste11_[KD]_P+_Ste7_[(ALS359)]; ! Ste5_[MEKK]--Ste11; ! Ste5_[MEK]--Ste7; ! Ste5_[BDSte5]--Ste5_[BDSte5]''': {
    'Rules': [
        'Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~U,AssocSte5!1) -> Ste11(AssocSte5!3).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte5!1)'],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']},

'''A_ppi_B; ! <comp1>
    <comp1>; OR <comp1C1>
    <comp1>; OR <comp2C1>
    <comp1C1>; AND A--C
    <comp1C1>; AND C--D
    <comp2C1>; AND A--C
    <comp2C1>; AND B--E''': {
    'Rules': [
        'A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA,AssocE!1).E(AssocB!1) <-> A(AssocB!3,AssocC!2).B(AssocA!3,AssocE!1).C(AssocA!2).E(AssocB!1)',
        'A(AssocB,AssocC!2).C(AssocA!2,AssocD!1).D(AssocC!1) + B(AssocA,AssocE) <-> A(AssocB!3,AssocC!2).B(AssocA!3,AssocE).C(AssocA!2,AssocD!1).D(AssocC!1)'],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']},

"""
    A_ppi_B; ! <comp1>
    <comp1>; OR <comp1C1>
    <comp1>; OR <comp1C2>
    <comp1C1>; AND A--A1
    <comp1C1>; AND A--A2
    <comp1C2>; AND B--B1
    <comp1C2>; AND B--B2
    A_ppi_B; x <comp2>
    <comp2>; OR <comp2C1>
    <comp2>; OR <comp2C2>
    <comp2C1>; AND A--C1
    <comp2C1>; AND A--C2
    <comp2C2>; AND A--D1
    <comp2C2>; AND A--D2""": {
    'Rules': ['A(AssocB,AssocC1!2,AssocD1!1).C1(AssocA!2).D1(AssocA!1) + B(AssocA,AssocB1!2,AssocB2!1).B1(AssocB!2).B2(AssocB!1) <-> A(AssocB!5,AssocC1!2,AssocD1!1).B(AssocA!5,AssocB1!4,AssocB2!3).B1(AssocB!4).B2(AssocB!3).C1(AssocA!2).D1(AssocA!1)',
              'A(AssocB,AssocC1,AssocC2!2,AssocD1!1).C2(AssocA!2).D1(AssocA!1) + B(AssocA,AssocB1!2,AssocB2!1).B1(AssocB!2).B2(AssocB!1) <-> A(AssocB!5,AssocC1,AssocC2!2,AssocD1!1).B(AssocA!5,AssocB1!4,AssocB2!3).B1(AssocB!4).B2(AssocB!3).C2(AssocA!2).D1(AssocA!1)',
              'A(AssocB,AssocC1!2,AssocD1,AssocD2!1).C1(AssocA!2).D2(AssocA!1) + B(AssocA,AssocB1!2,AssocB2!1).B1(AssocB!2).B2(AssocB!1) <-> A(AssocB!5,AssocC1!2,AssocD1,AssocD2!1).B(AssocA!5,AssocB1!4,AssocB2!3).B1(AssocB!4).B2(AssocB!3).C1(AssocA!2).D2(AssocA!1)',
              'A(AssocB,AssocC1,AssocC2!2,AssocD1,AssocD2!1).C2(AssocA!2).D2(AssocA!1) + B(AssocA,AssocB1!2,AssocB2!1).B1(AssocB!2).B2(AssocB!1) <-> A(AssocB!5,AssocC1,AssocC2!2,AssocD1,AssocD2!1).B(AssocA!5,AssocB1!4,AssocB2!3).B1(AssocB!4).B2(AssocB!3).C2(AssocA!2).D2(AssocA!1)',
              'A(AssocA1!4,AssocA2!3,AssocB,AssocC1!2,AssocD1!1).A1(AssocA!4).A2(AssocA!3).C1(AssocA!2).D1(AssocA!1) + B(AssocA,AssocB1,AssocB2) <-> A(AssocA1!5,AssocA2!4,AssocB!3,AssocC1!2,AssocD1!1).A1(AssocA!5).A2(AssocA!4).B(AssocA!3,AssocB1,AssocB2).C1(AssocA!2).D1(AssocA!1)',
              'A(AssocA1!4,AssocA2!3,AssocB,AssocC1,AssocC2!2,AssocD1!1).A1(AssocA!4).A2(AssocA!3).C2(AssocA!2).D1(AssocA!1) + B(AssocA,AssocB1,AssocB2) <-> A(AssocA1!5,AssocA2!4,AssocB!3,AssocC1,AssocC2!2,AssocD1!1).A1(AssocA!5).A2(AssocA!4).B(AssocA!3,AssocB1,AssocB2).C2(AssocA!2).D1(AssocA!1)',
              'A(AssocA1!4,AssocA2!3,AssocB,AssocC1!2,AssocD1,AssocD2!1).A1(AssocA!4).A2(AssocA!3).C1(AssocA!2).D2(AssocA!1) + B(AssocA,AssocB1,AssocB2) <-> A(AssocA1!5,AssocA2!4,AssocB!3,AssocC1!2,AssocD1,AssocD2!1).A1(AssocA!5).A2(AssocA!4).B(AssocA!3,AssocB1,AssocB2).C1(AssocA!2).D2(AssocA!1)',
              'A(AssocA1!4,AssocA2!3,AssocB,AssocC1,AssocC2!2,AssocD1,AssocD2!1).A1(AssocA!4).A2(AssocA!3).C2(AssocA!2).D2(AssocA!1) + B(AssocA,AssocB1,AssocB2) <-> A(AssocA1!5,AssocA2!4,AssocB!3,AssocC1,AssocC2!2,AssocD1,AssocD2!1).A1(AssocA!5).A2(AssocA!4).B(AssocA!3,AssocB1,AssocB2).C2(AssocA!2).D2(AssocA!1)'],
    'Tags': [1, 'ppi', 'A', 'B', 'contingencies', '!', 'difficult']}
}
DATA = [BOOL_EXAMPLE]