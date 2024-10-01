"""
Module containing UI option cards and controls plot views and setting which can be added to thr plot option panel.
"""
# The __init__.py is used to port all files in a folder into one module to simplify loading :)
# Not instead of needing to refer to individual files you can just type:
# ```from OptionCards import *```
from Plot.OptionCards.plotCard import *
from Plot.OptionCards.zygosityOption import ZygoOptionCard
from Plot.OptionCards.frequencyOption import FreqOptionCard
from .refOption import RefOptionCard
from .posCard import PosOptionCard
from Plot.OptionCards.mutfreqCard import MutFreqOptionCard