#!/usr/bin/env python

"""
rules_basic_data.py contains dictionary with basic reactions. 

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}

It anables to check whether rxncon input produces correct bngl rules code.
"""

# TODO: Relocalisation reactions are not tested yet.

REACTIONS_DATA = {
# basic reactions without contingencies.
'Kinase_P+_Target1': {
    'Rules':[
    'Kinase + Target1(Kinase~U) -> Kinase + Target1(Kinase~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']},

'Phosphatase_P-_Target1': {
    'Rules':[
    'Phosphatase + Target1(Phosphatase~P) -> Phosphatase + Target1(Phosphatase~U)'],
    'Tags': [
    1, 'P-', 'no contingencies']},

'Kinase_AP_Kinase': {
    'Rules':[
    'Kinase + Kinase(Kinase~U) -> Kinase + Kinase(Kinase~P)'],
    'Tags': [
    1, 'AP', 'no contingencies']},

'PDonor_PT_PAcceptor': {

'Rules':[
'PDonor(PAcceptor~P) + PAcceptor(PDonor~U) -> PDonor(PAcceptor~U) + PAcceptor(PDonor~P)'],
'Tags': [
1, 'PT', 'no contingencies']},


'Enzyme_GEF_GProt': {
    'Rules':[
    'Enzyme + GProt(Enzyme~U) -> Enzyme + GProt(Enzyme~P)'],
    'Tags': [
    1, 'GEF', 'no contingencies']},

'Enzyme_GAP_GProt': {
    'Rules':[
    'Enzyme + GProt(Enzyme~P) -> Enzyme + GProt(Enzyme~U)'],
    'Tags': [
    1, 'GAP', 'no contingencies']},

'EnzymeUb_Ub+_TargetUb': {
    'Rules':[
    'EnzymeUb + TargetUb(EnzymeUb~U) -> EnzymeUb + TargetUb(EnzymeUb~Ub)'],
    'Tags': [
    1, 'Ub+', 'no contingencies']},

'EnzymeUb_Ub-_TargetUb': {
    'Rules':[
    'EnzymeUb + TargetUb(EnzymeUb~Ub) -> EnzymeUb + TargetUb(EnzymeUb~U)'],
    'Tags': [
    1, 'Ub-', 'no contingencies']},

'EnzymeCUT_CUT_TargetCUT': {
    'Rules':[
    'EnzymeCUT + TargetCUT(EnzymeCUT~U) -> EnzymeCUT + TargetCUT(EnzymeCUT~Truncated)'],
    'Tags': [
    1, 'CUT', 'no contingencies']},

'A_P+_B': {
    'Rules':[
    'A + B(A~U) -> A + B(A~P)'],
    'Tags': [
    1, 'P+', 'no contingencies']},

'A_ppi_B': {
    'Rules':[
    'A(AssocB) + B(AssocA) <-> A(AssocB!1).B(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

'Ligand_i_Receptor': {
    'Rules':[
    'Ligand(AssocReceptor) + Receptor(AssocLigand) <-> Ligand(AssocReceptor!1).Receptor(AssocLigand!1)'],
    'Tags': [
    1, 'i', 'no contingencies']}, 

'TF_BIND_DNA': {
    'Rules':[
    'TF(AssocDNA) + DNA(AssocTF) <-> DNA(AssocTF!1).TF(AssocDNA!1)'],
    'Tags': [
    1, 'BIND', 'no contingencies']},

'PolII_Trsc_Gene': {
    'Rules':[
    'PolII -> PolII + GenemRNA'],
    'Tags': [
    1, 'TRSC', 'no contingencies']},

'Ribo_TRSL_Gene': {
    'Rules':[
    'Ribo + GenemRNA -> Ribo + GenemRNA + Gene'],
    'Tags': [
    1, 'TRSC', 'no contingencies']},

'Proteasome_DEG_Protein': {
    'Rules':[
    'Proteasome + Protein -> Proteasome'],
    'Tags': [
    1, 'DEG', 'no contingencies']},

'ProtA_[a]_ipi_ProtA_[b]': {
    'Rules':[
    'ProtA(a,b) <-> ProtA(a!1,b!1)'],
    'Tags': [
    1, 'ipi', 'no contingencies']}, 

'Sink_PRODUCE_Protein': {
    'Rules':[
    'Sink -> Sink + Protein'],
    'Tags': [
    1, 'PRODUCE', 'no contingencies']},

'Sink_CONSUME_Protein': {
    'Rules':[
    'Sink + Protein -> Sink'],
    'Tags': [
    1, 'CONSUME', 'no contingencies']},
}

CONTINGENCIES_DATA = {
    # basic reactions with contingencies.
    'A_ppi_C': {
    'Rules': [
    'A(AssocC) + C(AssocA) <-> A(AssocC!1).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

    'A_ppi_B; ! A--C': {
    'Rules': [
    'A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <-> A(AssocB!2,AssocC!1).B(AssocA!2).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'X_p-_A_[Z] \n A_ppi_B; ! A_[Z]-{P}': {
    'Rules': [
    'A(Z~P,AssocB) + B(AssocA) <-> A(Z~P,AssocB!1).B(AssocA!1)',
    'X + A(Z~P,AssocB!1).B(AssocA!1) -> X + A(Z~U,AssocB) + B(AssocA)',
    'X + A(Z~P,AssocB) -> X + A(Z~U,AssocB)'],
    'Tags': [
    1, 'p-', 'contingencies']},

    'A_ppi_B \n B_ppi_C; x A--B': {
    'Rules': [
    'A(AssocB) + B(AssocA,AssocC!1).C(AssocB!1) -> A(AssocB!1).B(AssocA!1,AssocC) + C(AssocB)',
    'A(AssocB) + B(AssocA,AssocC) <-> A(AssocB!1).B(AssocA!1,AssocC)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'A_ppi_B; x B--C \n B_ppi_C; x A--B': {
    'Rules': [
    'A(AssocB) + B(AssocA,AssocC) <-> A(AssocB!1).B(AssocA!1,AssocC)',
    'B(AssocA,AssocC) + C(AssocB) <-> B(AssocA,AssocC!1).C(AssocB!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Cdc42_[ED]_ppi_Ste20_[CRIB]; ! Cdc42_[GnP]-{P}; k+ Ste20_[BR]--PIP2 \n Ste20_[KD+CRIB]_ppi_Ste20_[KD+CRIB]; x Cdc42_[ED]--Ste20_[CRIB]': {
    'Rules': [
    'Cdc42(GnP~P,ED) + PIP2(AssocSte20!2).Ste20(BR!2,CRIB,KD+CRIB!1).Ste20(KD+CRIB!1) -> Cdc42(GnP~P,ED!1).PIP2(AssocSte20!2).Ste20(BR!2,CRIB!1,KD+CRIB) + Ste20(KD+CRIB)',
    'Cdc42(GnP~P,ED) + PIP2(AssocSte20!1).Ste20(BR!1,CRIB,KD+CRIB) <-> Cdc42(GnP~P,ED!1).PIP2(AssocSte20!2).Ste20(BR!2,CRIB!1,KD+CRIB)',
    'Cdc42(GnP~P,ED) + Ste20(BR,CRIB,KD+CRIB!1).Ste20(KD+CRIB!1) -> Cdc42(GnP~P,ED!1).Ste20(BR,CRIB!1,KD+CRIB) + Ste20(KD+CRIB)',
    'Cdc42(GnP~P,ED) + Ste20(BR,CRIB,KD+CRIB) <-> Cdc42(GnP~P,ED!1).Ste20(BR,CRIB!1,KD+CRIB)',
    'Ste20(CRIB,KD+CRIB) + Ste20(CRIB,KD+CRIB) <-> Ste20(CRIB,KD+CRIB!1).Ste20(CRIB,KD+CRIB!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Swi4_BIND_SCBG1; x Swi4_[n]--Swi4_[c] \n Swi4_[n]_ppi_Swi4_[c]': {
    'Rules': [
    'SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,n) + SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c) -> Swi4(AssocSCBG1,n!1).Swi4(AssocSCBG1,c!1) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'Swi4(AssocSCBG1,n) + Swi4(AssocSCBG1,c) <-> Swi4(AssocSCBG1,n!1).Swi4(AssocSCBG1,c!1)'],
    'Tags': [
    1, 'BIND', 'contingencies']},

    'Swi4_BIND_SCBFKS2; x Swi4_[n]--Swi4_[c] \n Swi4_BIND_SCBG1; x Swi4_[n]--Swi4_[c] \n Swi4_[n]_ppi_Swi4_[c]': {
    'Rules': [
    'SCBFKS2(AssocSwi4!1).SCBG1(AssocSwi4!2).Swi4(AssocSCBFKS2!1,AssocSCBG1!2,n) + SCBFKS2(AssocSwi4!1).SCBG1(AssocSwi4!2).Swi4(AssocSCBFKS2!1,AssocSCBG1!2,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBFKS2(AssocSwi4) + SCBFKS2(AssocSwi4) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'SCBFKS2(AssocSwi4!1).Swi4(AssocSCBFKS2!1,AssocSCBG1,n) + SCBFKS2(AssocSwi4!1).Swi4(AssocSCBFKS2!1,AssocSCBG1,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBFKS2(AssocSwi4) + SCBFKS2(AssocSwi4)',
    'SCBG1(AssocSwi4!1).Swi4(AssocSCBFKS2,AssocSCBG1!1,n) + SCBG1(AssocSwi4!1).Swi4(AssocSCBFKS2,AssocSCBG1!1,c) -> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1) + SCBG1(AssocSwi4) + SCBG1(AssocSwi4)',
    'Swi4(AssocSCBFKS2,AssocSCBG1,n) + Swi4(AssocSCBFKS2,AssocSCBG1,c) <-> Swi4(AssocSCBFKS2,AssocSCBG1,n!1).Swi4(AssocSCBFKS2,AssocSCBG1,c!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Sho1_[Cyt]_ppi_Ste11; ! <complex>; k+ Hkr1_[TMD]--Sho1_[TMD]\n <complex>; AND Opy_[BD:Ste50]--Ste50_[RA]; AND Ste11_[SAM]--Ste50_[SAM] \n Ste5_[MEKK]_ppi_Ste11; x Sho1_[Cyt]--Ste11':{
    'Rules': [
    'Hkr1(TMD!1).Sho1(Cyt,TMD!1) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5!3,SAM!2).Ste5(MEKK!3).Ste50(RA!1,SAM!2) -> Hkr1(TMD!4).Opy(BDSte50!1).Sho1(Cyt!3,TMD!4).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) + Ste5(MEKK)',
    'Hkr1(TMD!1).Sho1(Cyt,TMD!1) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) <-> Hkr1(TMD!4).Opy(BDSte50!1).Sho1(Cyt!3,TMD!4).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2)',
    'Sho1(Cyt,TMD) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5!3,SAM!2).Ste5(MEKK!3).Ste50(RA!1,SAM!2) -> Opy(BDSte50!1).Sho1(Cyt!3,TMD).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) + Ste5(MEKK)',
    'Sho1(Cyt,TMD) + Opy(BDSte50!1).Ste11(AssocSho1,AssocSte5,SAM!2).Ste50(RA!1,SAM!2) <-> Opy(BDSte50!1).Sho1(Cyt!3,TMD).Ste11(AssocSho1!3,AssocSte5,SAM!2).Ste50(RA!1,SAM!2)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    'Slt2_[DB]_ppi_Swi4_[c] \n Swi4_BIND_SCBG1; x Slt2_[DB]--Swi4_[c]; x Swi4_[n]--[c] \n Slt2_[DB]_ppi_Swi4_[c] \n Swi4_[n]_ipi_Swi4_[c]; x Slt2_[DB]--Swi4_[c]': {
    'Rules': [
    'Swi4(AssocSCBG1,c,n) + SCBG1(AssocSwi4) <-> SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c,n)',
    'Slt2(DB) + Swi4(AssocSCBG1,c!1,n!1) -> Slt2(DB!1).Swi4(AssocSCBG1,c!1,n)',
    'Slt2(DB) + SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c,n) -> Slt2(DB!1).Swi4(AssocSCBG1,c!1,n) + SCBG1(AssocSwi4)',
    'Slt2(DB) + Swi4(AssocSCBG1,c,n) <-> Slt2(DB!1).Swi4(AssocSCBG1,c!1,n)',
    'SCBG1(AssocSwi4!1).Swi4(AssocSCBG1!1,c,n) <-> Swi4(AssocSCBG1,c!1,n!1) + SCBG1(AssocSwi4)',
    'Swi4(AssocSCBG1,c,n) <-> Swi4(AssocSCBG1,c!1,n!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

    # conflict with ipi reaction
    'Swi6_[c]_ppi_Swi4_[c] \n Swi4_[n]_ipi_Swi4_[c]; x Swi6_[c]--Swi4_[c]': {
    'Rules': [
    'Swi6(c) + Swi4(c!1,n!1) -> Swi4(c!1,n).Swi6(c!1)',
    'Swi6(c) + Swi4(c,n) <-> Swi4(c!1,n).Swi6(c!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},

### simple conflict chain
    'X_p-_A \n A_ppi_B; ! A_[X]-{P} \n B_ppi_C; ! A--B \n C_ppi_D; ! B--C':{
    'Rules': [
    'X + A(X~P,AssocB!3).B(AssocA!3,AssocC!2).C(AssocB!2,AssocD!1).D(AssocC!1) -> X + A(X~U,AssocB) + B(AssocA,AssocC) + C(AssocB,AssocD) + D(AssocC)',
    'X + A(X~P,AssocB) -> X + A(X~U,AssocB)',
    'X + A(X~P,AssocB!1).B(AssocA!1,AssocC) -> X + A(X~U,AssocB) + B(AssocA,AssocC)',
    'X + A(X~P,AssocB!2).B(AssocA!2,AssocC!1).C(AssocB!1,AssocD) -> X + A(X~U,AssocB) + B(AssocA,AssocC) + C(AssocB,AssocD)'],
    'Tags': [
    1, 'p-', 'contingencies']},
### conflict chain with two alternative paths
    'X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B \n B_ppi_C; ! A--B \n C_ppi_D; ! B--C':{
    'Rules': [
    'X + A(X~P,AssocB,AssocF) -> X + A(X~U,AssocB,AssocF)',
    'X + A(X~P,AssocB!1,AssocF).B(AssocA!1,AssocC) -> X + A(X~U,AssocB,AssocF) + B(AssocA,AssocC)',
    'X + A(X~P,AssocB!2,AssocF!1).B(AssocA!2,AssocC).F(AssocA!1) -> X + A(X~U,AssocB,AssocF) + F(AssocA) + B(AssocA,AssocC)',
    'X + A(X~P,AssocB!2,AssocF).B(AssocA!2,AssocC!1).C(AssocB!1,AssocD) -> X + A(X~U,AssocB,AssocF) + B(AssocA,AssocC) + C(AssocB,AssocD)',
    'X + A(X~P,AssocB!3,AssocF).B(AssocA!3,AssocC!2).C(AssocB!2,AssocD!1).D(AssocC!1) -> X + A(X~U,AssocB,AssocF) + B(AssocA,AssocC) + C(AssocB,AssocD) + D(AssocC)',
    'X + A(X~P,AssocB!3,AssocF!1).B(AssocA!3,AssocC!2).C(AssocB!2,AssocD).F(AssocA!1) -> X + A(X~U,AssocB,AssocF) + F(AssocA) + B(AssocA,AssocC) + C(AssocB,AssocD)',
    'X + A(X~P,AssocB!4,AssocF!1).B(AssocA!4,AssocC!3).C(AssocB!3,AssocD!2).D(AssocC!2).F(AssocA!1) -> X + A(X~U,AssocB,AssocF) + F(AssocA) + B(AssocA,AssocC) + C(AssocB,AssocD) + D(AssocC)'],
    
    'Tags': [
    1, 'p-', 'contingencies']},

#### conflict chain with two alternative path excluding each other
    'X_p-_A \n A_ppi_B; ! A_[X]-{P} \n A_ppi_F; ! A--B; x A--C \n A_ppi_C; ! A--B; x A--F \n C_ppi_D; ! A--C':{
    'Rules': [
    'X + A(X~P,AssocB!2,AssocC,AssocF!1).B(AssocA!2).F(AssocA!1) -> X + A(X~U,AssocB,AssocC,AssocF) + F(AssocA) + B(AssocA)',
    'X + A(X~P,AssocB!3,AssocC!2,AssocF).B(AssocA!3).C(AssocA!2,AssocD!1).D(AssocC!1) -> X + A(X~U,AssocB,AssocC,AssocF) + C(AssocA,AssocD) + D(AssocC) + B(AssocA)',
    'X + A(X~P,AssocB!1,AssocC,AssocF).B(AssocA!1) -> X + A(X~U,AssocB,AssocC,AssocF) + B(AssocA)',
    'X + A(X~P,AssocB,AssocC,AssocF) -> X + A(X~U,AssocB,AssocC,AssocF)',
    'X + A(X~P,AssocB!2,AssocC!1,AssocF).B(AssocA!2).C(AssocA!1,AssocD) -> X + A(X~U,AssocB,AssocC,AssocF) + C(AssocA,AssocD) + B(AssocA)'],
    'Tags': [
    1, 'p-', 'contingencies']},


#### negative ipi contingency ####
    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; ! ProtA_[a]--[b]': {
    'Rules': [
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a!1,b!1) <-> ProtA(AssocProtC!1,a!2,b!2).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']},
##### positive ipi contingency
    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; x ProtA_[a]--[b]': {
    'Rules': [
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a,b) <-> ProtA(AssocProtC!1,a,b).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']},

    'Cdc42_ppi_Ste20; ! Cdc42_[GnP]-{P}; ! Ste20_[KD]--[CRIB2] \n Ste20_[KD]_ipi_Ste20_[CRIB2]': {
    'Rules': [
    'Cdc42(GnP~P,AssocSte20) + Ste20(AssocCdc42,CRIB2!1,KD!1) <-> Cdc42(GnP~P,AssocSte20!1).Ste20(AssocCdc42!1,CRIB2!2,KD!2)',
    'Ste20(CRIB2,KD) <-> Ste20(CRIB2!1,KD!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']}


}


DATA = [REACTIONS_DATA, CONTINGENCIES_DATA]