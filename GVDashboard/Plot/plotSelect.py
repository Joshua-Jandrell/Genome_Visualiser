# This script contains option controllers for selectable plot views

from typing import Tuple
from UI.optionPanel import OptionCtrl, OptionPanel, OptionFrame
from Plot.plotInfo import ZygoteView, RefView

class PlotOptionList(OptionFrame):
    def __init__(self, master, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, True, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        # Add plot options
        self.content.register_option(ZygoteOption(self.content,"Zygosity"))
        self.content.register_option(RefOption(self.content,"Ref. Genome"))

# Option control specifcally for zygosity inof
class ZygoteOption(OptionCtrl):
    def make_option_panel(self) -> OptionPanel:
        op = super().make_option_panel()
        op.label.configure(text="Zygosity Plot")
        op.value = ZygoteView()
        return op
    
class RefOption(OptionCtrl):
    def make_option_panel(self) -> OptionPanel:
        op = super().make_option_panel()
        op.label.configure(text="Reference Sequence")
        op.value = RefView()
        return op