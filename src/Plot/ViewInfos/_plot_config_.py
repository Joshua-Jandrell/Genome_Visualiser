"""
Contains configuration info for the view info system.
"""
import matplotlib as mpl
import matplotlib.style as mplstyle

mpl.rcParams['path.simplify_threshold'] = 1.0
mplstyle.use('fast')


# === Color ===
CASE_COLORS = ["#DF4D55", "#00000000", "#8AB8E2", "#A3EA4C", "#FEF65B"]
"""Format is [Base, no data,  no mutation, heterozygous, homozygous]"""

CTRL_COLORS = ["#A80003", "#00000000", "#2166AC", "#3DA13F", "#FFD700", ]
"""Format is [Base, not data, no mutation, heterozygous, homozygous]"""

ALLELE_COLORS = ["#00000000","grey", "#29E838", "#E829D8", "#E89829", "#2979E8"]
"""Format is [Base, not data, other, A, C, G, T]"""

# === Layout ===
VERT_LABEL_POS = 'top'