#!/usr/bin/env python

"""
pheromone_data.py contains dictionary with pheromone response reactions.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}

This data set can be tested:
- Each reaction independantely.
- All reaction together.
- Set of reactions together (based on one or more tags).
- Single reaction of choice (add something to the tags).
"""

PHEROMON_DATA = {
# ASOCCIATION
# ppi no contingenies
'alpha_ppi_Ste2': {
    'Rules':[
    'alpha(Ste2) + Ste2(alpha) <-> Ste2(alpha!1).alpha(Ste2!1)'],
    'Tags': [
    1, 'ppi', 'alpha', 'Ste2', 'no contingencies']},

# ppi contingencies
'Gpa1_ppi_Ste4; x Ste4--Ste5; x Ste4--Ste20; x Far1--Ste4; K- Gpa1-{P}': {
    'Rules':[
    'Gpa1(bd~U,Ste4) + Ste4(Far1,Gpa1,Ste20,Ste5) <-> Gpa1(bd~U,Ste4!1).Ste4(Far1,Gpa1!1,Ste20,Ste5)',
    'Gpa1(Ste4) + Ste4(Far1,Gpa1,Ste20,Ste5) <-> Gpa1(Ste4!1).Ste4(Far1,Gpa1!1,Ste20,Ste5)'],
      
    'Tags': [
    1, 'ppi', 'Gpa1', 'Ste4', 'contingencies', 'x', 'K-']},

'Ste5_ppi_Ste11; x Ste4--Ste5; x Ste5--Ste7; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}': {
    'Rules':[
    'Ste5(bd~U,Ste11,Ste4,Ste7) + Ste11(bd~U,Ste5) <-> Ste11(bd~U,Ste5!1).Ste5(bd~U,Ste11!1,Ste4,Ste7)'],
      
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste11', 'contingencies', 'x']},

# ##### contingency error #####
# '''Fus3_ppi_Ste7; x Fus3--Ste12; x Ste5--Ste7; K+ <ComplexL>
# <ComplexL>; and Ste5--Ste11
# <ComplexL>; and Ste5--Ste7
# <ComplexL>; and Ste4--Ste5
# <ComplexL>; and Ste4--Ste20
# <ComplexL>; and Ste11-{P}
# <ComplexL>; and Ste7-{P}
# <ComplexL>; and Ste5-{P}''': {
#     'Rules':[
#     'Fus3(Ste12,Ste7) + Ste7(Fus3,Ste5) <-> Fus3(Ste12,Ste7!1).Ste7(Fus3!1,Ste5)',
#     'Fus3(Ste12,Ste7) + Ste11(bd~P,Ste5!1).Ste20(Ste4!2).Ste4(Ste20!2,Ste5!3).Ste5(bd~P,Ste11!1,Ste4!3,Ste7!4).Ste7(bd~P,Fus3,Ste5!4) <-> Fus3(Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Ste20!3,Ste5!4).Ste5(bd~P,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'ppi', 'Fus3', 'Ste7', 'contingencies', 'x', 'K+', 'complex']},

'Ste5_ppi_Ste7; ! Fus3--Ste7; ! Ste5--Ste11; x Ste4--Ste5 ; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}': {
    'Rules':[
    'Ste11(bd~U,Ste5!1).Ste5(bd~U,Ste11!1,Ste4,Ste7) + Fus3(bd~U,Ste7!1).Ste7(bd~U,Fus3!1,Ste5) <-> Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste5(bd~U,Ste11!2,Ste4,Ste7!3).Ste7(bd~U,Fus3!1,Ste5!3)'],
      
    'Tags': [
    1, 'ppi', 'Ste5', 'Ste7', 'contingencies', 'x', '!']},

# #### Complex D formation w/ boolean notation: complex error ####
# '''Ste4_ppi_Ste5; x Ste4--Ste20 ; x Gpa1--Ste4; x Far1--Ste4; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}; ! <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste5(bd~U,Ste11!2,Ste4,Ste7!3).Ste7(bd~U,Fus3!1,Ste5!3) + Ste4(Far1,Gpa1,Ste20,Ste5) <-> Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste4(Far1,Gpa1,Ste20,Ste5!3).Ste5(bd~U,Ste11!2,Ste4!3,Ste7!4).Ste7(bd~U,Ste5!4)'],
      
#     'Tags': [
#     1, 'ppi', 'Ste4', 'Ste5', 'contingencies', 'x', '!', 'complex']},

# ##### Complex D formation w/o boolean notation: wrong BNGL string: 'x Ste7-{P}', 'x Ste11-{P}', 'x Fus3-{P}' and '! Fus3--Ste7' are ignored ####
# 'Ste4_ppi_Ste5; x Ste4--Ste20 ; x Gpa1--Ste4; x Far1--Ste4; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7': {
#     'Rules':[
#     'Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste5(bd~U,Ste11!2,Ste4,Ste7!3).Ste7(bd~U,Fus3!1,Ste5!3) + Ste4(Far1,Gpa1,Ste20,Ste5) <-> Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste4(Far1,Gpa1,Ste20,Ste5!3).Ste5(bd~U,Ste11!2,Ste4!3,Ste7!4).Ste7(bd~U,Ste5!4)'],
      
#     'Tags': [
#     1, 'ppi', 'Ste4', 'Ste5', 'contingencies', 'x', '!']},

# #### Complex E formation w/ boolean notation: same complex error as above####
# '''Ste4_ppi_Ste20; x Far1--Ste4; x Gpa1--Ste4; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}; ! <ComplexD>
# <ComplexD>; and Ste4--Ste5
# <ComplexD>; and <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste4(Far1,Gpa1,Ste20,Ste5!3).Ste5(bd~U,Fus3!1,Ste11!2,Ste4!3,Ste7!4).Ste7(bd~U,Ste5!4) + Ste20(Ste4) <-> Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(bd~U,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~U,Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'ppi', 'Ste4', 'Ste20', 'contingencies', 'x', '!', 'complex']},

# ##### Complex E formation w/o boolean notation: all phosphorylation states and Fus3 are missing in BNGL####
# 'Ste4_ppi_Ste20; x Far1--Ste4; x Gpa1--Ste4; x Ste11-{P}; x Ste7-{P}; x Fus3-{P}; x Ste5-{P}; ! Ste4--Ste5; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7': {
#     'Rules':[
#     'Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste4(Far1,Gpa1,Ste20,Ste5!3).Ste5(bd~U,Fus3!1,Ste11!2,Ste4!3,Ste7!4).Ste7(bd~U,Ste5!4) + Ste20(Ste4) <-> Fus3(bd~U,Ste7!1).Ste11(bd~U,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(bd~U,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~U,Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'ppi', 'Ste4', 'Ste20', 'contingencies', 'x', '!']},

'Fus3_ppi_Ste12; ! Fus3-{P}; x Fus3--Ste7': {
    'Rules':[
    'Fus3(bd~P,Ste12,Ste7) + Ste12(Fus3) <-> Fus3(bd~P,Ste12!1,Ste7).Ste12(Fus3!1)'],
      
    'Tags': [
    1, 'ppi', 'Fus3', 'Ste12', 'contingencies', 'x', '!']},

'Far1_ppi_Ste4; ! Far1-{P}; x Gpa1--Ste4; x Ste4--Ste5 ; x Ste4--Ste20; x Cdc28--Far1': {
    'Rules':[
    'Far1(bd~P,Cdc28,Ste4) + Ste4(Far1,Gpa1,Ste20,Ste5) <-> Far1(bd~P,Cdc28,Ste4!1).Ste4(Far1!1,Gpa1,Ste20,Ste5)'],
      
    'Tags': [
    1, 'ppi', 'Far1', 'Ste4', 'contingencies', 'x', '!']},

'Cdc28_ppi_Far1; ! Far1-{P}; x Far1--Ste4': {
    'Rules':[
    'Cdc28(Far1) + Far1(bd~P,Cdc28,Ste4) <-> Cdc28(Far1!1).Far1(bd~P,Cdc28!1,Ste4)'],
      
    'Tags': [
    1, 'ppi', 'Cdc28', 'Far1', 'contingencies', 'x', '!']},


# COVALENT MODIFICATION
# p+ contingencies
'Fus3_P+_Sst2; x Fus3--Ste7; x Fus3--Ste12; ! Fus3-{P}': {
    'Rules':[
    'Fus3(bd~P,Ste12,Ste7) + Sst2(Fus3~U) -> Fus3(bd~P,Ste12,Ste7) + Sst2(Fus3~P)'],
      
    'Tags': [
    1, 'P+', 'Fus3', 'Sst2', 'contingencies', 'x', '!']},

# #### Ste20_P+_Ste11 w/ boolean: complex error ####
# '''Ste20_P+_Ste11; ! <ComplexE>
# <ComplexE>; and Ste4--Ste20
# <ComplexE>; and <ComplexD>
# <ComplexD>; and Ste4--Ste5
# <ComplexD>; and <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(Ste7!1).Ste11(Ste20~U,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Fus3!1,Ste5!5)-> Fus3(Ste7!1).Ste11(Ste20~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'P+', 'Ste11', 'Ste20', 'contingencies', '!', 'complex']},

# #### Ste20_P+_Ste11 w/o boolean: Fus3 and information about Gpa1 and Far1 are missing in BNGL####
# 'Ste20_P+_Ste11; ! Ste4--Ste20; ! Ste4--Ste5; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7': {
#     'Rules':[
#     'Fus3(Ste7!1).Ste11(Ste20~U,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Fus3!1,Ste5!5)-> Fus3(Ste7!1).Ste11(Ste20~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'P+', 'Ste11', 'Ste20', 'contingencies', '!']},

# #### Ste11_P+_Ste7 w/ boolean: complex error ####
# '''Ste11_P+_Ste7; ! <ComplexF>
# <ComplexF>; and Ste11-{P}
# <ComplexF>; and <ComplexE>
# <ComplexE>; and Ste4--Ste20
# <ComplexE>; and <ComplexD>
# <ComplexD>; and Ste4--Ste5
# <ComplexD>; and <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(Ste7!1).Ste11(Ste20~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Ste11~U,Fus3!1,Ste5!5)-> Fus3(Ste7!1).Ste11(Ste20~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Ste11~P,Fus3!1,Ste5!5)'],

#     'Tags': [
#     1, 'P+', 'Ste7', 'Ste11', 'contingencies', '!', 'complex']},

# #### Ste11_P+_Ste7 w/o boolean: Ste4 and Ste20 are missing in BNGL####
# 'Ste11_P+_Ste7; ! Ste4--Ste20; ! Ste4--Ste5; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7; ! Ste11-{P}': {
#     'Rules':[
#     'Fus3(Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Ste11~U,Fus3!1,Ste5!5)-> Fus3(Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(Ste11~P,Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'P+', 'Ste11', 'Ste7', 'contingencies', '!']},

# #### Ste7_P+_Fus3 w/ boolean: complex error ####
# '''Ste7_P+_Fus3; x Fus3--Ste12; ! <ComplexG>
# <ComplexG>; and Ste7-{P}
# <ComplexG>; and <ComplexF>
# <ComplexF>; and Ste11-{P}
# <ComplexF>; and <ComplexE>
# <ComplexE>; and Ste4--Ste20
# <ComplexE>; and <ComplexD>
# <ComplexD>; and Ste4--Ste5
# <ComplexD>; and <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(Ste7~U,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)-> Fus3(Ste7~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)'],

#     'Tags': [
#     1, 'P+', 'Fus3', 'Ste7', 'contingencies', '!', 'x', 'complex']},

# #### Ste7_P+_Fus3 w/o boolean: Ste4, Ste11 and Ste20 are missing in BNGL ####
# 'Ste7_P+_Fus3; x Fus3--Ste12; ! Ste4--Ste20; ! Ste4--Ste5; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7; ! Ste11-{P}; ! Ste7-{P}': {
#     'Rules':[
#     'Fus3(Ste7~U,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)-> Fus3(Ste7~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)'],
      
#     'Tags': [
#     1, 'P+', 'Fus3', 'Ste7', 'contingencies', '!', 'x']},

# #### Fus3_P+_Ste5 w/ boolean: complex error ####
# '''Fus3_P+_Ste5; x Fus3--Ste12; ! <ComplexH>
# <ComplexH>; and Fus3-{P}
# <ComplexH>; and <ComplexG>
# <ComplexG>; and Ste7-{P}
# <ComplexG>; and <ComplexF>
# <ComplexF>; and Ste11-{P}
# <ComplexF>; and <ComplexE>
# <ComplexE>; and Ste4--Ste20
# <ComplexE>; and <ComplexD>
# <ComplexD>; and Ste4--Ste5
# <ComplexD>; and <ComplexC>
# <ComplexC>; and Fus3--Ste7
# <ComplexC>; and Ste5--Ste11
# <ComplexC>; and Ste5--Ste7''': {
#     'Rules':[
#     'Fus3(bd~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Fus3~U,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~U,Fus3!1,Ste5!5)-> Fus3(bd~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Fus3~P,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)'],

#     'Tags': [
#     1, 'P+', 'Fus3', 'Ste5', 'contingencies', '!', 'x', 'complex']},

# #### Fus3_P+_Ste5 w/o boolean: Ste20 and information about Gpa1 and Far1 are missing in BNGL ####
# 'Fus3_P+_Ste5; x Fus3--Ste12; ! Ste4--Ste20; ! Ste4--Ste5; ! Fus3--Ste7; ! Ste5--Ste11; ! Ste5--Ste7; ! Ste11-{P}; ! Ste7-{P}; ! Fus3-{P}': {
#     'Rules':[
#     'Fus3(bd~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Fus3~U,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)-> Fus3(bd~P,Ste12,Ste7!1).Ste11(bd~P,Ste5!2).Ste20(Ste4!3).Ste4(Far1,Gpa1,Ste20!3,Ste5!4).Ste5(Fus3~P,Ste11!2,Ste4!4,Ste7!5).Ste7(bd~P,Fus3!1,Ste5!5)'],

#     'Tags': [
#     1, 'P+', 'Fus3', 'Ste5', 'contingencies', '!', 'x']},


'Fus3_P+_Far1; x Fus3--Ste12; x Fus3--Ste7; x Far1--Ste4; x Cdc28--Far1; ! Fus3-{P}': {
    'Rules':[
    'Fus3(bd~P,Ste12,Ste7) + Far1(Fus3~U,Cdc28,Ste4) -> Fus3(bd~P,Ste12,Ste7) + Far1(Fus3~P,Cdc28,Ste4)'],

    'Tags': [
    1, 'P+', 'Fus3', 'Far1', 'contingencies', '!', 'x']},

# p- no contingecies
'dummy5_P-_Sst2': {
    'Rules':[
    'dummy5 + Sst2(dummy5~P) -> dummy5 + Sst2(dummy5~U)'],
      
    'Tags': [
    1, 'P-', 'dummy5', 'Sst2', 'no contingencies']},

# p- contingecies
'dummy3_P-_Fus3; x Fus3--Ste12; x Fus3--Ste7': {
    'Rules':[
    'dummy3 + Fus3(dummy3~P,Ste12,Ste7) -> dummy3 + Fus3(dummy3~U,Ste12,Ste7)'],
      
    'Tags': [
    1, 'P-', 'dummy3', 'Fus3', 'contingencies', 'x']},

'dummy4_P-_Far1; x Far1--Ste4; x Cdc28--Far1': {
    'Rules':[
    'dummy4 + Far1(dummy4~P,Cdc28,Ste4) -> dummy4 + Far1(dummy4~U,Cdc28,Ste4)'],
      
    'Tags': [
    1, 'P-', 'dummy4', 'Far1', 'contingencies', 'x']},

# gef contingencies
'Ste2_GEF_Gpa1; ! alpha--Ste2; ! Gpa1--Ste4': {
    'Rules':[
    'Ste2(alpha!1).alpha(Ste2!1) + Gpa1(Ste2~U,Ste4!1).Ste4(Gpa1!1) -> Ste2(alpha!1).alpha(Ste2!1) + Gpa1(Ste2~P,Ste4!1).Ste4(Gpa1!1)'],
      
    'Tags': [
    1, 'GEF', 'Ste2', 'Gpa1', 'contingencies', '!']},

# gap contingencies
'Sst2_GAP_Gpa1; ! Sst2-{P}; x Gpa1--Ste4': {
    'Rules':[
    'Sst2(bd~P) + Gpa1(Sst2~P,Ste4) -> Sst2(bd~P) + Gpa1(Sst2~U,Ste4)'],
      
    'Tags': [
    1, 'GAP', 'Sst2', 'Gpa1', 'contingencies', 'x', '!']},

'dummy2_GAP_Gpa1; x Gpa1--Ste4': {
    'Rules':[
    'dummy2 + Gpa1(dummy2~P,Ste4) -> dummy2 + Gpa1(dummy2~U,Ste4)'],
      
    'Tags': [
    1, 'GAP', 'dummy2', 'Gpa1', 'contingencies', 'x']},

# DEG no contingencies
'dummy1_DEG_Ste2': {
    'Rules':[
    'dummy1 + Ste2 -> dummy1'],
      
    'Tags': [
    1, 'DEG', 'dummy1', 'Ste2', 'no contingencies']},

# DEG contingencies
'Bar1_DEG_alpha; x alpha--Ste2': {
    'Rules':[
    'Bar1 + alpha(Ste2) -> Bar1'],
      
    'Tags': [
    1, 'DEG', 'Bar1', 'alpha', 'contingencies', 'x']},

}

DATA = [PHEROMON_DATA]
