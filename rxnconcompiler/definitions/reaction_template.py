REACTION_TEMPLATE = [{
    #### P+, ub+, gef
    'ReactionType:ID': '1.1.1.1',
    'Category': 'Covalent Modification',

    'ProductState[Component]': 'ComponentB',
    'SourceState[Component]': 'N/A',

    # 'ProductState[Modification]': '-{P}',
    # 'SourceState[Modification]': 'N/A',
    'Reversibility': 'irreversible',
    'Directionality': 'unidirectional'

},

    {
        #### P-, gap,
        'ReactionType:ID': '1.1.2.1',
        # 'ReactionType:ID': 'p-',
        'Category': 'Covalent Modification',

        'ProductState[Component]': 'N/A',
        'SourceState[Component]': 'ComponentB',
        # 'ProductState[Modification]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',
        # 'SourceState[Modification]': '-{P}',
    },

    {
        #### AP
        'ReactionType:ID': '1.1.1.2',
        'Category': 'Covalent Modification',

        'ProductState[Component]': 'ComponentB',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional'

        # 'ProductState[Modification]': '-{P}',

        # 'SourceState[Modification]': 'N/A'
    },

    {
        #### AP
        'ReactionType:ID': '1.1.2.2',
        'Category': 'Covalent Modification',

        'ProductState[Component]': 'N/A',
        'SourceState[Component]': 'ComponentB',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional'

        # 'ProductState[Modification]': '-{P}',

        # 'SourceState[Modification]': 'N/A'
    },

    {
        #### PT
        'ReactionType:ID': '1.1.3.1',
        'Category': 'Covalent Modification',

        'ProductState[Component]': 'ComponentB',
        'SourceState[Component]': 'ComponentA',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional'
        # 'ProductState[Modification]': '-{P}',
        # 'SourceState[Modification]': '-{P}'
    },

    {
        #### CUT
        'ReactionType:ID': "1.2.1.1",
        'Category': 'Covalent Modification',

        'ProductState[Component]': 'ComponentB',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional'
        # 'ProductState[Modification]': '-{Truncated}',
        # 'SourceState[Modification]': 'N/A'},
    },

    ######## Association Reactions #####
    {
        #### ppi, i, bind
        'ReactionType:ID': '2.1.1.1',
        'Category': 'Association',

        'ProductState[Component]': 'ComponentA',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'reversible',
        'Directionality': 'bidirectional',

        # 'ProductState[Modification]': '--ComponentB',
        # 'SourceState[Modification]': 'N/A'},

    },

    {
        #### ipi
        'ReactionType:ID': '2.1.1.2',
        'Category': 'Association',

        'ProductState[Component]': 'ComponentA',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'reversible',
        'Directionality': 'bidirectional',
        # 'ProductState[Modification]': '--ComponentB',
        # 'SourceState[Modification]': 'N/A'},

    },
    {
        #### Transcription
        'ReactionType:ID': "3.1.2",
        'Category': 'Synthesis/Degradation',

        'ProductState[Component]': 'ComponentB-mRNA',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',
        # 'ProductState[Modification]': 'N/A',
        # 'SourceState[Modification]': 'N/A'
    },
    {
        #### Translation
        'ReactionType:ID': "3.1.3",
        'Category': 'Synthesis/Degradation',

        'ProductState[Component]': 'ComponentB',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',
    },
    {
        #### Degradation
        'ReactionType:ID': "3.2.1",
        'Category': 'Synthesis/Degradation',

        'ProductState[Component]': 'N/A',
        'SourceState[Component]': 'ComponentB',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',

    },

    {
        # production
        'ReactionType:ID': "3.1.1",
        'Category': 'Synthesis/Degradation',

        'ProductState[Component]': 'ComponentB',
        'SourceState[Component]': 'N/A',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',
    },
    {
        ####
        'ReactionType:ID': "3.2.2",
        'Category': 'Synthesis/Degradation',

        'ProductState[Component]': 'N/A',
        'SourceState[Component]': 'ComponentB',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',

    },
    {
        ####
        'ReactionType:ID': "4.1",
        'Category': 'Relocalisation',

        'ProductState[Component]': '',
        'SourceState[Component]': '',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',

    },

    {
        ####
        'ReactionType:ID': "4.2",
        'Category': 'Relocalisation',

        'ProductState[Component]': '',
        'SourceState[Component]': '',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',

    },
    {
        ####
        'ReactionType:ID': "4.3",
        'Category': 'Relocalisation',

        'ProductState[Component]': '',
        'SourceState[Component]': '',

        'Reversibility': 'irreversible',
        'Directionality': 'unidirectional',

    },

]
