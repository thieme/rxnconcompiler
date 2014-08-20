#!/usr/bin/env python

"""
rule_input_data.py contains dictionaries with examples of rules with input.  
(e.g. [Start], [Turgor]). One dict represents single system,
that should run in BioNetGen.

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}
"""

REQUIRED = {
'A_ppi_B; ! [Start]': {
    'Rules':[
    'A(B) + B(A) <-> A(B!1).B(A!1)    kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', '!', 'input']}}

INHIBITORY = {
'A_ppi_B; x [Start]': {
    'Rules':[
    'A(B) + B(A) <-> A(B!1).B(A!1)    kf1_2*(1-k_Start), kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'x', 'input']}}

UPREGULATES = {
'A_ppi_B; K+ [Start]': {
    'Rules':[
    'A(B) + B(A) <-> A(B!1).B(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K+', 'input']}}

DOWNREGULATES = {
'A_ppi_B; K- [Start]': {
    'Rules':[
    'A(B) + B(A) <-> A(B!1).B(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K-', 'input']}}

CONSTANT = {
'A_ppi_C': {
    'Rules':[
    'A(C) + C(A) <-> A(C!1).C(A!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']},

'A_ppi_D': {
    'Rules':[
    'A(D) + D(A) <-> A(D!1).D(A!1)'],
    'Tags': [
    1, 'ppi', 'no contingencies']}}

BOOL_K_PLUS_AND = {
"""A_ppi_B; K+ <bool> 
<bool>; AND A--C; AND A--D; AND [Start]""": {
    'Rules':[
    'A(B,C!2,D!1).C(A!2).D(A!1) + B(A) <-> A(B!3,C!2,D!1).B(A!3).C(A!2).D(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Star',
    'A(B,C!1,D).C(A!1) + B(A) <-> A(B!2,C!1,D).B(A!2).C(A!1)    kf1_2, kr1_2',
    'A(B,C) + B(A) <-> A(B!1,C).B(A!1)    kf1_2, kr1_2'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K+', 'input', 'bool', 'AND']}}
BOOL_K_PLUS_AND.update(CONSTANT)

BOOL_K_MINUS_AND = {
"""A_ppi_B; K- <bool> 
<bool>; AND A--C; AND A--D; AND [Start]""": {
    'Rules':[
    'A(B,C!2,D!1).C(A!2).D(A!1) + B(A) <-> A(B!3,C!2,D!1).B(A!3).C(A!2).D(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start',
    'A(B,C!1,D).C(A!1) + B(A) <-> A(B!2,C!1,D).B(A!2).C(A!1)    kf1_2, kr1_2',
    'A(B,C) + B(A) <-> A(B!1,C).B(A!1)    kf1_2, kr1_2'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K-', 'input', 'bool', 'AND']}}
BOOL_K_MINUS_AND.update(CONSTANT)

BOOL_K_PLUS_OR = {
"""A_ppi_B; K+ <bool>
<bool>; OR A--C; OR A--D; OR [Start]""": {
    'Rules':[
    'A(B,C!1).C(A!1) + B(A) <-> A(B!2,C!1).B(A!2).C(A!1)    kf1_1, kr1_1',
    'A(B,C,D!1).D(A!1) + B(A) <-> A(B!2,C,D!1).B(A!2).D(A!1)    kf1_1, kr1_1',
    'A(B,C,D) + B(A) <-> A(B!1,C,D).B(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K+', 'input', 'bool', 'OR']}}
BOOL_K_PLUS_OR.update(CONSTANT)

BOOL_K_MINUS_OR = {
"""A_ppi_B; K- <bool>
<bool>; OR A--C; OR A--D; OR [Start]""": {
    'Rules':[
    'A(B,C!1).C(A!1) + B(A) <-> A(B!2,C!1).B(A!2).C(A!1)    kf1_1, kr1_1',
    'A(B,C,D!1).D(A!1) + B(A) <-> A(B!2,C,D!1).B(A!2).D(A!1)    kf1_1, kr1_1',
    'A(B,C,D) + B(A) <-> A(B!1,C,D).B(A!1)    kf1_2*(1-k_Start)+kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'K-', 'input', 'bool', 'OR']}}
BOOL_K_MINUS_OR.update(CONSTANT)

BOOL_REQ_AND = {
"""A_ppi_B; ! <bool>
<bool>; AND A--C; AND A--D; AND [Start]""": {
    'Rules':[
    'A(B,C!2,D!1).C(A!2).D(A!1) + B(A) <-> A(B!3,C!2,D!1).B(A!3).C(A!2).D(A!1)    kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', '!', 'input', 'bool', 'AND']}}
BOOL_REQ_AND.update(CONSTANT)

BOOL_INHIBIT_AND = {
"""A_ppi_B; x <bool>
<bool>; AND A--C; AND A--D; AND [Start]""": {
    'Rules':[
    'A(B,C!1,D).C(A!1) + B(A) <-> A(B!2,C!1,D).B(A!2).C(A!1)    kf1_2, kr1_2',
    'A(B,C) + B(A) <-> A(B!1,C).B(A!1)    kf1_2, kr1_2',
    'A(B,C!2,D!1).C(A!2).D(A!1) + B(A) <-> A(B!3,C!2,D!1).B(A!3).C(A!2).D(A!1)    kf1_2*(1-k_Start), kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'x', 'input', 'bool', 'AND']}}
BOOL_INHIBIT_AND.update(CONSTANT)

BOOL_REQ_OR = {
"""A_ppi_B; ! <bool>
<bool>; OR A--C; OR A--D; OR [Start]""": {
    'Rules':[
    'A(B,C!1).C(A!1) + B(A) <-> A(B!2,C!1).B(A!2).C(A!1)    kf1_1, kr1_1',
    'A(B,C,D!1).D(A!1) + B(A) <-> A(B!2,C,D!1).B(A!2).D(A!1)    kf1_1, kr1_1',
    'A(B,C,D) + B(A) <-> A(B!1,C,D).B(A!1)    kf1_1*k_Start, kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'x', 'input', 'bool', 'AND']}}
BOOL_REQ_OR.update(CONSTANT)

BOOL_INHIB_OR = {
"""A_ppi_B; x <bool>
<bool>; OR A--C; OR A--D; OR [Start]""": {
    'Rules':[
    'A(B,C,D) + B(A) <-> A(B!1,C,D).B(A!1)    kf1_2*(1-k_Start), kr1_2*(1-k_Start)+kr1_1*k_Start'],
    'Tags': [
    1, 'ppi', 'contingencies', 'x', 'input', 'bool', 'OR']}}
BOOL_INHIB_OR.update(CONSTANT)

RATES = {
"""A_ppi_B; ! <bool>
<bool>; OR A--C; OR A--D; OR [Start]
A_ppi_B; K+ A-{P}
A_ppi_B; K+ B-{P}""": {
    'Rules':[
    'kf3_1, kr3_1',
    'kf3_1*k_Start, kr3_2*(1-k_Start)+kr3_1*k_Start',
    'kf3_3, kr3_3',
    'kf3_3*k_Start, kr3_4*(1-k_Start)+kr3_3*k_Start',
    'kf3_5, kr3_5',
    'kf3_5*k_Start, kr3_6*(1-k_Start)+kr3_5*k_Start',
    'kf3_7, kr3_7',
    'kf3_7*k_Start, kr3_8*(1-k_Start)+kr3_7*k_Start',],
    'Tags': [
    1, 'ppi', 'contingencies', 'x', 'input', 'bool', 'AND']}}
RATES.update(CONSTANT)


DATA = [REQUIRED, INHIBITORY, UPREGULATES, DOWNREGULATES,\
        BOOL_K_PLUS_AND, BOOL_K_MINUS_AND, BOOL_K_PLUS_OR, \
        BOOL_K_MINUS_OR, BOOL_REQ_AND, BOOL_INHIBIT_AND, \
        BOOL_REQ_OR, BOOL_INHIB_OR, RATES]


