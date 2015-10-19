DEFAULT_DEFINITION = [
{
 'UID:Reaction': u'P+',
 'Reaction:Name': u'phosphorylation',
 'ReactionType:ID': u'1.1.1.1',
 'ReactionType:Name': 'Covalent_reversible_positive_trans',
 'ModifierBoundary': u'P',
 'Comments': '',

 },

{
 'UID:Reaction': u'P-',
 'Reaction:Name': u'dephosphorylation',

 'ReactionType:ID': u'1.1.2.1',
 'ReactionType:Name': 'Covalent_reversible_negative_trans',
 #'ReactionType:ID': 'p-',

 'ModifierBoundary': u'P',
 'Comments': ''
},

{
  'UID:Reaction': u'AP',
 'Reaction:Name': u'Autophosphorylation',
  'ReactionType:ID': u'1.1.1.2',
 'ReactionType:Name': 'Covalent_reversible_positive_cis',
  'ModifierBoundary': u'P',
  'Comments': '',
},

{
 'UID:Reaction': u'PT',
 'Reaction:Name': u'Phosphotransfer',
 'ReactionType:ID': u'1.1.3.1',
 'ReactionType:Name': 'Covalent_reversible_transfer_trans',
 'ModifierBoundary': u'P',
 'Comments': '',
},

{
'UID:Reaction': u'GEF',
'Reaction:Name': u'Guanine Nucleotide Exchange',
'ReactionType:ID': u'1.1.1.1',
'ReactionType:Name': 'Covalent_reversible_positive_trans',
'ModifierBoundary': u'GTP',

 'Comments': u'*G-proteins are assumed to bind GDP in their "basic" state. Exchange to GTP is denoted with the additional -{Pi}, which constitute the difference between the nucleotides.',
},

{
 'UID:Reaction': u'GAP',
 'Reaction:Name': u'GTPase Activation',
 'ReactionType:ID': u'1.1.2.1',
 'ReactionType:Name': 'Covalent_reversible_negative_trans',
 'ModifierBoundary': u'GTP',
 'Comments': u'*G-proteins are assumed to bind GDP in their "basic" state. Exchange to GTP is denoted with the additional -{Pi}, which constitute the difference between the nucleotides.',

},

 {
 'UID:Reaction': u'Ub+',
 'Reaction:Name': u'Ubiquitination',
 'ReactionType:ID': u'1.1.1.1',
  'ReactionType:Name': 'Covalent_reversible_positive_trans',
 'ModifierBoundary': u'Ub',
 'Comments': '',
},
{
 'UID:Reaction': u'Ub-',
 'Reaction:Name': u'dephosphorylation',

 'ReactionType:ID': u'1.1.2.1',
 'ReactionType:Name': 'Covalent_reversible_negative_trans',
 #'ReactionType:ID': 'p-',

 'ModifierBoundary': u'Ub',
 'Comments': ''
},

{
'UID:Reaction': u'CUT',
  'Reaction:Name': u'Proteolytic cleaveage',
'ReactionType:ID': "1.2.1.1",
 'ReactionType:Name': '',
 'ModifierBoundary': u'Truncated',
 'Comments': ''
},

#
#
#
#
{
#has to be changed

'UID:Reaction': u'ppi',
'Reaction:Name': u'protein-protein interaction',
'ReactionType:ID': u'2.1.1.1',
'ReactionType:Name': '',
'ModifierBoundary': u'N/A',

 'Comments': '',
},


{
#has to be changed

'UID:Reaction': u'ipi',
 'Reaction:Name': u'intra-protein interaction',
'ReactionType:ID': u'2.1.1.2',
 'ReactionType:Name': '',
 'ModifierBoundary': 'N/A',
 'Comments': u'*Self interaction',

},

{
#has to be changed

'UID:Reaction': u'i',
  'Reaction:Name': u'interaction (non-proteins)',
  'ReactionType:ID': "2.1.1.1",
 'ReactionType:Name': '',
'ModifierBoundary': u'N/A',
'Comments': '',

 },

{
#has to be changed

'UID:Reaction': u'BIND',
'Reaction:Name': u'Binding to DNA',
'ReactionType:ID': "2.1.1.1",
'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',
 'Comments': '',
},

#################   Synthesis/Degradation #################
#
{
#has to be changed
'UID:Reaction': u'TRSC',
 'Reaction:Name': u'Transcription',
 'ReactionType:ID': "3.1.2",
 'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',
 'Comments': '',
 },

#
{
'UID:Reaction': u'TRSL',
'Reaction:Name': u'Translation',
 'ReactionType:ID': "3.1.3",
 'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',
 'Comments': '',
 },

{
#has to be changed

'UID:Reaction': u'DEG',
'Reaction:Name': u'Degradation',
 'ReactionType:ID': "3.2.1",
 'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',
  'Comments': '',
},
#
{
#has to be changed

'UID:Reaction': u'CONSUME',
'Reaction:Name': u'Consumption',
  'ReactionType:ID': "3.2.2",
 'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',
 'Comments': '',
},

{
#has to be changed

'UID:Reaction': u'PRODUCE',
 'Reaction:Name': u'Production',

'ReactionType:ID': "3.1.1",
 'ReactionType:Name': '',
 'ModifierBoundary': u'N/A',

 'Comments': '',
},
#
#
#
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'NIMP',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Nucleus',
#  'Reaction:Name': u'Nuclear import',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'NIMP',
#  'Comments': '',
#  'ReactionType:ID': u'4.1.1',
#  'ProductState[Modification]': u'-{Nucleus}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'NEXP',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Nucleus, Cytoplasm',
#  'ReactionName': u'Nuclear export',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'NEXP',
#  'Comments': '',
#  'ReactionTypeID': u'4.1.2',
#  'ProductState[Modification]': u'-{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Nucleus}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'MIMP',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Mitochondria',
#  'ReactionName': u'Mitochondrial import',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'MIMP',
#  'Comments': '',
#  'ReactionTypeID': u'4.1.3',
#  'ProductState[Modification]': u'-{Mitochondria}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'MEXP',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Mitochondria, Cytoplasm',
#  'ReactionName': u'Mitochondrial export',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'MEXP',
#  'Comments': '',
#  'ReactionTypeID': u'4.1.4',
#  'ProductState[Modification]': u'-{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Mitochondria}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'TrnsCytExt',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Extracellular',
#  'ReactionName': u'Plasma membrane Cyt-\u02c3Ext ATPase pump',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'TrnsCytExt',
#  'Comments': '',
#  'ReactionTypeID': u'4.2.1',
#  'ProductState[Modification]': u'-{Extracellular}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'TrnsCytVac',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Vacuole',
#  'ReactionName': u'Vacuolar Cyt-\u02c3Vac ATPase pump',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'TrnsCytVac',
#  'Comments': '',
#  'ReactionTypeID': u'4.2.2',
#  'ProductState[Modification]': u'-{Vacuole}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'SymExtCyt',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Extracellular, Cytoplasm',
#  'ReactionName': u'Plasma membrane symporter',
#  'Reversibility': u'reversible',
#  'ReactionType': u'SymExtCyt',
#  'Comments': '',
#  'ReactionTypeID': u'4.3.1',
#  'ProductState[Modification]': u'-{Cytoplasm}, -{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Extracellular}, -{Extracellular}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'SymCytVac',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Vacuole',
#  'ReactionName': u'Vacuolar membrane symporter',
#  'Reversibility': u'reversible',
#  'ReactionType': u'SymCytVac',
#  'Comments': '',
#  'ReactionTypeID': u'4.3.2',
#  'ProductState[Modification]': u'-{Vacuole}, -{Vacuole}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'SymCytMit',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Mitochondria',
#  'ReactionName': u'Mitochondrial membrane symporter',
#  'Reversibility': u'reversible',
#  'ReactionType': u'SymCytMit',
#  'Comments': '',
#  'ReactionTypeID': u'4.3.3',
#  'ProductState[Modification]': u'-{Mitochondria}, -{Mitochondria}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'SymCytEnd',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Endosome',
#  'ReactionName': u'Endosomal membrane symporter',
#  'Reversibility': u'reversible',
#  'ReactionType': u'SymCytEnd',
#  'Comments': '',
#  'ReactionTypeID': u'4.3.4',
#  'ProductState[Modification]': u'-{Endosome}, -{Endosome}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'APExtCyt',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Extracellular, Cytoplasm',
#  'ReactionName': u'Plasma membrane antiporter',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'APExtCyt',
#  'Comments': '',
#  'ReactionTypeID': u'4.4.1',
#  'ProductState[Modification]': u'-{Cytoplasm}, -{Extracellular}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Extracellular}, -{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'APCytVac',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Vacuole',
#  'ReactionName': u'Vacuolar membrane antiporter',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'APCytVac',
#  'Comments': '',
#  'ReactionTypeID': u'4.4.2',
#  'ProductState[Modification]': u'-{Vacuole}, -{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Vacuole}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'APCytMit',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Mitochondria',
#  'ReactionName': u'Mitochondrial membrane antiporter',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'APCytMit',
#  'Comments': '',
#  'ReactionTypeID': u'4.4.3',
#  'ProductState[Modification]': u'-{Mitochondria}, -{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Mitochondria}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'APCytEnd',
#  'ProductState[Component]': u'ComponentB, ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Endosome',
#  'ReactionName': u'Endosomal membrane antiporter',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'APCytEnd',
#  'Comments': '',
#  'ReactionTypeID': u'4.4.4',
#  'ProductState[Modification]': u'-{Endosome}, -{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB, ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}, -{Endosome}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'FDExtCyt',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Extracellular, Cytoplasm',
#  'ReactionName': u'Plasma membrane channel',
#  'Reversibility': u'reversible',
#  'ReactionType': u'FDExtCyt',
#  'Comments': '',
#  'ReactionTypeID': u'4.5.1',
#  'ProductState[Modification]': u'-{Cytoplasm}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Extracellular}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'FDCytVac',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Vacuole',
#  'ReactionName': u'Vacuolar membrane channel',
#  'Reversibility': u'reversible',
#  'ReactionType': u'FDCytVac',
#  'Comments': '',
#  'ReactionTypeID': u'4.5.2',
#  'ProductState[Modification]': u'-{Vacuole}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'FDCytMit',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Mitochondria',
#  'ReactionName': u'Mitochondrial membrane channel',
#  'Reversibility': u'reversible',
#  'ReactionType': u'FDCytMit',
#  'Comments': '',
#  'ReactionTypeID': u'4.5.3',
#  'ProductState[Modification]': u'-{Mitochondria}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
#
# {
# #has to be changed
# 'Category': u'Relocalisation',
#  '!ReactionID': u'FDCytEnd',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'Cytoplasm, Endosome',
#  'ReactionName': u'Endosomal membrane channel',
#  'Reversibility': u'reversible',
#  'ReactionType': u'FDCytEnd',
#  'Comments': '',
#  'ReactionTypeID': u'4.5.4',
#  'ProductState[Modification]': u'-{Endosome}',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'-{Cytoplasm}'},
 ]