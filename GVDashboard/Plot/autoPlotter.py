"""Contains definition for the `AutoPlotter` class."""

from VCF.globalDatasetManger import GlobalDatasetManager
from UI.viewPanel import ViewPanel
from Plot.plotInfo import ViewPlotter, DataSetInfo, ZygoteView, RefView, ViewInfo_base
from Plot.plotSelect import PlotOptionPanel
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
        print("hmmm")
        data_available = len(dataset_names)
        if AutoPlotter.no_data  and data_available:
            # Make automatic plot
            AutoPlotter.make_autoPlot()

        
        # Update data variable to reflect if not data is present
        AutoPlotter.no_data = data_available

    def make_autoPlot():
        plot_data = GlobalDatasetManager.get_datasets()[0]

        # Check to see what plots have been selected 
        views = PlotOptionPanel.get_view_list()
        #views = select_views(plot_data)

        view_pane = ViewPanel.instance
        assert(isinstance(view_pane,ViewPanel))
        view_pane.make_plot(views=views)

def select_views(data:DataSetInfo)->list[ViewInfo_base]:
    """
    Selects views to be plotted based on size and nature of data.
    TODO Impliment
    """
    # get a reference to the view options panel
    z = ZygoteView()
    z.set_data(data)
    return [z]
    