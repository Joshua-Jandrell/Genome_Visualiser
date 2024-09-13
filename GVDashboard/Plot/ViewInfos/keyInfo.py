from matplotlib.axes import Axes as Axes
from . import ViewInfo_base

class KeyInfo(ViewInfo_base):
    """Special view class used to plot keys."""

    def __init__(self, views:list[ViewInfo_base]) -> None:
        self.views = views
        super().__init__()

    def get_desired_size(self) -> list[int]:
        return max(view.get_key_size() for view in self.views)
    
    def make_plots(self,axs:list[Axes],size:tuple[int,int]) -> str:
        for view in self.views:
            view.key(axs)