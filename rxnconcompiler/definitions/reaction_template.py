REACTION_TEMPLATE = [{
#### P+, ub+, gef
    'ReactionTypeID': u'1.1.1.1',
    'Category': u'Covalent Modification',

    'ProductState[Component]': u'ComponentB',
    'SourceState[Component]': u'N/A',

    #'ProductState[Modification]': u'-{P}',
    #'SourceState[Modification]': u'N/A',
    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional'

},

{
#### P-, gap,
    'ReactionTypeID': u'1.1.2.1',
    #'ReactionTypeID': 'p-',
    'Category': u'Covalent Modification',

    'ProductState[Component]': u'N/A',
    'SourceState[Component]': u'ComponentB',
    #'ProductState[Modification]': u'N/A',

    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional',
    #'SourceState[Modification]': u'-{P}',
     },


{
#### AP
    'ReactionTypeID': u'1.1.1.2',
    'Category': u'Covalent Modification',

    'ProductState[Component]': u'ComponentB',
    'SourceState[Component]': u'N/A',

    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional'

# 'ProductState[Modification]': u'-{P}',


 #'SourceState[Modification]': u'N/A'
 },

{
#### PT
'ReactionTypeID': u'1.1.3.1',
'Category': u'Covalent Modification',

 'ProductState[Component]': u'ComponentB',
'SourceState[Component]': u'ComponentA',

 'Reversibility': u'reversible',
 'Directionality': u'bidirectional'
 #'ProductState[Modification]': u'-{P}',

 #'SourceState[Modification]': u'-{P}'
},


{
#### CUT
 'ReactionTypeID': "1.2.1.1",
 'Category': u'Covalent Modification',

 'ProductState[Component]': u'ComponentB',
 'SourceState[Component]': u'N/A',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional'
 #'ProductState[Modification]': u'-{Truncated}',
 #'SourceState[Modification]': u'N/A'},
},

######## Association Reactions #####
{
#### ppi, i, bind
'ReactionTypeID': u'2.1.1.1',
'Category': u'Association',

'ProductState[Component]': u'ComponentA',
'SourceState[Component]': u'N/A',

'Reversibility': u'reversible',
'Directionality': u'nondirectional',


 #'ProductState[Modification]': u'--ComponentB',
 #'SourceState[Modification]': u'N/A'},

},

{
#### ipi
'ReactionTypeID': u'2.1.1.2',
'Category': u'Association',

'ProductState[Component]': u'ComponentA',
'SourceState[Component]': u'N/A',

'Reversibility': u'reversible',
'Directionality': u'nondirectional',
 #'ProductState[Modification]': u'--ComponentB',
 #'SourceState[Modification]': u'N/A'},

},
{
#### Transcription
    'ReactionTypeID': "3,1",
    'Category': u'Synthesis/Degradation',

    'ProductState[Component]': u'ComponentB-mRNA',
    'SourceState[Component]': u'N/A',

    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional',

# 'ProductState[Modification]': u'N/A',
#'SourceState[Modification]': u'N/A'
},
    {
#### Translation
 'ReactionTypeID': "3,2",
 'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'ComponentB',
 'SourceState[Component]': u'N/A',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',
# 'ProductState[Modification]': u'N/A',
 #'SourceState[Modification]': u'N/A'},

    },
{
#### Degredation
'ReactionTypeID': "3,4",
'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'N/A',
'SourceState[Component]': u'ComponentB',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',
 #'ProductState[Modification]': u'N/A',
# 'SourceState[Modification]': u'N/A'
},

{
#has to be changed
    'ReactionTypeID': "3,5",
'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'N/A',
'SourceState[Component]': u'ComponentB',

 'Reversibility': u'irreversible',
'Directionality': u'unidirectional',
 #'ProductState[Modification]': u'N/A',
 # 'SourceState[Modification]': u'N/A'
},
    {
#has to be changed
 'ReactionTypeID': "3,3",
 'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'ComponentB',
 'SourceState[Component]': u'N/A',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',


# 'ProductState[Modification]': u'N/A',


 #'SourceState[Modification]': u'N/A'
    },


]



