import customtkinter as ctk
import tkinter as tk

TOP_RIBBON_Y = 50
FRAME_HIGHT = 200

class TopRibbon(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=TOP_RIBBON_Y, corner_radius=0)

        # Add buttons to top ribbon
        self.file_button = FileButton(self)
        self.file_button.pack(side=ctk.LEFT, padx=20)

class FileButton(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master, text="File", command=self.picFile)

    def picFile(self):
        print("fff")
        ctk.filedialog()


        #########################################################

# This class is used to make the top menu bar for the visualizer app
# TODO: There is no custom tkinker widget for this so we will need to format it properly some time.
class TopMenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master=master)

        # Add file menu option
        self.file_menu = FileMenu(self)
        self.add_cascade(
            label="File",
            menu=self.file_menu,
            underline=0
        )

class FileMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master=master, tearoff=0)

        # add menu items to the File menu
        self.add_command(label='New')
        self.add_command(label='Open...')
        self.add_command(label='Close')
        self.add_separator()



class LayoutWrapper(ctk.CTkFrame):
    def __init__(self, master):
        super(master)

class LeftFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="blue")

        
# Creates the visualiser aplication with its basic functionailities
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gnome Visualizer")
        self.geometry("400x150")
        # self.grid_columnconfigure((0, 1), weight=1)

        # self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        # self.button.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        # self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        # self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        # self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
        self.menubar = TopMenuBar(master=self)
        self.config(menu=self.menubar)
        #self.top_ribbon = TopRibbon(self)
        #self.top_ribbon.pack(side=ctk.TOP, fill=ctk.X,)

        self.left_frame = LeftFrame(self)
        self.left_frame.pack(side = ctk.LEFT, fill=ctk.Y)
        
    def button_callback(self):
        print("button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()