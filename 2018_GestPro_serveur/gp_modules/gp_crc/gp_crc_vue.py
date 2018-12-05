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

        self.listeFiches =[]
        self.listeFramesFiches=[]
        self.idFiche=0
        
        #reference X-Y pour fenetres FichesCRC qui poppent
        self.frameX=25
        self.frameY=25

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
        self.creerBoutons()
        self.creercadresplash()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=1200,height=1200,bg="#282E3F")

        #scrollbar tests
        #self.canevasplash.config(scrollregion=(0,0,1200,2500))
        #self.sbar = ttk.Scrollbar(self.root)
        #self.sbar.config(command=self.canevasplash.yview)                   
        #self.canevasplash.config(yscrollcommand=self.sbar.set)
        #self.sbar.pack(side=RIGHT, fill=Y)


        self.canevasplash.bind("<MouseWheel>", self.OnMouseWheel)
        
        self.cadresplash.update_idletasks()
        
        self.canevasplash.pack(side=LEFT, expand=YES, fill=BOTH)       

      
    def creerBoutons(self):
        self.frameBoutons = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg='#282E3F')

        #self.frameBoutons.place (x=0,y=0,width=self.largeur,height=100)
        
        self.canevasBoutons=Canvas(                                
            self.frameBoutons,
            width=self.largeur,
            height=100,
            bg='#282E3F')                                         
        self.canevasBoutons.pack(fill=X, padx=1, pady=1)
        
        self.btnAjouterFiche=Button(                                    
            text="Ajouter Fiche",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.creerFiche)
        
        self.btnEnregistrerFiche=Button(                                    
            text="Enregistrer Fiche",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.saisirFiche)

        self.canevasBoutons.create_window(500,70,window=self.btnAjouterFiche,width=250,height=40)
        self.canevasBoutons.create_window(800,70,window=self.btnEnregistrerFiche,width=250,height=40)
        self.frameBoutons.pack()

    def creerFiche(self):
        self.listeFiches.append( Fiche(self,self.frameX,self.frameY))
        self.idFiche+=1

        
    """
    def creerFrameFiche(self):
        self.frameFiche = Frame(
            self.canevasplash, 
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
            
        
        self.listeFiches.append(self.frameFiche)
        
    def OnMouseWheel(self, event):
        #Scroll maison des FIches 
        #self.canevasplash.yview("scroll",event.delta,"units")
        firstFicheY = self.listeFiches[0].winfo_y()+event.delta
                 
        if(self.listeFiches !=None):
            if(firstFicheY <=100):
                for f in self.listeFiches:
                    fx = f.winfo_x()
                    fy = f.winfo_y()
                    f.place(x=fx,y=fy+event.delta,width=350,height=250)


        
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
        #self.enonceScrollb = ttk.Scrollbar(self.frameFiche, command=self.champResponsabilites.yview)
        #self.enonceScrollb.pack()
        #self.champResponsabilites['yscrollcommand'] = self.enonceScrollb.set
    """

    def OnMouseWheel(self, event):
        #Scroll maison des FIches 
        #self.canevasplash.yview("scroll",event.delta,"units")
        
        firstFicheY = self.listeFramesFiches[0].winfo_y()+event.delta
       
        if(self.listeFramesFiches !=None):
            if(firstFicheY <=100):
                for ff in self.listeFramesFiches:
                    fx = ff.winfo_x()
                    fy = ff.winfo_y() + event.delta
                    ff.place(x=fx,y=fy,width=350,height=250)
                    

    
    def saisirFiche(self):
        for f in self.listeFiches:
            f.saisirFiche()
            self.parent.saisirFiche(f.idFiche,f.classe,f.proprietaire,f.collaboration,f.responsabilites,f.variables)
        
    def afficherFiche(self):
        #creer x Fiches, rempli les champs avec les infos de la BD si existe
        listeFichesCRC=self.parent.lireFiche
        pass

    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()


class Fiche():
    def __init__(self,parent,x,y):
        self.parent=parent
        self.x=x
        self.y=y
        self.idFiche=self.parent.idFiche
        self.f_largeur=350
        self.f_hauteur=250
        self.classe=""
        self.proprietaire=""
        self.collaboration=""
        self.responsabilites=""
        self.variables=""
        
        self.creerFrameFiche()

    def creerFrameFiche(self):
        self.frameFiche = Frame(
            self.parent.canevasplash, 
            bd=1, 
            relief=RIDGE,
            bg='lightgray')
        
        self.frameFiche.place (x=self.x, 
            y=self.y, 
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

        if(self.x < 800):
            self.x += 400
            self.parent.frameX += 400
        else:
            self.x = 25
            self.y += 300
            self.parent.frameX = 25
            self.parent.frameY += 300
            
        self.parent.listeFramesFiches.append(self.frameFiche)

        
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
        #self.enonceScrollb = ttk.Scrollbar(self.frameFiche, command=self.champResponsabilites.yview)
        #self.enonceScrollb.pack()
        #self.champResponsabilites['yscrollcommand'] = self.enonceScrollb.set

    def saisirFiche(self):
        self.classe=self.champClasse.get()
        self.proprietaire=self.champProprietaire.get()
        self.collaboration=self.champCollaboration.get('0.0',END)
        self.responsabilites=self.champResponsabilites.get('0.0',END)
        self.variables=self.champVariables.get('0.0',END)
        






