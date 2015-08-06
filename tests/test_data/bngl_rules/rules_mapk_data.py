#!/usr/bin/env python

"""
mapk_data.py contains dictionary with all MAPK reactions.  

{rxncon_quick_string: 'Rules': [rule1, rule2 ...], 'Tags': [rtype ...]}

This data set can be tested:
- Each reaction independantely.
- All reaction together.
- Set of reactions together (based on one or more tags).
- Single reaction of choice (add something to the tags).
"""

from mapk_data.rules_mapk_bind_data import DATA as BIND
from mapk_data.rules_mapk_i_data import DATA as INTERACTION
from mapk_data.rules_mapk_ppi_data import DATA as PPI
from mapk_data.rules_mapk_pplus_data import DATA as PPLUS
from mapk_data.rules_mapk_pminus_data import DATA as PMINUS
from mapk_data.rules_mapk_gef_data import DATA as GEF
from mapk_data.rules_mapk_gap_data import DATA as GAP
from mapk_data.rules_mapk_ap_data import DATA as AP
from mapk_data.rules_mapk_pt_data import DATA as PT
from mapk_data.rules_mapk_deg_data import DATA as DEG
from mapk_data.rules_mapk_cut_data import DATA as CUT
from mapk_data.rules_mapk_ub_data import DATA as UB
from mapk_data.rules_mapk_ipi_data import DATA as IPI

MAPK_DATA = {}

# ASOCCIATION
MAPK_DATA.update(BIND[0])
MAPK_DATA.update(INTERACTION[0])
MAPK_DATA.update(PPI[0])
# COVALENT MODIFICATION
MAPK_DATA.update(PPLUS[0])
MAPK_DATA.update(PMINUS[0])
MAPK_DATA.update(GEF[0])
MAPK_DATA.update(GAP[0])
MAPK_DATA.update(AP[0])
MAPK_DATA.update(PT[0])
MAPK_DATA.update(CUT[0])
MAPK_DATA.update(UB[0])
MAPK_DATA.update(IPI[0])
# DEGRADATION / SYNTHESIS
MAPK_DATA.update(DEG[0])

DATA = [MAPK_DATA]
