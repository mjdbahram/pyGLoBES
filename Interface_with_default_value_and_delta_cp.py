#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# colors http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as tm
import tkinter.ttk as ttk
from functools import partial
from tkinter import filedialog

from itertools import count


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter.colorchooser import askcolor

import numpy as np

import time
import os

class main_window:
    def __init__(self, master):
        
        #===================== variables 
        self.shiftdown = 0
        self.ProjName = tk.StringVar()
        self.Experiment = tk.StringVar()
        
        self.lang1 = tk.StringVar()
        self.lang2 = tk.StringVar()
        
        
        #==================== frame maker
        self.master = master
        self.master.title("GLoBES")
        self.master.geometry("500x800")
        self.master.protocol("WM_DELETE_WINDOW", self.exitt)


        self.menu = tk.Menu(self.master)
        self.master.config(menu = self.menu)
        
        self.subm1 = tk.Menu(self.menu)
        self.menu.add_cascade(label='File',menu=self.subm1)
        self.subm1.add_command(label='Exit',command=self.exitt)
        
        self.subm2 = tk.Menu(self.menu)
        self.menu.add_cascade(label='Help',menu=self.subm2)
        self.subm2.add_command(label='About',command=self.abt)
        
        
        #===================== fonts
        self.BIG_FONTS = ('calibri',19,'bold')
        self.NORMAL_FONTS = ('calibri',11)
        
        self.master.option_add("*Font", self.NORMAL_FONTS)
        
        
        #==============================    Globes Logo
        self.homescreenImage = tk.PhotoImage(file='./Logos/globes-logo-small.gif')
        self.homescreenLabel = tk.Label(self.master, image=self.homescreenImage).pack(side = 'top', pady = 5)
        
        #==============================    Window title
        self.label1 = tk.Label(self.master, text="GLoBES Model Config",
                      relief="solid",
                      width=20,
                      borderwidth = 0,
                      font= self.BIG_FONTS)
        self.label1.pack(side = 'top', pady = 5)
        
        # ===========================     project creator
        self.project_creator_field()


        # ===========================     Experiment Selector
        self.selecting_experiment()        
        
        # ===========================     Add Experiment
        self.add_experiment()
        
        
        #=========================== Selecting Parameters
        self.add_parameters()
        
        #=========================== Run Parameters
        self.run_parameters()
        
        #====== run and exit
        RunGlobes(self.master)
        # self.run()
        
        #===== ploting
        Plotter(self.master)



        
    def exitt(self):
        #if tm.askokcancel("Quit", "Do you really wish to quit?"):
            self.master.destroy()

    def abt(self):
        tm.showinfo('About us','RBB')
        
        
    def project_creator_field(self):
        width = 20
        self.label2 = tk.Label(self.master, text ="Project Name",
                         width=width)
        self.label2.place(relwidth=0.3,
                          relheight=0.04,
                          relx=0.1,
                          rely= self.shiftdown + 0.3)
        # md = tk.StringVar()
        self.entry_2 = tk.Entry(self.master, width=width+10, textvar=self.ProjName, bg = 'white')
        
        self.entry_2.place(relwidth=0.4,
                           relheight=0.04,
                           relx=0.48,
                           rely= self.shiftdown + 0.3)
    
            
    def selecting_experiment(self):
        width = 20
        self.label_6 = tk.Label(self.master,
                  text='Experiment')
        self.label_6.place(relwidth=0.3,
                           relheight=0.04,
                           relx=0.1,
                           rely=0.41)

        
                                
        list1 = ['NFstandard', 'D-Chooz_far', 'D-Chooz_near', 'DocPlots','Reactor1','Browse...']       
        self.Experiment.set('Select Experiment')
        self.Experiment.trace("w", self.new_label)
        self.droplist = tk.OptionMenu(self.master, self.Experiment, *list1)
        self.droplist.config(width=width)
        self.droplist.place(relwidth=0.4,
                           relheight=0.05,
                           relx=0.48,
                           rely=0.41)
        
        open_file = Open_File(self.master)
        self.open_button = open_file.open_button
        self.path_entry = open_file.path_entry

                                
    def new_label(self, *args):
        if (self.Experiment.get() == 'Browse...'):
            self.open_button.place(relwidth=0.3,
                               relheight=0.04,
                               relx=0.1,
                               rely= 0.45)
    
            self.path_entry.place(relwidth=0.4,
                               relheight=0.04,
                               relx=0.48,
                               rely= 0.45)
            self.shiftdown = 0.05
            
        else:
            self.open_button.place_forget()
            self.path_entry.place_forget()
            self.shift = 0.0
            
            


            
            
    def add_experiment(self):
        self.sub_check_var = tk.BooleanVar()
        
        def disable_enable_button(button, var):
            button.config(state = tk.NORMAL if var else tk.DISABLED)
            
        self.add_experiment_check = tk.Checkbutton(self.master,
                                                  text='Add Experiment',
                                                  variable=self.sub_check_var,
                                                  command= lambda: disable_enable_button(self.add_experiment_button, self.sub_check_var.get()))
            
        self.add_experiment_check.place(relwidth=0.3,
                                       relheight=0.04,
                                       relx=0.1,
                                       rely=0.5)
    

        
        newpage =  experiment_page()
        newpage.toggle_top()    
        self.add_experiment_button = tk.Button(self.master,
                                               text = 'Add Experiment',
                                               width = 25,
                                               command = newpage.toggle_top)
        
        self.add_experiment_button.config(state = tk.DISABLED)
        self.add_experiment_button.place(relwidth=0.4,
                                       relheight=0.04,
                                       relx=0.48,
                                       rely=0.5)

        
    def new_window(self):        
        self.NewWindow = tk.Toplevel(self.master)
        self.NewWindow.title("Add experiment")
        self.app = experiment_page(self.NewWindow)
    

    def add_parameters(self):
        
        param_page =  parameters_page()
        param_page.toggle_top_params()    
        self.add_params_button = tk.Button(self.master,
                                               text = 'Parameter Setup',
                                               width = 25,
                                               command = param_page.toggle_top_params)

        self.add_params_button.place(relwidth=0.4,
                                       relheight=0.04,
                                       relx=0.25,
                                       rely=0.6)

    def run_parameters(self):
        
        param_page =  running_parameters_page()
        param_page.toggle_top_params()    
        self.add_params_button = tk.Button(self.master,
                                               text = 'Runnig Parameters',
                                               width = 25,
                                               command = param_page.toggle_top_params)

        self.add_params_button.place(relwidth=0.4,
                                       relheight=0.04,
                                       relx=0.25,
                                       rely=0.7)

# exppppppppppppppppppppppppppppppp
class experiment_page(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.row_counter = 1
        self.counter = 1
        self.experiment_num = str(self.counter).zfill(2)
        
        self.hidden_state = False
        self.protocol("WM_DELETE_WINDOW", self.toggle_top)
        
        self.scrollFrame = ScrollFrame(self, 800, 300)
        self.underscrollFrame = UnderScrollFrame(self, 800, 0)

        self.add_button = tk.Button(self.underscrollFrame, text="Add Experiment", command=self.add)
        #self.print_button = tk.Button(self.underscrollFrame, text="Print")#, command=self.print_values)




        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True) 
        self.underscrollFrame.pack(side="bottom", fill=tk.X)#, expand=True) 

        self.add_button.pack(side="left")
        #self.print_button.pack(side="left")


    def add(self):
        item = select_experiment_item(self.scrollFrame.viewPort, self.row_counter, self.experiment_num)
        item.custom_grid()
        self.scrollFrame.move2end()
        self.row_counter += 1
        self.counter += 1
        self.experiment_num = str(self.counter).zfill(2)
        

    def toggle_top(self):
        if self.hidden_state:
            self.deiconify()
            self.hidden_state = False
        else:
            self.withdraw()
            self.hidden_state = True
    

            



class select_experiment_item():
    def __init__(self, master, row_counter, experiment_num):
        self.master = master
        self.lines = []
        self.experiment_num = experiment_num
        self.row_counter = row_counter
        
        open_file = Open_File(self.master)
        self.open_button = open_file.open_button
        self.path_entry = open_file.path_entry


        self.CheckVar = tk.IntVar(value=1)
        self.experiment_checkbox = tk.Checkbutton(self.master, variable=self.CheckVar)
        
        
        # selecting the experiment
        experiment_list = ['NFstandard', 'D-Chooz_far', 'D-Chooz_near', 'DocPlots','Reactor1','Browse...'] 
        self.experiment_var = tk.StringVar(value="Select Experiment")
        self.experiment_var.trace("w", self.new_label)
        self.experiment_menu_button = tk.OptionMenu(self.master, self.experiment_var , self.experiment_var.get(), *experiment_list)
        
        
        line = [self.experiment_checkbox , self.experiment_menu_button]
        self.lines.append(line)
        


    def custom_grid(self):
        c_counter = 1
        for l in self.lines[-1]:
            text = "%s"%self.experiment_num 
            text = text.zfill(2)

            tk.Label(self.master, text = text).grid(row = self.row_counter, column = 0 )
            l.grid(row = self.row_counter, column = c_counter )
            c_counter += 1
            

    
    def new_label(self, *args):
        if (self.experiment_var.get() == 'Browse...'):
            self.open_button.grid(row = self.row_counter , column = 40 )
    
            self.path_entry.grid(row = self.row_counter , column = 50 )
            
        else:
            self.open_button.grid_forget()
            self.path_entry.grid_forget()


        
        
class Open_File:
    def __init__(self, master):
        self.master = master
        self.file_path = ''
        
        self.open_button = tk.Button(master,
               text = 'Open',
               command = self.open_file)
        
        self.v = tk.StringVar(root)#, value = self.file_path)
        self.path_entry = tk.Entry(master, width=40, bg = 'white', textvariable=self.v)
        self.path_entry.xview_moveto(1)

        

        
        
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes = (("ADEL Files", "*.glb")
                                                             ,("All files", "*.*") ))
        
        if self.file_path:  #check if file path is not None or empty
            self.v.set(self.file_path)  
            self.path_entry.xview_moveto(1)
                
            
class ScrollFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent) # create a frame (self)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, borderwidth=0,  width=self.width, height=self.height)   
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel) 
        
        self.viewPort = tk.Frame(self.canvas)   
              
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) 
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview) 
        
        
        
        
        self.canvas.configure(yscrollcommand=self.vsb.set)                      
        self.canvas.configure(xscrollcommand=self.hsb.set) 


        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
                                      
        self.canvas.pack(side="left", fill="both", expand=True)                     
        self.canvas.create_window((4,6), window=self.viewPort, anchor="nw",          
                                  tags="self.viewPort")
 

        self.viewPort.bind("<Configure>", self.onFrameConfigure) 
        
    def move2end(self):
        self.canvas.yview_moveto(1)
        


       


    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1

            self.canvas.yview_scroll(move, "units")
                
                    

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))       


class UnderScrollFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent) # create a frame (self)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, borderwidth=0,  width=self.width, height=self.height)         
        self.viewPort = tk.Frame(self.canvas)
        self.canvas.pack(side="top", fill=tk.X, expand=True)                     



class parameters_page(tk.Toplevel):   
    def __init__(self):
        super().__init__()
        
        self.hidden_state = False
        self.protocol("WM_DELETE_WINDOW", self.toggle_top_params)
        
        canvas_width = 500
        canvas_height = 100
        
        self.canvas_true_values = parameters_canvas(self, tk.NORMAL, 'True', canvas_width, canvas_height)
        self.canvas_test_values = parameters_canvas(self, tk.NORMAL, 'Test', canvas_width, canvas_height)
        
        self.canvas_central_values = parameters_canvas(self,tk.DISABLED, 'Central', canvas_width, canvas_height)
        

        
        
        #self.canvas_central_values_check = parameters_canvas(self, 'Central', canvas_width,canvas_height        
        
        self.canvas_true_values.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_test_values.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_central_values.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    

#************************************
        #********************************8
#*****************************************====================================================================        

    def toggle_top_params(self):
        if self.hidden_state:
            self.deiconify()
            self.hidden_state = False
        else:
            self.withdraw()
            self.hidden_state = True       
       
class running_parameters_page(tk.Toplevel):   
    def __init__(self):
        super().__init__()
        
        self.hidden_state = False
        self.protocol("WM_DELETE_WINDOW", self.toggle_top_params)
        
        canvas_width = 500
        canvas_height = 100
        
        self.canvas_first = running_parameters_canvas(self, tk.NORMAL, 'First Parameter', canvas_width, canvas_height)
        
        self.canvas_second = running_parameters_canvas(self,tk.DISABLED, 'Second Parameter', canvas_width, canvas_height)
        

        
        
        #self.canvas_central_values_check = parameters_canvas(self, 'Central', canvas_width,canvas_height        
        
        self.canvas_first.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas_second.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    

#************************************
        #********************************8
#*****************************************====================================================================        

    def toggle_top_params(self):
        if self.hidden_state:
            self.deiconify()
            self.hidden_state = False
        else:
            self.withdraw()
            self.hidden_state = True   
#========================================================================================        
class parameters_canvas(tk.Frame):
    def __init__(self, parent, state ,  title, width, height):
        super().__init__(parent) # create a frame (self)
        self.title = title
        self.width = width
        self.height = height
        self.canvas_var = tk.BooleanVar()
        self.state = state
        self.recon = False
        
        
        self.canvas = tk.Canvas(self, borderwidth=2, relief = tk.GROOVE, width=self.width, height=self.height)         
        self.viewPort = tk.Frame(self.canvas)
        
        
        if self.title == "Central":
            self.central_check = tk.Checkbutton(self, text="Active",
                                                variable=self.canvas_var,
                                                command= lambda: self.disable_enable_canvas(self.canvas_var.get()))
         
            self.central_check.pack(side=tk.LEFT, fill=tk.Y)
            self.canvas_label = tk.Label(self, text = self.title , bg = 'wheat1').pack(side=tk.TOP ,fill=tk.BOTH, expand = True)

        else:
            self.canvas_label = tk.Label(self, text = self.title , bg = 'wheat1').pack(side=tk.TOP ,fill=tk.BOTH, expand = True)
        self.param(self.recon)
        
    def disable_enable_canvas(self,var):
        if var:
            self.param(recon = True)
        else:
            self.param(recon = False)
            
    def param(self, recon):
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        params_labels(self.canvas,self.title)
        self.theta12 = params_vals(self.canvas, self.state, self.title, "Theta 12", 1, 7, 10, recon)
        self.theta13 = params_vals(self.canvas, self.state, self.title, "Theta 13", 2, 7, 10, recon)
        self.theta23 = params_vals(self.canvas, self.state, self.title, "Theta 23", 3, 7, 10, recon)
        
        self.dm2 = params_vals(self.canvas, self.state, self.title, "dm2-21", 4, 7, 10, recon)
        self.crap1 = params_vals(self.canvas, self.state, self.title, "dm2-3l", 5, 7, 10, recon)
        self.deltacp = params_vals(self.canvas, self.state, self.title, "delta-cp", 6, 7, 10, recon)
        self.crap2 = params_vals(self.canvas, self.state, self.title, "density", 7, 7, 10, recon)
        #params_vals(self.canvas, "Theht",)
        
class running_parameters_canvas(tk.Frame):
    def __init__(self, parent, state ,  title, width, height):
        super().__init__(parent) # create a frame (self)
        self.title = title
        self.width = width
        self.height = height
        self.canvas_var = tk.BooleanVar()
        self.state = state
        self.recon = False
        
        
        self.canvas = tk.Canvas(self, borderwidth=2, relief = tk.GROOVE, width=self.width, height=self.height)         
        self.viewPort = tk.Frame(self.canvas)
        
        
        if self.title == "Second Parameter":
            self.central_check = tk.Checkbutton(self, text="Active",
                                                variable=self.canvas_var,
                                                command= lambda: self.disable_enable_canvas(self.canvas_var.get()))
         
            self.central_check.pack(side=tk.LEFT, fill=tk.Y)
            self.canvas_label = tk.Label(self, text = self.title , bg = 'wheat1').pack(side=tk.TOP ,fill=tk.BOTH, expand = True)

        else:
            self.canvas_label = tk.Label(self, text = self.title , bg = 'wheat1').pack(side=tk.TOP ,fill=tk.BOTH, expand = True)
        self.param(self.recon)
        
    def disable_enable_canvas(self,var):
        if var:
            self.param(recon = True)
        else:
            self.param(recon = False)
            
    def param(self, recon):
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        run_params_labels(self.canvas, self.title, self.state)
        self.theta12 = params_vals(self.canvas, self.state, self.title, "Initial Value", 1, 10, 10, recon)
        self.theta13 = params_vals(self.canvas, self.state, self.title, "Final Value", 2, 10, 10, recon)
        self.theta23 = params_vals(self.canvas, self.state, self.title, "Step size", 3, 10, 10, recon)
        

#============================================================================

class params_labels:
    def __init__(self, canvas,canvas_title): 
        self.canvas = canvas
        
        self.label_param_value = tk.Label(self.canvas, text = "Parameter")
        self.label_param_value.grid(row = 0, column = 0)
        

        self.label_param_value = tk.Label(self.canvas, text = 'Value')
        self.label_param_value.grid(row = 1, column = 0)


        
        # first uncertainty
        if canvas_title == "True":
            self.label_param_value = tk.Label(self.canvas, text = 'Uncertainty')
            self.label_param_value.grid(row = 2, column = 0)
                    
    
            # labels
            self.label_param_value = tk.Label(self.canvas, text = 'Fix or Free')
            self.label_param_value.grid(row = 3, column = 0, rowspan = 2)
            
class run_params_labels:
    def __init__(self,canvas,canvas_title, state): 
        self.canvas = canvas
        self.state = state
        self.label_param_value = tk.Label(self.canvas, text = "Parameter")
        self.label_param_value.grid(row = 0, column = 0)
        

        self.param2run = tk.StringVar()

        list1 = ['Theta12', 'Theta13', 'Theta23', 'dm2-21','dm2-3l', 'delta-cp']       
        self.param2run.set('Select Parameter')
        #self.param2run.trace("w", self.new_label)
        self.droplist = tk.OptionMenu(self.canvas, self.param2run, *list1)
        self.droplist.config(width=20)
        self.droplist.grid(row = 1, column = 0)
        


        
        


class params_vals:
    def __init__(self,canvas, state, canvas_title, title, column, width, height, recon = False):
        self.title = title
        self.canvas = canvas
        self.column = column
        self.width = width
        self.height = height
        self.state = state
        self.recon = recon
        
        value_dict = {'Theta 12':33.82, 'Theta 13':8.61, 'Theta 23':48.3, 'dm2-21':7.39,'dm2-3l':2.523, 'delta-cp':222.0, 'density':1.0}
        uncertainty_dict = {'Theta 12':0.0125, 'Theta 13':0.13, 'Theta 23':1.5, 'dm2-21':0.205,'dm2-3l':0.031, 'delta-cp':33, 'density':0.05}
        
        tk.Grid.rowconfigure(self.canvas, 0, weight=1)
        tk.Grid.columnconfigure(self.canvas, 0, weight=1)
        
        self.label_param_value = tk.Label(self.canvas, text = self.title)
        self.label_param_value.grid(row = 0, column = self.column, sticky='EW')
        
        self.value = tk.StringVar()
        self.entry_param_value = tk.Entry(self.canvas, state = self.state, width=self.width, textvar=self.value, bg='white')
        tk.Grid.columnconfigure(self.canvas, 1, weight=1)
        self.entry_param_value.grid(row = 1, column = self.column, sticky='EW')
        
        """
        self.deg_var = tk.StringVar()
        self.check_deg = tk.Radiobutton(self.canvas, state = self.state, text='Degrees',variable=self.deg_var, value = 'deg')
        tk.Grid.columnconfigure(self.canvas, 2, weight=1)
        self.check_deg.grid(row = 2, column = self.column, sticky='EW')
        
        self.rad_var = tk.StringVar()
        self.check_rad = tk.Radiobutton(self.canvas, state = self.state, text='radian',variable=self.rad_var, value = 'rad')
        tk.Grid.columnconfigure(self.canvas, 3, weight=1)
        self.check_rad.grid(row = 3, column = self.column, sticky='EW')
        """        
        
        
        
        if canvas_title == "True":
            self.param_uncertainty = tk.StringVar()
            self.entry_param_uncertainty = tk.Entry(self.canvas, state = self.state, width=self.width, textvar=self.param_uncertainty, bg='white')
            tk.Grid.columnconfigure(self.canvas, 2, weight=1)
            self.entry_param_uncertainty.grid(row = 2, column = self.column, sticky='EW')
                    
            
            # free or fixed
            self.free_var = tk.BooleanVar()
            self.check_free = tk.Radiobutton(self.canvas, state = self.state, text='Free',variable=self.free_var, value = 'free')
            tk.Grid.columnconfigure(self.canvas, 3, weight=1)
            self.check_free.grid(row = 3, column = self.column, sticky='EW')
            
            self.fix_var = tk.BooleanVar()
            self.check_fixed = tk.Radiobutton(self.canvas, state = self.state, text='Fixed',variable=self.free_var, value = 'fixed')
            tk.Grid.columnconfigure(self.canvas, 4, weight=1)
            self.check_fixed.grid(row = 4, column = self.column, sticky='EW')
        
        if self.recon:
            self.entry_param_value.config(state = tk.NORMAL)
            
        if canvas_title == "True":
            self.entry_param_uncertainty.config(state = tk.NORMAL)

            self.check_free.config(state = tk.NORMAL)

            self.check_fixed.config(state = tk.NORMAL)
            
            
            

            
        if canvas_title == "True" or canvas_title == "Test":
            self.entry_param_value.insert(tk.END, value_dict[self.title])
            
        if canvas_title == "True":
            self.entry_param_uncertainty .insert(tk.END, uncertainty_dict[self.title])
        


#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================
#=======================================================================Guru 
#=======================================================================
#=======================================================================
#=======================================================================

class RunGlobes():
    def __init__(self, master):
        self.master = master
        self.b1 = tk.Button(self.master, text = 'RUN',width=12, bg='brown', fg='white', command = self.new_window).place(relx=0.3, rely=0.8)
        
    def new_window(self):        
        self.NewWindow = tk.Toplevel(self.master)
        self.NewWindow.title("Running")
                
        lbl = ImageLabel(self.NewWindow)
        lbl.pack()
        lbl.load('./Logos/hourglass.gif')
        
        init_time = time.time() 
        tt = ElapsedTime(self.NewWindow, init_time)
        tt.timer()
        
        RunControlButton(self.NewWindow)   
        
class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
            
class  ElapsedTime():
    def __init__(self, master, init_time):
        self.master = master
        self.init_time = init_time
        self.timer_label = tk.Label(self.master, font = ('calibri', 40, 'bold')) 
        self.timer_label.pack()
    
    def timer(self):
        now = time.time() - self.init_time
        h = 0
        m = 0
        s = 0
        if now // 3600 != 0:
            h = int(now // 3600)
            now = now % 3600
        if now // 60 != 0:
            m = int(now // 60)
            now = now % 60

        s = int(now)

        time_string = ":".join([str(h).zfill(2),str(m).zfill(2),str(s).zfill(2)])

        self.timer_label.config(text = time_string) 
        self.timer_label.after(1000, self.timer)
        
class RunControlButton():
    def __init__(self, master):
        self.master = master
        self.stop_button = tk.Button(self.master, text = 'Stop', command = self.stop_running)
        self.stop_button.pack()
        self.open_project_button = tk.Button(self.master, text = 'Open Project', command = self.open_file)
        self.open_project_button.pack()
        
    def open_file(self):
        os.system("xdg-open /home/majido/Desktop/Scons/1/majid1 &") 
        
    def stop_running(self):
        if tm.askokcancel("Quit", "Do you really wish to halt the process?"):
            self.master.destroy()
        
       
class Plotter:
    def __init__(self, master):
        self.master = master
        self.b1 = tk.Button(self.master, text = 'Plot',width=12, bg='brown', fg='white', command = self.new_window).place(relx=0.3, rely=0.9)
        
    def new_window(self):        
        self.NewWindow = tk.Toplevel(self.master)
        self.NewWindow.title("Ploting")
        pp = Ploter(self.NewWindow)
        pp.PlotWidgets()
        
        
        
    
class Ploter:
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    DEFAULT_STYLE = '-'
    def __init__(self, master, size = (5,4), dpi = 100):
        self.master = master
        self.size = size
        self.dpi = dpi
        self.color = self.DEFAULT_COLOR
        self.style = self.DEFAULT_STYLE
        self.fig = Figure(figsize = self.size, dpi=self.dpi)
        self.canvas = FigureCanvasTkAgg(self.fig , master=self.master)
        self.plotsetupFrame = PlotsetupFrame(self.master,300,0)

        self.width = 20
        
        self.ax = self.fig.add_subplot(111)
        self.t = np.arange(0, 3, 0.01)
        self.tf = 2 * np.sin(2 * np.pi * self.t)
        
    def PlotWidgets(self):
        self.plotsetupFrame.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.plotsetupFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        
        
        toolbar = NavigationToolbar2TkAgg(self.canvas, self.master)
        toolbar.pack(side=tk.BOTTOM, anchor = tk.W, fill=tk.BOTH, expand=1)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
       

        
        #=============== Adding Option widgets
        rely = 0.05 
        y_shift = 0.1
        relx_r = 0.3; relx_l = 0.0
        
        num = -0.6
        
        num += 1
        self.plot_title = tk.StringVar()
        self.title_label = tk.Label(self.plotsetupFrame, text ="Plot Title")
        self.title_entry = tk.Entry(self.plotsetupFrame, width=self.width, textvar=self.plot_title, bg='white')
        
        self.title_label.place(relwidth=0.3, relheight=0.05, relx=relx_l, rely= rely + (num)*y_shift)
        self.title_entry.place(relwidth=0.6, relheight=0.05, relx=relx_r, rely= rely + (num)*y_shift)


        num += 1
        self.x_label = tk.StringVar()
        self.xtitle_label = tk.Label(self.plotsetupFrame, text ="X Label")
        self.xlabel_entry = tk.Entry(self.plotsetupFrame, width=self.width, textvar=self.x_label, bg='white')
        
        self.xtitle_label.place(relwidth=0.3, relheight=0.05, relx=relx_l, rely= rely + (num)*y_shift)
        self.xlabel_entry.place(relwidth=0.4, relheight=0.05, relx=relx_r, rely= rely + (num)*y_shift)
        
        #----------- log
        self.x_log = tk.Label(self.plotsetupFrame, text ="Log")
        self.x_log_var = tk.BooleanVar()
        self.x_log_check = tk.Checkbutton(self.plotsetupFrame, variable=self.x_log_var)
        
        self.x_log.place(relx=0.72, rely= rely + (num)*y_shift)
        self.x_log_check.place(relx=0.82, rely= rely + (num)*y_shift)
        
        num += 1
        self.y_label = tk.StringVar()
        self.ytitle_label = tk.Label(self.plotsetupFrame, text ="Y Label")
        self.ylabel_entry = tk.Entry(self.plotsetupFrame, width=self.width, textvar=self.y_label, bg='white')
        
        self.ytitle_label.place(relwidth=0.3, relheight=0.05, relx=relx_l, rely= rely + (num)*y_shift)
        self.ylabel_entry.place(relwidth=0.4, relheight=0.05, relx=relx_r, rely= rely + (num)*y_shift)
        
        #----------- log
        self.y_log = tk.Label(self.plotsetupFrame, text ="Log")
        self.y_log_var = tk.BooleanVar()
        self.y_log_check = tk.Checkbutton(self.plotsetupFrame, variable=self.y_log_var)
        
        self.y_log.place(relx=0.72, rely= rely + (num)*y_shift)
        self.y_log_check.place(relx=0.82, rely= rely + (num)*y_shift)
        
        #print(self.x_log_var)
        num += 1
        
        '''
        self.ytitle_label = tk.Label(self.plotsetupFrame, text ="Major grid")
        self.ytitle_label.place(relwidth=0.3, relheight=0.05, relx=relx_l, rely= rely + (num)*y_shift)
        
        num += 1
        self.major_grid = tk.BooleanVar()
        self.major_grid_check = tk.Checkbutton(self.plotsetupFrame, variable=self.major_grid,
                                               command= lambda: self.GridWidgets(self.plotsetupFrame, self.major_grid.get(), num, rely, y_shift))
        self.major_grid_check.place(relx=0.1, rely= rely + (num)*y_shift)
        self.GridWidgets(self.plotsetupFrame, None, num,  rely, y_shift)
        '''

        
        self.update_button = tk.Button(self.plotsetupFrame, text = "Update",command = self.ploter).place( relwidth=0.4,
                                                                                      relheight=0.2,
                                                                                      relx=relx_r,
                                                                                      rely= rely + (num)*y_shift)
 

        

        self.LineWidgets(self.plotsetupFrame,None, 6,  rely, y_shift)
            
        
        self.ploter()
        

    def GridWidgets(self,master, state, num, rely, y_shift):
        
        x_shift = 0.45
        x_init = 0.3

            
        list1 = ["Solid", "Dashed", "Dash-dot", 'Dotted'] 
        self.grid_line_style = tk.StringVar()
        self.grid_line_style.set('Grid Style')
        self.grid_line_style.trace("w", self.choose_style)
        droplist = tk.OptionMenu(master, self.grid_line_style, *list1)
        droplist.config(width=10)
        droplist.place(relx= x_init, rely= rely + (num)*y_shift)
        
        color_button = tk.Button(master = master, text='color',
                                 command = self.choose_color)
        color_button.place(relx=x_init + x_shift, rely= rely + (num)*y_shift)
        
        if state:
            droplist.config(state = tk.NORMAL)
            color_button.config(state = tk.NORMAL)
        else:
            droplist.config(state = tk.DISABLED)
            color_button.config(state = tk.DISABLED)
            



    def LineWidgets(self, master,line_legend, num,  rely, y_shift):
        """
        make this class **********************************
        """
        
        x_shift = 0.45
        x_init = 0.1

        if line_legend != None:
            self.line_lenged_label = tk.Label(master, text =line_legend,)
            self.line_lenged_label.place(relx= x_init, rely= rely + (num)*y_shift)
            x_init += 0.2
            
        list1 = ["Solid", "Dashed", "Dash-dot", 'Dotted'] 
        self.line_style = tk.StringVar()
        self.line_style.set('Line Style')
        self.line_style.trace("w", self.choose_style)
        droplist = tk.OptionMenu(master, self.line_style, *list1)
        droplist.config(width=10)
        droplist.place(relx= x_init, rely= rely + (num)*y_shift)
        
        color_button = tk.Button(master = master, text='color',
                                 command = self.choose_color)
        color_button.place(relx=x_init + x_shift, rely= rely + (num)*y_shift)
        

    def ploter(self):
        self.ax.clear()
        style = self.style
        self.ax.plot(self.t, self.tf, style , color = self.color)
        
        if self.x_log_var.get():
            self.ax.set_xscale('log')
    
        if self.y_log_var.get():
            self.ax.set_yscale('log')
            
        if self.plot_title.get():
            self.ax.set_title(self.plot_title.get())
            
        if self.x_label.get():
            self.ax.set_xlabel(self.x_label.get())
            
        if self.y_label.get():
            self.ax.set_ylabel(self.y_label.get())

        #self.ax.set_yscale('log')
        self.canvas.draw()
        self.canvas.draw_idle()
        

    def choose_color(self):
        style = self.style
        self.color = askcolor(color=self.color)[1]
        self.ax.plot(self.t, self.tf, style , color = self.color)
        self.canvas.draw_idle()
        
        #self.canvas.draw()
    def choose_style(self, * args):
        if self.line_style.get() == "Solid":
            self.style = '-'
            self.ploter()
        if self.line_style.get() == "Dashed":
            self.style = '--'
            self.ploter()
        if self.line_style.get() == "Dash-dot":
            self.style = '-.'
            self.ploter()
        if self.line_style.get() == "Dotted":
            self.style = ':'
            self.ploter()


         
            

class PlotsetupFrame(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent) # create a frame (self)
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(self, borderwidth=0,  width=self.width, height=self.height)         
        self.viewPort = tk.Frame(self.canvas)
        self.canvas.pack(side=tk.TOP, anchor = tk.NE, fill=tk.X, expand=True)      

        '''
        # ======= 5
        label_5 = tk.Label(self.master,text='Experiment',
                          relief = 'solid',
                          width=20,
                          font=('arial',10,'bold')).place(x=80,y=370)
        list1 = ['NFstandard', 'D-Chooz_far', 'D-Chooz_near', 'DocPlots','Reactor1','Custom..']
        # mod = tk.StringVar()
        droplist = tk.OptionMenu(self.master, Experiment, *list1)
        Experiment.set('Experiment')
        droplist.config(width=15)
        droplist.place(x=250, y=370)
        
        #====== 6
        label_6 = tk.Label(self.master, text='Plot',
                          relief = 'solid',
                          width=20,
                          font=('arial',10,'bold')).place(x=80,y=420)
        c6 = tk.Checkbutton(self.master,text='Show',
                            variable=lang1).place(x=250,y=420)
        
        c61 = tk.Checkbutton(self.master,text='Save',
                            variable=lang2).place(x=340,y=420)
        
        

        ''' 


        


root = tk.Tk()
app = main_window(root)
root.mainloop()

