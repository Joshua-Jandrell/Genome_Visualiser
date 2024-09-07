import customtkinter
import tkinter as tk


class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="open toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def __del__(self):
        print("killed the app")

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        self.toplevel_window.focus()  # if window exists focus it
        self.toplevel_window.grab_set()
        print("yeeet")

from tkinter import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk) 

# plot function is created for 
# plotting the graph in 
# tkinter window 
def plot(): 
    # list of squares 
    y = [i**2 for i in range(101)] 

    # adding the subplot 
    plot1 = fig.add_subplot(111) 

    # plotting the graph 
    plot1.plot(y) 

    canvas.draw() 

    # placing the canvas on the Tkinter window 
    w =canvas.get_tk_widget()
    w.pack() 

    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                window) 
    toolbar.update() 

    # placing the toolbar on the Tkinter window 
    canvas.get_tk_widget().pack()
     
# the main Tkinter window 
window = App() 
dummy = Frame(window)
dummy.pack()


# setting the title 
window.title('Plotting in Tkinter') 

# dimensions of the main window 
window.geometry("500x500") 

# button that displays the plot 
plot_button = Button(master = window, 
					command = plot, 
					height = 2, 
					width = 10, 
					text = "Plot") 

# place the button 
# in main window 
plot_button.pack() 


# the figure that will contain the plot 
fig = Figure(figsize = (5, 5), 
            dpi = 100) 

# list of squares 
y = [i**2 for i in range(101)] 

# adding the subplot 
plot1 = fig.add_subplot(111) 

# plotting the graph 
plot1.plot(y) 

# creating the Tkinter canvas 
# containing the Matplotlib figure 
canvas = FigureCanvasTkAgg(fig, 
                        master = window) 


# run the gui 
window.mainloop() 