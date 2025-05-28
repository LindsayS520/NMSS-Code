#Created by: Lindsay Spence (RES/DSA/AAB Co-Op)
#Associated with: Tina Ghosh (Project Mentor), Luis Betancourt (Branch Cheif), Don Marksberry (Client)
#Date last updated: 10/21/2024
#Purpose: Creates GUI to analyze MACCS plume data to determine proper radioisotope disperion maximum distance.

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from tkinter import ttk, messagebox
from queue import Queue, Empty
from tkinter import *
from tkinter.ttk import *
import sys
from tkinter import font
import project as proj

#Create App class
class LaunchAnalysisApp:
    
    #Initalize certain components/functions
    def __init__(self, root):
        
        
        #Create root and title of App
        self.root = root
        self.root.title("MPD - MACCS Plume Determinant")

        self.filepath = tk.StringVar()
        
        # Make GUI a certain size
        self.root.geometry("1250x700")
        
        # Create GUI components
        self.create_widgets()

    #Function to create the widgets on the GUI
    def create_widgets(self):
        
        # Create a Notebook widget
        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill="both")
        
        #Create frames for the desired amount of tabs
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        
        #Add the frames to the notebook
        notebook.add(tab1, text="   File Entry   ")
        notebook.add(tab2, text= "   PLUM Analytics   ")
        notebook.add(tab3, text= "   OUT Analytics   ")
        notebook.add(tab4, text= "   GAC Analytics   ")
        
        #Label the GUI for the user (title of the program)
        tk.Label(tab1, text= "MPD - MACCS Plume Determinate")
        tk.Label(tab2, text = "MPD - MACCS Plume Determinate")
        tk.Label(tab3, text = "MPD - MACCS Plume Determinate")
        tk.Label(tab4, text = "MPD - MACCS Plume Determinate")
        
        #Init input file type to 0 (aka .plum file)
        self.file_type = tk.IntVar(value = 0)
        
        #Create and place radio button for input file type
        tk.Label(tab1, text="Input File Type:").grid(row=1, column = 0, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text=".plum File", variable=self.file_type, value = 0, command=self.update_file_selection).grid(row=2, column = 2, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text=".out File", variable=self.file_type, value = 1, command=self.update_file_selection).grid(row=2, column = 3, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text=".gac File", variable=self.file_type, value = 2, command=self.update_file_selection).grid(row=2, column = 4, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text=".txt File", variable=self.file_type, value = 3, command=self.update_file_selection).grid(row=2, column = 5, padx=10, pady=5, sticky='e')

        # Create frames for different file selections
        self.plum_frame = tk.Frame(tab1)
        self.gac_frame = tk.Frame(tab1)
        self.out_frame = tk.Frame(tab1)
        self.txt_frame = tk.Frame(tab1)

        # Initialize file path variables
        self.filepath_plum = tk.StringVar()
        self.filepath_gac = tk.StringVar()
        self.filepath_out = tk.StringVar()
        self.filepath_txt = tk.StringVar()

        # PLUM file selection widgets
        tk.Label(self.plum_frame, text="Select PLUM File:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        tk.Label(tab1, text="*", fg="red").grid(row=3, column=0, sticky="w")
        tk.Entry(self.plum_frame, textvariable=self.filepath_plum, width=50).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.plum_frame, text="Browse", command=self.browse_fileplum).grid(row=3, column=2, padx=10, pady=5)

        # GAC file selection widgets
        tk.Label(self.gac_frame, text="Select GAC File:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        tk.Label(tab1, text="*", fg="red").grid(row=3, column=0, sticky="w")
        tk.Entry(self.gac_frame, textvariable=self.filepath_gac, width=50).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.gac_frame, text="Browse", command=self.browse_filegac).grid(row=3, column=2, padx=10, pady=5)

        # OUT file selection widgets
        tk.Label(self.out_frame, text="Select OUT File:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        tk.Label(tab1, text="*", fg="red").grid(row=3, column=0, sticky="w")
        tk.Entry(self.out_frame, textvariable=self.filepath_out, width=50).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.out_frame, text="Browse", command=self.browse_fileout).grid(row=3, column=2, padx=10, pady=5)

        # TXT file selection widgets
        tk.Label(self.txt_frame, text="Select TXT File:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        tk.Label(tab1, text="*", fg="red").grid(row=3, column=0, sticky="w")
        tk.Entry(self.txt_frame, textvariable=self.filepath_txt, width=50).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.txt_frame, text="Browse", command=self.browse_filetxt).grid(row=3, column=2, padx=10, pady=5)

        # Initialize the selection
        self.update_file_selection()
        
        self.windRoseChoice = tk.IntVar(value = 1) # Sets default value of choice to Yes for now
        
        # Create frames for different windrose selection
        self.WndRose_frame = tk.Frame(tab1)
        self.noWndRose_frame = tk.Frame(tab1)
        self.zoom_amount_frame = tk.Frame(tab1)
        
        # Wind Rose plot for time integrated ground concentracion at the end of the simulation 
        tk.Label(tab1, text="Create time integrated ground concetration wind rose at end of simulation (.gac only): ").grid(row=4, column = 0, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text="Yes", variable=self.windRoseChoice, value = 0, command=self.update_windrose_selection).grid(row=4, column = 1, padx=10, pady=5, sticky='e')
        tk.Radiobutton(tab1, text="No", variable=self.windRoseChoice, value = 1, command=self.update_windrose_selection).grid(row=4, column = 2, padx=10, pady=5, sticky='e')

        self.zoom = tk.IntVar(value = 0)

        tk.Label(self.WndRose_frame, text = "Zoom Type: ").grid(row=6, column=0, columnspan=1, pady=5)
        tk.Radiobutton(self.WndRose_frame, text="Zoom In", variable = self.zoom, value=2, command = self.update_zoom_entry).grid(row=6, column=3, columnspan=1, pady=5)
        tk.Radiobutton(self.WndRose_frame, text="Zoom Out", variable = self.zoom, value=1, command = self.update_zoom_entry).grid(row=6, column=2, columnspan=1, pady=5)
        tk.Radiobutton(self.WndRose_frame, text="No Zoom", variable = self.zoom, value=0, command=self.update_zoom_entry).grid(row=6, column=1, columnspan=1, pady=5)

        tk.Label(self.zoom_amount_frame, text = "Zoom amount: ").grid(row = 6, column = 5, columnspan=1, pady = 5)
        self.zoom_val = tk.Entry(self.zoom_amount_frame).grid(row = 6, column = 6, columnspan = 2, pady=5)
        
        
        style = Style()
        style.configure('TButton', font =
                    ('TkDefaultFont', 10, 'bold'),
                            borderwidth = '4')
        
        
        style.map('TButton', foreground = [('active', '!disabled', 'green')],
                            background = [('active', 'black')])
        runa1 = Button(tab1, text="Run Analysis", command=self.analysis).grid(row=10, column=1, columnspan=3, pady=5)
        
        
        #Start of Tab2 (PLUM Analytics) widgets
        tk.Label(tab2, text='PLEASE ONLY USE THIS TAB IF A .plum FILE or _plum.txt FILE WAS USED', fg = 'blue', font = ('TkDefaultFont', 12, "bold")).grid(row = 0, column = 2, padx = 10, pady = 10)
        
        tk.Label(tab2, text='Longitude and latitude extracted from file: ').grid(row = 1, column = 0)
        
        tk.Label(tab2, text='Spatial Endpoint Distances').grid(row = 2, column = 0)
        
        #tk.Label(tab2, )
        
        #Start of Tab2 (PLUM Analytics) widgets
        tk.Label(tab3, text='PLEASE ONLY USE THIS TAB IF A .out FILE or _out.txt FILE WAS USED', fg = 'blue', font = ('TkDefaultFont', 12, "bold")).grid(row = 0, column = 2, padx = 10, pady = 10)
        
        
        #Start of Tab2 (PLUM Analytics) widgets
        tk.Label(tab4, text='PLEASE ONLY USE THIS TAB IF A .gac FILE or _gac.txt FILE WAS USED', fg = 'blue', font = ('TkDefaultFont', 12, "bold")).grid(row = 0, column = 2, padx = 10, pady = 10)
        
        
    def getEndPtDist(self):
        print('parse file through the end point distance')
        
#Function to browse possible txt files
    def browse_fileplum(self):
        
        # Open file dialog and set the selected file path to the entry
        filepath = filedialog.askopenfilename(filetypes=[("PLUM files", "*.plum")])
        if filepath:
            self.filepath_plum.set(filepath)
            self.file_type.set(0)
            self.update_file_selection()

#Function to browse possible txt files
    def browse_filegac(self):
        
        # Open file dialog and set the selected file path to the entry
        filepath = filedialog.askopenfilename(filetypes=[("GAC files", "*.gac")])
        if filepath:
            self.filepath_gac.set(filepath)
            self.file_type.set(2)
            self.update_file_selection()

#Function to browse possible txt files
    def browse_fileout(self):
        
        # Open file dialog and set the selected file path to the entry
        filepath = filedialog.askopenfilename(filetypes=[("OUT files", "*.out")])
        if filepath:
            self.filepath_out.set(filepath)
            self.file_type.set(1)
            self.update_file_selection()

#Function to browse possible txt files
    def browse_filetxt(self):
        
        # Open file dialog and set the selected file path to the entry
        filepath = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])
        if filepath:
            self.filepath_txt.set(filepath)
            self.file_type.set(3)
            self.update_file_selection()

#Function to update the file selection option (txt, plum, out, gac)
    def update_file_selection(self):
        
        # Show or hide frames based on the selected file type
        if self.file_type.get() == 0:
            self.plum_frame.grid(row=3, column=0, columnspan=3, pady=5)
            self.gac_frame.grid_forget()
            self.out_frame.grid_forget()
            self.txt_frame.grid_forget()
        elif self.file_type.get() == 1:
            self.out_frame.grid(row=3, column=0, columnspan=3, pady=5)
            self.plum_frame.grid_forget()
            self.gac_frame.grid_forget()
            self.txt_frame.grid_forget()
        elif self.file_type.get() == 2:
            self.gac_frame.grid(row=3, column=0, columnspan=3, pady=5)
            self.plum_frame.grid_forget()
            self.out_frame.grid_forget()
            self.txt_frame.grid_forget()
        else:
            self.txt_frame.grid(row=3, column=0, columnspan=3, pady=5)
            self.plum_frame.grid_forget()
            self.out_frame.grid_forget()
            self.gac_frame.grid_forget()


    def update_windrose_selection(self):
        
        # Show or hide frames based on the selected file type
        if self.windRoseChoice.get() == 0:
            self.WndRose_frame.grid(row=6, column=0, columnspan=3, pady=5)
            self.noWndRose_frame.grid_forget()
        elif self.windRoseChoice.get() == 1:
            #self.noWndRose_frame.grid(row=6, column=0, columnspan=3, pady=5)
            self.WndRose_frame.grid_forget()


    def update_zoom_entry(self):
        
        if self.zoom.get() == 1 or self.zoom.get() == 2:
            self.zoom_amount_frame.grid(row = 6, column = 4, columnspan=5, pady = 5, sticky = 'w')
        elif self.zoom.get() == 0:
            self.zoom_amount_frame.grid_forget()

    def analysis(self):
        
        # Show loading window
        self.show_loading_window()

        # Create a queue to communicate with the main thread
        self.queue = Queue()
        
        if self.zoom.get() == 0:
            self.zoom_val = 0

        #Line that creates folder to keep all figures in if user currently doesn't have one.
        proj.makeFolders()
        
        if self.file_type.get() == 0:
            proj.functionCalls(self.filepath_plum.get(), self.file_type.get(), self.zoom.get(), self.zoom_val)
        elif self.file_type.get() == 1:
            proj.functionCalls(self.filepath_out.get(), self.file_type.get(), self.zoom.get(), self.zoom_val)
        elif self.file_type.get() == 2:
            proj.functionCalls(self.filepath_gac.get(), self.file_type.get(), self.zoom.get(), self.zoom_val)
        else:
            proj.functionCalls(self.filepath_txt.get(), self.file_type.get(), self.zoom.get(), self.zoom_val)
        self.queue.put("success")
        
        # Periodically check the queue for messages
        self.check_queue()   
        
    def check_queue(self):
        
        #Try/except to check queue.
        try:
            message = self.queue.get_nowait()
        except Empty:
            self.root.after(100, self.check_queue)
            return

        #Close loading window when process is stopped.
        self.close_loading_window()
        if message == "success":
            messagebox.showinfo("Info", "Analysis completed successfully.")
        else:
            messagebox.showerror("Error", f"Failed to read the file: {message}")

    
    #Function to provide a loading window to users so they know that something is happening
    def show_loading_window(self):
        
        #Create and display the loading window.
        self.loading_window = tk.Toplevel(self.root)
        self.loading_window.title("Processing")
        self.loading_window.geometry("200x100")
        tk.Label(self.loading_window, text="Analyzing data...").pack(pady=5)
        self.progress_bar = ttk.Progressbar(self.loading_window, mode="indeterminate")
        self.progress_bar.pack(expand=True)
        self.progress_bar.start()        

    #Function to close the loading window when analysis is completed
    def close_loading_window(self):
        
        #Check that there is a loading window to close, if there is --> close it.
        if hasattr(self, 'loading_window'):
            self.loading_window.destroy()
     

        
#Run main method
if __name__ == "__main__":
    root = tk.Tk()
    app = LaunchAnalysisApp(root)
    root.mainloop()