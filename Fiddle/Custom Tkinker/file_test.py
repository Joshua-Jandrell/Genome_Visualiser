import customtkinter as ctk

def get_file():
    filename = ctk.filedialog.askopenfilename(title="Select File",filetypes=[("VCF files","*.vcf")])
    print(filename)

app = ctk.CTk()
button = ctk.CTkButton(app,text="fie",command=get_file)
button.pack()
app.mainloop()