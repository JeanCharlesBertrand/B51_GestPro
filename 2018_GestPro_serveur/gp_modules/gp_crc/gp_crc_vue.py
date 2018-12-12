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
        self.listeBD = self.parent.selectFromCRC()
        self.listeBDFiche = []
        self.idFiche=0
        
        #reference X-Y pour fenetres FichesCRC qui poppent
        self.frameX=25
        self.frameY=25

        self.creercadres()
        self.changecadre(self.cadresplash)
        
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
        
        self.canevasplash.bind("<MouseWheel>", self.OnMouseWheel)
        
        self.cadresplash.update_idletasks()
        
        self.canevasplash.pack(side=LEFT, expand=YES, fill=BOTH)
      
    def creerBoutons(self):
        self.frameBoutons = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg='#282E3F')
        
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
            text="Enregistrer",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.saisirFiche)

        self.btnLireBD=Button(                                    
            text="Importer Fiches du Projet",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.afficherFiches)

        self.canevasBoutons.create_window(300,70,window=self.btnAjouterFiche,width=250,height=40)
        self.canevasBoutons.create_window(600,70,window=self.btnEnregistrerFiche,width=250,height=40)
        self.canevasBoutons.create_window(900,70,window=self.btnLireBD,width=250,height=40)

        self.frameBoutons.pack()

    def creerFiche(self):
        self.listeFiches.append( Fiche(self,self.frameX,self.frameY))
        self.idFiche+=1


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
            f.saisirFicheIndividuelle()
            self.parent.insertIntoCRC(f.idFiche,f.classe,f.proprietaire,f.collaboration,f.responsabilites,f.parametres)
            print(f.idFiche,f.classe,f.proprietaire,f.collaboration,f.responsabilites,f.parametres)  
        
    def afficherFiches(self):

        for liste in self.listeBD:
            self.creerFiche()
            for l in liste:
                self.listeBDFiche.append(l)
            
        for f in self.listeFiches:
            f.idFiche = int(self.listeBDFiche[2])
            f.classe = str(self.listeBDFiche[3])
            f.proprietaire = str(self.listeBDFiche[4])
            f.collaboration = str(self.listeBDFiche[5])
            f.responsabilities = str(self.listeBDFiche[6])
            f.parametres = str(self.listeBDFiche[7])
            f.afficherFiche()

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
        self.parametres=""
        
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
        
        self.labelParametres = Label(
            self.frameFiche, 
            bd=1, 
            relief=RIDGE, 
            text="Parametres",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")

        self.canevasFiche.create_window(80,20, window = self.labelClasse,width=150, height=15)
        self.canevasFiche.create_window(80,60, window = self.labelProprietaire,width=150, height=15)
        self.canevasFiche.create_window(250,20, window = self.labelCollaboration,width=150, height=15)
        self.canevasFiche.create_window(80,100, window = self.labelResponsabilites,width=150, height=15)
        self.canevasFiche.create_window(250,100, window = self.labelParametres,width=150, height=15)


    def creerChampsTexteFiche(self):
        self.champClasse = Entry()
        self.champProprietaire = Entry()
        self.champCollaboration = Text()
        self.champResponsabilites = Text()
        self.champParametres = Text()

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
        
        self.champParametres.config(
            bg='white',
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#4C9689")
     
        self.canevasFiche.create_window(80,40,window=self.champClasse, width=150, height=20)
        self.canevasFiche.create_window(80,80,window=self.champProprietaire, width=150, height=20)
        self.canevasFiche.create_window(250,60, window = self.champCollaboration,width=150, height=50)
        self.canevasFiche.create_window(85,165, window = self.champResponsabilites,width=160, height=110)
        self.canevasFiche.create_window(250,165, window = self.champParametres,width=160, height=110)
        
    def saisirFicheIndividuelle(self):
        self.classe=self.champClasse.get()
        self.proprietaire=self.champProprietaire.get()
        self.collaboration=self.champCollaboration.get('0.0',END)
        self.responsabilites=self.champResponsabilites.get('0.0',END)
        self.parametres=self.champParametres.get('0.0',END)

    def afficherFiche(self):
        self.champClasse.delete(0,END)
        self.champClasse.insert(0,self.classe)
        self.champProprietaire.delete(0,END)
        self.champProprietaire.insert(0,self.proprietaire)
        self.champCollaboration.delete('0.0',self.END)
        self.champCollaboration.insert('0.0',self.collaboration)
        self.champResponsabilites.delete('0.0',END)
        self.champResponsabilites.insert('0.0',self.responsabilites)
        self.champParametres.delete('0.0',END)
        self.champParametres.insert('0.0',self.parametres)
        
        






