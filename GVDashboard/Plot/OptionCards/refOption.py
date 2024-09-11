from Plot.OptionCards import PlotOptionCard, PlotOptionCtrl, OptionCard
from Plot.plotInfo import RefView

class RefOptionCtrl(PlotOptionCtrl):
    def make_option_card(self) -> OptionCard:
        op = super().make_option_card()
        op.label.configure(text="Reference Sequence")
        op.set_value(RefView())
        return op