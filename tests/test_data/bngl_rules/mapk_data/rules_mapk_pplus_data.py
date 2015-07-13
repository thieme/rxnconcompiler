#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all P+ reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_PPLUS_DATA = {
# COVALENT MODIFICATION
# P+ contingencies
'Bck1_[KD]_P+_Mkk1_[(S377)]; k+ Bck1_[AssocMkk1]--Mkk1_[AssocBck1]; x Bck1_[n]--Bck1_[n]': {
    'Rules':[
    'Bck1(AssocMkk1!1,n).Mkk1(S377~U,AssocBck1!1) -> Bck1(AssocMkk1!1,n).Mkk1(S377~P,AssocBck1!1)',
    'Bck1(AssocMkk1,n) + Mkk1(S377~U,AssocBck1) -> Bck1(AssocMkk1,n) + Mkk1(S377~P,AssocBck1)'],
    'Tags': [
    1, 'P+', 'Bck1', 'Mkk1', 'contingencies', 'K+', 'x']},

'Bck1_[KD]_P+_Mkk1_[(T381)]; k+ Bck1_[AssocMkk1]--Mkk1_[AssocBck1]; x Bck1_[n]--Bck1_[n]': {
    'Rules':[
    'Bck1(AssocMkk1!1,n).Mkk1(T381~U,AssocBck1!1) -> Bck1(AssocMkk1!1,n).Mkk1(T381~P,AssocBck1!1)',
    'Bck1(AssocMkk1,n) + Mkk1(T381~U,AssocBck1) -> Bck1(AssocMkk1,n) + Mkk1(T381~P,AssocBck1)'],
    'Tags': [
    1, 'P+', 'Bck1', 'Mkk1', 'contingencies', 'K+', 'x']},

'Bck1_[KD]_P+_Mkk2_[(S370)]; k+ Bck1_[AssocMkk2]--Mkk2_[AssocBck1]; x Bck1_[n]--Bck1_[n]': {
    'Rules':[
    'Bck1(AssocMkk2!1,n).Mkk2(S370~U,AssocBck1!1) -> Bck1(AssocMkk2!1,n).Mkk2(S370~P,AssocBck1!1)',
    'Bck1(AssocMkk2,n) + Mkk2(S370~U,AssocBck1) -> Bck1(AssocMkk2,n) + Mkk2(S370~P,AssocBck1)'],
    'Tags': [
    1, 'P+', 'Bck1', 'Mkk2', 'contingencies', 'K+', 'x']},

'Bck1_[KD]_P+_Mkk2_[(T374)]; k+ Bck1_[AssocMkk2]--Mkk2_[AssocBck1]; x Bck1_[n]--Bck1_[n]': {
    'Rules':[
    'Bck1(AssocMkk2!1,n).Mkk2(T374~U,AssocBck1!1) -> Bck1(AssocMkk2!1,n).Mkk2(T374~P,AssocBck1!1)',
    'Bck1(AssocMkk2,n) + Mkk2(T374~U,AssocBck1) -> Bck1(AssocMkk2,n) + Mkk2(T374~P,AssocBck1)'],
    'Tags': [
    1, 'P+', 'Bck1', 'Mkk2', 'contingencies', 'K+', 'x']},

'Fus3_[KD]_P+_Dig1; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Dig1(Fus3~U) -> Fus3(T180~P,Y182~P) + Dig1(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Dig1', 'contingencies', '!']},

'Fus3_[KD]_P+_Dig2; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Dig2(Fus3~U) -> Fus3(T180~P,Y182~P) + Dig2(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Dig2', 'contingencies', '!']},

'Fus3_[KD]_P+_Far1_[(T306)]; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Far1(T306~U) -> Fus3(T180~P,Y182~P) + Far1(T306~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Far1', 'contingencies', '!']},

'Fus3_[KD]_P+_Msg5; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Msg5(Fus3~U) -> Fus3(T180~P,Y182~P) + Msg5(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Msg5', 'contingencies', '!']},

'Fus3_[KD]_P+_Sst2_[(S539)]; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Sst2(S539~U) -> Fus3(T180~P,Y182~P) + Sst2(S539~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Sst2', 'contingencies', '!']},

'Fus3_[KD]_P+_Ste12; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Ste12(Fus3~U) -> Fus3(T180~P,Y182~P) + Ste12(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Ste12', 'contingencies', '!']},

'Fus3_[KD]_P+_Ste5; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Ste5(Fus3~U) -> Fus3(T180~P,Y182~P) + Ste5(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Ste5', 'contingencies', '!']},

'Fus3_[KD]_P+_Ste7; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Ste7(Fus3~U) -> Fus3(T180~P,Y182~P) + Ste7(Fus3~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Ste7', 'contingencies', '!']},

'Fus3_[KD]_P+_Tec1_[(T273)]; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Tec1(T273~U) -> Fus3(T180~P,Y182~P) + Tec1(T273~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Ste5', 'contingencies', '!']},

'Fus3_[KD]_P+_Tec1_[(T276)]; ! Fus3_[(T180)]-{P}; ! Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P) + Tec1(T276~U) -> Fus3(T180~P,Y182~P) + Tec1(T276~P)'],
    'Tags': [
    1, 'P+', 'Fus3', 'Ste5', 'contingencies', '!']},

'Hog1_[KD]_P+_Hot1_[(S30)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Hot1(S30~U) -> Hog1(T174~P,Y176~P) + Hot1(S30~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[KD]_P+_Hot1_[(S70)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Hot1(S70~U) -> Hog1(T174~P,Y176~P) + Hot1(S70~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[KD]_P+_Hot1_[(S153)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Hot1(S153~U) -> Hog1(T174~P,Y176~P) + Hot1(S153~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[KD]_P+_Hot1_[(S360)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Hot1(S360~U) -> Hog1(T174~P,Y176~P) + Hot1(S360~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[KD]_P+_Hot1_[(S410)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Hot1(S410~U) -> Hog1(T174~P,Y176~P) + Hot1(S410~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[KD]_P+_Rck2_[c(S519)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Rck2(cS519~U) -> Hog1(T174~P,Y176~P) + Rck2(cS519~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Rck2', 'contingencies', '!']},

'Hog1_[KD]_P+_Sic1_[(T173)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Sic1(T173~U) -> Hog1(T174~P,Y176~P) + Sic1(T173~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Sic1', 'contingencies', '!']},

'Hog1_[KD]_P+_Sko1_[n(S108)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Sko1(nS108~U) -> Hog1(T174~P,Y176~P) + Sko1(nS108~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Sko1', 'contingencies', '!']},

'Hog1_[KD]_P+_Sko1_[n(S113)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Sko1(nS113~U) -> Hog1(T174~P,Y176~P) + Sko1(nS113~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Sko1', 'contingencies', '!']},

'Hog1_[KD]_P+_Sko1_[n(S126)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Sko1(nS126~U) -> Hog1(T174~P,Y176~P) + Sko1(nS126~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Sko1', 'contingencies', '!']},

'Hog1_[KD]_P+_Smp1_[(S348)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Smp1(S348~U) -> Hog1(T174~P,Y176~P) + Smp1(S348~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Smp1', 'contingencies', '!']},

'Hog1_[KD]_P+_Smp1_[(S357)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Smp1(S357~U) -> Hog1(T174~P,Y176~P) + Smp1(S357~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Smp1', 'contingencies', '!']},

'Hog1_[KD]_P+_Smp1_[(S376)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Smp1(S376~U) -> Hog1(T174~P,Y176~P) + Smp1(S376~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Smp1', 'contingencies', '!']},

'Hog1_[KD]_P+_Smp1_[(T365)]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P) + Smp1(T365~U) -> Hog1(T174~P,Y176~P) + Smp1(T365~P)'],
    'Tags': [
    1, 'P+', 'Hog1', 'Smp1', 'contingencies', '!']},

'Kss1_[KD]_P+_Dig1; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Dig1(Kss1~U) -> Kss1(T183~P,Y185~P) + Dig1(Kss1~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Dig1', 'contingencies', '!']},

'Kss1_[KD]_P+_Dig2; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Dig2(Kss1~U) -> Kss1(T183~P,Y185~P) + Dig2(Kss1~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Dig2', 'contingencies', '!']},

'Kss1_[KD]_P+_Sst2_[(S539)]; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Sst2(S539~U) -> Kss1(T183~P,Y185~P) + Sst2(S539~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Sst2', 'contingencies', '!']},

'Kss1_[KD]_P+_Ste12; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Ste12(Kss1~U) -> Kss1(T183~P,Y185~P) + Ste12(Kss1~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Ste12', 'contingencies', '!']},

'Kss1_[KD]_P+_Ste5; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Ste5(Kss1~U) -> Kss1(T183~P,Y185~P) + Ste5(Kss1~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Ste5', 'contingencies', '!']},

'Kss1_[KD]_P+_Ste7; ! Kss1_[(T183)]-{P}; ! Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~P,Y185~P) + Ste7(Kss1~U) -> Kss1(T183~P,Y185~P) + Ste7(Kss1~P)'],
    'Tags': [
    1, 'P+', 'Kss1', 'Ste7', 'contingencies', '!']},

'Mkk1_[KD]_P+_Slt2_[(T190)]; ! Mkk1_[(S377)]-{P}; ! Mkk1_[(T381)]-{P}; ! Mkk1_[n]--Slt2_[n]': {
    'Rules':[
    'Mkk1(S377~P,T381~P,n!1).Slt2(T190~U,n!1) -> Mkk1(S377~P,T381~P,n!1).Slt2(T190~P,n!1)'],
    'Tags': [
    1, 'P+', 'Mkk1', 'Slt2', 'contingencies', '!']},

'Mkk1_[KD]_P+_Slt2_[(Y192)]; ! Mkk1_[(S377)]-{P}; ! Mkk1_[(T381)]-{P}; ! Mkk1_[n]--Slt2_[n]': {
    'Rules':[
    'Mkk1(S377~P,T381~P,n!1).Slt2(Y192~U,n!1) -> Mkk1(S377~P,T381~P,n!1).Slt2(Y192~P,n!1)'],
    'Tags': [
    1, 'P+', 'Mkk1', 'Slt2', 'contingencies', '!']},

'Mkk2_[KD]_P+_Slt2_[(T190)]; ! Mkk2_[(S370)]-{P}; ! Mkk2_[(T374)]-{P}; ! Mkk2_[n]--Slt2_[n]': {
    'Rules':[
    'Mkk2(S370~P,T374~P,n!1).Slt2(T190~U,n!1) -> Mkk2(S370~P,T374~P,n!1).Slt2(T190~P,n!1)'],
    'Tags': [
    1, 'P+', 'Mkk2', 'Slt2', 'contingencies', '!']},

'Mkk2_[KD]_P+_Slt2_[(Y192)]; ! Mkk2_[(S370)]-{P}; ! Mkk2_[(T374)]-{P}; ! Mkk2_[n]--Slt2_[n]': {
    'Rules':[
    'Mkk2(S370~P,T374~P,n!1).Slt2(Y192~U,n!1) -> Mkk2(S370~P,T374~P,n!1).Slt2(Y192~P,n!1)'],
    'Tags': [
    1, 'P+', 'Mkk2', 'Slt2', 'contingencies', '!']},

'Pbs2_[KD]_P+_Hog1_[(T174)]; k+ Hog1_[CD]--Pbs2_[HBD-1]; k+ Hog1_[PBD-2]--Pbs2_[HBD-1]; ! Pbs2_[AL(S514)]-{P}; ! Pbs2_[AL(T518)]-{P}': {
    'Rules':[
    'Hog1(T174~U,CD!2,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!2).Pbs2(HBD1!1) -> Hog1(T174~P,CD!2,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!2).Pbs2(HBD1!1)',
    'Hog1(T174~U,CD,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!1) -> Hog1(T174~P,CD,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!1)',
    'Hog1(T174~U,CD!1,PBD2).Pbs2(ALS514~P,ALT518~P,HBD1!1) -> Hog1(T174~P,CD!1,PBD2).Pbs2(ALS514~P,ALT518~P,HBD1!1)',
    'Pbs2(ALS514~P,ALT518~P,HBD1) + Hog1(T174~U,CD,PBD2) -> Pbs2(ALS514~P,ALT518~P,HBD1) + Hog1(T174~P,CD,PBD2)'],
    'Tags': [
    1, 'P+', 'Pbs2', 'Hog1', 'contingencies', 'K+', 'complicated', 'ask MK']},

'Pbs2_[KD]_P+_Hog1_[(Y176)]; k+ Hog1_[CD]--Pbs2_[HBD-1]; k+ Hog1_[PBD-2]--Pbs2_[HBD-1]; ! Pbs2_[AL(S514)]-{P}; ! Pbs2_[AL(T518)]-{P}': {
    'Rules':[
    'Hog1(Y176~U,CD!2,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!2).Pbs2(HBD1!1) -> Hog1(Y176~P,CD!2,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!2).Pbs2(HBD1!1)',
    'Hog1(Y176~U,CD,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!1) -> Hog1(Y176~P,CD,PBD2!1).Pbs2(ALS514~P,ALT518~P,HBD1!1)',
    'Hog1(Y176~U,CD!1,PBD2).Pbs2(ALS514~P,ALT518~P,HBD1!1) -> Hog1(Y176~P,CD!1,PBD2).Pbs2(ALS514~P,ALT518~P,HBD1!1)',
    'Pbs2(ALS514~P,ALT518~P,HBD1) + Hog1(Y176~U,CD,PBD2) -> Pbs2(ALS514~P,ALT518~P,HBD1) + Hog1(Y176~P,CD,PBD2)'],
    'Tags': [
    1, 'P+', 'Pbs2', 'Hog1', 'contingencies', 'K+', 'complicated', 'ask MK']},

'Pkc1_[KD]_P+_Bck1_[(S939)]; k+ Pkc1_[C1]--Rho1_[ED]; k+ Pkc1_[AssocPS]--PS_[AssocPkc1]; k+ Pkc1_[AL(T983)]-{P}': {
    'Rules':[
    'PS(AssocPkc1!2).Pkc1(ALT983~P,AssocPS!2,C1!1).Rho1(ED!1) + Bck1(S939~U) -> PS(AssocPkc1!2).Pkc1(ALT983~P,AssocPS!2,C1!1).Rho1(ED!1) + Bck1(S939~P)',
    'PS(AssocPkc1!1).Pkc1(ALT983~P,AssocPS!1,C1) + Bck1(S939~U) -> PS(AssocPkc1!1).Pkc1(ALT983~P,AssocPS!1,C1) + Bck1(S939~P)',
    'Pkc1(ALT983~P,AssocPS,C1!1).Rho1(ED!1) + Bck1(S939~U) -> Pkc1(ALT983~P,AssocPS,C1!1).Rho1(ED!1) + Bck1(S939~P)',
    'Pkc1(ALT983~P,AssocPS,C1) + Bck1(S939~U) -> Pkc1(ALT983~P,AssocPS,C1) + Bck1(S939~P)',
    'PS(AssocPkc1!2).Pkc1(ALT983~U,AssocPS!2,C1!1).Rho1(ED!1) + Bck1(S939~U) -> PS(AssocPkc1!2).Pkc1(ALT983~U,AssocPS!2,C1!1).Rho1(ED!1) + Bck1(S939~P)',
    'PS(AssocPkc1!1).Pkc1(ALT983~U,AssocPS!1,C1) + Bck1(S939~U) -> PS(AssocPkc1!1).Pkc1(ALT983~U,AssocPS!1,C1) + Bck1(S939~P)',
    'Pkc1(ALT983~U,AssocPS,C1!1).Rho1(ED!1) + Bck1(S939~U) -> Pkc1(ALT983~U,AssocPS,C1!1).Rho1(ED!1) + Bck1(S939~P)',
    'Pkc1(ALT983~U,AssocPS,C1) + Bck1(S939~U) -> Pkc1(ALT983~U,AssocPS,C1) + Bck1(S939~P)'],
    'Tags': [
    1, 'P+', 'Pkc1', 'Bck1', 'contingencies', 'K+']},

'Pkh1_[KD]_P+_Pkc1_[AL(T983)]; k+ Pkh1_[AssocPHS]--PHS_[AssocPkh1]': {
    'Rules':[
    'PHS(AssocPkh1!1).Pkh1(AssocPHS!1) + Pkc1(ALT983~U) -> PHS(AssocPkh1!1).Pkh1(AssocPHS!1) + Pkc1(ALT983~P)',
    'Pkh1(AssocPHS) + Pkc1(ALT983~U) -> Pkh1(AssocPHS) + Pkc1(ALT983~P)'],
    'Tags': [
    1, 'P+', 'Pkh1', 'Pkc1', 'contingencies', 'K+']},

'Pkh2_[KD]_P+_Pkc1_[AL(T983)]; k+ Pkh2_[AssocPHS]--PHS_[AssocPkh2]': {
    # TODO: Now we are not really distinguishing beetwen domains and residues
    'Rules':[
    'PHS(AssocPkh2!1).Pkh2(AssocPHS!1) + Pkc1(ALT983~U) -> PHS(AssocPkh2!1).Pkh2(AssocPHS!1) + Pkc1(ALT983~P)',
    'Pkh2(AssocPHS) + Pkc1(ALT983~U) -> Pkh2(AssocPHS) + Pkc1(ALT983~P)'],
    'Tags': [
    1, 'P+', 'Pkh2', 'Pkc1', 'contingencies', 'K+']},

'Sln1_[HK]_P+_Sln1_[HK(H576)]; ! Sln1_[BDSln1]--Sln1_[BDSln1]; k+ [Turgor]': {
    'Rules':[
    'Sln1(BDSln1!1).Sln1(HKH576~U,BDSln1!1) -> Sln1(BDSln1!1).Sln1(HKH576~P,BDSln1!1)'],
    'Tags': [
    1, 'P+', 'Sln1', 'contingencies', '!', 'K+', 'input']},

'Slt2_[KD]_P+_Msg5; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Msg5(Slt2~U) -> Slt2(T190~P,Y192~P) + Msg5(Slt2~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Msg5', 'contingencies', '!']},

'Slt2_[KD]_P+_Rlm1_[c(S427)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Rlm1(cS427~U) -> Slt2(T190~P,Y192~P) + Rlm1(cS427~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Rlm1', 'contingencies', '!']},
   
'Slt2_[KD]_P+_Rlm1_[c(T439))]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Rlm1(cT439~U) -> Slt2(T190~P,Y192~P) + Rlm1(cT439~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Rlm1', 'contingencies', '!']},

'Slt2_[KD]_P+_Rom2; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Rom2(Slt2~U) -> Slt2(T190~P,Y192~P) + Rom2(Slt2~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Rom2', 'contingencies', '!']},

'Slt2_[KD]_P+_Sir3_[(S275)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Sir3(S275~U) -> Slt2(T190~P,Y192~P) + Sir3(S275~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Sir3', 'contingencies', '!']},

'Slt2_[KD]_P+_Sir3_[(S282)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Sir3(S282~U) -> Slt2(T190~P,Y192~P) + Sir3(S282~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Sir3', 'contingencies', '!']},    

'Slt2_[KD]_P+_Sir3_[(S289)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Sir3(S289~U) -> Slt2(T190~P,Y192~P) + Sir3(S289~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Sir3', 'contingencies', '!']}, 

'Slt2_[KD]_P+_Sir3_[(S295)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Sir3(S295~U) -> Slt2(T190~P,Y192~P) + Sir3(S295~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Sir3', 'contingencies', '!']},

'Slt2_[KD]_P+_Swi4; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Swi4(Slt2~U) -> Slt2(T190~P,Y192~P) + Swi4(Slt2~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Swi4', 'contingencies', '!']},

'Slt2_[KD]_P+_Swi6_[(S238)]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}': {
    'Rules':[
    'Slt2(T190~P,Y192~P) + Swi6(S238~U) -> Slt2(T190~P,Y192~P) + Swi6(S238~P)'],
    'Tags': [
    1, 'P+', 'Slt2', 'Swi6', 'contingencies', '!']},

'Ssk2_[KD]_P+_Pbs2_[AL(S514)]; ! Ssk2_[(T1460)]-{P}; ! Pbs2_[RSD1]--Ssk2_[KD]': {
    'Rules':[
    'Pbs2(ALS514~U,RSD1!1).Ssk2(T1460~P,KD!1) -> Pbs2(ALS514~P,RSD1!1).Ssk2(T1460~P,KD!1)'],
    'Tags': [
    1, 'P+', 'Ssk2', 'Pbs2', 'contingencies', '!', 'dimer']},

'Ssk2_[KD]_P+_Pbs2_[AL(T518)]; ! Ssk2_[(T1460)]-{P}; ! Pbs2_[RSD1]--Ssk2_[KD]': {
    'Rules':[
    'Pbs2(ALT518~U,RSD1!1).Ssk2(T1460~P,KD!1) -> Pbs2(ALT518~P,RSD1!1).Ssk2(T1460~P,KD!1)'],
    'Tags': [
    1, 'P+', 'Ssk2', 'Pbs2', 'contingencies', '!', 'dimer']},

'Ssk22_[KD]_P+_Pbs2_[AL(S514)]; ! Pbs2_[RSD1]--Ssk22_[KD]; ! Ssk1_[AssocSsk22]--Ssk22_[AssocSsk1]': {
    'Rules':[
    'Pbs2(ALS514~U,RSD1!2).Ssk1(AssocSsk22!1).Ssk22(AssocSsk1!1,KD!2) -> Pbs2(ALS514~P,RSD1!2).Ssk1(AssocSsk22!1).Ssk22(AssocSsk1!1,KD!2)'],
    'Tags': [
    1, 'P+', 'Ssk22', 'Pbs2', 'contingencies', '!', 'dimer']},

'Ssk22_[KD]_P+_Pbs2_[AL(T518)]; ! Pbs2_[RSD1]--Ssk22_[KD]; ! Ssk1_[AssocSsk22]--Ssk22_[AssocSsk1]': {
    'Rules':[
    'Pbs2(ALT518~U,RSD1!2).Ssk1(AssocSsk22!1).Ssk22(AssocSsk1!1,KD!2) -> Pbs2(ALT518~P,RSD1!2).Ssk1(AssocSsk22!1).Ssk22(AssocSsk1!1,KD!2)'],
    'Tags': [
    1, 'P+', 'Ssk22', 'Pbs2', 'contingencies', '!', 'dimer']},

'Ste11_[KD]_P+_Pbs2_[AL(S514)]; x Ste11_[CBD]--Ste11_[KD]; ! Pbs2_[RSD2]--Ste11_[n]; ! Sho1_[CyT]--Ste11_[BDSho1]; ! Pbs2_[RSD2PR]--Sho1_[CyTSH3]' :{
    'Rules':[
    'Pbs2(ALS514~U,RSD2!2,RSD2PR!3).Sho1(CyT!1).Sho1(CyTSH3!3).Ste11(BDSho1!1,CBD,n!2) -> Pbs2(ALS514~P,RSD2!2,RSD2PR!3).Sho1(CyT!1).Sho1(CyTSH3!3).Ste11(BDSho1!1,CBD,n!2)'],
    'Tags': [
    1, 'P+', 'Ste11', 'Pbs2', 'contingencies', 'x', '!', 'ask MK']},

'Ste11_[KD]_P+_Pbs2_[AL(T518)]; x Ste11_[CBD]--Ste11_[KD]; ! Pbs2_[RSD2]--Ste11_[n]; ! Sho1_[CyT]--Ste11_[BDSho1]; ! Pbs2_[RSD2PR]--Sho1_[CyTSH3]' :{
    'Rules':[
    'Pbs2(ALT518~U,RSD2!2,RSD2PR!3).Sho1(CyT!1).Sho1(CyTSH3!3).Ste11(BDSho1!1,CBD,n!2) -> Pbs2(ALT518~P,RSD2!2,RSD2PR!3).Sho1(CyT!1).Sho1(CyTSH3!3).Ste11(BDSho1!1,CBD,n!2)'],
    'Tags': [
    1, 'P+', 'Ste11', 'Pbs2', 'contingencies', 'x', '!', 'ask MK']},

'''Ste11_[KD]_P+_Ste7_[AL(S359)]; x Ste11_[CBD]--Ste11_[KD]; ! <STE11-7>
<STE11-7>; or Ste7_[AssocSte11]--Ste11_[AssocSte7]
<STE11-7>; or <Ste7-5-5-11>
<Ste7-5-5-11>; and Ste5_[MEKK]--Ste11_[AssocSte5]
<Ste7-5-5-11>; and Ste5_[MEK]--Ste7_[AssocSte5]
<Ste7-5-5-11>; and Ste5_[BDSte5]--Ste5_[BDSte5]''': {
    'Rules':[
    'Ste11(AssocSte7!1,CBD).Ste7(ALS359~U,AssocSte11!1) -> Ste11(AssocSte7!1,CBD).Ste7(ALS359~P,AssocSte11!1)',
    'Ste11(AssocSte5!3,AssocSte7,CBD).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!3,AssocSte7,CBD).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALS359~P,AssocSte11,AssocSte5!1)'],
    'Tags': [
    1, 'P+', 'Ste11', 'Ste7', 'contingencies', '!', 'x', 'bool']},

'''Ste11_[KD]_P+_Ste7_[AL(T363)]; x Ste11_[CBD]--Ste11_[KD]; ! <STE11-7>
<STE11-7>; or Ste7_[AssocSte11]--Ste11_[AssocSte7]
<STE11-7>; or <Ste7-5-5-11>
<Ste7-5-5-11>; and Ste5_[MEKK]--Ste11_[AssocSte5]
<Ste7-5-5-11>; and Ste5_[MEK]--Ste7_[AssocSte5]
<Ste7-5-5-11>; and Ste5_[BDSte5]--Ste5_[BDSte5]''': {
    'Rules':[
    'Ste11(AssocSte7!1,CBD).Ste7(ALT363~U,AssocSte11!1) -> Ste11(AssocSte7!1,CBD).Ste7(ALT363~P,AssocSte11!1)',
    'Ste11(AssocSte5!3,AssocSte7,CBD).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALT363~U,AssocSte11,AssocSte5!1) -> Ste11(AssocSte5!3,AssocSte7,CBD).Ste5(BDSte5!2,MEK!1,MEKK!3).Ste5(BDSte5!2).Ste7(ALT363~P,AssocSte11,AssocSte5!1)'],
    'Tags': [
    1, 'P+', 'Ste11', 'Ste7', 'contingencies', '!', 'x', 'bool']},

'''Ste20_[KD]_P+_Ste11_[CBD(S302)]; k+ Ste20_[SerThr]-{P}; x Ste20_[KD]--Ste20_[CRIB]; ! <Ste11^{M}>
<Ste11^{M}>; or Sho1_[CyT]--Ste11_[BDSho1]
<Ste11^{M}>; or <Ste11^{M/5}>
<Ste11^{M/5}>; and Ste5_[MEKK]--Ste11_[AssocSte5]
<Ste11^{M/5}>; and <Ste5^{M}>
<Ste5^{M}>; and Ste4_[BDSte5]--Ste5_[nRING-H2]
<Ste5^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
''': {
    'Rules':[
    'Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDS302~U,BDSho1!1) -> Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDS302~P,BDSho1!1)',
    'Ste20(SerThr~P,KD) + Ste11(CBDS302~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~P,KD) + Ste11(CBDS302~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)',
    'Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDS302~U,BDSho1!1) -> Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDS302~P,BDSho1!1)',
    'Ste20(SerThr~U,KD) + Ste11(CBDS302~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~U,KD) + Ste11(CBDS302~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)'],
    'Tags': [
    1, 'P+', 'Ste20', 'Ste11', 'contingencies', 'K+', 'x', 'bool']},

'''Ste20_[KD]_P+_Ste11_[CBD(S306)]; k+ Ste20_[SerThr]-{P}; x Ste20_[KD]--Ste20_[CRIB]; ! <Ste11^{M}>
<Ste11^{M}>; or Sho1_[CyT]--Ste11_[BDSho1]
<Ste11^{M}>; or <Ste11^{M/5}>
<Ste11^{M/5}>; and Ste5_[MEKK]--Ste11_[AssocSte5]
<Ste11^{M/5}>; and <Ste5^{M}>
<Ste5^{M}>; and Ste4_[BDSte5]--Ste5_[nRING-H2]
<Ste5^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]''': {
    'Rules':[
    'Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDS306~U,BDSho1!1) -> Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDS306~P,BDSho1!1)',
    'Ste20(SerThr~P,KD) + Ste11(CBDS306~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~P,KD) + Ste11(CBDS306~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)',
    'Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDS306~U,BDSho1!1) -> Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDS306~P,BDSho1!1)',
    'Ste20(SerThr~U,KD) + Ste11(CBDS306~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~U,KD) + Ste11(CBDS306~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)'],
    'Tags': [
    1, 'P+', 'Ste20', 'Ste11', 'contingencies', 'K+', 'x', 'bool']},

'''Ste20_[KD]_P+_Ste11_[CBD(T307)]; k+ Ste20_[SerThr]-{P}; x Ste20_[KD]--Ste20_[CRIB]; ! <Ste11^{M}>
<Ste11^{M}>; or Sho1_[CyT]--Ste11_[BDSho1]
<Ste11^{M}>; or <Ste11^{M/5}>
<Ste11^{M/5}>; and Ste5_[MEKK]--Ste11_[AssocSte5]
<Ste11^{M/5}>; and <Ste5^{M}>
<Ste5^{M}>; and Ste4_[BDSte5]--Ste5_[nRING-H2]
<Ste5^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]''': {
    'Rules':[
    'Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDT307~U,BDSho1!1) -> Ste20(SerThr~P,KD) + Sho1(CyT!1).Ste11(CBDT307~P,BDSho1!1)',
    'Ste20(SerThr~P,KD) + Ste11(CBDT307~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~P,KD) + Ste11(CBDT307~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)',
    'Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDT307~U,BDSho1!1) -> Ste20(SerThr~U,KD) + Sho1(CyT!1).Ste11(CBDT307~P,BDSho1!1)',
    'Ste20(SerThr~U,KD) + Ste11(CBDT307~U,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1) -> Ste20(SerThr~U,KD) + Ste11(CBDT307~P,AssocSte5!2,BDSho1).Ste18(AssocSte4!3).Ste4(AssocSte18!3,BDSte5!1).Ste5(MEKK!2,nRINGH2!1)'],
    'Tags': [
    1, 'P+', 'Ste20', 'Ste11', 'contingencies', 'K+', 'x', 'bool']},

'Ste7_[KD]_P+_Fus3_[(T180)]; ! Ste7_[AL(S359)]-{P}; ! Ste7_[AL(T363)]-{P}; ! Fus3_[AssocSte5]--Ste5_[Unlock]': {
    'Rules':[
    'Ste7(ALS359~P,ALT363~P) + Fus3(T180~U,AssocSte5!1).Ste5(Unlock!1) -> Ste7(ALS359~P,ALT363~P) + Fus3(T180~P,AssocSte5!1).Ste5(Unlock!1)'],
    'Tags': [
    1, 'P+', 'Ste7', 'Fus3', 'contingencies', '!']},

'Ste7_[KD]_P+_Fus3_[(Y182)]; ! Ste7_[AL(S359)]-{P}; ! Ste7_[AL(T363)]-{P}; ! Fus3_[AssocSte5]--Ste5_[Unlock]': {
    'Rules':[
    'Ste7(ALS359~P,ALT363~P) + Fus3(Y182~U,AssocSte5!1).Ste5(Unlock!1) -> Ste7(ALS359~P,ALT363~P) + Fus3(Y182~P,AssocSte5!1).Ste5(Unlock!1)'],
    'Tags': [
    1, 'P+', 'Ste7', 'Fus3', 'contingencies', '!']},

'Ste7_[KD]_P+_Kss1_[(T183)]; ! Ste7_[AL(S359)]-{P}; ! Ste7_[AL(T363)]-{P}; ! Kss1_[CD]--Ste7_[BDMAPK]': {
    'Rules':[
    'Kss1(T183~U,CD!1).Ste7(ALS359~P,ALT363~P,BDMAPK!1) -> Kss1(T183~P,CD!1).Ste7(ALS359~P,ALT363~P,BDMAPK!1)'],
    'Tags': [
    1, 'P+', 'Ste7', 'Kss1', 'contingencies', '!']},

'Ste7_[KD]_P+_Kss1_[(Y185)]; ! Ste7_[AL(S359)]-{P}; ! Ste7_[AL(T363)]-{P}; ! Kss1_[CD]--Ste7_[BDMAPK]': {
    'Rules':[
    'Kss1(Y185~U,CD!1).Ste7(ALS359~P,ALT363~P,BDMAPK!1) -> Kss1(Y185~P,CD!1).Ste7(ALS359~P,ALT363~P,BDMAPK!1)'],
    'Tags': [
    1, 'P+', 'Ste7', 'Kss1', 'contingencies', '!']},
}

DATA = [MAPK_PPLUS_DATA]