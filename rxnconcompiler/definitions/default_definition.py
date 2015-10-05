DEFAULT_DEFINITION = [
{
 'ReactionDefinitionID': u'P+',
 'ReactionName': u'phosphorylation',
 'ReactionTypeID': u'1.1.1.1',
 'ReactionTypeName': 'Covalent_reversible_positive_trans',
 'ModifierBoundary': u'P',
 'Comments': '',

 },

{
 'ReactionDefinitionID': u'P-',
 'ReactionName': u'dephosphorylation',

 'ReactionTypeID': u'1.1.2.1',
 'ReactionTypeName': 'Covalent_reversible_negative_trans',
 #'ReactionTypeID': 'p-',

 'ModifierBoundary': u'P',
 'Comments': ''
},

{
  'ReactionDefinitionID': u'AP',
 'ReactionName': u'Autophosphorylation',
  'ReactionTypeID': u'1.1.1.2',
 'ReactionTypeName': 'Covalent_reversible_positive_cis',
  'ModifierBoundary': u'P',
  'Comments': '',
},

{
 'ReactionDefinitionID': u'PT',
 'ReactionName': u'Phosphotransfer',
 'ReactionTypeID': u'1.1.3.1',
 'ReactionTypeName': 'Covalent_reversible_transfer_trans',
 'ModifierBoundary': u'P',
 'Comments': '',
},

{
'ReactionDefinitionID': u'GEF',
'ReactionName': u'Guanine Nucleotide Exchange',
'ReactionTypeID': u'1.1.1.1',
'ReactionTypeName': 'Covalent_reversible_positive_trans',
'ModifierBoundary': u'GTP',

 'Comments': u'*G-proteins are assumed to bind GDP in their "basic" state. Exchange to GTP is denoted with the additional -{Pi}, which constitute the difference between the nucleotides.',
},

{
 'ReactionDefinitionID': u'GAP',
 'ReactionName': u'GTPase Activation',
 'ReactionTypeID': u'1.1.2.1',
 'ReactionTypeName': 'Covalent_reversible_negative_trans',
 'ModifierBoundary': u'GTP',
 'Comments': u'*G-proteins are assumed to bind GDP in their "basic" state. Exchange to GTP is denoted with the additional -{Pi}, which constitute the difference between the nucleotides.',

},

 {
 'ReactionDefinitionID': u'Ub+',
 'ReactionName': u'Ubiquitination',
 'ReactionTypeID': u'1.1.1.1',
  'ReactionTypeName': 'Covalent_reversible_positive_trans',
 'ModifierBoundary': u'Ub',
 'Comments': '',
},


{
'ReactionDefinitionID': u'CUT',
  'ReactionName': u'Proteolytic cleaveage',
'ReactionTypeID': "1.2.1.1",
 'ReactionTypeName': '',
 'ModifierBoundary': u'Truncated',
 'Comments': ''
},

#
#
#
#
{
#has to be changed

'ReactionDefinitionID': u'ppi',
'ReactionName': u'protein-protein interaction',
'ReactionTypeID': u'2.1.1.1',
 'ReactionTypeName': '',
'ModifierBoundary': u'N/A',

 'Comments': '',
},


{
#has to be changed

'ReactionDefinitionID': u'ipi',
 'ReactionName': u'intra-protein interaction',
'ReactionTypeID': u'2.1.1.2',
 'ReactionTypeName': '',
 'ModifierBoundary': 'N/A',
 'Comments': u'*Self interaction',

},

{
#has to be changed

'ReactionDefinitionID': u'i',
  'ReactionName': u'interaction (non-proteins)',
  'ReactionTypeID': "2.1.1.1",
 'ReactionTypeName': '',
'ModifierBoundary': u'N/A',
'Comments': '',

 },

{
#has to be changed

'ReactionDefinitionID': u'BIND',
'ReactionName': u'Binding to DNA',
'ReactionTypeID': "2.1.1.1",
'ReactionTypeName': '',
 'ModifierBoundary': u'N/A',
 'Comments': '',
},
 
#
#
# {
# #has to be changed
# 'Category': u'Synthesis/Degradation',
# '!ReactionID': u'TRSC',
#  'ProductState[Component]': u'ComponentB-mRNA',
#  'Modifier or Boundary': u'N/A',
#  'ReactionName': u'Transcription',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'TRSC',
#  'Comments': '',
#  'ReactionTypeID': "3.1",
#  'ProductState[Modification]': u'N/A',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'N/A',
#  'SourceState[Modification]': u'N/A'},
#
# {
# #has to be changed
# 'Category': u'Synthesis/Degradation',
# '!ReactionID': u'TRSL',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'N/A',
#  'ReactionName': u'Translation',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'TRSL',
#  'Comments': '',
#  'ReactionTypeID': "3.2",
#  'ProductState[Modification]': u'N/A',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'N/A',
#  'SourceState[Modification]': u'N/A'},
#
# {
# #has to be changed
# 'Category': u'Synthesis/Degradation',
# '!ReactionID': u'DEG',
#  'ProductState[Component]': u'N/A',
#  'Modifier or Boundary': u'N/A',
#  'ReactionName': u'Degradation',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'DEG',
#  'Comments': '',
#  'ReactionTypeID': "3.3",
#  'ProductState[Modification]': u'N/A',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'N/A'},
#
# {
# #has to be changed
# 'Category': u'Synthesis/Degradation',
# '!ReactionID': u'CONSUME',
#  'ProductState[Component]': u'N/A',
#  'Modifier or Boundary': u'N/A',
#  'ReactionName': u'Consumption',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'CONSUME',
#  'Comments': '',
#  'ReactionTypeID': "3.4",
#  'ProductState[Modification]': u'N/A',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'ComponentB',
#  'SourceState[Modification]': u'N/A'},
#
# {
# #has to be changed
# 'Category': u'Synthesis/Degradation',
# '!ReactionID': u'PRODUCE',
#  'ProductState[Component]': u'ComponentB',
#  'Modifier or Boundary': u'N/A',
#  'ReactionName': u'Production',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'PRODUCE',
#  'Comments': '',
#  'ReactionTypeID': "3.5",
#  'ProductState[Modification]': u'N/A',
#  'Directionality': u'unidirectional',
#  'SourceState[Component]': u'N/A',
#  'SourceState[Modification]': u'N/A'},
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
#  'ReactionName': u'Nuclear import',
#  'Reversibility': u'irreversible',
#  'ReactionType': u'NIMP',
#  'Comments': '',
#  'ReactionTypeID': u'4.1.1',
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