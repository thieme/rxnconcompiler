#!/usr/bin/env python

"""
rules_mapk_ppi_data.py contains dictionary with all ppi reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_PPI_DATA = {
# ASSOCCIATION
# ppi no contingenies

#################### ADDED BY LENA TO MAKE BioNetGen runing
# WARNING: required state Cdc4_[SCF]--SCF_[Cdc4] not produced in the reactions. Add the coresponding reaction or the appropriate molecule types and seed species.
# WARNING: required state Swi4_[n]--Swi4_[c] not pro
'Cdc4_[SCF]_ppi_SCF_[Cdc4]': {
    'Rules':[
    'Cdc4(SCF) + SCF(Cdc4) <-> Cdc4(SCF!1).SCF(Cdc4!1)'],
    'Tags': [
    1, 'ppi', 'Cdc4', 'SCF', 'no contingencies']},

'Swi4_[n]_ppi_Swi4_[c]': {
    'Rules':[
    'Swi4(n) + Swi4(c) <-> Swi4(n!1).Swi4(c!1)'],
    'Tags': [
    1, 'ppi', 'Swi4', 'no contingencies']},
###################

'Bck1_ppi_Mkk1': {
    'Rules':[
    'Bck1(AssocMkk1) + Mkk1(AssocBck1) <-> Bck1(AssocMkk1!1).Mkk1(AssocBck1!1)'],
    'Tags': [
    1, 'ppi', 'Bck1', 'Mkk1', 'no contingencies']},

'Bck1_ppi_Mkk2': {
    'Rules':[
    'Bck1(AssocMkk2) + Mkk2(AssocBck1) <-> Bck1(AssocMkk2!1).Mkk2(AssocBck1!1)'],
    'Tags': [
    1, 'ppi', 'Bck1', 'Mkk2', 'no contingencies']},

'Cdc24_ppi_Far1_[c]': {
    'Rules':[
    'Cdc24(AssocFar1) + Far1(c) <-> Cdc24(AssocFar1!1).Far1(c!1)'],
    'Tags': [
    1, 'ppi', 'Cdc24', 'Far1', 'no contingencies']},

'Cdc24_ppi_Ste5_[c]': {
    'Rules':[
    'Cdc24(AssocSte5) + Ste5(c) <-> Cdc24(AssocSte5!1).Ste5(c!1)'],
    'Tags': [
    1, 'ppi', 'Cdc24', 'Ste5', 'no contingencies']},

'Cdc4_ppi_SCF': {
    'Rules':[
    'Cdc4(AssocSCF) + SCF(AssocCdc4) <-> Cdc4(AssocSCF!1).SCF(AssocCdc4!1)'],
    'Tags': [
    1, 'ppi', 'Cdc4', 'SCF', 'no contingencies']},

'Cdc42_ppi_Msb2_[CyT]': {
    'Rules':[
    'Cdc42(AssocMsb2) + Msb2(CyT) <-> Cdc42(AssocMsb2!1).Msb2(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Cdc42', 'Msb2', 'no contingencies']},

'Cyc8_[TPR1-3]_ppi_Tup1_[n]': {
    'Rules':[
    'Cyc8(TPR13) + Tup1(n) <-> Cyc8(TPR13!1).Tup1(n!1)'],
    'Tags': [
    1, 'ppi', 'Cyc8', 'Tup1', 'no contingencies']},

'Dig1_[Dsite]_ppi_Fus3_[CD/7m]': {
    'Rules':[
    'Dig1(Dsite) + Fus3(CD7m) <-> Dig1(Dsite!1).Fus3(CD7m!1)'],
    'Tags': [
    1, 'ppi', 'Dig1', 'Fus3', 'no contingencies']},

'Dig1_[Dsite]_ppi_Kss1_[CD/7m]': {
    'Rules':[
    'Dig1(Dsite) + Kss1(CD7m) <-> Dig1(Dsite!1).Kss1(CD7m!1)'],
    'Tags': [
    1, 'ppi', 'Dig1', 'Kss1', 'no contingencies']},

'Dig2_[Dsite]_ppi_Fus3_[CD/7m]': {
    'Rules':[
    'Dig2(Dsite) + Fus3(CD7m) <-> Dig2(Dsite!1).Fus3(CD7m!1)'],
    'Tags': [
    1, 'ppi', 'Dig2', 'Fus3', 'no contingencies']},

'Dig2_[Dsite]_ppi_Kss1_[CD/7m]': {
    'Rules':[
    'Dig2(Dsite) + Kss1(CD7m) <-> Dig2(Dsite!1).Kss1(CD7m!1)'],
    'Tags': [
    1, 'ppi', 'Dig2', 'Kss1', 'no contingencies']},

'Far1_[n/BD:Fus3]_ppi_Fus3_[CD]': {
    'Rules':[
    'Far1(nBDFus3) + Fus3(CD) <-> Far1(nBDFus3!1).Fus3(CD!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Msg5', 'no contingencies']},

'Fus3_[CD]_ppi_Msg5_[n]': {
    'Rules':[
    'Fus3(CD) + Msg5(n) <-> Fus3(CD!1).Msg5(n!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Msg5', 'no contingencies']},

'Fus3_ppi_Ste5_[MAPK]': {
    'Rules':[
    'Fus3(AssocSte5) + Ste5(MAPK) <-> Fus3(AssocSte5!1).Ste5(MAPK!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ste5', 'no contingencies']},

'Fus3_[CD]_ppi_Ste7_[BD:MAPK]': {
    'Rules':[
    'Fus3(CD) + Ste7(BDMAPK) <-> Fus3(CD!1).Ste7(BDMAPK!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ste7', 'no contingencies']},

'Fus3_ppi_Tec1_[n]': {
    'Rules':[
    'Fus3(AssocTec1) + Tec1(n) <-> Fus3(AssocTec1!1).Tec1(n!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Tec1', 'no contingencies']},

'Gpa1_[BD:Rec]_ppi_Ste2_[CyT]': {
    'Rules':[
    'Gpa1(BDRec) + Ste2(CyT) <-> Gpa1(BDRec!1).Ste2(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Gpa1', 'Ste2', 'no contingencies']},

'Gpa1_[BD:Rec]_ppi_Ste3_[CyT]': {
    'Rules':[
    'Gpa1(BDRec) + Ste3(CyT) <-> Gpa1(BDRec!1).Ste3(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Gpa1', 'Ste3', 'no contingencies']},

'Hog1_[CD]_ppi_Pbs2_[HBD-1]': {
    'Rules':[
    'Hog1(CD) + Pbs2(HBD1) <-> Hog1(CD!1).Pbs2(HBD1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Pbs2', 'no contingencies']},

'Hog1_[CD]_ppi_Ptp3': {
    'Rules':[
    'Hog1(CD) + Ptp3(AssocHog1) <-> Hog1(CD!1).Ptp3(AssocHog1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Ptp3', 'no contingencies']},

'Hog1_[CD]_ppi_Rck2_[c]': {
    'Rules':[
    'Hog1(CD) + Rck2(c) <-> Hog1(CD!1).Rck2(c!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Rck2', 'no contingencies']},

'Hog1_ppi_Sic1': {
    'Rules':[
    'Hog1(AssocSic1) + Sic1(AssocHog1) <-> Hog1(AssocSic1!1).Sic1(AssocHog1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Sic1', 'no contingencies']},

'Hog1_ppi_Sko1_[n]': {
    'Rules':[
    'Hog1(AssocSko1) + Sko1(n) <-> Hog1(AssocSko1!1).Sko1(n!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Sko1', 'no contingencies']},

'Hog1_ppi_Smp1': {
    'Rules':[
    'Hog1(AssocSmp1) + Smp1(AssocHog1) <-> Hog1(AssocSmp1!1).Smp1(AssocHog1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Smp1', 'no contingencies']},

'Kss1_ppi_Msg5_[n]': {
    'Rules':[
    'Kss1(AssocMsg5) + Msg5(n) <-> Kss1(AssocMsg5!1).Msg5(n!1)'],
    'Tags': [
    1, 'ppi', 'Kss1', 'Msg5', 'no contingencies']},

'Kss1_ppi_Ste5_[MAPK]': {
    'Rules':[
    'Kss1(AssocSte5) + Ste5(MAPK) <-> Kss1(AssocSte5!1).Ste5(MAPK!1)'],
    'Tags': [
    1, 'ppi', 'Kss1', 'Ste5', 'no contingencies']},

'Kss1_[CD]_ppi_Ste7_[BD:MAPK]': {
    'Rules':[
    'Kss1(CD) + Ste7(BDMAPK) <-> Kss1(CD!1).Ste7(BDMAPK!1)'],
    'Tags': [
    1, 'ppi', 'Kss1', 'Ste7', 'no contingencies']},

'Kss1_ppi_Tec1_[c]': {
    'Rules':[
    'Kss1(AssocTec1) + Tec1(c) <-> Kss1(AssocTec1!1).Tec1(c!1)'],
    'Tags': [
    1, 'ppi', 'Kss1', 'Tec1', 'no contingencies']},

'Mid2_[CyT]_ppi_Rom2': {
    'Rules':[
    'Mid2(CyT) + Rom2(AssocMid2) <-> Mid2(CyT!1).Rom2(AssocMid2!1)'],
    'Tags': [
    1, 'ppi', 'Mid2', 'Rom2', 'no contingencies']},

'Mid2_[CyT]_ppi_Zeo1': {
    'Rules':[
    'Mid2(CyT) + Zeo1(AssocMid2) <-> Mid2(CyT!1).Zeo1(AssocMid2!1)'],
    'Tags': [
    1, 'ppi', 'Mid2', 'Zeo1', 'no contingencies']},

'Mkk1_ppi_Pkc1': {
    'Rules':[
    'Mkk1(AssocPkc1) + Pkc1(AssocMkk1) <-> Mkk1(AssocPkc1!1).Pkc1(AssocMkk1!1)'],
    'Tags': [
    1, 'ppi', 'Mkk1', 'Pkc1', 'no contingencies']},

'Mkk1_[n]_ppi_Slt2_[n]': {
    'Rules':[
    'Mkk1(n) + Slt2(n) <-> Mkk1(n!1).Slt2(n!1)'],
    'Tags': [
    1, 'ppi', 'Mkk1', 'Slt2', 'no contingencies']},

'Mkk2_[n]_ppi_Slt2_[n]': {
    'Rules':[
    'Mkk2(n) + Slt2(n) <-> Mkk2(n!1).Slt2(n!1)'],
    'Tags': [
    1, 'ppi', 'Mkk2', 'Slt2', 'no contingencies']},

'Mlp1_ppi_Rlm1_[c]': {
    'Rules':[
    'Mlp1(AssocRlm1) + Rlm1(c) <-> Mlp1(AssocRlm1!1).Rlm1(c!1)'],
    'Tags': [
    1, 'ppi', 'Mlp1', 'Rlm1', 'no contingencies']},

'Msg5_[n]_ppi_Slt2_[n]': {
    'Rules':[
    'Msg5(n) + Slt2(n) <-> Msg5(n!1).Slt2(n!1)'],
    'Tags': [
    1, 'ppi', 'Msg5', 'Slt2', 'no contingencies']},

'Mtl1_ppi_Rom2': {
    'Rules':[
    'Mtl1(AssocRom2) + Rom2(AssocMtl1) <-> Mtl1(AssocRom2!1).Rom2(AssocMtl1!1)'],
    'Tags': [
    1, 'ppi', 'Mtl1', 'Rom2', 'no contingencies']},

'Nbp2_[SH3]_ppi_Pbs2_[SIM2]': {
    'Rules':[
    'Nbp2(SH3) + Pbs2(SIM2) <-> Nbp2(SH3!1).Pbs2(SIM2!1)'],
    'Tags': [
    1, 'ppi', 'Nbp2', 'Pbs2', 'no contingencies']},

'Nbp2_[n]_ppi_Ptc1': {
    'Rules':[
    'Nbp2(n) + Ptc1(AssocNbp2) <-> Nbp2(n!1).Ptc1(AssocNbp2!1)'],
    'Tags': [
    1, 'ppi', 'Nbp2', 'Ptc1', 'no contingencies']},

'Nbp2_[SH3]_ppi_Ste20_[PR]': {
    'Rules':[
    'Nbp2(SH3) + Ste20(PR) <-> Nbp2(SH3!1).Ste20(PR!1)'],
    'Tags': [
    1, 'ppi', 'Nbp2', 'Ste20', 'no contingencies']},

'Opy2_[BD:Ste50]_ppi_Ste50_[RA]': {
    'Rules':[
    'Opy2(BDSte50) + Ste50(RA) <-> Opy2(BDSte50!1).Ste50(RA!1)'],
    'Tags': [
    1, 'ppi', 'Opy2', 'Ste50', 'no contingencies']},

'Pbs2_[RSD1]_ppi_Ssk2_[KD]': {
    'Rules':[
    'Pbs2(RSD1) + Ssk2(KD) <-> Pbs2(RSD1!1).Ssk2(KD!1)'],
    'Tags': [
    1, 'ppi', 'Pbs2', 'Ssk2', 'no contingencies']},

'Pbs2_[KD]_ppi_Ssk2_[KD]': {
    'Rules':[
    'Pbs2(KD) + Ssk2(KD) <-> Pbs2(KD!1).Ssk2(KD!1)'],
    'Tags': [
    1, 'ppi', 'Pbs2', 'Ssk2', 'no contingencies']},

'Pbs2_[RSD1]_ppi_Ssk22_[KD]': {
    'Rules':[
    'Pbs2(RSD1) + Ssk22(KD) <-> Pbs2(RSD1!1).Ssk22(KD!1)'],
    'Tags': [
    1, 'ppi', 'Pbs2', 'Ssk2', 'no contingencies']},

'Pbs2_[RSD2]_ppi_Ste11_[n]': {
    'Rules':[
    'Pbs2(RSD2) + Ste11(n) <-> Pbs2(RSD2!1).Ste11(n!1)'],
    'Tags': [
    1, 'ppi', 'Pbs2', 'Ste11', 'no contingencies']},

'Pkc1_[HR1]_ppi_Rho1': {
    'Rules':[
    'Pkc1(HR1) + Rho1(AssocPkc1) <-> Pkc1(HR1!1).Rho1(AssocPkc1!1)'],
    'Tags': [
    1, 'ppi', 'Pkc1', 'Rho1', 'no contingencies']},

'Rho1_ppi_Ste4': {
    'Rules':[
    'Rho1(AssocSte4) + Ste4(AssocRho1) <-> Rho1(AssocSte4!1).Ste4(AssocRho1!1)'],
    'Tags': [
    1, 'ppi', 'Rho1', 'Ste4', 'no contingencies']},

'Rlm1_[c]_ppi_Slt2': {
    'Rules':[
    'Rlm1(c) + Slt2(AssocRlm1) <-> Rlm1(c!1).Slt2(AssocRlm1!1'],
    'Tags': [
    1, 'ppi', 'Rlm1', 'Slt2', 'no contingencies']},

'Rlm1_ppi_Smp1': {
    'Rules':[
    'Rlm1(AssocSmp1) + Smp1(AssocRlm1) <-> Rlm1(AssocSmp1!1).Smp1(AssocRlm1!1)'],
    'Tags': [
    1, 'ppi', 'Rlm1', 'Smp1', 'no contingencies']},

'Rom2_[n]_ppi_Slg1_[CyT]': {
    'Rules':[
    'Rom2(n) + Slg1(CyT) <-> Rom2(n!1).Slg1(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Rom2', 'Slg1', 'no contingencies']},

'Rom2_ppi_Wsc2': {
    'Rules':[
    'Rom2(AssocWsc2) + Wsc2(AssocRom2) <-> Rom2(AssocWsc2!1).Wsc2(AssocRom2!1)'],
    'Tags': [
    1, 'ppi', 'Rom2', 'Wsc2', 'no contingencies']},

'Sdp1_ppi_Slt2': {
    'Rules':[
    'Sdp1(AssocSlt2) + Slt2(AssocSdp1) <-> Sdp1(AssocSlt2!1).Slt2(AssocSdp1!1)'],
    'Tags': [
    1, 'ppi', 'Sdp1', 'Slt2', 'no contingencies']},

'Sho1_[CyT]_ppi_Ste50_[m]': {
    'Rules':[
    'Sho1(CyT) + Ste50(m) <-> Sho1(CyT!1).Ste50(m!1)'],
    'Tags': [
    1, 'ppi', 'Sho1', 'Ste50', 'no contingencies']},

'Sln1_[BD:Sln1]_ppi_Sln1_[BD:Sln1]': {
    'Rules':[
    'Sln1(BDSln1) + Sln1(BDSln1) <-> Sln1(BDSln1!1).Sln1(BDSln1!1)'],
    'Tags': [
    1, 'ppi', 'Sln1', 'no contingencies', 'homodimer']},

'Sln1_[RR]_ppi_Ypd1': {
    'Rules':[
    'Sln1(RR) + Ypd1(AssocSln1) <-> Sln1(RR!1).Ypd1(AssocSln1!1)'],
    'Tags': [
    1, 'ppi', 'Sln1', 'Ypd1', 'no contingencies']},

'Ssk1_[BD:Ssk1]_ppi_Ssk1_[BD:Ssk1]': {
    'Rules':[
    'Ssk1(BDSsk1) + Ssk1(BDSsk1) <-> Ssk1(BDSsk1!1).Ssk1(BDSsk1!1)'],
    'Tags': [
    1, 'ppi', 'Ssk1', 'no contingencies']},

'Ssk1_[RR]_ppi_Ypd1': {
    'Rules':[
    'Ssk1(RR) + Ypd1(AssocSsk1) <-> Ssk1(RR!1).Ypd1(AssocSsk1!1)'],
    'Tags': [
    1, 'ppi', 'Ssk1', 'Ypd1', 'no contingencies']},

'Ste11_[SAM]_ppi_Ste50_[SAM]': {
    'Rules':[
    'Ste11(SAM) + Ste50(SAM) <-> Ste11(SAM!1).Ste50(SAM!1)'],
    'Tags': [
    1, 'ppi', 'Ste11', 'Ste50', 'no contingencies']},

'Ste2_[CyT]_ppi_Sst2_[n/DEP]': {
    'Rules':[
    'Ste2(CyT) + Sst2(nDEP) <-> Sst2(nDEP!1).Ste2(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Ste2', 'Sst2', 'no contingencies']},

'Ste2_[TMD]_ppi_Ste2_[TMD]': {
    'Rules':[
    'Ste2(TMD) + Ste2(TMD) <-> Ste2(TMD!1).Ste2(TMD!1)'],
    'Tags': [
    1, 'ppi', 'Ste2', 'no contingencies']},

'Ste3_[CyT]_ppi_Sst2_[n/DEP]': {
    'Rules':[
    'Ste3(CyT) + Sst2(nDEP) <-> Sst2(nDEP!1).Ste3(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Ste3', 'Sst2', 'no contingencies']},

'Ste4_ppi_Ste18': {
    'Rules':[
    'Ste4(AssocSte18) + Ste18(AssocSte4) <-> Ste18(AssocSte4!1).Ste4(AssocSte18!1)'],
    'Tags': [
    1, 'ppi', 'Ste4', 'Ste18', 'no contingencies']},

'Ste5_ppi_Ste20': {
    'Rules':[
    'Ste5(AssocSte20) + Ste20(AssocSte5) <-> Ste20(AssocSte5!1).Ste5(AssocSte20!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste20', 'no contingencies']},

'Ste5_[MEK]_ppi_Ste7': {
    'Rules':[
    'Ste5(MEK) + Ste7(AssocSte5) <-> Ste5(MEK!1).Ste7(AssocSte5!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste7', 'no contingencies']},

'Ste7_ppi_Ste11': {
    'Rules':[
    'Ste7(AssocSte11) + Ste11(AssocSte7) <-> Ste11(AssocSte7!1).Ste7(AssocSte11!1)'],
    'Tags': [
    1, 'ppi', 'Ste7', 'Ste11', 'no contingencies']},

# ppi contingencies

'Bck1_[n]_ppi_Bck1_[n]; k- Bck1_[(S939)]-{P}': {
    'Rules':[
    'Bck1(S939~U,n) + Bck1(S939~U,n) <-> Bck1(S939~U,n!1).Bck1(S939~U,n!1)',
    'Bck1(S939~P,n) + Bck1(S939~P,n) <-> Bck1(S939~P,n!1).Bck1(S939~P,n!1)'],
    'Tags': [
    1, 'ppi', 'Bck1', 'contingencies', 'K-']},

'Cdc24_ppi_Ste4; x Gpa1_[AssocSte4]--Ste4_[BDGpa1]; 0 Far1_[nRING-H2]--Ste4_[AssocFar1]': {
    'Rules':[
    'Cdc24(AssocSte4) + Ste4(AssocCdc24,BDGpa1) <-> Cdc24(AssocSte4!1).Ste4(AssocCdc24!1,BDGpa1)'],
    'Tags': [
    1, 'ppi', 'Cdc24', 'Ste4', 'contingencies', '0', 'x']},

'Cdc4_[WD40]_ppi_Tec1_[CPD]; ! Tec1_[(T276)]-{P}; ! Tec1_[(T273)]-{P}': {
    'Rules':[
    'Cdc4(WD40) + Tec1(T273~P,T276~P,CPD) <-> Cdc4(WD40!1).Tec1(T273~P,T276~P,CPD!1)'],
    'Tags': [
    1, 'ppi', 'Cdc4', 'Tec1', 'contingencies', '!']},

'Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2_[AssocSte20]': {
    'Rules':[
    'Cdc42(GnP~P,ED) + Ste20(BR,CRIB) <-> Cdc42(GnP~P,ED!1).Ste20(BR,CRIB!1)',
    'Cdc42(GnP~P,ED) + PIP2(AssocSte20!1).Ste20(BR!1,CRIB) <-> Cdc42(GnP~P,ED!1).PIP2(AssocSte20!2).Ste20(BR!2,CRIB!1)'],
    'Tags': [
    1, 'ppi', 'Cdc42', 'Ste20', 'contingencies', '!', 'K+']},

'Cdc42_ppi_Ste50_[RA]; 0 Cdc42_[GnP]-{P}': {
    'Rules':[
    'Cdc42(AssocSte50) + Ste50(RA) <-> Cdc42(AssocSte50!1).Ste50(RA!1)'],
    'Tags': [
    1, 'ppi', 'Cdc42', 'Ste50', 'contingencies', '0']},

'Dig1_ppi_Ste12_[c]; k- Dig1-{P}; k+ Dig2_[AssocSte12]--Ste12_[nDBD]; k+ Kss1_[AssocSte12]--Ste12_[AssocKss1]; k+ Fus3_[AssocSte12]--Ste12_[AssocFus3]': {
    'Rules':[
    'Dig1(bd~U,AssocSte12) + Dig2(AssocSte12!3).Fus3(AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3!1,AssocKss1!2,c,nDBD!3) <-> Dig1(bd~U,AssocSte12!1).Dig2(AssocSte12!4).Fus3(AssocSte12!2).Kss1(AssocSte12!3).Ste12(AssocFus3!2,AssocKss1!3,c!1,nDBD!4)',
    'Dig1(bd~P,AssocSte12) + Dig2(AssocSte12!3).Fus3(AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3!1,AssocKss1!2,c,nDBD!3) <-> Dig1(bd~P,AssocSte12!1).Dig2(AssocSte12!4).Fus3(AssocSte12!2).Kss1(AssocSte12!3).Ste12(AssocFus3!2,AssocKss1!3,c!1,nDBD!4)',
    'Dig1(bd~U,AssocSte12) + Fus3(AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3!1,AssocKss1!2,c,nDBD) <-> Dig1(bd~U,AssocSte12!1).Fus3(AssocSte12!2).Kss1(AssocSte12!3).Ste12(AssocFus3!2,AssocKss1!3,c!1,nDBD)',
    'Dig1(bd~P,AssocSte12) + Fus3(AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3!1,AssocKss1!2,c,nDBD) <-> Dig1(bd~P,AssocSte12!1).Fus3(AssocSte12!2).Kss1(AssocSte12!3).Ste12(AssocFus3!2,AssocKss1!3,c!1,nDBD)',
    'Dig1(bd~U,AssocSte12) + Dig2(AssocSte12!2).Fus3(AssocSte12!1).Ste12(AssocFus3!1,AssocKss1,c,nDBD!2) <-> Dig1(bd~U,AssocSte12!1).Dig2(AssocSte12!3).Fus3(AssocSte12!2).Ste12(AssocFus3!2,AssocKss1,c!1,nDBD!3)',
    'Dig1(bd~P,AssocSte12) + Dig2(AssocSte12!2).Fus3(AssocSte12!1).Ste12(AssocFus3!1,AssocKss1,c,nDBD!2) <-> Dig1(bd~P,AssocSte12!1).Dig2(AssocSte12!3).Fus3(AssocSte12!2).Ste12(AssocFus3!2,AssocKss1,c!1,nDBD!3)',
    'Dig1(bd~U,AssocSte12) + Fus3(AssocSte12!1).Ste12(AssocFus3!1,AssocKss1,c,nDBD) <-> Dig1(bd~U,AssocSte12!1).Fus3(AssocSte12!2).Ste12(AssocFus3!2,AssocKss1,c!1,nDBD)',
    'Dig1(bd~P,AssocSte12) + Fus3(AssocSte12!1).Ste12(AssocFus3!1,AssocKss1,c,nDBD) <-> Dig1(bd~P,AssocSte12!1).Fus3(AssocSte12!2).Ste12(AssocFus3!2,AssocKss1,c!1,nDBD)',
    'Dig1(bd~U,AssocSte12) + Dig2(AssocSte12!2).Kss1(AssocSte12!1).Ste12(AssocFus3,AssocKss1!1,c,nDBD!2) <-> Dig1(bd~U,AssocSte12!1).Dig2(AssocSte12!3).Kss1(AssocSte12!2).Ste12(AssocFus3,AssocKss1!2,c!1,nDBD!3)',
    'Dig1(bd~P,AssocSte12) + Dig2(AssocSte12!2).Kss1(AssocSte12!1).Ste12(AssocFus3,AssocKss1!1,c,nDBD!2) <-> Dig1(bd~P,AssocSte12!1).Dig2(AssocSte12!3).Kss1(AssocSte12!2).Ste12(AssocFus3,AssocKss1!2,c!1,nDBD!3)',
    'Dig1(bd~U,AssocSte12) + Kss1(AssocSte12!1).Ste12(AssocFus3,AssocKss1!1,c,nDBD) <-> Dig1(bd~U,AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3,AssocKss1!2,c!1,nDBD)',
    'Dig1(bd~P,AssocSte12) + Kss1(AssocSte12!1).Ste12(AssocFus3,AssocKss1!1,c,nDBD) <-> Dig1(bd~P,AssocSte12!1).Kss1(AssocSte12!2).Ste12(AssocFus3,AssocKss1!2,c!1,nDBD)',
    'Dig1(bd~U,AssocSte12) + Dig2(AssocSte12!1).Ste12(AssocFus3,AssocKss1,c,nDBD!1) <-> Dig1(bd~U,AssocSte12!1).Dig2(AssocSte12!2).Ste12(AssocFus3,AssocKss1,c!1,nDBD!2)',
    'Dig1(bd~P,AssocSte12) + Dig2(AssocSte12!1).Ste12(AssocFus3,AssocKss1,c,nDBD!1) <-> Dig1(bd~P,AssocSte12!1).Dig2(AssocSte12!2).Ste12(AssocFus3,AssocKss1,c!1,nDBD!2)',
    'Dig1(bd~U,AssocSte12) + Ste12(AssocFus3,AssocKss1,c,nDBD) <-> Dig1(bd~U,AssocSte12!1).Ste12(AssocFus3,AssocKss1,c!1,nDBD)',
    'Dig1(bd~P,AssocSte12) + Ste12(AssocFus3,AssocKss1,c,nDBD) <-> Dig1(bd~P,AssocSte12!1).Ste12(AssocFus3,AssocKss1,c!1,nDBD)'],
    'Tags': [
    1, 'ppi', 'Dig1', 'Ste12', 'contingencies', 'K+']},

'Dig2_ppi_Ste12_[n/DBD]; k- Dig2-{P}; k+ Dig1_[AssocSte12]--Ste12_[c]; x Ste12_[nDB]--Tec1_[AssocSte12]': {
    'Rules':[
    'Dig2(bd~U,AssocSte12) + Dig1(AssocSte12!1).Ste12(c!1,nDB,nDBD) <-> Dig1(AssocSte12!2).Dig2(bd~U,AssocSte12!1).Ste12(c!2,nDB,nDBD!1)',
    'Dig2(bd~P,AssocSte12) + Dig1(AssocSte12!1).Ste12(c!1,nDB,nDBD) <-> Dig1(AssocSte12!2).Dig2(bd~P,AssocSte12!1).Ste12(c!2,nDB,nDBD!1)',
    'Dig2(bd~U,AssocSte12) + Ste12(c,nDB,nDBD) <-> Dig2(bd~U,AssocSte12!1).Ste12(c,nDB,nDBD!1)',
    'Dig2(bd~P,AssocSte12) + Ste12(c,nDB,nDBD) <-> Dig2(bd~P,AssocSte12!1).Ste12(c,nDB,nDBD!1)'],
    'Tags': [
    1, 'ppi', 'Dig2', 'Ste12', 'contingencies', 'K+', 'x']},

'Far1_[n/RING-H2]_ppi_Ste4; x Gpa1_[AssocSte4]--Ste4_[BDGpa1]; 0 Cdc24_[AssocSte4]--Ste4_[AssocCdc24]': {
    'Rules':[
    'Far1(nRINGH2) + Ste4(AssocFar1,BDGpa1) <-> Far1(nRINGH2!1).Ste4(AssocFar1!1,BDGpa1)'],
    'Tags': [
    1, 'ppi', 'Far1', 'Ste4', 'contingencies', '0', 'x']},

'Fus3_[n]_ppi_Gpa1_[n]; k+ Gpa1_[GnP]-{P}; k+ Fus3_[(T180)]-{P}; k+ Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(T180~P,Y182~P,n) + Gpa1(GnP~P,n) <-> Fus3(T180~P,Y182~P,n!1).Gpa1(GnP~P,n!1)',
    'Fus3(T180~P,Y182~P,n) + Gpa1(GnP~U,n) <-> Fus3(T180~P,Y182~P,n!1).Gpa1(GnP~U,n!1)',
    'Fus3(T180~U,Y182~P,n) + Gpa1(GnP~P,n) <-> Fus3(T180~U,Y182~P,n!1).Gpa1(GnP~P,n!1)',
    'Fus3(T180~U,Y182~P,n) + Gpa1(GnP~U,n) <-> Fus3(T180~U,Y182~P,n!1).Gpa1(GnP~U,n!1)',
    'Fus3(T180~P,Y182~U,n) + Gpa1(GnP~P,n) <-> Fus3(T180~P,Y182~U,n!1).Gpa1(GnP~P,n!1)',
    'Fus3(T180~P,Y182~U,n) + Gpa1(GnP~U,n) <-> Fus3(T180~P,Y182~U,n!1).Gpa1(GnP~U,n!1)',
    'Fus3(T180~U,Y182~U,n) + Gpa1(GnP~P,n) <-> Fus3(T180~U,Y182~U,n!1).Gpa1(GnP~P,n!1)',
    'Fus3(T180~U,Y182~U,n) + Gpa1(GnP~U,n) <-> Fus3(T180~U,Y182~U,n!1).Gpa1(GnP~U,n!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Gpa1', 'contingencies', 'K+']},

'Fus3_[CD]_ppi_Ptp3_[CH2]; 0 Fus3_[(Y182)]-{P}': {
    'Rules':[
    'Fus3(CD) + Ptp3(CH2) <-> Fus3(CD!1).Ptp3(CH2!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ptp3', 'contingencies', '0']},

'Fus3_ppi_Ste12; k- Fus3_[(T180)]-{P}; k- Fus3_[(Y182)]-{P}; k+ Dig1_[AssocSte12]--Ste12_[c]': {
    'Rules':[
    'Fus3(T180~U,Y182~U,AssocSte12) + Dig1(AssocSte12!1).Ste12(AssocFus3,c!1) <-> Dig1(AssocSte12!2).Fus3(T180~U,Y182~U,AssocSte12!1).Ste12(AssocFus3!1,c!2)',
    'Fus3(T180~P,Y182~U,AssocSte12) + Dig1(AssocSte12!1).Ste12(AssocFus3,c!1) <-> Dig1(AssocSte12!2).Fus3(T180~P,Y182~U,AssocSte12!1).Ste12(AssocFus3!1,c!2)',
    'Fus3(T180~U,Y182~P,AssocSte12) + Dig1(AssocSte12!1).Ste12(AssocFus3,c!1) <-> Dig1(AssocSte12!2).Fus3(T180~U,Y182~P,AssocSte12!1).Ste12(AssocFus3!1,c!2)',
    'Fus3(T180~P,Y182~P,AssocSte12) + Dig1(AssocSte12!1).Ste12(AssocFus3,c!1) <-> Dig1(AssocSte12!2).Fus3(T180~P,Y182~P,AssocSte12!1).Ste12(AssocFus3!1,c!2)',
    'Fus3(T180~U,Y182~U,AssocSte12) + Ste12(AssocFus3,c) <-> Fus3(T180~U,Y182~U,AssocSte12!1).Ste12(AssocFus3!1,c)',
    'Fus3(T180~P,Y182~U,AssocSte12) + Ste12(AssocFus3,c) <-> Fus3(T180~P,Y182~U,AssocSte12!1).Ste12(AssocFus3!1,c)',
    'Fus3(T180~U,Y182~P,AssocSte12) + Ste12(AssocFus3,c) <-> Fus3(T180~U,Y182~P,AssocSte12!1).Ste12(AssocFus3!1,c)',
    'Fus3(T180~P,Y182~P,AssocSte12) + Ste12(AssocFus3,c) <-> Fus3(T180~P,Y182~P,AssocSte12!1).Ste12(AssocFus3!1,c)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ptp3', 'contingencies', '0']},

'Fus3_ppi_Ste5_[Unlock]; ! Ste5_[MEK]--Ste7_[AssocSte5]; ! Fus3_[CD]--Ste7_[BDMAPK]': {
    'Rules':[
    'Fus3(AssocSte5,CD!1).Ste7(BDMAPK!1) + Ste5(MEK!1,Unlock).Ste7(AssocSte5!1) <-> Fus3(AssocSte5!3,CD!2).Ste5(MEK!1,Unlock!3).Ste7(BDMAPK!2).Ste7(AssocSte5!1)'],
    'Tags': [
    1, 'ppi', 'Fus3', 'Ptp3', 'contingencies', '!', 'difficault']},

'Gpa1_ppi_Ste4_[BD:Gpa1]; x Gpa1_[GnP]-{P}': {
    'Rules':[
    'Gpa1(GnP~U,AssocSte4) + Ste4(BDGpa1) <-> Gpa1(GnP~U,AssocSte4!1).Ste4(BDGpa1!1)'],
    'Tags': [
    1, 'ppi', 'Gpa1', 'Ste4', 'contingencies', 'x']},

'Hkr1_[TMD]_ppi_Sho1_[TMD]; k- [Turgor]': {
    'Rules':[
    'Hkr1(TMD) + Sho1(TMD) <-> Hkr1(TMD!1).Sho1(TMD!1)'],
    'Tags': [
    1, 'ppi', 'Hkr1', 'Sho1', 'contingencies', 'K-', 'input']},

'Hog1_[n]_ppi_Hot1_[m]; ! Hog1_[(T174)]-{P}; ! Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(T174~P,Y176~P,n) + Hot1(m) <-> Hog1(T174~P,Y176~P,n!1).Hot1(m!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Hot1', 'contingencies', '!']},

'Hog1_[PBD-2]_ppi_Pbs2_[HBD-1]; k+ Hog1_[CD]--Pbs2_[HBD-1]': {
    'Rules':[
    'Hog1(PBD2) + Pbs2(HBD1) <-> Hog1(PBD2!1).Pbs2(HBD1!1)',
    'Hog1(CD,PBD2) + Pbs2(HBD1) <-> Hog1(CD,PBD2!1).Pbs2(HBD1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Pbs2', 'contingencies', 'K+', 'difficault']},

'Hog1_[CD]_ppi_Ptp2; k+ Hog1_[(Y176)]-{P}': {
    'Rules':[
    'Hog1(Y176~P,CD) + Ptp2(AssocHog1) <-> Hog1(Y176~P,CD!1).Ptp2(AssocHog1!1)',
    'Hog1(Y176~U,CD) + Ptp2(AssocHog1) <-> Hog1(Y176~U,CD!1).Ptp2(AssocHog1!1)'],
    'Tags': [
    1, 'ppi', 'Hog1', 'Ptp2', 'contingencies', 'K+']},

'Kss1_ppi_Ste12; k- Kss1_[(T183)]-{P}; k- Kss1_[(Y185)]-{P}': {
    'Rules':[
    'Kss1(T183~U,Y185~U,AssocSte12) + Ste12(AssocKss1) <-> Kss1(T183~U,Y185~U,AssocSte12!1).Ste12(AssocKss1!1)',
    'Kss1(T183~P,Y185~U,AssocSte12) + Ste12(AssocKss1) <-> Kss1(T183~P,Y185~U,AssocSte12!1).Ste12(AssocKss1!1)',
    'Kss1(T183~U,Y185~P,AssocSte12) + Ste12(AssocKss1) <-> Kss1(T183~U,Y185~P,AssocSte12!1).Ste12(AssocKss1!1)',
    'Kss1(T183~P,Y185~P,AssocSte12) + Ste12(AssocKss1) <-> Kss1(T183~P,Y185~P,AssocSte12!1).Ste12(AssocKss1!1)'],
    'Tags': [
    1, 'ppi', 'Kss1', 'Ste12', 'contingencies', 'K-']},

'MFa_ppi_Ste3_[Receptor]; ! MFa': {
    # TODO: contingencies with components are ignored now
    'Rules':[
    'MFa(AssocSte3) + Ste3(Receptor) <-> MFa(AssocSte3!1).Ste3(Receptor!1)'],
    'Tags': [
    1, 'ppi', 'MFa', 'Ste3', 'contingencies', '!', 'todo']},

'MFalpha_ppi_Ste2_[Receptor]; ! MFalpha': {
    # TODO: contingencies with components are ignored now
    'Rules':[
    'MFalpha(AssocSte2) + Ste2(Receptor) <-> MFalpha(AssocSte2!1).Ste2(Receptor!1)'],
    'Tags': [
    1, 'ppi', 'MFalpha', 'Ste2', 'contingencies', '!', 'todo']},

'Msb2_[TMD]_ppi_Sho1_[TMD]; k- [Turgor]': {
    'Rules':[
    'Msb2(TMD) + Sho1(TMD) <-> Msb2(TMD!1).Sho1(TMD!1)'],
    'Tags': [
    1, 'ppi', 'Msb2', 'Sho1', 'contingencies', 'K-', 'input']},

'Msb2_[CyT]_ppi_Sho1_[CyT]; k+ Msb2_[HMH/CD]-{Truncated}; k- [Turgor]': {
    'Rules':[
    'Msb2(HMHCD~Truncated,CyT) + Sho1(CyT) <-> Msb2(HMHCD~Truncated,CyT!1).Sho1(CyT!1)',
    'Msb2(HMHCD~U,CyT) + Sho1(CyT) <-> Msb2(HMHCD~U,CyT!1).Sho1(CyT!1)'],
    'Tags': [
    1, 'ppi', 'Msb2', 'Sho1', 'contingencies', 'K-', 'K+', 'input']},

'Pbs2_[RSD2/PR]_ppi_Sho1_[CyT/SH3]; k+ Hkr1_[TMD]--Sho1_[TMD]; k+ Msb2_[TMD]--Sho1_[TMD]; k+ Msb2_[CyT]--Sho1_[CyT]': {
    'Rules':[
    'Pbs2(RSD2PR) + Hkr1(TMD!2).Msb2(CyT!1).Sho1(CyT!1,CyTSH3,TMD!2) <-> Hkr1(TMD!3).Msb2(CyT!2).Pbs2(RSD2PR!1).Sho1(CyT!2,CyTSH3!1,TMD!3)',
'Pbs2(RSD2PR) + Msb2(CyT!1,TMD!2).Sho1(CyTSH3,TMD!2).Sho1(CyT!1) <-> Msb2(CyT!1,TMD!3).Pbs2(RSD2PR!2).Sho1(CyTSH3!2,TMD!3).Sho1(CyT!1)',
'Pbs2(RSD2PR) + Hkr1(TMD!2).Msb2(CyT!1).Sho1(CyT!1,CyTSH3,TMD!2) <-> Hkr1(TMD!3).Msb2(CyT!2).Pbs2(RSD2PR!1).Sho1(CyT!2,CyTSH3!1,TMD!3)',
'Pbs2(RSD2PR) + Msb2(CyT!1).Sho1(CyT!1,CyTSH3,TMD) <-> Msb2(CyT!2).Pbs2(RSD2PR!1).Sho1(CyT!2,CyTSH3!1,TMD)',
'Pbs2(RSD2PR) + Hkr1(TMD!1).Sho1(CyT,CyTSH3,TMD!1) <-> Hkr1(TMD!2).Pbs2(RSD2PR!1).Sho1(CyT,CyTSH3!1,TMD!2)',
'Pbs2(RSD2PR) + Msb2(CyT,TMD!1).Sho1(CyT,CyTSH3,TMD!1) <-> Msb2(CyT,TMD!2).Pbs2(RSD2PR!1).Sho1(CyT,CyTSH3!1,TMD!2)',
'Pbs2(RSD2PR) + Hkr1(TMD!1).Sho1(CyT,CyTSH3,TMD!1) <-> Hkr1(TMD!2).Pbs2(RSD2PR!1).Sho1(CyT,CyTSH3!1,TMD!2)',
'Pbs2(RSD2PR) + Sho1(CyT,CyTSH3,TMD) <-> Pbs2(RSD2PR!1).Sho1(CyT,CyTSH3!1,TMD)'],
    'Tags': [
    1, 'ppi', 'Pbs2', 'Sho1', 'contingencies', 'K+', 'complicated', 'ask MK']},


'Pkc1_[C1]_ppi_Rho1_[ED]; ! Rho1_[GnP]-{P}': {
    'Rules':[
    'Pkc1(C1) + Rho1(GnP~P,ED) <-> Pkc1(C1!1).Rho1(GnP~P,ED!1)'],
    'Tags': [
    1, 'ppi', 'Pkc1', 'Rho1', 'contingencies', '!']},


'Sho1_[CyT]_ppi_Ste11_[BD:Sho1]': {
    'Rules':['Sho1(CyT) + Ste11(BDSho1) <-> Sho1(CyT!1).Ste11(BDSho1!1)'],
    'Tags': [
    1, 'ppi', 'Sho1', 'Ste11', 'contingencies', 'x', 'K+', 'bool', 'complicated', 'ask MK']},    


'''Sho1_[CyT]_ppi_Ste11_[BD:Sho1]; x Ste5_[MEKK]--Ste11_[AssocSte5]; k+ Hkr1_[TMD]--Sho1_[TMD]; k+ Msb2_[TMD]--Sho1_[TMD]; k+ Msb2_[CyT]--Sho1_[CyT]; ! <Ste11^{M/50}>
<Ste11^{M/50}>; and Opy2_[BDSte50]--Ste50_[RA]
<Ste11^{M/50}>; and Ste11_[SAM]--Ste50_[SAM]''': {
    'Rules':[
    'Hkr1(TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Msb2(TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Msb2(TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Hkr1(TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Sho1(CyT,TMD) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Opy2(BDSte50!1).Sho1(CyT!3,TMD).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Hkr1(TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Msb2(CyT,TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Msb2(CyT,TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Hkr1(TMD!1).Sho1(CyT,TMD!1) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy2(BDSte50!1).Sho1(CyT!3,TMD!4).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)',
    'Sho1(CyT,TMD) + Opy2(BDSte50!1).Ste11(AssocSte5,BDSho1,SAM!2).Ste50(RA!1,SAM!2) <-> Opy2(BDSte50!1).Sho1(CyT!3,TMD).Ste11(AssocSte5,BDSho1!3,SAM!2).Ste50(RA!1,SAM!2)'],
    'Tags': [
    1, 'ppi', 'Sho1', 'Ste11', 'contingencies', 'x', 'K+', 'bool', 'complicated', 'ask MK']},    

'Sko1_[n]_ppi_Tup1; k- Sko1_[n(S108)]-{P}; k- Sko1_[n(S113)]-{P}; k- Sko1_[n(S126)]-{P}': {
    'Rules':[
    'Sko1(nS108~U,nS113~U,nS126~U,n) + Tup1(AssocSko1) <-> Sko1(nS108~U,nS113~U,nS126~U,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~P,nS113~U,nS126~U,n) + Tup1(AssocSko1) <-> Sko1(nS108~P,nS113~U,nS126~U,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~U,nS113~P,nS126~U,n) + Tup1(AssocSko1) <-> Sko1(nS108~U,nS113~P,nS126~U,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~P,nS113~P,nS126~U,n) + Tup1(AssocSko1) <-> Sko1(nS108~P,nS113~P,nS126~U,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~U,nS113~U,nS126~P,n) + Tup1(AssocSko1) <-> Sko1(nS108~U,nS113~U,nS126~P,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~P,nS113~U,nS126~P,n) + Tup1(AssocSko1) <-> Sko1(nS108~P,nS113~U,nS126~P,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~U,nS113~P,nS126~P,n) + Tup1(AssocSko1) <-> Sko1(nS108~U,nS113~P,nS126~P,n!1).Tup1(AssocSko1!1)',
    'Sko1(nS108~P,nS113~P,nS126~P,n) + Tup1(AssocSko1) <-> Sko1(nS108~P,nS113~P,nS126~P,n!1).Tup1(AssocSko1!1)'],
    'Tags': [
    1, 'ppi', 'Slt2', 'Swi4', 'contingencies', '!', '0']},

'Slt2_[DB]_ppi_Swi4_[c]; ! Slt2_[(T190)]-{P}; ! Slt2_[(Y192)]-{P}; 0 Swi4_[c]--Swi6_[c]': {
    'Rules':[
    'Slt2(T190~P,Y192~P,DB) + Swi4(c) <-> Slt2(T190~P,Y192~P,DB!1).Swi4(c!1)'],
    'Tags': [
    1, 'ppi', 'Slt2', 'Swi4', 'contingencies', '!', '0']},

'Ssk1_[RR]_ppi_Ssk2_[BD:Ssk1]; x Ssk1_[RR(D544)]-{P}': {
    'Rules':[
    'Ssk1(RRD544~U,RR) + Ssk2(BDSsk1) <-> Ssk1(RRD544~U,RR!1).Ssk2(BDSsk1!1)'],
    'Tags': [
    1, 'ppi', 'Ssk1', 'Ssk2', 'contingencies', 'x']},

'Ssk1_ppi_Ssk22; x Ssk1_[RR(D544)]-{P}': {
    'Rules':[
    'Ssk1(RRD544~U,AssocSsk22) + Ssk22(AssocSsk1) <-> Ssk1(RRD544~U,AssocSsk22!1).Ssk22(AssocSsk1!1)'],
    'Tags': [
    1, 'ppi', 'Ssk1', 'Ssk22', 'contingencies', 'x']},

'Ste11_[CBD]_ppi_Ste11_[KD]; k- Ste11_[CBD(S302)]-{P}; k- Ste11_[CBD(S306)]-{P}; k- Ste11_[CBD(T307)]-{P}': {
    'Rules':[
    'Ste11(CBDS302~U,CBDS306~U,CBDT307~U,CBD) + Ste11(CBDS302~U,CBDS306~U,CBDT307~U,KD) <-> Ste11(CBDS302~U,CBDS306~U,CBDT307~U,CBD!1).Ste11(CBDS302~U,CBDS306~U,CBDT307~U,KD!1)',
    'Ste11(CBDS302~P,CBDS306~U,CBDT307~U,CBD) + Ste11(CBDS302~P,CBDS306~U,CBDT307~U,KD) <-> Ste11(CBDS302~P,CBDS306~U,CBDT307~U,CBD!1).Ste11(CBDS302~P,CBDS306~U,CBDT307~U,KD!1)',
    'Ste11(CBDS302~U,CBDS306~P,CBDT307~U,CBD) + Ste11(CBDS302~U,CBDS306~P,CBDT307~U,KD) <-> Ste11(CBDS302~U,CBDS306~P,CBDT307~U,CBD!1).Ste11(CBDS302~U,CBDS306~P,CBDT307~U,KD!1)',
    'Ste11(CBDS302~P,CBDS306~P,CBDT307~U,CBD) + Ste11(CBDS302~P,CBDS306~P,CBDT307~U,KD) <-> Ste11(CBDS302~P,CBDS306~P,CBDT307~U,CBD!1).Ste11(CBDS302~P,CBDS306~P,CBDT307~U,KD!1)',
    'Ste11(CBDS302~U,CBDS306~U,CBDT307~P,CBD) + Ste11(CBDS302~U,CBDS306~U,CBDT307~P,KD) <-> Ste11(CBDS302~U,CBDS306~U,CBDT307~P,CBD!1).Ste11(CBDS302~U,CBDS306~U,CBDT307~P,KD!1)',
    'Ste11(CBDS302~P,CBDS306~U,CBDT307~P,CBD) + Ste11(CBDS302~P,CBDS306~U,CBDT307~P,KD) <-> Ste11(CBDS302~P,CBDS306~U,CBDT307~P,CBD!1).Ste11(CBDS302~P,CBDS306~U,CBDT307~P,KD!1)',
    'Ste11(CBDS302~U,CBDS306~P,CBDT307~P,CBD) + Ste11(CBDS302~U,CBDS306~P,CBDT307~P,KD) <-> Ste11(CBDS302~U,CBDS306~P,CBDT307~P,CBD!1).Ste11(CBDS302~U,CBDS306~P,CBDT307~P,KD!1)',
    'Ste11(CBDS302~P,CBDS306~P,CBDT307~P,CBD) + Ste11(CBDS302~P,CBDS306~P,CBDT307~P,KD) <-> Ste11(CBDS302~P,CBDS306~P,CBDT307~P,CBD!1).Ste11(CBDS302~P,CBDS306~P,CBDT307~P,KD!1)'],
    'Tags': [
    1, 'ppi', 'Ste11', 'contingencies', 'K-']},

'Ste12_[n/DB]_ppi_Tec1; x Dig2_[AssocSte12]--Ste12_[nDBD]': {
    'Rules':[
    'Ste12(nDB,nDBD) + Tec1(AssocSte12) <-> Ste12(nDB!1,nDBD).Tec1(AssocSte12!1)'],
    'Tags': [
    1, 'ppi', 'Ste12', 'Tec1', 'contingencies', 'x']},

'Ste20_[KD]_ppi_Ste20_[CRIB]; x Cdc42_[ED]--Ste20_[CRIB]': {
    'Rules':[
    'Ste20(CRIB,KD) + Ste20(CRIB) <-> Ste20(CRIB,KD!1).Ste20(CRIB!1)'],
    'Tags': [
    1, 'ppi', 'Ste20', 'contingencies', 'x', 'difficault']},

'Ste4_ppi_Ste20_[c]; x Gpa1_[AssocSte4]--Ste4_[BDGpa1]': {
    'Rules':[
    'Ste4(AssocSte20,BDGpa1) + Ste20(c) <-> Ste20(c!1).Ste4(AssocSte20!1,BDGpa1)'],
    'Tags': [
    1, 'ppi', 'Ste4', 'Ste20', 'contingencies', 'x']},

'Ste4_[BD:Ste5]_ppi_Ste5_[n/RING-H2]; x Gpa1_[AssocSte4]--Ste4_[BDGpa1]': {
    'Rules':[
    'Ste4(BDGpa1,BDSte5) + Ste5(nRINGH2) <-> Ste4(BDGpa1,BDSte5!1).Ste5(nRINGH2!1)'],
    'Tags': [
    1, 'ppi', 'Ste4', 'Ste5', 'contingencies', 'x']},

'Ste5_[MEKK]_ppi_Ste11; x Sho1_[CyT]--Ste11_[BDSho1]': {
    'Rules':[
    'Ste5(MEKK) + Ste11(AssocSte5,BDSho1) <-> Ste11(AssocSte5!1,BDSho1).Ste5(MEKK!1)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste11', 'contingencies', 'x']},

'Ste5_[BD:Ste5]_ppi_Ste5_[BD:Ste5]; ! Ste4_[BDSte5]--Ste5_[nRING-H2]': {
    'Rules':[
    'Ste4(BDSte5!1).Ste5(BDSte5,nRINGH2!1) + Ste4(BDSte5!1).Ste5(BDSte5,nRINGH2!1) <-> Ste4(BDSte5!3).Ste4(BDSte5!2).Ste5(BDSte5!1,nRINGH2!3).Ste5(BDSte5!1,nRINGH2!2)'],
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste11', 'contingencies', '!', 'difficault']},

'Swi4_[c]_ppi_Swi6_[c]; 0 Slt2_[DB]--Swi4_[c]': {
    'Rules':[
    'Swi4(c) + Swi6(c) <-> Swi4(c!1).Swi6(c!1)'],
    'Tags': [
    1, 'ppi', 'Swi4', 'Swi6', 'contingencies', '0']},

}

DATA = [MAPK_PPI_DATA]