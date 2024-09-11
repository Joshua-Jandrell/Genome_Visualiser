from Plot.OptionCards import PlotOptionCard, PlotOptionCtrl, OptionCard
from Plot.plotInfo import ZygoteView

# Option control specifcally for zygosity inof
class ZygoteOptionCtrl(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        op.label.configure(text="Zygosity Plot")
        op.set_value(ZygoteView())
        return op
        