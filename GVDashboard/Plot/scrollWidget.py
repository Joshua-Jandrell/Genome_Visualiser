# Scrollbar widget 
import customtkinter as ctk
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

from .ViewInfos import ViewInfo_base
from Plot.plotUpdate import PlotUpdate
from Util.box import Box
class ScrollWidget(ctk.CTkFrame):
    """Scroll bar widget used to scroll a matplotlib figure."""

    # Take plot info, location, and canvas 
    def __init__(self, master:Canvas) -> None:
        super().__init__(master=master, fg_color="transparent", height=20)
        self.scroll_slider = ctk.CTkSlider(self, orientation="horizontal")
        self.scroll_slider.pack(side=ctk.TOP, fill=ctk.X)
        self.view:ViewInfo_base|None = None

    def set_view(self, view:ViewInfo_base):
        "Set the scroll view"

        self.view =view
        # subscribe to view update event 
        view.update_event.add_listener(self.__on_view_update)

        min, max, window = view.get_x_scroll_params()
        self.scroll_slider.configure(command = self.do_scroll, from_ = min, to = max-window)
        self.scroll_slider.set(min)

                
        #scroll_bar.configure(command=A.test_scroll)
        self.scroll_slider._button_length = self.get_button_scale(range=max-min, window=window)

    def do_scroll(self, value):
        if self.view is None: return
        self.view.scroll_x(value)
        PlotUpdate.update()

    def clear_view(self):
        """Hide the scroll view"""
        if self.view is not None:
            self.view.update_event.remove_listener(self.__on_view_update)
            self.view = None
        self.place_forget()

    def __on_view_update(self, view):
        """Event to bae called (automatically) when the view info is updated."""
        min, max, window = self.view.get_x_scroll_params()
        self.scroll_slider.configure(from_ = min, to = max-window)

    def get_button_scale(self, range:float, window:float):
        return window/range * self.winfo_width()
    
    def destroy(self):
        self.clear_view()
        return super().destroy()

class ScrollManager():
    """
    Static class used to manage the creation and deletion of scrollbar widgets.
    """

    __canvas:Canvas|None = None
    __used_scrolls:list[ScrollWidget] = []
    __spare_scrolls:list[ScrollWidget] = []

    def set_scroll_canvas(canvas:Canvas):
        ScrollManager.__canvas = canvas

    @classmethod
    def clear_scrolls(cls):
        """Clear all the scrolls bars."""
        for scroll in cls.__used_scrolls:
            scroll.clear_view()
        cls.__spare_scrolls += cls.__used_scrolls
        cls.__used_scrolls.clear()

    @classmethod
    def make_scroll(cls, view:ViewInfo_base, scroll_box:Box):
        """Static method used to make scroll view widgets."""
        if ScrollManager.__canvas is None: return

        scroll = cls.get_scroll()
        scroll.place(relx=scroll_box.get_left(),
                   rely=1-scroll_box.get_top(),
                   relwidth = scroll_box.get_width(),
                   anchor='nw')
        scroll.set_view(view=view)

    @classmethod
    def get_scroll(cls)->ScrollWidget:
        if len(cls.__spare_scrolls) > 0:
            scroll = cls.__spare_scrolls.pop()
            cls.__used_scrolls.append(scroll)
            return scroll
        else:
            scroll = ScrollWidget(master = ScrollManager.__canvas)
            cls.__used_scrolls.append(scroll)
            return scroll
