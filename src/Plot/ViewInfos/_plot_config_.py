"""
Contains configuration info for the view info system.
"""
import matplotlib as mpl
import matplotlib.style as mplstyle

mpl.rcParams['path.simplify_threshold'] = 1.0
mplstyle.use('fast')


# === Color ===
NO_DATA = "#22000000"
CASE_COLORS = ["#DF4D55", NO_DATA, "#8AB8E2", "#A3EA4C", "#FEF65B"]
"""Format is [Base, no data,  no mutation, heterozygous, homozygous]"""

CTRL_COLORS = ["#A80003", "#00000000", "#2166AC", "#3DA13F", "#FFD700", ]
"""Format is [Base, not data, no mutation, heterozygous, homozygous]"""

ALLELE_COLORS = ["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8","#12A66A","grey","#E60000"]
"""Format is [Base, not data, other, A, C, G, T, insert, mutate, delete]"""
EXTRA_ALLELE_COLORS = ["#DDDDDD", "#29E83880", "#E829D880", "#E8982980", "#2979E880","#12A66A80","#DDDDDD","#E6000080"]
""" Format is [het_other, het_A, het_C, het_G, het_T, het_insert, het_mutate, het_delete]"""
ALLELE_COLOR_OFFSET = 8
# === Layout ===
VERT_LABEL_POS = 'top'

