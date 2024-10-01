import customtkinter as ctk

from customtkinter import ThemeManager

from UI.filePicker import FilePicker

if __name__ == "__main__":
    app = ctk.CTk()
    fp = FilePicker(app)
    fp.pack()
    app.mainloop()
    print(ThemeManager.theme['CTkEntry'])
