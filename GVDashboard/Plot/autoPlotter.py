"""Contains definition for the `AutoPlotter` class."""

from VCF.globalDatasetManger import GlobalDatasetManager
from UI.viewPanel import ViewPanel
from Plot.plotInfo import ViewPlotter, DataSetInfo, ZygoteView, RefView, ViewInfo_base
from Plot.plotSelect import PlotOptionPanel, ZYGOSITY_OPT

CLEAR_ON_DATASET_DELETE = True # If set to true the figure will be completely cleared if no datasets are available 
class AutoPlotter():
    """
    Static class used to automatically update plot views based on selected data.\n
    Contains several methods to estimate view settings most appropriate for data.
    """
    def set_active(active:bool):
        if active:
            GlobalDatasetManager.add_listener(AutoPlotter.__on_data_update)
            AutoPlotter.no_data = len(GlobalDatasetManager.get_datasets()) == 0
        else:
            GlobalDatasetManager.remove_listener(AutoPlotter.__on_data_update)

    def __on_data_update(dataset_names:list[str]):
        data_available = len(dataset_names) > 0
        if AutoPlotter.no_data  and data_available:
            # Make automatic plot
            AutoPlotter.make_autoPlot()

        # Update data variable to reflect if not data is present
        AutoPlotter.no_data = not data_available

    def make_autoPlot():
        plot_data = GlobalDatasetManager.get_datasets()[0]

        # Check to see what plots have been selected 
        views = PlotOptionPanel.get_view_list()

        if len(views) == 0:
            views = select_views(plot_data)

        # Set the view for each plot to the new data
        for v in views:
            v.set_data(plot_data)

        ViewPanel.set_plots(views)
def select_views(data:DataSetInfo)->list[ViewInfo_base]:
    """
    Selects views to be plotted based on size and nature of data.
    TODO Impliment
    """
    # get a reference to the view options panel
    PlotOptionPanel.select_instance_option(ZYGOSITY_OPT)
    z = ZygoteView()
    z.set_data(data)
    return [z]
    