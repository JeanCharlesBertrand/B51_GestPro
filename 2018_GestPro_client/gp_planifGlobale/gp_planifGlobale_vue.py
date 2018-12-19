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
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.root.title(self.parent.getNomProjet())
        self.root.iconbitmap('image/tk_logo.ico')
		
        self.couleur500 = "#344955"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#000000"
        self.couleurAccent = "#FAAB1A"
        self.couleurSelection = "#FF4181"
		
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
    
    def insert(self):
        self.lb.insert(0, self.txtInput.get("1.0", END))
        self.liste=self.lb.get(0, END)
        print(self.liste)                
        self.parent.insertIntoPlanif(self.liste) 

    #def prepaInsertList(self):
    #    self.liste=list()
    #    for i in self.lb:
    #        self.liste.append(i)    
    #    return self.liste
    
    def showListeSelect(self):
        self.lb.delete(0,END)
        lista=self.parent.selectFromPlanif()
        if lista is not None:
            for i in lista:
                for n in i:
                    self.lb.insert(END, n)
                    
    def creercadres(self):
        self.mainWindow()

    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=640,height=480,bg=self.couleur500)
        self.canevasplash.pack()
        
    def mainWindow(self):
        # Main Frame
        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TFrame', background=self.couleur500, foreground=self.couleurTexte1)
        self.mainFrame = ttk.Frame(self.root, style='My.TFrame')
        self.mainFrame.pack()
        
        # Frame Title bar
        self.frameTitleBar = ttk.Frame(self.mainFrame)
        self.frameTitleBar.grid(row=0, column=1, padx=15, pady=10)
        self.labelNomProjet = ttk.Label(self.frameTitleBar, text="SÉQUENCE DE DÉVELOPPEMENT", font = ("Arial", 20), background=self.couleur500, foreground=self.couleurAccent)
        self.labelNomProjet.grid(row=0, column=1)
        
        # Input Text 
        self.frameTextInput = ttk.Frame(self.mainFrame)
        self.frameTextInput.grid(row=1, column=1, padx=15, pady=10)
        self.txtInput = Text(self.frameTextInput, width=70, height=2, wrap=WORD, relief=SUNKEN)
        self.txtInput.grid(row=0, column=1)
        
        """
        # Frame Top Buttons
        self.topButtons = ttk.Frame(self.mainFrame, style='My.TFrame')
        self.topButtons.grid(row=1, column=1, pady=25)
        
        self.btn1 = Button(self.topButtons, text="Update", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1)
        self.btn1.grid(row = 0, column = 0, padx=10)
        self.btn2 = Button(self.topButtons, text="Save", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1)
        self.btn2.grid(row = 0, column = 1, padx=10)
        """
        
        # Frame ListBox
        self.listBoxFrame = Frame(self.mainFrame)
        self.listBoxFrame.grid(row=2, column=1)
        
        # ListBox contenant les items
        self.lb=Listbox(self.listBoxFrame, height=30, width=100, selectmode=SINGLE)
        self.lb.grid(row=1, column=0)
        
        #Attach scrollbar to the List
        self.sb1=Scrollbar(self.listBoxFrame)
        self.sb1.grid(row=1, column=1)
        
        #Apply scrollbar to the list
        self.lb.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.lb.yview)
        
        #Frame pour les bouton Move Up et Move Down
        self.frameBottomBar = ttk.Frame(self.mainFrame, style='My.TFrame')
        self.frameBottomBar.grid(row=3, column=1, pady=25)
        
        self.btnAdd = Button(self.frameBottomBar, text="Ajouter", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1,command=self.insert)
        self.btnAdd.grid(row=0, column=0, padx=10)
        self.btnMoveUp = Button(self.frameBottomBar, text="Monter", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1, command = self.moveUp)
        self.btnMoveUp.grid(row=0, column=1, padx=10)
        self.btnMoveDown = Button(self.frameBottomBar, text="Descendre", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1, command = self.moveDown)
        self.btnMoveDown.grid(row=0, column=2, padx=10)
        self.btnRemove = Button(self.frameBottomBar, text="Effacer", font = ("Arial", 12), background=self.couleurAccent, foreground=self.couleurTexte1, command = self.delete)
        self.btnRemove.grid(row=0, column=3, padx=10)
        
        #Add to listbox
        
        self.showListeSelect()
    
    def move(self):
        value = self.lb.get(self.lb.curselection())
        x1 = self.lb.curselection()[0]
        self.lb.selection_clear(x1)
        if x1+1==self.lb.size():
            self.lb.selection_set(0)
        else:
            self.lb.selection_set(x1+1)
            
        
    def delete(self):
        self.lb.delete(self.lb.curselection())
        self.liste=self.lb.get(0, END)
        self.parent.insertIntoPlanif(self.liste) 
        
        self.lb.selection_set(0)
        self.lb.focus_set()  
            
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
            
       
        
        self.liste=self.lb.get(0, END)
        self.parent.insertIntoPlanif(self.liste) 
        
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
            
        self.liste=self.lb.get(0, END)
        self.parent.insertIntoPlanif(self.liste) 
        
        self.lb.selection_set(pos+1, pos+1)
        self.lb.focus_set()  

        
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    