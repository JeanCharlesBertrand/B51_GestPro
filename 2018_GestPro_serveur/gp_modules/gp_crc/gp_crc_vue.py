# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp

class Vue():
    def __init__(self,parent,largeur=1200,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        
        #reference X-Y pour fenetres FichesCRC qui poppent
        self.frameX=25
        self.frameY=100

        self.creercadres()
        self.changecadre(self.cadresplash)


#==========================================================================================       
# saisir avec numero idProjet, afficher ce qui existe
# avoir un bouton sauvegarder? verifier que chaque carte est unique par son nom/classe .. ?
# scrollbar, resize
#
#==========================================================================================
        
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
        self.creercadresplash()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=1200,height=1200,bg="#282E3F")

        #scrollbar tests
        self.canevasplash.config(scrollregion=(0,0,1200,1200))
        sbar = ttk.Scrollbar(self.root)
        sbar.config(command=self.canevasplash.yview)                   
        self.canevasplash.config(yscrollcommand=sbar.set)              
        sbar.pack(side=RIGHT, fill=Y)
        
        self.canevasplash.pack(side=LEFT, expand=YES, fill=BOTH)       
        self.creerBoutons()
      
    def creerBoutons(self):
        btnAjouterFiche=Button(                                    
            text="Ajouter Fiche",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.creerFrameFiche)
        
        btnEnregistrerFiche=Button(                                    
            text="Enregistrer Fiche",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.saisirFiche)

        self.canevasplash.create_window(500,20,window=btnAjouterFiche,width=250,height=40)
        self.canevasplash.create_window(800,20,window=btnEnregistrerFiche,width=250,height=40)

    def creerFrameFiche(self):
        self.frameFiche = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg='lightgray')
        
        self.frameFiche.place (x=self.frameX, 
            y=self.frameY, 
            width=350, 
            height=250)
        
        self.canevasFiche=Canvas(                                
            self.frameFiche,
            width=350,
            height=250,
            bg='lightgray')                                         
        self.canevasFiche.pack(fill=X, padx=1, pady=1)
        
        self.creerLabelsFiche()
        self.creerChampsTexteFiche()

        if(self.frameX < 800):
            self.frameX += 400
        else:
            self.frameX = 25
            self.frameY += 300


    def creerLabelsFiche(self):
        self.labelClasse = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Classe",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")
        
        self.labelProprietaire = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Proprietaire",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")

        self.labelCollaboration = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Collaboration",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")
        
        self.labelResponsabilites = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Responsabilites",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")
        
        self.labelVariables = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Variables",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")

        self.canevasFiche.create_window(80,20, window = self.labelClasse,width=150, height=15)
        self.canevasFiche.create_window(80,60, window = self.labelProprietaire,width=150, height=15)
        self.canevasFiche.create_window(250,20, window = self.labelCollaboration,width=150, height=15)
        self.canevasFiche.create_window(80,100, window = self.labelResponsabilites,width=150, height=15)
        self.canevasFiche.create_window(250,100, window = self.labelVariables,width=150, height=15)


    def creerChampsTexteFiche(self):
        self.champClasse = Entry()
        self.champProprietaire = Entry()
        self.champCollaboration = Text()
        self.champResponsabilites = Text()
        self.champVariables = Text()

        self.champClasse.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689",justify='center')

        self.champProprietaire.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689",justify='center')

        self.champCollaboration.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689")
        
        self.champResponsabilites.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689")
        
        self.champVariables.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689")
     
        self.canevasFiche.create_window(80,40,window=self.champClasse, width=150, height=20)
        self.canevasFiche.create_window(80,80,window=self.champProprietaire, width=150, height=20)
        self.canevasFiche.create_window(250,60, window = self.champCollaboration,width=150, height=50)
        self.canevasFiche.create_window(85,165, window = self.champResponsabilites,width=160, height=110)
        self.canevasFiche.create_window(250,165, window = self.champVariables,width=160, height=110)
        
        #scroller dans texte
        self.enonceScrollb = ttk.Scrollbar(self.frameFiche, command=self.champResponsabilites.yview)
        self.enonceScrollb.pack()
        self.champResponsabilites['yscrollcommand'] = self.enonceScrollb.set

    def saisirFiche(self):
        classe=self.champClasse.get()
        proprietaire=self.champProprietaire.get()
        collaboration=self.champCollaboration.get()
        responsabilites=self.champResponsabilites.get()
        variables=self.champVariables.get()

        self.parent.saisirFiche(classe,proprietaire,collaboration,responsabilites,variables)
        
    def afficherFiche(self):
        #creer x Fiches, rempli les champs avec les infos de la BD si existe 
        listeFichesCRC=self.parent.lireFiche
        pass
        

    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    
