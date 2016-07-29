# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 11:57:47 2016

@author: Lukas Adamowicz
"""

#import numpy as np
from sympy import Eq,sympify,solve
import tkinter
import tkinter.messagebox as tkmb
import tkinter.filedialog as tkfd


class EquationSolver(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent=parent
        self.initialize()
        

    def initialize(self):
        self.grid()
        
        
        self.eqstr = tkinter.StringVar()
        
        eq_lab = tkinter.Label(self,text='Equation: ')
        eq_lab.grid(column=0,row=1,sticky='w')
        
        self.equation = tkinter.Entry(self,width=60,textvariable=self.eqstr,\
                exportselection=0)
        self.equation.insert(0,'Enter Equation with spaces between variables and symbols')
#        self.equation.insert(0,'( T1 - T0 )/ dt = ( u1 - u0 )/ dx')
        self.equation.grid(columnspan=3,column=1,row=1,sticky='w'+'e')
        
        eq_scroll = tkinter.Scrollbar(self,orient='horizontal',\
            borderwidth=5,command=self.__scrollHandler)
        eq_scroll.grid(columnspan=3,column=1,row=2,sticky='w'+'e')
        eq_scroll.config(command=self.equation.xview)
        self.equation.config(xscrollcommand=eq_scroll.set)
        
        frame = tkinter.Frame(self,relief='sunken', height=25,width=200,padx=50)
        frame.grid(column=0,row=0,sticky='w')
        
        self.output = tkinter.Text(self,height=5,width=60,borderwidth=5)
        self.output.grid(columnspan=3,column=1,rowspan = 3, row=4,sticky='w')
        
        output_label = tkinter.Label(self,text = 'Output: ')
        output_label.grid(column=0,row=4,sticky='w')
        
        label1 = tkinter.Label(self,text='Variable to solve for: ')
        label1.grid(column=0,row=3,sticky='w')
        
        solve_button = tkinter.Button(self,text = 'Solve',command = self.SolveButton)
        solve_button.grid(column=2,row=3,sticky='w')
        
        self.solve_for = tkinter.Entry(self)
        self.solve_for.grid(column=1,row=3,sticky='w')
        
        menubar = tkinter.Menu(self)
        file_menu = tkinter.Menu(menubar,tearoff=0)
        file_menu.add_command(label='Import Entry',command = self.ImportEntry)
        file_menu.add_command(label='Export Output',command = self.ExportOutput)
        file_menu.add_command(label='Export Entry',command = self.ExportEntry)
        file_menu.add_command(label='Quit',command = self.quit)
        
        help_menu = tkinter.Menu(menubar,tearoff=0)
        help_menu.add_command(label = 'Help',command = self.HelpButton)
        
        
        view_menu = tkinter.Menu(menubar,tearoff=0)
        self.indexing_options = tkinter.IntVar()
        view_menu.add_checkbutton(label='Indexing Options',\
            variable = self.indexing_options, command = self.ViewIndexOptions)
        
        menubar.add_cascade(label='File',menu=file_menu)
        menubar.add_cascade(label='View',menu=view_menu)
        menubar.add_cascade(label='Help',menu=help_menu)
        self.config(menu=menubar)
        
        #------------Indexing Options-----------
        self.or_lab = tkinter.Label(self,text='Original')
        self.or_lab.grid(column=5,row=1)
        self.or_lab.grid_remove()
        self.ch_lab = tkinter.Label(self,text='New')
        self.ch_lab.grid(column=6,row=1)
        self.ch_lab.grid_remove()
        self.label=dict()
        self.index_or_ent = dict()
        self.index_ch_ent = dict()
        self.ind_ct = 4
        
        self.ind_or = dict()
        self.ind_ch = dict()
        for i in range(self.ind_ct):
            ltxt = 'Index %i: '%i
            self.ind_or[i] = tkinter.StringVar()
            self.ind_ch[i] = tkinter.StringVar()
            
            self.label[i] = tkinter.Label(self,text = ltxt,padx=5)
            self.label[i].grid(column=4,row=i+2)
            self.label[i].grid_remove()
            
            self.index_or_ent[i] = tkinter.Entry(self,width=10,\
                textvariable=self.ind_or[i],exportselection=0)
            self.index_or_ent[i].grid(column=5,row=i+2)
            self.index_or_ent[i].grid_remove()
            
            self.index_ch_ent[i] = tkinter.Entry(self,width=10,\
                textvariable=self.ind_ch[i],exportselection=0)
            self.index_ch_ent[i].grid(column=6,row=i+2)
            self.index_ch_ent[i].grid_remove()
        
        self.apply_button = tkinter.Button(self,text='Apply',command=self.ApplyButton)
        self.apply_button.grid(column=5,row=0)
        self.apply_button.grid_remove()
        
        self.more_ind = tkinter.Button(self,text='+ Index',command=self.MoreInd)
        self.more_ind.grid(column=6,row=0)
        self.more_ind.grid_remove()
        

    def ApplyButton(self):
        #self.solved_var, self.solve_var_str
        self.output.config(state='normal')
        solved_var_ind = self.solved_var
        solve_var_str_ind = self.solve_var_str
        for i in range(self.ind_ct):
            solved_var_ind = solved_var_ind.replace(self.ind_or[i].get(),\
                self.ind_ch[i].get())
            solve_var_str_ind = solve_var_str_ind.replace(self.ind_or[i].get(),\
                self.ind_ch[i].get())
        self.output.delete(1.0,'end')
        self.output.insert('end',solve_var_str_ind+' = ')
        self.output.insert('end',solved_var_ind)
        self.output.config(state='disabled')
    
    def MoreInd(self):
        self.ind_ct+=1
#        self.more_ind.grid(column=6,row=self.ind_ct+2)
#        self.apply_button.grid(column=5,row=self.ind_ct+2)
        self.ind_or[self.ind_ct-1] = tkinter.StringVar()
        self.ind_ch[self.ind_ct-1] = tkinter.StringVar()
        ltxt = 'Index %i:'%int(self.ind_ct-1)
        self.label[self.ind_ct-1] = tkinter.Label(self,text=ltxt)
        self.label[self.ind_ct-1].grid(column=4,row=self.ind_ct+1)
        self.index_or_ent[self.ind_ct-1] = tkinter.Entry(self,width=10,\
            textvariable=self.ind_or[self.ind_ct-1],exportselection=0)
        self.index_or_ent[self.ind_ct-1].grid(column=5,row=self.ind_ct+1)      
        self.index_ch_ent[self.ind_ct-1] = tkinter.Entry(self,width=10,\
            textvariable=self.ind_ch[self.ind_ct-1],exportselection=0)
        self.index_ch_ent[self.ind_ct-1].grid(column=6,row=self.ind_ct+1)        
        
    def ViewIndexOptions(self):
        if self.indexing_options.get() == 0:
            self.apply_button.grid_remove()
            self.more_ind.grid_remove()
            self.or_lab.grid_remove()
            self.ch_lab.grid_remove()
            for i in range(self.ind_ct):
                self.label[i].grid_remove()
                self.index_or_ent[i].grid_remove()
                self.index_ch_ent[i].grid_remove()
        else:
            self.apply_button.grid()
            self.more_ind.grid()
            self.or_lab.grid()
            self.ch_lab.grid()
            for i in range(self.ind_ct):
                self.label[i].grid()
                self.index_or_ent[i].grid()
                self.index_ch_ent[i].grid()
        
    def HelpButton(self):
        help_text = 'Equation solver interface\n' + \
        '-Variables must be seperated from other symbols by spaces\n' + \
        '  -Ex: ( x1 - x2 )/( x4 - x5 ) = 5* x5\n' + \
        '-Equal sign must be surrounded by spaces\n\n' + \
        '-For proper index replacement, use surrounding brackets\n' + \
        '    and commas to ensure wrong indices are not changed\n' + \
        '  -Ex: [j, to [1:-1,'
        tkmb.showinfo(title='Help',message=help_text)
    
    def ExportOutput(self):
        #self.solved_var, self.solve_var_str
        export_file = tkfd.asksaveasfilename(defaultextension='.txt',\
        filetypes=(('Text File','.txt'),('Python File','.py'),('All Files','*.*')))
        
        file = open(export_file,'w')
        file.write(self.solve_var_str+' = ')
        file.write(self.solved_var)
        file.write('\n')
        file.close()
    
    def ExportEntry(self):
        export_file = tkfd.asksaveasfilename(defaultextension='.txt',\
            filetypes=(('Text File','.txt'),('Python File','.py'),('All Files','*.*')))
        
        file = open(export_file,'w')
        file.write(self.equation.get())
        file.write('\n')
        file.close()
        
    def ImportEntry(self):
        import_file = tkfd.askopenfilename()
        
        file = open(import_file,'r')
        entry = file.readline()
        file.close()
        self.equation.delete(0,'end')
        self.equation.insert(0,entry)
        
    def SolveButton(self):
        self.output.config(state='normal')
        self.output.delete(1.0,'end')
        str_equation = self.equation.get()
        self.solve_var_str = self.solve_for.get()
        if ' = ' in str_equation:
            RHS = str_equation.split(' = ')[0]
            LHS = str_equation.split(' = ')[1]
            rhs_split = RHS.split(' ')
            varis = dict()
            rhs_join = []
            count=0
            for item in rhs_split:
                if any(c.isalpha() for c in item) and item not in varis.keys():
                    varis[item] = 'x'+str(count).zfill(3)
                    rhs_join.append(varis[item])
                    count+=1
                elif item in varis.keys():
                    rhs_join.append(varis[item])
                else:
                    rhs_join.append(item)               
            rhs_sym = ' '.join(rhs_join)
            
            lhs_split = LHS.split(' ')
            lhs_join = []
            for item in lhs_split:
                if any(c.isalpha() for c in item) and item not in varis.keys():
                    varis[item] = 'x'+str(count).zfill(3)
                    lhs_join.append(varis[item])
                    count+=1
                elif item in varis.keys():
                    lhs_join.append(varis[item])
                else:
                    lhs_join.append(item)
            lhs_sym = ' '.join(lhs_join)            
            
            sym_full_eq = Eq(sympify(rhs_sym),sympify(lhs_sym))
            
            if self.solve_var_str in varis.keys():
                solve_var = varis[self.solve_var_str]
            else:
                self.output.insert('end','Variable to solve for not in equation')
                return
            self.solved_var = str(solve(sym_full_eq,solve_var)[0])
            for key in varis.keys():
                self.solved_var = self.solved_var.replace(varis[key],key)
            self.output.insert('end',self.solve_var_str+' = ')
            self.output.insert('end',self.solved_var)
        else:
            self.output.insert('end','Not an equation')
        self.output.config(state='disabled')
    
    def __scrollHandler(self,*L):
        op,howMany = L[0],L[1]
        
        if op=='scroll':
            units=L[2]
            self.equation.xview_scroll(howMany,units)
        elif op =='moveto':
            self.equation.xview_moveto(howMany)
        

#( T1 - T0 )/ dt = ( u1 - u0 )/ dx       
        
if __name__=="__main__":
    app=EquationSolver(None)
    app.title('Equation Solver')
    app.iconbitmap('EquationSolver.ico')
    app.resizable(0,0)
    #app.configure(bg='blue')
    app.mainloop()