REACTION_TEMPLATE = [{
#### P+, ub+, gef
    'ReactionType:ID': u'1.1.1.1',
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
    'ReactionType:ID': u'1.1.2.1',
    #'ReactionType:ID': 'p-',
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
    'ReactionType:ID': u'1.1.1.2',
    'Category': u'Covalent Modification',

    'ProductState[Component]': u'ComponentB',
    'SourceState[Component]': u'N/A',

    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional'

# 'ProductState[Modification]': u'-{P}',


 #'SourceState[Modification]': u'N/A'
 },

{
#### AP
    'ReactionType:ID': u'1.1.2.2',
    'Category': u'Covalent Modification',

    'ProductState[Component]': u'N/A',
    'SourceState[Component]': u'ComponentB',

    'Reversibility': u'irreversible',
    'Directionality': u'unidirectional'

# 'ProductState[Modification]': u'-{P}',


 #'SourceState[Modification]': u'N/A'
 },
{
#### PT
'ReactionType:ID': u'1.1.3.1',
'Category': u'Covalent Modification',

 'ProductState[Component]': u'ComponentB',
'SourceState[Component]': u'ComponentA',

 'Reversibility': u'reversible',
 'Directionality': u'unidirectional'
 #'ProductState[Modification]': u'-{P}',

 #'SourceState[Modification]': u'-{P}'
},


{
#### CUT
 'ReactionType:ID': "1.2.1.1",
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
'ReactionType:ID': u'2.1.1.1',
'Category': u'Association',

'ProductState[Component]': u'ComponentA',
'SourceState[Component]': u'N/A',

'Reversibility': u'reversible',
'Directionality': u'bidirectional',


 #'ProductState[Modification]': u'--ComponentB',
 #'SourceState[Modification]': u'N/A'},

},

{
#### ipi
'ReactionType:ID': u'2.1.1.2',
'Category': u'Association',

'ProductState[Component]': u'ComponentA',
'SourceState[Component]': u'N/A',

'Reversibility': u'reversible',
'Directionality': u'bidirectional',
 #'ProductState[Modification]': u'--ComponentB',
 #'SourceState[Modification]': u'N/A'},

},
{
#### Transcription
    'ReactionType:ID': "3.1.2",
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
 'ReactionType:ID': "3.1.3",
 'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'ComponentB',
 'SourceState[Component]': u'N/A',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',
    },
{
#### Degradation
'ReactionType:ID': "3.2.1",
'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'N/A',
'SourceState[Component]': u'ComponentB',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',

},

{
#production
 'ReactionType:ID': "3.1.1",
 'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'ComponentB',
 'SourceState[Component]': u'N/A',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',
    },
{
####
'ReactionType:ID': "3.2.2",
'Category': u'Synthesis/Degradation',

 'ProductState[Component]': u'N/A',
'SourceState[Component]': u'ComponentB',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',

},

{
####
'ReactionType:ID': "4.1",
'Category': u'Relocalisation',

 'ProductState[Component]': '',
'SourceState[Component]': '',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',

},

{
####
'ReactionType:ID': "4.2",
'Category': u'Relocalisation',

 'ProductState[Component]': '',
'SourceState[Component]': '',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',

},
{
####
'ReactionType:ID': "4.3",
'Category': u'Relocalisation',

 'ProductState[Component]': '',
'SourceState[Component]': '',

 'Reversibility': u'irreversible',
 'Directionality': u'unidirectional',

},
]



