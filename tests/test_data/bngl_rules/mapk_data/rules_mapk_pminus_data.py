#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all P- reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_PMINUS_DATA = {
# COVALENT MODIFICATION
# P- no contingencies
'Msg5_[PD]_P-_Kss1_[(T183)]': {
    'Rules':[
    'Msg5 + Kss1(T183~P) -> Msg5 + Kss1(T183~U)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Kss1', 'no contingencies']},

'Msg5_[PD]_P-_Kss1_[(Y185)]': {
    'Rules':[
    'Msg5 + Kss1(Y185~P) -> Msg5 + Kss1(Y185~U)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Kss1', 'no contingencies']},

'Ptc2_[PD]_P-_Hog1_[(T174)]': {
    'Rules':[
    'Ptc2 + Hog1(T174~P) -> Ptc2 + Hog1(T174~U)'],
    'Tags': [
    1, 'P-', 'Ptc2', 'Hog1', 'no contingencies', 'K+']},

'Ptc3_[PD]_P-_Hog1_[(T174)]': {
    'Rules':[
    'Ptc3 + Hog1(T174~P) -> Ptc3 + Hog1(T174~U)'],
    'Tags': [
    1, 'P-', 'Ptc3', 'Hog1', 'no contingencies', 'K+']},

'Ptp2_[PD]_P-_Fus3_[(Y182)]': {
    'Rules':[
    'Ptp2 + Fus3(Y182~P) -> Ptp2 + Fus3(Y182~U)'],
    'Tags': [
    1, 'P-', 'Ptc3', 'Hog1', 'no contingencies']},

'Ptp2_[PD]_P-_Slt2_[(Y192)]': {
    'Rules':[
    'Ptp2 + Slt2(Y192~P) -> Ptp2 + Slt2(Y192~U)'],
    'Tags': [
    1, 'P-', 'Ptc2', 'Slt2', 'no contingencies']},

# p- contingencies
'Msg5_[PD]_P-_Fus3_[(T180)]; k+ Fus3_[CD]--Msg5_[n]': {
    # TODO: Fus3_[T180]-{P} True (product state in Absolute requirements in header)
    # StateApplicator as an interface betwen State and Molecule ???
    'Rules':[
    'Fus3(T180~P,CD!1).Msg5(n!1) -> Fus3(T180~U,CD!1).Msg5(n!1)',
    'Msg5(n) + Fus3(T180~P,CD) -> Msg5(n) + Fus3(T180~U,CD)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Fus3', 'contingencies', 'K+', 'todo']},

'Msg5_[PD]_P-_Fus3_[(Y182)]; k+ Fus3_[CD]--Msg5_[n]': {
    'Rules':[
    'Fus3(Y182~P,CD!1).Msg5(n!1) -> Fus3(Y182~U,CD!1).Msg5(n!1)',
    'Msg5(n) + Fus3(Y182~P,CD) -> Msg5(n) + Fus3(Y182~U,CD)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Fus3', 'contingencies', 'K+']},

'Msg5_[PD]_P-_Slt2_[(T190)]; ! Msg5_[n]--Slt2_[n]': {
    'Rules':[
    'Msg5(n!1).Slt2(T190~P,n!1) -> Msg5(n!1).Slt2(T190~U,n!1)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Slt2', 'contingencies', '!']},

'Msg5_[PD]_P-_Slt2_[(Y192)]; ! Msg5_[n]--Slt2_[n]': {
    'Rules':[
    'Msg5(n!1).Slt2(Y192~P,n!1) -> Msg5(n!1).Slt2(Y192~U,n!1)'],
    'Tags': [
    1, 'P-', 'Msg5', 'Slt2', 'contingencies', '!']},

'''Ptc1_[PD]_P-_Hog1_[(T174)]; k+ <Pbs2-Nbp2-Ptc1>
<Pbs2-Nbp2-Ptc1>; and Nbp2_[SH3]--Pbs2_[SIM2]
<Pbs2-Nbp2-Ptc1>; and Nbp2_[n]--Ptc1_[AssocNbp2]''': {
    'Rules':[
    'Nbp2(SH3!2,n!1).Pbs2(SIM2!2).Ptc1(AssocNbp2!1) + Hog1(T174~P) -> Nbp2(SH3!2,n!1).Pbs2(SIM2!2).Ptc1(AssocNbp2!1) + Hog1(T174~U)',
    'Nbp2(SH3,n!1).Ptc1(AssocNbp2!1) + Hog1(T174~P) -> Nbp2(SH3,n!1).Ptc1(AssocNbp2!1) + Hog1(T174~U)',
    'Ptc1(AssocNbp2) + Hog1(T174~P) -> Ptc1(AssocNbp2) + Hog1(T174~U)'],
    'Tags': [
    1, 'P-', 'Ptc1', 'Hog1', 'contingencies', 'K+', 'bool']},

'Ptp2_[PD]_P-_Hog1_[(Y176)]; k+ Hog1_[CD]--Ptp2_[AssocHog1]': {
    'Rules':[
    'Hog1(Y176~P,CD!1).Ptp2(AssocHog1!1) -> Hog1(Y176~U,CD!1).Ptp2(AssocHog1!1)',
    'Ptp2(AssocHog1) + Hog1(Y176~P,CD) -> Ptp2(AssocHog1) + Hog1(Y176~U,CD)'],
    'Tags': [
    1, 'P-', 'Ptp2', 'Hog1', 'contingencies', 'K+']},

'Ptp3_[PD]_P-_Fus3_[(Y182)]; k+ Fus3_[CD]--Ptp3_[CH2]': {
    'Rules':[
    'Fus3(Y182~P,CD!1).Ptp3(CH2!1) -> Fus3(Y182~U,CD!1).Ptp3(CH2!1)',
    'Ptp3(CH2) + Fus3(Y182~P,CD) -> Ptp3(CH2) + Fus3(Y182~U,CD)'],
    'Tags': [
    1, 'P-', 'Ptp3', 'Fus3', 'contingencies', 'K+']},

'Ptp3_[PD]_P-_Hog1_[(Y176)]; k+ Hog1_[CD]--Ptp3_[AssocHog1]': {
    'Rules':[
    'Hog1(Y176~P,CD!1).Ptp3(AssocHog1!1) -> Hog1(Y176~U,CD!1).Ptp3(AssocHog1!1)',
    'Ptp3(AssocHog1) + Hog1(Y176~P,CD) -> Ptp3(AssocHog1) + Hog1(Y176~U,CD)'],
    'Tags': [
    1, 'P-', 'Ptp3', 'Hog1', 'contingencies', 'K+']},

'Sdp1_[PD]_P-_Slt2_[(T190)]; ! Sdp1_[AssocSlt2]--Slt2_[AssocSdp1]': {
    'Rules':[
    'Sdp1(AssocSlt2!1).Slt2(T190~P,AssocSdp1!1) -> Sdp1(AssocSlt2!1).Slt2(T190~U,AssocSdp1!1)'],
    'Tags': [
    1, 'P-', 'Sdp1', 'Slt2', 'contingencies', '!', 'single substrate']},

'Sdp1_[PD]_P-_Slt2_[(Y192)]; ! Sdp1_[AssocSlt2]--Slt2_[AssocSdp1]': {
    'Rules':[
    'Sdp1(AssocSlt2!1).Slt2(Y192~P,AssocSdp1!1) -> Sdp1(AssocSlt2!1).Slt2(Y192~U,AssocSdp1!1)'],
    'Tags': [
    1, 'P-', 'Sdp1', 'Slt2', 'contingencies', '!', 'single substrate']},

}

DATA = [MAPK_PMINUS_DATA]