# This script contains the classes and panel used for data selection
from GVDashboard.UI.optionPanel import OptionPanel
from UI.optionPanel import OptionCtrl, OptionList

from VCF.filterInfo import DataSet

# Panel used 

# Class used to create dataset option panels
class DataOption(OptionCtrl):
    def make_option_panel(self) -> OptionPanel:
        op = super().make_option_panel()