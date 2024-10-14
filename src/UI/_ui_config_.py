import customtkinter as ctk

HEADING_SIZE = 14
HEADING_WEIGHT = 'bold'

def get_h1()->ctk.CTkFont:
    return ctk.CTkFont(size=HEADING_SIZE, weight=HEADING_WEIGHT)