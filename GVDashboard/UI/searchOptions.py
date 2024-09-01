# This script contains the search query options to loop from the vcf database

import customtkinter as ctk

SEARCH_PANEL_WIDTH = 200

class SearchPanel(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master=master,)

