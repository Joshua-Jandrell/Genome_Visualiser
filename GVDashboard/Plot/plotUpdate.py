from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

class PlotUpdate():
    """
    Static class used to update canvas after views have been modified.
    """
    __canvas:FigCanvas|None = None

    def set_canvas(canvas:FigCanvas):
        PlotUpdate.__canvas = canvas

    def update():
        if PlotUpdate.__canvas is not None:
            PlotUpdate.__canvas.draw_idle()
