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
    'PDonor(PAcceptor~P) + PAcceptor(PDonor~U) <-> PDonor(PAcceptor~U) + PAcceptor(PDonor~P)'],
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
    'Rules':[
    'A(AssocC) + C(AssocA) <-> A(AssocC!1).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

    'A_ppi_B; ! A--C': {
    'Rules':[
    'A(AssocB,AssocC!1).C(AssocA!1) + B(AssocA) <-> A(AssocB!2,AssocC!1).B(AssocA!2).C(AssocA!1)'],
    'Tags': [
    1, 'ppi', 'contingencies']},
    
    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; ! ProtA_[a]--[b]': {
    'Rules':[
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a!1,b!1) <-> ProtA(AssocProtC!1,a!2,b!2).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']},

    'ProtC_ppi_ProtA; ! ProtC_[Gnp]-{P}; x ProtA_[a]--[b]': {
    'Rules':[
    'ProtC(Gnp~P,AssocProtA) + ProtA(AssocProtC,a,b) <-> ProtA(AssocProtC!1,a,b).ProtC(Gnp~P,AssocProtA!1)'],
    'Tags': [
    1, 'ipi', 'contingencies']}
}


DATA = [REACTIONS_DATA, CONTINGENCIES_DATA]