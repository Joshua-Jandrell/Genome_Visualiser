# Scrollbar widget 
from typing import Literal
import customtkinter as ctk
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigCanvas

from .ViewInfos import ViewInfo_base
from Plot.plotUpdate import PlotUpdate
from Util.box import Box
from Util.event import Event

class ScrollWidget(ctk.CTkFrame):
    """Scroll bar widget used to scroll a matplotlib figure."""

    # Take plot info, location, and canvas 
    def __init__(self, master:Canvas, orientation:Literal['horizontal', 'vertical'], width:int=20, height:int=20) -> None:

        super().__init__(master=master, fg_color="lightgrey", border_color='black', border_width=1, height=height, width=width, corner_radius=0)
        self.scroll_slider = ctk.CTkScrollbar(master=self, orientation=orientation, command=self._do_scroll)
        self.scroll_slider.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, pady=1, padx=1)
        self._dir = orientation
        self.view:ViewInfo_base|None = None

        self.scroll_event = Event()
        """
        Event called whenever the bar is scrolling.
        """

    def set_view(self, view:ViewInfo_base):
        "Set the scroll view"

        if view == self.view:
            return

        if self.view is not None:
            self.clear_view()

        self.view =view

        # subscribe to view update event 
        view.update_event.add_listener(self.__on_view_update)

        self.__aupdate_scroll()

    def _do_scroll(self, *args):

        if args[0] != 'moveto': return

        value = args[1]

        if self.view is None: return
        elif self._dir == 'vertical':
            self.view.scroll_y(value)
        elif self._dir == 'horizontal':
            self.view.scroll_x(value)
        
        self.scroll_event.invoke()

    def clear_view(self):
        """Hide the scroll view"""
        if self.view is not None:
            self.view.update_event.remove_listener(self.__on_view_update)
            self.view = None
        self.place_forget()

    def __on_view_update(self, view:ViewInfo_base):
        """Event to bae called (automatically) when the view info is updated."""
        self.__aupdate_scroll()
        
    def __aupdate_scroll(self):
        view = self.view
        if self._dir == 'horizontal':
            pt, size = view.get_x_scroll_params()
        else:
            pt, size = view.get_y_scroll_params()
        
        self.scroll_slider.set(pt, size)


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
    __used_x_scrolls:list[ScrollWidget] = []
    __spare_x_scrolls:list[ScrollWidget] = []
    __used_y_scrolls:list[ScrollWidget] = []
    __spare_y_scrolls:list[ScrollWidget] = []

    def set_scroll_canvas(canvas:Canvas):
        ScrollManager.__canvas = canvas

    @classmethod
    def clear_scrolls(cls):
        """Clear all the scrolls bars."""
        for scroll in cls.__used_x_scrolls:
            scroll.clear_view()
        cls.__spare_x_scrolls += cls.__used_x_scrolls
        cls.__used_x_scrolls.clear()
        for scroll in cls.__used_y_scrolls:
            scroll.clear_view()
        cls.__spare_y_scrolls += cls.__used_y_scrolls
        cls.__used_y_scrolls.clear()


    @classmethod
    def make_scroll(cls, view:ViewInfo_base, scroll_box:Box, orientation:Literal['horizontal', 'vertical']):
        """Static method used to make scroll view widgets."""
        if ScrollManager.__canvas is None: return

        scroll = cls.get_scroll(0,0,orientation)
        scroll.place(relx=scroll_box.get_left(),
                   rely=1-scroll_box.get_top(),
                   relwidth = scroll_box.get_width(),
                   relheight = scroll_box.get_height(),
                   anchor='nw')
        scroll.set_view(view=view)

    @classmethod
    def get_scroll(cls, width:int, hight:int, orientation:Literal['horizontal', 'vertical'])->ScrollWidget:
        if orientation == 'horizontal':
            if len(cls.__spare_x_scrolls) > 0:
                scroll = cls.__spare_x_scrolls.pop()
                cls.__used_x_scrolls.append(scroll)
                return scroll
            else:
                scroll = ScrollWidget(master = ScrollManager.__canvas, width=width, height=hight, orientation=orientation)
                cls.__used_x_scrolls.append(scroll)
                return scroll
        elif orientation == 'vertical':
            if len(cls.__spare_y_scrolls) > 0:
                scroll = cls.__spare_y_scrolls.pop()
                cls.__used_y_scrolls.append(scroll)
                return scroll
            else:
                scroll = ScrollWidget(master = ScrollManager.__canvas, width=width, height=hight, orientation=orientation)
                cls.__used_y_scrolls.append(scroll)
                return scroll
        else:
            raise ValueError(f"Unknown orientation \"{orientation}\"")

