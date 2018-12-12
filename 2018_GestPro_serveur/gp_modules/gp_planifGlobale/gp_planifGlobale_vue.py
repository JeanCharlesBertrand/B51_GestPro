# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp

class Vue():
    def __init__(self,parent,largeur=800,hauteur=600):
        self.root=Tk()
        self.root.title(self.parent.getNomProjet())
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.creercadres()
        
    def changemode(self,cadre):
        if self.modecourant:
            self.modecourant.pack_forget()
        self.modecourant=cadre
        self.modecourant.pack(expand=1,fill=BOTH)            

    def changecadre(self,cadre,etend=0):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        if etend:
            self.cadreactif.pack(expand=1,fill=BOTH)
        else:
            self.cadreactif.pack()
    
        
    def creercadres(self):
        self.mainWindow()

                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=640,height=480,bg="#282E3F")
        self.canevasplash.pack()
        
    def mainWindow(self):
        # Main Frame
        self.mainFrame = ttk.Frame(root)
        self.mainFrame.pack()
        
        # Barre de bouton du haut
        self.frameTitleBar = ttk.Frame(self.mainFrame)
        self.frameTitleBar.pack()
        self.btn1 = ttk.Button(self.frameTitleBar, text="Update")
        self.btn1.grid(row = 0, column = 0)
        self.btn2 = ttk.Button(self.frameTitleBar, text="Save")
        self.btn2.grid(row = 0, column = 1)
        
        # Label titre
        self.frameSequenceDev = ttk.Frame(self.mainFrame)
        self.frameSequenceDev.pack()
        self.txtTache = ttk.Label(self.frameSequenceDev, text="Séquence de développement")
        self.txtTache.grid(row=0, column=0)
        
        # ListBox contenant les items
        self.lb=Listbox(self.frameSequenceDev, height=20, width=50, selectmode=EXTENDED)
        #self.lb.grid(row=1, column=0, rowspan=6,columnspan=2)
        self.lb.grid(row=1, column=0)
        
        #Attach scrollbar to the List
        self.sb1=Scrollbar(self.frameSequenceDev)
        self.sb1.grid(row=1, column=1)
        
        #Apply scrollbar to the list
        self.lb.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.lb.yview)
        
        
        #Frame pour les bouton Move Up et Move Down
        self.frameBottomBar = ttk.Frame(self.mainFrame)
        self.frameBottomBar.pack()
        
        self.btnMoveUp = ttk.Button(self.frameBottomBar, text="Move Up", command = self.moveUp)
        self.btnMoveUp.grid(row=0, column=0)
        self.btnMoveDown = ttk.Button(self.frameBottomBar, text="Move Down", command = self.moveDown)
        self.btnMoveDown.grid(row=1, column=0)
        
        #Add to listbox
        self.lb.insert(0, "Tâche 1")
        self.lb.insert(1, "Tâche 2")
        self.lb.insert(2, "Tâche 3")
        self.lb.insert(3, "Tâche 4")
        self.lb.insert(4, "Tâche 5")
        self.lb.insert(5, "Tâche 6")
        self.lb.insert(6, "Tâche 7")
    
    def move(self):
        value = self.lb.get(self.lb.curselection())
        x1 = self.lb.curselection()[0]
        self.lb.selection_clear(x1)
        if x1+1==self.lb.size():
            self.lb.selection_set(0)
        else:
            self.lb.selection_set(x1+1)
            
    def listItemSelection(self):
        selection = self.lb.curselection()
        print(selection)
        return selection
        
    def moveUp(self):
        posList = self.lb.curselection()
        # exit if the list is empty
        if not posList:
            return
    
        for pos in posList:
            # skip if item is at the top
            if pos == 0:
                continue
            text = self.lb.get(pos)
            self.lb.delete(pos)
            self.lb.insert(pos-1, text)
            
        self.lb.selection_set(pos-1, pos-1)
        self.lb.focus_set()
        
    def moveDown(self):
            posList = self.lb.curselection()
            # exit if the list is empty
            if not posList:
                return
        
            for pos in posList:
                # skip if item is at the top
                if pos == 0:
                    continue
                text = self.lb.get(pos)
                self.lb.delete(pos)
                self.lb.insert(pos+1, text)
                
            self.lb.selection_set(pos+1, pos+1)
            self.lb.focus_set()    

        
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    