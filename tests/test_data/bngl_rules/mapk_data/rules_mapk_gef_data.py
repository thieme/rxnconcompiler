#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all GEF reactions from MAPK network.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

MAPK_GEF_DATA = {
# COVALENT MODIFICATION
# gef no contingencies
'Rom1_[DH]_GEF_Rho1_[GnP]': {
    'Rules':[
    'Rom1 + Rho1(GnP~U) -> Rom1 + Rho1(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Rom1', 'Rho1', 'no contingencies']},

'Tus1_[DH]_GEF_Rho1_[GnP]': {
    'Rules':[
    'Tus1 + Rho1(GnP~U) -> Tus1 + Rho1(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Tus1', 'Rho1', 'no contingencies']},

# gef contingencies
'''Cdc24_[GEF]_GEF_Cdc42_[GnP]; k+ <Cdc24^{M}>
<Cdc24^{M}>; or <Cdc24^{M/4}>
<Cdc24^{M/4}>; and Cdc24_[AssocSte4]--Ste4_[AssocCdc24]
<Cdc24^{M/4}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
<Cdc24^{M}>; or <Cdc24^{M/F}>
<Cdc24^{M/F}>; and Cdc24_[AssocFar1]--Far1_[c]
<Cdc24^{M/F}>; and <Far1^{M}>
<Far1^{M}>; and Far1_[nRING-H2]--Ste4_[AssocFar1]
<Far1^{M}>; and Ste4_[AssocSte18]--Ste18_[AssocSte4]
<Cdc24^{M}>; or [START]''': {
    'Rules':[
    # Cdc24,       Ste18, Ste4 
    'Cdc24(AssocSte4!1).Ste18(AssocSte4!2).Ste4(AssocCdc24!1,AssocSte18!2) + Cdc42(GnP~U) -> Cdc24(AssocSte4!1).Ste18(AssocSte4!2).Ste4(AssocCdc24!1,AssocSte18!2) + Cdc42(GnP~P)',
    # Cdc24, Far1, Ste18, Ste4
    'Cdc24(AssocFar1!4,AssocSte4!3).Far1(c!4,nRINGH2!1).Ste18(AssocSte4!2).Ste4(AssocCdc24!3,AssocSte18).Ste4(AssocFar1!1,AssocSte18!2) + Cdc42(GnP~U) -> Cdc24(AssocFar1!4,AssocSte4!3).Far1(c!4,nRINGH2!1).Ste18(AssocSte4!2).Ste4(AssocCdc24!3,AssocSte18).Ste4(AssocFar1!1,AssocSte18!2) + Cdc42(GnP~P)',
    # Cdc24, Far1, Ste18, Ste4
    'Cdc24(AssocFar1!3,AssocSte4).Far1(c!3,nRINGH2!1).Ste18(AssocSte4!2).Ste4(AssocFar1!1,AssocSte18!2) + Cdc42(GnP~U) -> Cdc24(AssocFar1!3,AssocSte4).Far1(c!3,nRINGH2!1).Ste18(AssocSte4!2).Ste4(AssocFar1!1,AssocSte18!2) + Cdc42(GnP~P)',
    # Cdc24, Far1,        Ste4, Ste4
    'Cdc24(AssocFar1!3,AssocSte4!2).Far1(c!3,nRINGH2!1).Ste4(AssocCdc24!2,AssocSte18).Ste4(AssocFar1!1,AssocSte18) + Cdc42(GnP~U) -> Cdc24(AssocFar1!3,AssocSte4!2).Far1(c!3,nRINGH2!1).Ste4(AssocCdc24!2,AssocSte18).Ste4(AssocFar1!1,AssocSte18) + Cdc42(GnP~P)',
    # Cdc24, Far1,        Ste4
    'Cdc24(AssocFar1!2,AssocSte4!1).Far1(c!2,nRINGH2).Ste4(AssocCdc24!1,AssocSte18) + Cdc42(GnP~U) -> Cdc24(AssocFar1!2,AssocSte4!1).Far1(c!2,nRINGH2).Ste4(AssocCdc24!1,AssocSte18) + Cdc42(GnP~P)',
    # Cdc24,              Ste4
    'Cdc24(AssocFar1,AssocSte4!1).Ste4(AssocCdc24!1,AssocSte18) + Cdc42(GnP~U) -> Cdc24(AssocFar1,AssocSte4!1).Ste4(AssocCdc24!1,AssocSte18) + Cdc42(GnP~P)',
    # Cdc24, Far1,              Ste4
    'Cdc24(AssocFar1!2,AssocSte4).Far1(c!2,nRINGH2!1).Ste4(AssocFar1!1,AssocSte18) + Cdc42(GnP~U) -> Cdc24(AssocFar1!2,AssocSte4).Far1(c!2,nRINGH2!1).Ste4(AssocFar1!1,AssocSte18) + Cdc42(GnP~P)',
    # Cdc24, Far1
    'Cdc24(AssocFar1!1,AssocSte4).Far1(c!1,nRINGH2) + Cdc42(GnP~U) -> Cdc24(AssocFar1!1,AssocSte4).Far1(c!1,nRINGH2) + Cdc42(GnP~P)',
    # Cdc24, 
    'Cdc24(AssocFar1,AssocSte4) + Cdc42(GnP~U) -> Cdc24(AssocFar1,AssocSte4) + Cdc42(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Cdc24', 'Cdc42', 'contingencies', 'K+', 'bool', 'input']},

'Rom2_[DH]_GEF_Rho1_[GnP]; k+ Rom2_[n]--Slg1_[CyT]; k+ Rom2_[AssocWsc2]--Wsc2_[AssocRom2]; k+ Mtl1_[AssocRom2]--Rom2_[AssocMtl1]; k+ Mid2_[CyT]--Rom2_[AssocMid2]': {
    'Rules':[
    'Mid2(CyT!3).Mtl1(AssocRom2!4).Rom2(AssocMid2!3,AssocMtl1!4,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mid2(CyT!3).Mtl1(AssocRom2!4).Rom2(AssocMid2!3,AssocMtl1!4,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mid2(CyT!2).Mtl1(AssocRom2!3).Rom2(AssocMid2!2,AssocMtl1!3,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mid2(CyT!2).Mtl1(AssocRom2!3).Rom2(AssocMid2!2,AssocMtl1!3,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mid2(CyT!2).Mtl1(AssocRom2!3).Rom2(AssocMid2!2,AssocMtl1!3,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~U) -> Mid2(CyT!2).Mtl1(AssocRom2!3).Rom2(AssocMid2!2,AssocMtl1!3,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~P)',
    'Mid2(CyT!1).Mtl1(AssocRom2!2).Rom2(AssocMid2!1,AssocMtl1!2,AssocWsc2,n) + Rho1(GnP~U) -> Mid2(CyT!1).Mtl1(AssocRom2!2).Rom2(AssocMid2!1,AssocMtl1!2,AssocWsc2,n) + Rho1(GnP~P)',
    'Mid2(CyT!3).Rom2(AssocMid2!3,AssocMtl1,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mid2(CyT!3).Rom2(AssocMid2!3,AssocMtl1,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mid2(CyT!2).Rom2(AssocMid2!2,AssocMtl1,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mid2(CyT!2).Rom2(AssocMid2!2,AssocMtl1,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mid2(CyT!2).Rom2(AssocMid2!2,AssocMtl1,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~U) -> Mid2(CyT!2).Rom2(AssocMid2!2,AssocMtl1,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~P)',
    'Mid2(CyT!1).Rom2(AssocMid2!1,AssocMtl1,AssocWsc2,n) + Rho1(GnP~U) -> Mid2(CyT!1).Rom2(AssocMid2!1,AssocMtl1,AssocWsc2,n) + Rho1(GnP~P)',
    'Mtl1(AssocRom2!3).Rom2(AssocMid2,AssocMtl1!3,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mtl1(AssocRom2!3).Rom2(AssocMid2,AssocMtl1!3,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mtl1(AssocRom2!2).Rom2(AssocMid2,AssocMtl1!2,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Mtl1(AssocRom2!2).Rom2(AssocMid2,AssocMtl1!2,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Mtl1(AssocRom2!2).Rom2(AssocMid2,AssocMtl1!2,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~U) -> Mtl1(AssocRom2!2).Rom2(AssocMid2,AssocMtl1!2,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~P)',
    'Mtl1(AssocRom2!1).Rom2(AssocMid2,AssocMtl1!1,AssocWsc2,n) + Rho1(GnP~U) -> Mtl1(AssocRom2!1).Rom2(AssocMid2,AssocMtl1!1,AssocWsc2,n) + Rho1(GnP~P)',
    'Rom2(AssocMid2,AssocMtl1,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Rom2(AssocMid2,AssocMtl1,AssocWsc2!1,n!2).Slg1(CyT!2).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Rom2(AssocMid2,AssocMtl1,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~U) -> Rom2(AssocMid2,AssocMtl1,AssocWsc2!1,n).Wsc2(AssocRom2!1) + Rho1(GnP~P)',
    'Rom2(AssocMid2,AssocMtl1,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~U) -> Rom2(AssocMid2,AssocMtl1,AssocWsc2,n!1).Slg1(CyT!1) + Rho1(GnP~P)',
    'Rom2(AssocMid2,AssocMtl1,AssocWsc2,n) + Rho1(GnP~U) -> Rom2(AssocMid2,AssocMtl1,AssocWsc2,n) + Rho1(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Rom2', 'Rho1', 'contingencies', 'K+']},

'Ste2_GEF_Gpa1_[GnP]; k+ MFalpha_[AssocSte2]--Ste2_[Receptor]': {
    'Rules':[
    'MFalpha(AssocSte2!1).Ste2(Receptor!1) + Gpa1(GnP~U) -> MFalpha(AssocSte2!1).Ste2(Receptor!1) + Gpa1(GnP~P)',
    'Ste2(Receptor) + Gpa1(GnP~U) -> Ste2(Receptor) + Gpa1(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Ste2', 'Gpa1', 'contingencies', 'K+']},

'Ste3_GEF_Gpa1_[GnP]; k+ MFa_[AssocSte3]--Ste3_[Receptor]': {
    'Rules':[
    'MFa(AssocSte3!1).Ste3(Receptor!1) + Gpa1(GnP~U) -> MFa(AssocSte3!1).Ste3(Receptor!1) + Gpa1(GnP~P)',
    'Ste3(Receptor) + Gpa1(GnP~U) -> Ste3(Receptor) + Gpa1(GnP~P)'],
    'Tags': [
    1, 'GEF', 'Ste3', 'Gpa1', 'contingencies', 'K+']},
}

DATA = [MAPK_GEF_DATA]
