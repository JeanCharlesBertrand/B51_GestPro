 #===============================================================================
#     Nom fichier : gp_maquette_vue.py
#     Nom projet: OrmÃda
#     Creation date: 2018/12/10
#     Description: Creation du visuel du module de maquette
#     Creator: Julien Desgagne
#     Version 1.0
#===============================================================================

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
from PIL._imaging import outline

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp

class Vue():
    
    GROSSEUR_CRAYON_DEFAUT = 5.0
    COULEUR_DEFAUT = 'black'
    
    def __init__(self):
        #self.parent = parent
        self.root = tix.Tk()
        #self.root.overrideredirect(1)
        self.root.title("Omada")
        #self.root.iconbitmap('image/tk_logo.ico')
        #self.parent = parent
        #self.modele = None

        self.largeur = 1000        # Largeur de la fenetre de ce module
        self.hauteur = 800        # Hauteur de la fenetre de ce module

        # Calculer les dimensions de la fenetre
        self.lEcran = self.root.winfo_screenwidth() # Largeur de l'ecran de l'usager
        self.hEcran = self.root.winfo_screenheight() # Hauteur de l'ecran de l'usager

        # Calculer les coordonnees X et Y pour la fenetre de ce module
        self.x = (self.lEcran/2) - (self.largeur/2)
        self.y = (self.hEcran/2) - (self.hauteur/2)

        # Definir les dimensions du module et la position sur l'ecran
        self.root.geometry('%dx%d+%d+%d' % (self.largeur,self.hauteur,self.x,self.y))

        # Couleur de theme pour le projet
        self.couleur500 = "#282E3F"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#FFFFFF"
        self.couleurAccent = "#4C9689"
        self.couleurSelection = "#FF4181"

        self.images = {}
        self.creerCadres()
        #self.changercadre(self.frameModule)

    def changeMode(self,cadre):
        if self.modeCourant:
            self.modeCourant.pack_forget()
        self.modeCourant=cadre
        self.modeCourant.pack(expand=1,fill=BOTH)            

    def changeCadre(self,cadre,etend=0):
        if self.cadreActif:
            self.cadreActif.pack_forget()
        self.cadreActif = cadre
        if etend:
            self.cadreActif.pack(expand=1,fill=BOTH)
        else:
            self.cadreActif.pack()

    def creerCadres(self):
        self.creerFrameModule()

    def creerFrameModule(self):
        self.frameModule = Frame(self.root)
        self.frameBarreOutils = Frame(self.frameModule, bg = self.couleurAccent, width = 1000,height = 50)
        self.frameZoneDessin = Frame(self.frameModule, bg = self.couleur500, width = 1000,height = 750)
        self.canevasDessin = Canvas(self.frameZoneDessin, bg = self.couleurTexte1, width = 950, height = 700)

        self.frameModule.pack(fill="both", expand=1)
        self.frameBarreOutils.pack(fill=X)
        self.frameZoneDessin.pack(fill="both", expand=1)
        self.canevasDessin.pack(fill="both", expand=1, padx = 25, pady = 25)

        self.btnCrayon = Button(self.frameBarreOutils, text = 'Crayon',height = 2, command = self.utiliserCrayon)
        self.btnRect = Button(self.frameBarreOutils, text = 'Rect',height = 2, command = self.utiliserRectangle)
        self.btnEfface = Button(self.frameBarreOutils, text = 'Efface',height = 2, command = self.utiliserEfface)
        self.btnChoixCouleur = Button(self.frameBarreOutils, text = 'Couleurs',height = 2, command = self.choisirCouleur)
        self.btnChoisirTrait = Scale(self.frameBarreOutils, from_= 1, to = 10, orient = HORIZONTAL, bg = self.couleur500, 
            fg = self.couleurTexte1, highlightbackground = self.couleur500, activebackground = self.couleurSelection, 
            troughcolor = self.couleurAccent)
        #self.btnRectangle = Button(self.frameBarreOutils, text = 'Rectangle', height = 2, command = self.utiliserRectangle)
        self.btnClear = Button(self.frameBarreOutils, text = 'Clear', height = 2, command = self.clearCanevas)
        self.btnNew = Button(self.frameBarreOutils, text = 'New', height = 2, command = self.nouvelleMaquette)
        
        self.btnNew.grid(row = 0, column = 0)
        self.btnCrayon.grid(row=0, column=1)
        self.btnRect.grid(row=0, column=2)
        self.btnEfface.grid(row = 0, column = 3)
        self.btnChoixCouleur.grid(row=0, column=4)
        self.btnChoisirTrait.grid(row=0, column=5)
        self.btnClear.grid(row = 0, column = 6)
        #self.btnRectangle.grid(row = 0, column = 5)

        self.setup()
        #self.creerVariable()

    def creerVariable(self, parent):
        self.parent = parent
        self.rect_x0 = 0
        self.rect_y0 = 0
        self.rect_x1 = 0
        self.rect_y1 = 0
        self.rectId = None
        self.deplacer = False

    def setup(self):
        self.oldX = None
        self.oldY = None
        self.epaisseurTrait = self.btnChoisirTrait.get()
        self.couleur = self.COULEUR_DEFAUT
        self.effaceActive = False
        self.boutonActif = None
        self.canevasDessin.bind('<Button>', self.dessine)
        self.canevasDessin.bind('<ButtonRelease-1>', self.reset)

    def utiliserCrayon(self):
        self.activerBtn(self.btnCrayon)

    def utiliserRectangle(self):
        self.activerBtn(self.btnRect)

    def choisirCouleur(self):
        self.effaceActive = False
        self.couleur = askcolor(color = self.couleur)[1]

    def utiliserEfface(self):
        self.activerBtn(self.btnEfface, mode_efface = True)

    def clearCanevas(self):
        self.canevasDessin.delete("all")

    def activerBtn(self, choix_bouton, mode_efface = False):
        if self.boutonActif:
            self.boutonActif.config(relief = RAISED)
        choix_bouton.config(relief = SUNKEN)
        self.boutonActif = choix_bouton
        self.effaceActive = mode_efface

    def dessine(self, event):
        print("dessine", self.boutonActif)
        #toto = input("On attend")
        self.epaisseurTrait = self.btnChoisirTrait.get()
        couleur = 'white' if self.effaceActive else self.couleur 
        if self.oldX and self.oldY:
            print("Erreur if", self.boutonActif)
            self.canevasDessin.create_line(    
                self.oldX, self.oldY, event.x, 
                event.y,width = self.epaisseurTrait, fill = couleur,
                capstyle = ROUND, smooth = TRUE, splinesteps = 36)
        self.oldX = event.x
        self.oldY = event.y

    def reset(self, event):
        formeType = self.boutonActif.cget('text')
        self.parent.ajouteForme(self.boutonActif.cget('text'),self.couleur, self.epaisseurTrait,[self.oldX, self.oldY, event.x, event.y] )
        if formeType == 'Rect':
            self.canevasDessin.create_rectangle(self.oldX, self.oldY, event.x, event.y)
        self.boutonActif = None
        self.oldX = None
        self.oldY = None
    
    def nouvelleMaquette(self):      
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 350, 20
        self.frameCreateProject = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg= self.couleur500)
        self.frameCreateProject.place(
            x=self.__winX, 
            y=250, 
            width=300, 
            height=260)
        
        self.labelCreateProject = Label(
            self.frameCreateProject, 
            bd=1, 
            relief=RIDGE, 
            text="Nouvelle maquette",fg= self.couleurAccent,
            font = ("Courier New", 12, "bold"),
            bg = self.couleur500)
        self.labelCreateProject.pack(fill=X, padx=1, pady=1)
        
        self.canevasCreation = Canvas(
            self.frameCreateProject, 
            width=300,
            height=360,
            bg = self.couleur500, 
            bd=0, 
            highlightbackground = self.couleur500)
        self.canevasCreation.pack(fill=X, padx=1, pady=1)
        
        ## When the button is pressed, make sure we get the first coordinates
        self.labelCreateProject.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelCreateProject.bind('<B1-Motion>', self.MoveWindow1)
        self.frameCreateProject.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frameCreateProject.bind('<B1-Motion>', self.MoveWindow1)

        self.compteur = 0
        self.compteurY = 50
        
        #usager, mot de passe, confirmation, email, question de sécurité, réponse sécurité, btnOk
        self.champnomMaquette = Entry()
        self.champnomOrganisation = Entry()
        self.champdescription = Entry()
        
        self.btnConfirmerCreation = Button(
            text="Creer",
            bg = self.couleur500,
            fg = self.couleurTexte1,                            #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = self.couleurAccent,
            command= self.creerMaquette)
        
        
        self.canevasCreation.create_window(                           
            150,180,window=self.btnConfirmerCreation,width=200,height=25)
        self.btnQuitter = Button( text='X', command=self.frameCreateProject.destroy, bg="red", relief = "sunken" )
        self.canevasCreation.create_window( 280,-10,window=self.btnQuitter,width=25,height=22 )
        self.textProjet = "Nom du projet"
        self.textOrganisation = "Nom de la maquette"
        self.textdescription = "Courte description"
        
        self.entryListe = [self.champnomProjet, self.champnomOrganisation, self.champdescription]
        self.texteListe = [self.textProjet, self.textOrganisation, self.textdescription]
        
        for self.entry in self.entryListe:
            self.champsTexte = self.texteListe[self.compteur]
            self.construitEntry(self.entry,self.champsTexte,2)
            self.compteur += 1
            self.compteurY += 43
    
    def creerMaquette(self):
    	nomMaquette = self.champnomMaquette
    	self.parent.creerMaquette(nomMaquette)
    
    def construitEntry(self, entry, champsTexte, v):
        self.entry.insert(0, champsTexte)
        self.entry.bind('<FocusIn>',lambda event: self.on_entry_click(event,entry,champsTexte))
        self.entry.bind('<FocusOut>',lambda event: self.on_focusout(event,entry,champsTexte))
        self.entry.config(
            bg="#4C9689",                                         # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')

        if v==1:
            self.canevasSignIn.create_window(                          
                150,self.compteurY,window=self.entry,width=250,height=25)
        elif v==2:
            self.canevasCreation.create_window(                            
                150,self.compteurY,window=self.entry,width=250,height=25)
        else:
            self.canevasAjouterMembre.create_window(                         
                150,self.compteurY,window=self.entry,width=250,height=25)

    def on_entry_click(self, event,entry, champsTexte):
        if entry.get() == champsTexte:
           entry.delete(0, "end") 
           entry.insert(0, '') 
           entry.config(fg = 'white')

    def on_focusout(self, event, entry, champsTexte):
        if entry.get() == '':
            entry.insert(0, champsTexte)
            entry.config(fg = 'white')
    
    def MoveWindow1(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__lastX = event.x_root
        self.frameCreateProject.place_configure(x=self.__winX)
        
    def startMoveWindow(self,event):
        self.__lastX= event.x_root


if __name__ == '__main__':
    m=Vue()
    m.root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
