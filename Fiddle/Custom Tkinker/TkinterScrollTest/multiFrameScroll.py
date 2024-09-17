# A simple script used to test if a single tkinter scroll frame can be used to scroll multiple panels
from typing import Tuple
import customtkinter as ctk

class DoubleScrollFrame(ctk.CTkFrame):
    # From: https://github.com/TomSchimansky/CustomTkinter/issues/2084
    def __init__(self, master):
        super().__init__(master=master, fg_color="transparent") 

        vscrollbar = ctk.CTkScrollbar(master=self, orientation="vertical", fg_color="transparent", bg_color="transparent")
        vscrollbar.pack(fill="y", side="right", expand=False)

        hscrollbar = ctk.CTkScrollbar(master=self, orientation="horizontal", fg_color="transparent", bg_color="transparent")
        hscrollbar.pack(fill="x", side="bottom", expand=False)

        canvas = ctk.CTkCanvas(self, bd=0,
                               width=300,
                               height=300,
                               highlightthickness=0,
                               yscrollcommand=vscrollbar.set,
                               xscrollcommand=hscrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)

        vscrollbar.configure(command=canvas.yview)
        hscrollbar.configure(command=canvas.xview)

        canvas.xview_moveto = 0
        canvas.yview_moveto = 0
        self.canvas = canvas

        self.interior = interior = ctk.CTkFrame(master=canvas)

        for i in range(20):
            for j in range(20):
                dummy = ctk.CTkFrame(interior, fg_color="blue", width=30, height=30)
                dummy.grid(row=i, column=j, padx=5, pady=5)

        interior.bind("<Configure>", self._configure_interior)

    def _configure_interior(self,event):
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

class App(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self.geometry("600x600")
        top_frame = ctk.CTkScrollableFrame(self, width=300, height=30,orientation="horizontal")
        # populate top frame with dummy blocks
        for i in range(2):
            for j in range(20):
                dummy = ctk.CTkFrame(top_frame, fg_color="blue", width=10, height=10)
                dummy.grid(row=i, column=j, padx=5, pady=5)
        top_frame.grid(row=0, column=1, sticky='ew')
        side_frame = ctk.CTkScrollableFrame(self, width=30, height=10)
        side_frame.grid(row=1, column=0)


        # mind_frame = ctk.CTkScrollableFrame(self, orientation="horizontal vertical")
        centre_window = ctk.CTkFrame(self)
        centre_window.grid(row=1, column=1, sticky='nsew')
        canvas = ctk.CTkCanvas(centre_window, bd=0, highlightthickness=0, 
                                width = 200, height = 300)
        canvas.pack_propagate(0)
        for i in range(20):
            for j in range(20):
                dummy = ctk.CTkFrame(canvas, fg_color="blue", width=10, height=10)
                dummy.grid(row=i, column=j, padx=5, pady=5)
        canvas.pack(expand=True, fill="both")

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        bottom_scroll = ctk.CTkScrollbar(self, orientation="horizontal", command=canvas.yview)
        bottom_scroll.grid(row=3, column=1)
        #bottom_scroll.configure(command=self.scroll_x_cmd)

        test = DoubleScrollFrame(self)
        test.grid(row=4, column=1)

        canvas.configure(xscrollcommand=bottom_scroll.set)

        

    def scroll_x_cmd(self, event, event2):
        print(event)
        print(event2)

if __name__ == "__main__":
    app = App()
    app.mainloop()


    # app = ctk.CTk()
    # app.grid_rowconfigure(0, weight=1)
    # app.grid_columnconfigure(0, weight=1)

    # # create scrollable textbox
    # tk_textbox = ctk.CTkTextbox(app, activate_scrollbars=False)
    # tk_textbox.grid(row=0, column=0, sticky="nsew")

    # # create CTk scrollbar
    # ctk_textbox_scrollbar = ctk.CTkScrollbar(app, command=tk_textbox.yview)
    # ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

    # # connect textbox scroll event to CTk scrollbar
    # tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

    # app.mainloop()


