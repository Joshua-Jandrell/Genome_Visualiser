
        
        #Position heading Textbox:
        self.position_headingLabel = ctk.CTkLabel(self.content, text=" Genome Position Range", justify="center", height=_height)
        self.position_headingLabel.grid(row=0, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
        #Textbox:
        self.position_startLabel = ctk.CTkLabel(self.content, text="From:", width=_width_fromto, height=_height)
        self.position_startLabel.grid(row=1, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w") #
        #input field:
        self.input_pos_min = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.position_start = ctk.CTkEntry(self.content, textvariable=self.input_pos_min, width= _width, height=_height) #begin_posrange=self.input_pos_start)
        self.position_start.grid(row=1, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") #padx=0, pady=0, 
        #Textbox:
        self.position_minstartLabel = ctk.CTkLabel(self.content, text=(min_pos,"(min)"), width=_width_fromto, height=_height)
        self.position_minstartLabel.grid(row=1, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        #Next row:
        #Textbox:
        self.position_endLabel = ctk.CTkLabel(self.content, text="To:", width=_width_fromto, height=_height) #, compound="top", justify="left", anchor="w")
        self.position_endLabel.grid(row=2, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w")
        #input field:
        self.input_pos_max = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.position_end = ctk.CTkEntry(self.content,textvariable=self.input_pos_max, width= _width, height=_height) # end_posrange=self.input_pos_end)
        self.position_end.grid(row=2, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") 
        #Textbox:
        self.position_maxendLabel = ctk.CTkLabel(self.content, text=(max_pos,"(max)"), width=_width_fromto, height=_height)
        self.position_maxendLabel.grid(row=2, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        # Add traces to read in position input values:
        self.input_pos_min.trace_add(mode="write", callback=self.read_in_pos)
        self.input_pos_max.trace_add(mode="write", callback=self.read_in_pos)
        
        
      ####### quality range:   ##############
        dw = self.get_datawrap()
        min_pos, max_pos = dw.get_file_pos_range()   ##############   REDO
        
        #Quality heading Textbox:
        self.quality_headingLabel = ctk.CTkLabel(self.content, text="Variant Quality Range", justify="center", height=_height)
        self.quality_headingLabel.grid(row=3, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
        #Textbox:
        self.quality_startLabel = ctk.CTkLabel(self.content, text="From:", width=_width_fromto, height=_height)
        self.quality_startLabel.grid(row=4, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w") #
        #input field:
        self.input_qual_min = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.quality_start = ctk.CTkEntry(self.content, textvariable=self.input_qual_min, width=_width, height=_height) #begin_posrange=self.input_pos_start)
        self.quality_start.grid(row=4, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") #padx=0, pady=0, 
        #Textbox:
        self.quality_minstartLabel = ctk.CTkLabel(self.content, text=("0 (min)"), width=_width_fromto, height=_height)
        self.quality_minstartLabel.grid(row=4, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        #Next row:
        #Textbox:
        self.quality_endLabel = ctk.CTkLabel(self.content, text="To:", width=_width_fromto, height=_height) #, compound="top", justify="left", anchor="w")
        self.quality_endLabel.grid(row=5, column=0,columnspan=1, padx=_entry_padx, pady=_pady, sticky="w")
        #input field:
        self.input_qual_max = ctk.StringVar(value="-") # A custom tkinter variable that can be linked to a UI input element 
        self.quality_end = ctk.CTkEntry(self.content,textvariable=self.input_qual_max, width= _width, height=_height) # end_posrange=self.input_pos_end)
        self.quality_end.grid(row=5, column=1, columnspan=1, padx=_padx_entrybox, pady=_pady, sticky="w") 
        #Textbox:
        self.quality_maxendLabel = ctk.CTkLabel(self.content, text=("100 (max)"), width=_width_fromto, height=_height)
        self.quality_maxendLabel.grid(row=5, column=2, columnspan=1, padx=_padx_lastcol, pady=_pady, sticky="w")
        
        # Add traces to read in sample quality input values:
        self.input_qual_min.trace_add(mode="write", callback=self.read_in_qual)
        self.input_qual_max.trace_add(mode="write", callback=self.read_in_qual)

     ###### Sort options:    ##############
     #Sort heading Textbox:
        self.quality_headingLabel = ctk.CTkLabel(self.content, text="Sort Samples by :", justify="center", height=_height)
        self.quality_headingLabel.grid(row=6, column=0, columnspan=3, padx=_padx_head, pady=_pady, sticky="ew")
    
     # Quality and Population Radio Buttons:
        self.set_sort_mode = ctk.IntVar(value=int(SortMode.BY_POSITION))

        self.positionRadioButton = ctk.CTkRadioButton(self.content, text="Position\n(low to high)", variable=self.set_sort_mode, value=SortMode.BY_POSITION, command=self.set_dw_sortmode, width=50, height=_height)
        self.positionRadioButton.grid(row=7, column=0, padx=_padx_entrybox, pady=_pady, sticky="w")
        
        self.qualityRadioButton = ctk.CTkRadioButton(self.content, text="Quality\n(100 to 0)", variable=self.set_sort_mode, value=SortMode.BY_QUALITY, command=self.set_dw_sortmode, width=50, height=_height)
        self.qualityRadioButton.grid(row=7, column=1, padx=_padx_entrybox, pady=15, sticky="w")

        # self.populationRadioButton = ctk.CTkRadioButton(self, text="Population\n(alphabetically)", variable=self.set_sort_mode, value=SortMode.BY_POPULATION, command=self.set_dw_sortmode)
        # self.populationRadioButton.grid(row=7, column=1, padx=5, pady=5, sticky="w")
        
        #Sort heading Textbox:
        self.instruct_headingLabel = ctk.CTkLabel(self.content, text="Click the Plot button to apply filter options.", justify="center", fg_color='light green')
        self.instruct_headingLabel.grid(row=9, column=0, columnspan=3, padx=_padx_lastcol, pady=_pady, sticky="ew")