#!/usr/bin/env python

"""
mapk_ap_data.py contains dictionary with all AP (autophosphorilation) reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_AP_DATA = {
# MODIFICATION
# AP no contingencies
'Ste20_[KD]_AP_Ste20_[SerThr]': {
    'Rules':[
    'Ste20 + Ste20(SerThr~U) -> Ste20 + Ste20(SerThr~P)'],
    'Tags': [
    1, 'AP', 'Ste20', 'no contingencies']},

# AP contingencies
'Rck2_AP_Rck2_[Ser]; k+ Rck2_[c(S519)]-{P}': {
    'Rules':[
    'Rck2(cS519~P) + Rck2(Ser~U,cS519~P) -> Rck2(cS519~P) + Rck2(Ser~P,cS519~P)',
	'Rck2(cS519~U) + Rck2(Ser~U,cS519~U) -> Rck2(cS519~U) + Rck2(Ser~P,cS519~U)'],
    'Tags': [
    1, 'AP', 'Rck2', 'contingencies', 'K+', 'ask MK']},

'''Ssk2_[KD]_AP_Ssk2_[(T1460)]; k+ <Ssk1Ssk2>
<Ssk1Ssk2>; and Ssk1_[BDSsk1]--Ssk1_[BDSsk1]
<Ssk1Ssk2>; and Ssk1_[RR]--Ssk2_[BDSsk1]''': {
    'Rules':[
    'Ssk1(BDSsk1!2,RR!1).Ssk1(BDSsk1!2).Ssk2(T1460~U,BDSsk1!1) -> Ssk1(BDSsk1!2,RR!1).Ssk1(BDSsk1!2).Ssk2(T1460~P,BDSsk1!1)',
	'Ssk1(BDSsk1,RR!1).Ssk2(T1460~U,BDSsk1!1) -> Ssk1(BDSsk1,RR!1).Ssk2(T1460~P,BDSsk1!1)',
	'Ssk2(T1460~U,BDSsk1) -> Ssk2(T1460~P,BDSsk1)'],
    'Tags': [
    1, 'AP', 'Ssk2', 'contingencies', 'K+', 'bool', 'ask MK']},

}

DATA = [MAPK_AP_DATA]
