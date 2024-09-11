import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create a Tkinter window
root = tk.Tk()
root.title("Matplotlib with Scrollbars")
root.geometry("800x600")

# Create a frame for the canvas and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=1)

# Create a canvas widget
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Add a scrollbar to the canvas
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas
scrollable_frame = tk.Frame(canvas)

# Add this new frame to a window in the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

# Create a matplotlib figure and add subplots
fig, axs = plt.subplots(10, 1, figsize=(8, 30))  # Example with 10 subplots

# Populate subplots with data
x = np.linspace(0, 10, 100)
for ax in axs:
    ax.plot(x, np.sin(x))

# Add the figure to the Tkinter canvas
figure_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
figure_canvas.draw()
figure_canvas.get_tk_widget().pack()

# Function for updating scroll region
def configure_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Bind the configure event to update scroll region
scrollable_frame.bind("<Configure>", configure_scroll_region)

# Start the Tkinter main loop
root.mainloop()