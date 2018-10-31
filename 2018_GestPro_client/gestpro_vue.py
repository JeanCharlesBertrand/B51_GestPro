#===============================================================================
# 	Nom fichier : gestpro_vue.py
#	Ormàda
# 	Creation date: 2018/10/22
#	Description: Création du GUI et des éléments visuel du projet 
#	Creator: Julien Desgagné
#	Version 1.0
#===============================================================================

# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
import signal

#===============================================================================
# 	Description: Classe principale d'affichage
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

class Vue():
    def __init__(self,parent,monip,largeur=200,hauteur=200):
        self.root=tix.Tk()
        self.root.title("Omada")
        self.root.iconbitmap('image/tk_logo.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.monip=monip
        self.parent=parent
        self.modele=None
        self.nom=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.modes={}
        self.modecourant=None
        self.cadreactif=None
        self.creercadres()
        self.changecadre(self.frameLogin)

#===============================================================================
# 	Description: Aucune utilité dans le code actuel. À retiré  
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h50 
#===============================================================================

    #def changemode(self,cadre):
        #if self.modecourant:
        #    self.modecourant.pack_forget()
        #self.modecourant=cadre
        #self.modecourant.pack(expand=1,fill=BOTH)

#===============================================================================
# 	Description: Change le frame actif. Efface le frame actuel et le remplace
#				 par le frame passé en paramètre.
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h48 
#===============================================================================

    def changecadre(self,cadre,etend=0):
        if self.cadreactif:
            self.cadreactif.pack_forget()
        self.cadreactif=cadre
        if etend:
            self.cadreactif.pack(expand=1,fill=BOTH)
        else:
            self.cadreactif.pack()

#===============================================================================
# 	Description: Affiche la liste des modules présent dans le dossier du projet.
#				 Cette fonction est appelé dans le controlleur par la fontion
#				 loginclient().
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def chargercentral(self,rep):
        for i in rep:
            self.listemodules.insert(END,i)
        self.changecadre(self.cadrecentral)

#===============================================================================
# 	Description: Créer les différents frames utilisés dans le projet 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================
        
    def creercadres(self):
        self.creerFrameLogin()
        self.creercadresplash()
        self.creercadrecentral()

#===============================================================================
# 	Description: Création du frame de login pour l'usager
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def creerFrameLogin(self):
        self.frameLogin = Frame(self.root)						# Création frameLogin
        self.canevasLogin=Canvas(								# Ajout d'un canvas de le frame
            self.frameLogin,
            width=600,
            height=400,
            bg="#282E3F")										# Couleur de fond [Bleu-gris]
        self.img_logo2 = PhotoImage (file = "image/logo3.png")	# Importer image logo
        x = 300                                     			# Position x,y de l'image sur canevas
        y = 100                                     
        self.canevasLogin.create_image (						# Dessiner logo sur le canevas
        	x, y, image = self.img_logo2)
        self.canevasLogin.pack()
        self.nomsplash=Entry(									# Champs entré no.1
            bg="#4C9689",										# Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')					# Couleur de texte [blanc]
        
        self.nomsplash.insert(0, "username")					# Placeholder dans le champs no.1
        self.ipsplash=Entry(									# Champs entré no.2
            bg="#4C9689",										# Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center',					# Couleur de texte [blanc]
            show="*")											# Remplace le texte par des '*'
        
        self.ipsplash.insert(0, "password")						# Placeholder password
        btnConnecter=Button(									# Création bouton connection
            text="Connecter au serveur",
            bg="#4C9689",										# Couleur bouton [cyan]
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.loginClient2)			# Couleur de texte [blanc]
        btnInscription=Button(                                    # Création bouton connection
            text="S'inscrire",
            bg="#282E3F",                                       # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.frameQuiBouge)           # Couleur de texte [blanc]
        self.canevasLogin.create_window(						# Dessiner no.1 sur canevas
        	300,175,window=self.nomsplash,width=250,height=40)
        self.canevasLogin.create_window(						# Dessiner no.2 sur canevas
        	300,225,window=self.ipsplash,width=250,height=40)	
        self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
        	300,300,window=btnConnecter,width=250,height=40)
        self.canevasLogin.create_window(                        # Dessiner bouton connecter sur canevas
            300,350,window=btnInscription,width=250,height=40)
        
#===============================================================================
# 	Description: 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def creercadresplash(self):									
        self.cadresplash=Frame(self.root)						# Création frameLogin
        self.canevasplash=Canvas(								# Ajout d'un canvas de le frame
            self.cadresplash,
            width=600,
            height=400,
            bg="#282E3F")
        self.img_logo = PhotoImage (file = "image/logo3.png")
        x = 300                                     
        y = 100                                     
        self.canevasplash.create_image (
            x, y, image = self.img_logo)
        self.canevasplash.pack()
        self.nomsplash=Entry(
            bg="#4C9689",
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        
        self.nomsplash.insert(0, "jmd")
        self.ipsplash=Entry(
            bg="#4C9689",
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        
        self.ipsplash.insert(0, self.monip)
        #self.balIp=tix.Balloon(self.cadresplash,state="balloon")
        #self.balIp.bind_widget(self.canevasplash,msg="identifiez vous et indiquez l'adresse du serveur")
        btnConnecter=Button(
            text="Connecter au serveur",
            bg="#4C9689",
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.loginclient)
        btninscription=Button(
                text="Inscription",
                bg="#4C9689",
                relief = "raised",
                font = ("Courier New", 12, "bold"),
                fg = "#dbdbdb",command=self.afficherChampsInscription)
        self.canevasplash.create_window(300,341,window=btninscription,width=250,height=40)
        self.mpsplash=Entry(
            bg="#4C9689",
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        self.mpsplash.insert(0, "*****")
        self.canevasplash.create_window(300,135,window=self.mpsplash,width=250,height=40)
        self.canevasplash.create_window(300,175,window=self.nomsplash,width=250,height=40)
        self.canevasplash.create_window(300,225,window=self.ipsplash,width=250,height=40)
        self.canevasplash.create_window(300,300,window=btnConnecter,width=250,height=40)

    def afficherChampsInscription(self): #Est déclenchée par le bouton Inscription

        '''Tous les champs déclarés ici sont temporaires et vont être remplacés par l'interface 
        de Julien. Ça serait pratique de garder les noms =)'''
        self.champIdentifiant = Entry(self.canevasplash, bg="pink") #Champ identifiant TEMPORAIRE
        self.canevasplash.create_window(500,100,window=self.champIdentifiant,width=100,height=20)
        self.champMotDePasse = Entry(show='*')
        self.canevasplash.create_window(500,130,window=self.champMotDePasse,width=100,height=20)
        self.champConfirmMotDePasse = Entry(show='*')
        self.canevasplash.create_window(500,160,window=self.champConfirmMotDePasse,width=100,height=20)
        self.champCourriel = Entry(self.canevasplash, bg="pink")
        self.canevasplash.create_window(500,190,window=self.champCourriel,width=100,height=20)        
        btnconfirmer=Button(
            text="Confirmer",
            bg="#4C9689",
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.inscrireClient)
        self.canevasplash.create_window(500,220,window=btnconfirmer,width=100,height=20)

#===============================================================================
# 	Description: 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/23 - 9h15 
#===============================================================================
    
    def creercadrecentral(self):
        self.cadrecentral=Frame(self.root)
        self.canevacentral=Canvas(
            self.cadrecentral,
            width=1200,
            height=800,
            bg="#282E3F")                           #Bleu-gris
        self.canevacentral.pack()
        
        self.listemodules=Listbox(
            bg="#282E3F",                           #Bleu-gris
            borderwidth=0,
            relief=FLAT,
            width=20,
            height=6,
            fg = "#dbdbdb",                         #texte blanc
            font = ("Courier New", 12, "bold"),
            highlightbackground= "#282E3F")         #Contour bleu-gris
        self.ipcentral=Entry(bg="pink")
        self.ipcentral.insert(0, self.monip)
        btnConnecter=Button(
            text="Requerir module",
            bg="#4C9689",                           #Cyan
            fg = "#dbdbdb",                         #texte blanc
            justify='center',
            font = ("Courier New", 12, "bold"),
            command=self.requetemodule)
        self.canevacentral.create_window(
            300,
            150,
            window=self.listemodules)
        self.canevacentral.create_window(
            300,
            250,
            window=btnConnecter,
            width=250,
            height=40)
        
        btnquitproc=Button(
            text="Fermer dernier module",
            bg="#4C9689",                           #Cyan
            fg = "#dbdbdb",                         #texte blanc
            justify='center',
            font = ("Courier New", 12, "bold"),
            command=self.closeprocess)

        btnMandat = Button(
        	text="Mandat",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnAnalyse = Button(
        	text="Analyse",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnCasUsage = Button(
        	text="Cas usage",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnScenario = Button(
        	text="Scenario",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnInventaire = Button(
        	text="Inventaire",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command= null)
        btnMaquette = Button(
        	text="Maquette",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnCRC = Button(
        	text="CRC",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnModelisation = Button(
        	text="Modelisation",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        btnTimePlaner = Button(
        	text="Time planner",
        	bg="#282E3F",
        	fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 15, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
            #command=none)
        
        self.canevacentral.create_window(80,10,window=btnMandat,width=150,height=15)
        self.canevacentral.create_window(80,25,window=btnAnalyse,width=150,height=15)
        self.canevacentral.create_window(80,40,window=btnCasUsage,width=150,height=15)
        self.canevacentral.create_window(80,55,window=btnScenario,width=150,height=15)
        self.canevacentral.create_window(80,70,window=btnInventaire,width=150,height=15)
        self.canevacentral.create_window(80,85,window=btnMaquette,width=150,height=15)
        self.canevacentral.create_window(80,100,window=btnCRC,width=150,height=15)
        self.canevacentral.create_window(80,115,window=btnModelisation,width=150,height=15)
        self.canevacentral.create_window(80,130,window=btnTimePlaner,width=150,height=15)
        self.canevacentral.create_window(300,300,window=btnquitproc,width=250,height=40)

#===============================================================================
# 	Description: 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def closeprocess(self):
        self.parent.fermerprocessus()

    def requetemodule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requetemodule(mod)
        
    def loginclient(self):
        ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
        identifiant=self.nomsplash.get() # noter notre identifiant
        motDePasse = self.mpsplash.get() #Lit le mot de passe
        connexionValide = True #Vérifier si les champs sont remplis
        '''Tous les print() qui suivent devrait être changés pour des Label+createwindow
            à coté/sous le champ correspondant dans le UI'''

        if not identifiant:
            print("Veuillez entrer un identifiant")
            connexionValide = False
        if not motDePasse:
            print("Veuillez entrer un mot de passe")
            connexionValide = False
        if connexionValide:
            self.parent.loginclient(ipserveur,identifiant, motDePasse)

    def inscrireClient(self):
        if self.validerInformations(): #Si les champs ont été remplis
            ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
            self.parent.inscrireSiDisponibles(ipserveur, self.identifiant, self.courriel, self.mp1 )#Envoie à client_main

    def validerInformations(self):#S'assure que les champs sont remplis + '@' et '.' ds courriel
        self.identifiant = self.champIdentifiant.get()
        self.mp1 = self.champMotDePasse.get()
        self.mp2 = self.champConfirmMotDePasse.get()
        self.courriel = self.champCourriel.get()
        infosValides = True
        
        if self.identifiant is "":
            print("Veuillez vous choisir un identifiant.")
            
        if self.mp1 != self.mp2:
            print("Les passwords entres sont differents")#Changer ces print pour des Label qui s'affichent à côté/sous les champs
            infosValides = False
            
        if ('@' not in self.courriel) or ("." not in self.courriel):
            print("Veuillez saisir un courriel valide.")
            infosValides = False

        if self.mp1 is "":
            print("Veuillez saisir un mot de passe.")
            infosValides = False
        return infosValides
        #    if self.parent.serveur.inscrireSiDisponibles(self.identifiant, self.courriel):
        #        self.parent.serveur.setMotDePasse(self.identifiant, self.mp1)
        #        print("Inscrit!")

    def loginClient2(self):
        self.frameLogin.pack_forget()
        self.changecadre(self.cadresplash)

    def fermerfenetre(self):
        # Ici, on pourrait mettre des actions a faire avant de fermer (sauvegarder, avertir etc) 
        self.parent.fermefenetre()

    def frameQuiBouge(self):    
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 300, 20
        self.frameSignIn = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg="#282E3F")
        self.frameSignIn.place(
            x=self.__winX, 
            y=20, 
            width=300, 
            height=360)
        
        self.labelSignIn = Label(
            self.frameSignIn, 
            bd=1, 
            relief=RIDGE, 
            text="Inscription",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")
        self.labelSignIn.pack(fill=X, padx=1, pady=1)
        
        self.canevasSignIn = Canvas(
            self.frameSignIn, 
            width=300,
            height=360,
            bg="#282E3F", 
            bd=0, 
            highlightbackground ="#282E3F")
        self.canevasSignIn.pack(fill=X, padx=1, pady=1)
        
        ## When the button is pressed, make sure we get the first coordinates
        self.labelSignIn.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelSignIn.bind('<B1-Motion>', self.MoveWindow)
        self.frameSignIn.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frameSignIn.bind('<B1-Motion>', self.MoveWindow)

        #usager, mot de passe, confirmation, email, question de sécurité, réponse sécurité, btnOk
        self.nomUsager = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        self.motDePasse = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center',show="*")
        self.confirmationMDP = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center',show="*")
        self.email = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        self.questionSecurite = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        self.reponseQuestion = Entry(
            bg="#4C9689",                                       # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        btnConfirmerInscription = Button(
            text="S'inscrire",
            bg="#282E3F",
            fg = "#dbdbdb",                         #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")

        self.canevasSignIn.create_window(                        
            150,50,window=self.nomUsager,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,90,window=self.motDePasse,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,130,window=self.confirmationMDP,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,170,window=self.email,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,210,window=self.questionSecurite,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,250,window=self.reponseQuestion,width=250,height=25)
        self.canevasSignIn.create_window(                        
            150,280,window=btnConfirmerInscription,width=200,height=25)


    def startMoveWindow(self, event):
    ## When the movement starts, record current root coordinates
        self.__lastX= event.x_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        ## Use root coordinates to compute offset for inside window coordinates
        self.__winX += event.x_root - self.__lastX
        #self.__winY += event.y_root - self.__lastY
        ## Remember last coordinates
        self.__lastX = event.x_root
        ## Move inside window
        self.frameSignIn.place_configure(x=self.__winX)

    
if __name__ == '__main__':
    m=Vue(0,"jmd","127.0.0.1")
    m.root.mainloop()
    
