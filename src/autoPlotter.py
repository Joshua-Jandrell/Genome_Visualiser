"""Contains definition for the `AutoPlotter` class."""

from VCF.globalDatasetManger import GlobalDatasetManager
from viewPanel import ViewPanel
from Plot.plotInfo import DataSetInfo, ViewInfo_base
from Plot.ViewInfos import ZygoteView, RefView
from Plot.plotSelect import PlotOptionPanel, PlotOptionCard, ZYGOSITY_OPT, REF_OPT, FREQ_BAR_OPT

CLEAR_ON_DATASET_DELETE = True # If set to true the figure will be completely cleared if no datasets are available 
class AutoPlotter():
    view_change_ignore_flag = False # If set true, plot changes will be ignored
    """
    Static class used to automatically update plot views based on selected data.\n
    Contains several methods to estimate view settings most appropriate for data.
    """
    def set_active(active:bool):
        if active:
            GlobalDatasetManager.add_listener(AutoPlotter.__on_data_update)
            AutoPlotter.no_data = len(GlobalDatasetManager.get_datasets()) == 0
            # subscribe to plot change events
            PlotOptionPanel.listen(AutoPlotter.__on_plots_update)
        else:
            GlobalDatasetManager.remove_listener(AutoPlotter.__on_data_update)
            # Unsubscribe from plot change events
            PlotOptionPanel.listen_stop(AutoPlotter.__on_plots_update)

    def __on_data_update(dataset_names:list[str]):
        AutoPlotter.view_change_ignore_flag =True # Stop views from double plotting
        data_available = len(dataset_names) > 0
        if AutoPlotter.no_data  and data_available:
            # Make automatic plot
            AutoPlotter.make_autoPlot()

        # Update data variable to reflect if not data is present
        AutoPlotter.no_data = not data_available

        if AutoPlotter.no_data:
            ViewPanel.set_plots([])

        AutoPlotter.view_change_ignore_flag = False

    def __on_plots_update(option_list:PlotOptionPanel,option_cards:list[PlotOptionCard]):
        """Called when plot options list is updated."""
        if AutoPlotter.view_change_ignore_flag: return
        ViewPanel.set_plots(PlotOptionPanel.get_view_list())

    def make_autoPlot():

        plot_data = GlobalDatasetManager.get_datasets()[0]

        # Check to see what plots have been selected 
        views = PlotOptionPanel.get_view_list()

        if len(views) == 0:
            views = select_views(plot_data)

        ViewPanel.set_plots(views)
def select_views(data:DataSetInfo)->list[ViewInfo_base]:
    """
    Selects views to be plotted based on size and nature of data.
    TODO Impliment
    """
    # get a reference to the view options panel
    PlotOptionPanel.select_instance_option(REF_OPT)
    PlotOptionPanel.select_instance_option(FREQ_BAR_OPT)

    views = PlotOptionPanel.get_view_list()
    return views
    