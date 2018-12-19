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
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.parent=parent
        self.root.iconbitmap('image/tk_logo.ico')
        self.root.title(self.parent.getNomProjet())
        self.modele=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.cadreactif=None
        self.root.resizable(False, False)

        self.listeFiches =[]
        self.listeFramesFiches=[]
        self.listeBD = self.parent.selectFromCRC()

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
                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=1200,height=1200,bg="#282E3F")
        self.img_logo2 = PhotoImage (file = "image/logo3.png")
        x=300
        y=100
        self.labelTitre = Label(
            self.cadresplash, 
            bd=1, 
            relief=RIDGE, 
            text="Module CRC ",fg="#4C9689",
            font = ("Courier New", 15, "bold"),
            bg="#282E3F")

        self.canevasplash.bind("<MouseWheel>", self.OnMouseWheel)
        
        self.cadresplash.update_idletasks()
        
        self.canevasplash.pack(side=LEFT, expand=YES, fill=BOTH)
        


        #=== LOAD LES FICHES PRESENTES DANS LE PROJET ====
        self.afficherFichesBD()
      
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

        self.labelTitre = Label(
            self.frameBoutons, 
            bd=1, 
            relief=RIDGE, 
            text="Module CRC ",fg="#4C9689",
            font = ("Courier New", 15, "bold"),
            bg="#282E3F")
        
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
        

        self.canevasBoutons.create_window(300,70,window=self.btnAjouterFiche,width=250,height=40)
        self.canevasBoutons.create_window(900,70,window=self.btnEnregistrerFiche,width=250,height=40)
        self.canevasBoutons.create_window(600,30,window=self.labelTitre,width=250,height=40)
        self.frameBoutons.pack()

    def creerFiche(self):
        self.listeFiches.append( Fiche(self,self.frameX,self.frameY))
        self.idFiche+=1

    def OnMouseWheel(self, event):
        #Scroll maison des FIches 
       
        firstFicheY = self.listeFramesFiches[0].winfo_y()+event.delta
       
        if(self.listeFramesFiches !=None):
            if(firstFicheY <=100):
                for ff in self.listeFramesFiches:
                    fx = ff.winfo_x()
                    fy = ff.winfo_y() + event.delta
                    ff.place(x=fx,y=fy,width=350,height=250)

    def recupererListeMembres(self):
        return self.parent.getListeMembres()

    def deleteFromCRC(self,ficheEnlever,idFiche,classe,proprietaire,collaboration,responsabilites,parametres):
        self.listeFiches.remove(ficheEnlever)
        self.parent.deleteFromCRC(idFiche,classe,proprietaire,collaboration,responsabilites,parametres)
        
    def rafraichirApresDelete(self):
        self.saisirFiche()
        
        #self.canevasplash.delete(ALL)
        
        for f in self.listeFiches:
            f.effacerFiche()
            
        self.listeFiches =[]
        self.listeFramesFiches=[]
        self.listeBD = self.parent.selectFromCRC()
        self.frameX=25
        self.frameY=25
        
        self.afficherFichesBD()
        
    def saisirFiche(self):
        for f in self.listeFiches:
            f.saisirFicheIndividuelle()
            self.parent.insertIntoCRC(f.idFiche,f.classe,f.proprietaire,f.collaboration,f.responsabilites,f.parametres)
     
    def afficherFichesBD(self):
        noTempFiche=0
        for liste in self.listeBD:
            f = Fiche(self,self.frameX,self.frameY)
            self.listeFiches.append(f)    
            f.idFiche = int(liste[2])
            f.classe = liste[3]
            f.proprietaire = liste[4]
            f.collaboration = liste[5]
            f.responsabilites = liste[6]
            f.parametres = liste[7]

            if( f.idFiche > noTempFiche):
                noTempFiche = f.idFiche
            f.afficherFiche()
        self.idFiche = noTempFiche+1
    
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
        self.btnQuitter = Button( text='X', command=self.deleteFiche, bg="red", relief = "sunken" )
        self.canevasFiche.create_window( 336,6,window=self.btnQuitter,width=20,height=20 )
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
        
    def deleteFiche(self):
        self.parent.deleteFromCRC(self,self.idFiche,self.classe,self.proprietaire,self.collaboration,self.responsabilites,self.parametres)
        self.parent.listeFramesFiches.remove(self.frameFiche)
        #self.frameFiche = None
        self.frameFiche.destroy()
        self.parent.rafraichirApresDelete()
    def effacerFiche(self):
        self.frameFiche.destroy()
        
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
        
        self.varProprio = StringVar()
        self.fetchValeur =self.varProprio.get()
        
        self.comboProprietaire = ttk.Combobox(self.frameFiche,font=("Courier New", 12, "bold"),textvariable=self.fetchValeur,state='readonly')
        self.comboProprietaire.bind('<<ComboboxSelected>>',self.selectProprietaire)
        self.comboProprietaire['values'] = self.parent.recupererListeMembres()
        self.frameFiche.option_add('*TCombobox*Listbox.font',("Courier New", 12, "bold"))
        self.comboProprietaire.current(0)

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
        self.canevasFiche.create_window(80,80,window=self.comboProprietaire, width=150, height=20)
        self.canevasFiche.create_window(250,60, window = self.champCollaboration,width=150, height=50)
        self.canevasFiche.create_window(85,165, window = self.champResponsabilites,width=160, height=110)
        self.canevasFiche.create_window(250,165, window = self.champParametres,width=160, height=110)
        
    def saisirFicheIndividuelle(self):
        self.classe=self.champClasse.get()
        self.proprietaire=self.comboProprietaire.get()
        self.collaboration=self.champCollaboration.get('0.0',END)
        self.responsabilites=self.champResponsabilites.get('0.0',END)
        self.parametres=self.champParametres.get('0.0',END)


    def afficherFiche(self):
        self.champClasse.delete(0,END)
        self.champClasse.insert(0,self.classe)
        self.champCollaboration.delete('0.0',END)
        self.champCollaboration.insert('0.0',self.collaboration)
        self.champResponsabilites.delete('0.0',END)
        self.champResponsabilites.insert('0.0',self.responsabilites)
        self.champParametres.delete('0.0',END)
        self.champParametres.insert('0.0',self.parametres)

        self.listeMembres= self.parent.recupererListeMembres()
        index = 0
        for i in self.listeMembres:
            if(i[0]==self.proprietaire):
                self.comboProprietaire.current(index)
            index+=1
        
    def selectProprietaire(self,evt):
        self.proprietaire=self.comboProprietaire.get()

    





