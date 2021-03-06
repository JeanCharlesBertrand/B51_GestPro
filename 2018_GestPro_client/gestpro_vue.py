  #===============================================================================
#     Nom fichier : gestpro_vue.py
#     Orma da
#     Creation date: 2018/10/22
#     Description: Creation du GUI et des elements visuel du projet 
#     Creator: Julien Desgagne
#     Version 1.0
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
#     Description: Classe principale d'affichage
#     Creator: Julien Desgagne
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================

class Vue():
    def __init__(self,parent,monip,largeur=200,hauteur=200):
        self.parent=parent
        self.root=tix.Tk()
        self.root.title("Omada")
        self.root.iconbitmap('image/tk_logo.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.parent.fermefenetre)

        self.couleur500 = "#344955"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#000000"
        self.couleurAccent = "#FAAB1A"
        self.couleurSelection = "#FF4181"

        self.monip=monip
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
        self.erreurAjout=None
        self.root.resizable(False, False)


#===============================================================================
#     Description: cadre temporaire pour tester les fonctionnalitÃ©s
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30
#===============================================================================    

    def creerFrameSelectProjet(self):
        self.frameSelectProjet = Frame(self.root)                         # CrÃ©ation frameSelectProjet
        self.canevasSelectProjet=Canvas(                                # Ajout d'un canvas de le frame
            self.frameSelectProjet,
            width=600,
            height=400,
            bg=self.couleur500)
        self.canevasSelectProjet.pack()

        self.listeProjets=Listbox(
            bg=self.couleurAccent,                            #Bleu-gris
            borderwidth=0,
            relief=FLAT,
            width=25,
            height=8,
            fg = self.couleurTexte1,                            #texte blanc
            font = ("Courier New", 12, "bold"),
            highlightbackground= self.couleur500)
        
        btnSelection=Button(                                    # CrÃ©ation bouton connection
            text="Selection Projet",
            bg=self.couleurAccent,                                             # Couleur bouton [cyan]
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,command=self.requeteProjet)
        
        btnCreation=Button(                                       # CrÃ©ation bouton connection
            text="Creer un projet",
            bg=self.couleur500,                                        # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,command=self.frameQuiBougeCreationProjet)           # Couleur de texte [blanc]
        
        self.canevasSelectProjet.create_window(
            300,
            150,
            window=self.listeProjets)
            
        self.canevasSelectProjet.create_window(                           # Dessiner bouton connecter sur canevas
            300,270,window=btnSelection,width=250,height=40)
        
        self.canevasSelectProjet.create_window(                           # Dessiner bouton connecter sur canevas
            300,315,window=btnCreation,width=250,height=40)

#===============================================================================
#     Description: valider et get infos pour creation projet
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30
#===============================================================================    

    def validerInformationsCreationProjet(self):
        self.nomProjet = self.champnomProjet.get()
        self.nomOrganisation = self.champnomOrganisation.get()
        self.description = self.champdescription.get()
         
        infosValides = True
        
        if self.nomProjet is "" or self.nomProjet == self.textProjet:
            infosValides=False
            print("Nom de projet invalide")
        
        if self.nomOrganisation == self.textOrganisation:
            self.nomOrganisation=""
            print("1")

        
        if self.description == self.textdescription:
            self.description==""
            print("2")
        
        return infosValides

#===============================================================================
#     Description: valide infos et send modele qui send au serveur
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30
#===============================================================================    
    
    def creerProjet(self):
        if self.validerInformationsCreationProjet(): #Si les champs ont Ã©tÃ© remplis
            if(self.cadreactif==self.frameAccueil):
                self.parent.creerSiDisponibles(self.nomProjet, self.description, self.nomOrganisation, TRUE)#Envoie Ã Â  client_main
            else:
                self.parent.creerSiDisponibles(self.nomProjet, self.description, self.nomOrganisation, FALSE)
 
#===============================================================================
#     Description: Temporaire fenetre pop pour creer projet
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30
#===============================================================================    
    
    def frameQuiBougeCreationProjet(self):      
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 200, 20
        self.frameCreateProject = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg=self.couleur500)
        self.frameCreateProject.place(
            x=self.__winX, 
            y=20, 
            width=300, 
            height=260)
        
        self.labelCreateProject = Label(
            self.frameCreateProject, 
            bd=1, 
            relief=RIDGE, 
            text="Creation du projet",fg=self.couleurAccent,
            font = ("Courier New", 12, "bold"),
            bg=self.couleur500)
        self.labelCreateProject.pack(fill=X, padx=1, pady=1)
        
        self.canevasCreation = Canvas(
            self.frameCreateProject, 
            width=300,
            height=360,
            bg=self.couleur500, 
            bd=0, 
            highlightbackground =self.couleur500)
        self.canevasCreation.pack(fill=X, padx=1, pady=1)
        
        ## When the button is pressed, make sure we get the first coordinates
        self.labelCreateProject.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelCreateProject.bind('<B1-Motion>', self.MoveWindow1)
        self.frameCreateProject.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frameCreateProject.bind('<B1-Motion>', self.MoveWindow1)

        self.compteur = 0
        self.compteurY = 50
        
        #usager, mot de passe, confirmation, email, question de sÃ©curitÃ©, rÃ©ponse sÃ©curitÃ©, btnOk
        self.champnomProjet = Entry()
        self.champnomOrganisation = Entry()
        self.champdescription = Entry()
        
        btnConfirmerCreation = Button(
            text="Creer",
            bg=self.couleur500,
            fg = self.couleurTexte1,                            #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = self.couleurAccent,
            command=self.creerProjet)
        
        self.canevasCreation.create_window(                           
            150,180,window=btnConfirmerCreation,width=200,height=25)
        self.btnQuitter = Button( text='X', command=self.frameCreateProject.destroy, bg="red", relief = "sunken" )
        self.canevasCreation.create_window( 280,-10,window=self.btnQuitter,width=25,height=25 )
        self.textProjet = "Nom du projet"
        self.textOrganisation = "Nom de l'organisation"
        self.textdescription = "Courte description"
        
        self.entryListe = [self.champnomProjet, self.champnomOrganisation, self.champdescription]
        self.texteListe = [self.textProjet, self.textOrganisation, self.textdescription]
        
        for self.entry in self.entryListe:
            self.champsTexte = self.texteListe[self.compteur]
            self.construitEntry(self.entry,self.champsTexte,2)
            self.compteur += 1
            self.compteurY += 43
        
    def MoveWindow1(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__lastX = event.x_root
        self.frameCreateProject.place_configure(x=self.__winX)
    

#===============================================================================
#     Description: prend en selection le nom de projet over dans la liste
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30 
#===============================================================================

    def requeteProjet(self):
        if self.listeProjets.size() > 0:
            try:
                pro=self.listeProjets.selection_get()
                if pro:
                    self.parent.selectionProjet(pro)
            except Exception as e:
                if e:
                    pass
    
#===============================================================================
#     Description: change le cadre et insÃ¨re la liste des projets associÃ©s au membre dans la fenÃªtre de sÃ©lection d'un projet
#     Creator: Guillaume Geoffroy
#     Last modified: 2018/11/04 - 12h30
#===============================================================================    
    
    def chargerSelectProjet(self, liste):
        self.listeProjets.delete(0,'end')
        for i in liste:
            for n in i:
                self.listeProjets.insert(END,n)
        self.changecadre(self.frameSelectProjet)

#===============================================================================
#     Description: Change le frame actif. Efface le frame actuel et le remplace
#                  par le frame passe en parama¨tre.
#     Creator: Julien Desgagne
#     Last modified: 2018/10/22 - 21h48 
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
#     Description: Affiche la liste des modules present dans le dossier du projet.
#                  Cette fonction est appele dans le controlleur par la fontion
#                  loginclient().
#     Creator: Julien Desgagne
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def chargercentral(self):
        #for i in self.parent.serveur.modulesdisponibles:
        #     self.listemodules.insert(END,i)
        self.changecadre(self.frameAccueil)

#===============================================================================
#     Description: Creer les differents frames utilises dans le projet 
#     Creator: Julien Desgagne
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================
        
    def creercadres(self):
        self.creerFrameLogin()
        #self.creercadresplash()
        self.creerFrameAccueil()
        self.creerFrameSelectProjet()

#===============================================================================
#     Description: Création du frame de login pour l'usager
#     Creator: Julien Desgagne
#     Last modified: 2018/11/05 - 8h00
#===============================================================================

    def creerFrameLogin(self):
        self.frameLogin = Frame(self.root)                          # Creation frameLogin
        self.canevasLogin=Canvas(                                 # Ajout d'un canvas de le frame
            self.frameLogin,
            width=600,
            height=400,
            bg=self.couleur500)                                         # Couleur de fond [Bleu-gris]
        self.img_logo2 = PhotoImage (file = "image/logo4.png")      # Importer image logo
        x = 300                                                       # Position x,y de l'image sur canevas
        y = 100 

        self.compteurTexte = 0
        self.compteurLoginY = 175

        self.canevasLogin.create_image (                        # Dessiner logo sur le canevas
            x, y, image = self.img_logo2)
        self.canevasLogin.pack()
        self.nomsplash=Entry(                                     # Champs entre no.1
            bg=self.couleurAccent,                                         # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')                    # Couleur de texte [blanc]
        

        self.loginMDP=Entry(                                    # Champs entre no.2
            bg=self.couleurAccent,                                         # Couleur de fond [cyan]
            relief = "sunken",
            show = '*',
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')                    # Couleur de texte [blanc]
            #show="*")                                              # Remplace le texte par des '*'

        #################################
        #Rajouter ip ici
        self.ipsplash=Entry(
            bg=self.couleurAccent,
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')
        
        #self.ipsplash.insert(0, self.monip)
        #################################
        
                    # Placeholder password
        btnConnecter=Button(                                    # Creation bouton connection
            text="Connecter au serveur",
            bg=self.couleurAccent,                                             # Couleur bouton [cyan]
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,command=self.loginclient)            # Couleur de texte [blanc]
            
        btnInscription=Button(                                        # Creation bouton connection
            text="S'inscrire",
            bg=self.couleur500,                                         # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,command=self.frameQuiBouge)               # Couleur de texte [blanc]
        self.canevasLogin.create_window(                        # Dessiner bouton connecter sur canevas
            300,300,window=btnConnecter,width=250,height=40)
        self.canevasLogin.create_window(                        # Dessiner bouton connecter sur canevas
            290,350,window=btnInscription,width=250,height=40)
            
        ######    AJOUT IP 
        self.canevasLogin.create_window(300,400,window=self.ipsplash,width=250,height=40)
        ######
        self.texteNomSplash = "Identifiant"       
        self.texteLoginMDP = "Mot de passe"
        self.listeConnexion = [self.nomsplash, self.loginMDP, self.ipsplash]
        self.texteListe = [self.texteNomSplash, self.texteLoginMDP, self.monip]

        self.btnOption = Button(relief = FLAT, bg = self.couleur500)
        self.photo = PhotoImage(file = "image/Setting2.png")
        self.btnOption.config(image = self.photo, width = 15, height = 15)

        self.canevasLogin.create_window(570,370, window = self.btnOption)

        for self.entry2 in self.listeConnexion:
            self.champsText2 = self.texteListe[self.compteurTexte]
            self.construitEntryLogin(self.entry2,self.champsText2)
            self.compteurTexte += 1
            self.compteurLoginY += 30

    def construitEntryLogin(self, entry2, champsText2):
        self.entry2.insert(0, champsText2)
        self.entry2.bind('<FocusIn>',lambda event: self.on_entry_click2(event,entry2,champsText2))
        self.entry2.bind('<FocusOut>',lambda event: self.on_focusout2(event,entry2,champsText2))
        self.entry2.config(                                        
            bg=self.couleurAccent,                                         
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')

        self.canevasLogin.create_window(                        
            300,self.compteurLoginY,window=self.entry2,width=250,height=25)

    def on_entry_click2(self, event,entry2, champsText2):
        if entry2.get() == champsText2:
           entry2.delete(0, "end") 
           entry2.insert(0, '') 
           entry2.config(fg = 'white')

    def on_focusout2(self, event, entry2, champsText2):
        if entry2.get() == '':
            entry2.insert(0, champsText2)
            entry2.config(fg = 'white')
        

#===============================================================================
#     Description: 
#     Creator: Julien Desgagne
#     Last modified: 2018/11/05 - 7h25 
#===============================================================================

    def frameQuiBouge(self):    
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 300, 20
        self.frameSignIn = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg=self.couleur500)
        self.frameSignIn.place(
            x=self.__winX, 
            y=20, 
            width=300, 
            height=360)
        
        self.labelSignIn = Label(
            self.frameSignIn, 
            bd=1, 
            relief=RIDGE, 
            text="Inscription",fg=self.couleurAccent,
            font = ("Courier New", 12, "bold"),
            bg=self.couleur500)
        self.labelSignIn.pack(fill=X, padx=1, pady=1)
        
        self.canevasSignIn = Canvas(
            self.frameSignIn, 
            width=300,
            height=360,
            bg=self.couleur500, 
            bd=0, 
            highlightbackground =self.couleur500)
        self.canevasSignIn.pack(fill=X, padx=1, pady=1)
        
        ## When the button is pressed, make sure we get the first coordinates
        self.labelSignIn.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelSignIn.bind('<B1-Motion>', self.MoveWindow)
        self.frameSignIn.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frameSignIn.bind('<B1-Motion>', self.MoveWindow)

        #usager, mot de passe, confirmation, email, question de securite, reponse securite, btnOk
        self.compteur = 0
        self.compteurY = 50

        self.nomUsager = Entry()
        self.motDePasse = Entry( show= '*')
        self.confirmationMDP = Entry(show= '*')
        self.email = Entry()
        self.questionSecurite = Entry()
        self.reponseQuestion = Entry()
        self.btnConfirmerInscription = Button(
            text="S'inscrire",
            bg=self.couleur500,
            fg = self.couleurTexte1,                               #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = self.couleurAccent,
            command=self.inscrireClient)

        self.canevasSignIn.create_window(                          
            150,310,window=self.btnConfirmerInscription,width=200,height=25)
        self.btnQuitter = Button( text='X', command=self.frameSignIn.destroy, bg="red", relief = "sunken" )
        self.canevasSignIn.create_window( 280,-10,window=self.btnQuitter,width=25,height=25 )
        self.textNomUsager = "Nom usager"
        self.textMotDePasse = "Mot de passe"
        self.textEmail = "email@email.com"
        self.textQuestionSecurite = "Entrer une question de securite"
        self.textReponseQuestion = "Entrer votre reponse"

        #self.placeHolderText = 'test'
        self.entryListe = [self.nomUsager, self.motDePasse, self.confirmationMDP, self.email,self.questionSecurite, self.reponseQuestion]
        self.texteListe = [self.textNomUsager, self.textMotDePasse, self.textMotDePasse,self.textEmail,self.textQuestionSecurite, self.textReponseQuestion]

        for self.entry in self.entryListe:
            self.champsTexte = self.texteListe[self.compteur]
            self.construitEntry(self.entry,self.champsTexte,1)
            self.compteur += 1
            self.compteurY += 43
            
        self.erreurIDInvalide = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Veuillez vous choisir un identifiant.")
        self.erreurIDDejaUtilise = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Cet identifiant existe deja , veuillez en choisir un autre")
        self.erreurPWDifferents = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Les passwords entres sont differents.")
        self.erreurCourrielInvalide = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Veuillez saisir un courriel valide.")
        self.erreurCourrielDejaUtilise = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Cet courriel existe deja , veuillez en choisir un autre")
        self.erreurMPInvalide = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Veuillez saisir un mot de passe.")
        self.erreurQSInvalide = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Veuillez saisir une question de securite.")
        self.erreurRSInvalide = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="Veuillez saisir une reponse a la question de securite.")
        self.erreurAutre = Label(self.frameSignIn, fg="red", bg=self.couleur500, height=1, text="")
    
    def construitEntry(self, entry, champsTexte, v):
        self.entry.insert(0, champsTexte)
        self.entry.bind('<FocusIn>',lambda event: self.on_entry_click(event,entry,champsTexte))
        self.entry.bind('<FocusOut>',lambda event: self.on_focusout(event,entry,champsTexte))
        self.entry.config(
            bg=self.couleurAccent,                                         # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')

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

    def startMoveWindow(self,event):
        self.__lastX= event.x_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__lastX = event.x_root
        self.frameSignIn.place_configure(x=self.__winX)

#===============================================================================
#     Description: 
#     Creator: Julien Desgagne
#     Last modified: 2018/10/23 - 9h15 
#===============================================================================
    
    
    def creerFrameAccueil(self):
        self.frameAccueil = Frame(self.root)
        self.frameModule = Frame(self.frameAccueil,bg=self.couleur500, width = 200, height = 800)
        self.frameInfo = Frame(self.frameAccueil,bg=self.couleur500, width = 998, height = 800)
        self.frameBorder = Frame(self.frameAccueil,bg = "black", width = 2, height = 800)

        self.frameModule.grid(row = 0, column = 1, sticky = "nse")
        self.frameBorder.grid(row = 0, column =2, sticky = "ns")
        self.frameInfo.grid(row = 0, column = 3, sticky = "nse")

        self.frameModule.grid_rowconfigure(20, weight = 0)
        self.frameModule.grid_columnconfigure(2, weight =0)
    
    def creerBoutonFrameModule(self):       
        self.canevasModule = Canvas(self.frameModule,bg=self.couleur500,bd=0, highlightthickness=0, width = 200, height = 800)
        self.canevasModule.grid(row = 0, column = 0, sticky = "nsew")
        
        y=70
        cles=[*self.parent.getModulesDisponibles()]
        
        for cle in cles:
            btnX = Button(text=cle,
                          bg=self.couleur500,
                          fg = self.couleurTexte1,                            
                          font = ("Arial", 15),
                          relief="flat",
                          activebackground = self.couleurAccent, 
                          width = 15, 
                          anchor = W)
        
            btnX.bind("<ButtonRelease-1>", self.requeteModule)
            self.canevasModule.create_window(100, y, window=btnX,width=130,height=30)
            y+=30
            
        self.btnCreationSprint  = Button(text = "     Creation sprint", command = self.utilisezCreationSprint)
        self.btnScrum           = Button(text = "     Scrum(s)", command = self.utilisezScrum)
        self.btnProbleme        = Button(text = "     Problème", command = self.utilisezProbleme)
        self.btnDebriefing      = Button(text = "     Debriefing", command = self.utilisezDebriefing)
        self.btnCalendrier      = Button(text = "     Calendrier", command = self.utilisezCalendrier)
        self.btnStats           = Button(text = "     Statistique", command = self.utilisezStatistique)
        self.btnPlanif          = Button(text = " Planification", command = self.utilisezPlanif)
        self.btnImplementation  = Button(text = " Implementation", command = self.utilisezImple)
        self.btnSyntheseStats   = Button(text = " Synthese et stats", command = self.utilisezSynthese)
        self.btnChat            = Button(text = " Chat", command = self.utilisezChat)
        self.btnQuitter         = Button(text = " Quitter", command = self.utilisezQuitter)
        
        self.lblVersion = Label(bd=1, text="Version Alpha 1.92",fg=self.couleurAccent,font = ("Arial", 10),bg=self.couleur500)

        self.listeModule = [self.btnCreationSprint,self.btnScrum,self.btnProbleme,
                            self.btnDebriefing,self.btnCalendrier,self.btnStats]

        self.listeEtapeProjet = [self.btnPlanif, self.btnImplementation, self.btnSyntheseStats, self.btnChat, self.btnQuitter]

        for self.etapeProjet in self.listeEtapeProjet:
            self.creerBtnEtapeProjet(self.etapeProjet)

        for self.module in self.listeModule:
            self.creerBtnModule(self.module)

        self.canevasModule.create_window(100,310, window=self.btnCreationSprint,width=200,height=30)
        self.canevasModule.create_window(100,340, window=self.btnScrum,width=200,height=30)
        self.canevasModule.create_window(100,370, window=self.btnProbleme,width=200,height=30)
        self.canevasModule.create_window(100,400, window=self.btnDebriefing,width=200,height=30)
        self.canevasModule.create_window(100,480, window=self.btnCalendrier,width=200,height=30)
        self.canevasModule.create_window(100,510, window=self.btnStats,width=200,height=30)
        self.canevasModule.create_window(140,790,window=self.lblVersion, width=120, height=30)

        self.canevasModule.create_window(100,30, window=self.btnPlanif,width=200,height=30)
        self.canevasModule.create_window(100,270, window=self.btnImplementation,width=200,height=30)
        self.canevasModule.create_window(100,440, window=self.btnSyntheseStats,width=200,height=30)
        self.canevasModule.create_window(100,550, window=self.btnChat,width=200,height=30)
        self.canevasModule.create_window(100,590, window=self.btnQuitter,width=200,height=30)

        self.setup()

    def setup(self):
        self.boutonNumber = 0
        self.boutonActif = None

    def utilisezPlanif(self):
        self.activerBtn(self.btnPlanif)
        self.boutonNumber = 0
        self.canevasInfo.delete("all")
        self.creerInfoProjet()

    def utilisezImple(self):
        self.activerBtn(self.btnImplementation)
        self.boutonNumber = 0

    def utilisezSynthese(self):
        self.activerBtn(self.btnSyntheseStats)
        self.boutonNumber = 0

    def utilisezChat(self):
        self.activerBtn(self.btnChat)
        self.boutonNumber = 0

    def utilisezQuitter(self):
        self.activerBtn(self.btnQuitter)
        self.boutonNumber = 0

    def utilisezCreationSprint(self):
        self.activerBtn(self.btnCreationSprint, choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def utilisezScrum(self):
        self.activerBtn(self.btnScrum, choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def utilisezProbleme(self):
        self.activerBtn(self.btnProbleme, choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def utilisezDebriefing(self):
        self.activerBtn(self.btnDebriefing,  choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def utilisezStatistique(self):
        self.activerBtn(self.btnStats, choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def utilisezCalendrier(self):
        self.activerBtn(self.btnCalendrier, choix = True)
        self.underConstruction()
        self.boutonNumber = 1

    def activerBtn(self, choix_bouton, choix = False):
        if self.boutonActif:
            if not choix and self.boutonNumber == 0:
                self.boutonActif.config(relief = FLAT, bg = self.couleur500, fg = self.couleurAccent)
            elif not choix and self.boutonNumber == 1:
                self.boutonActif.config(relief = FLAT, bg = self.couleur500, fg = self.couleurTexte1)
            elif choix and self.boutonNumber == 0:
                self.boutonActif.config(relief = FLAT, bg = self.couleur500, fg = self.couleurAccent)
            elif choix and self.boutonNumber == 1:
                self.boutonActif.config(relief = FLAT, bg = self.couleur500, fg = self.couleurTexte1)

        choix_bouton.config(relief = SUNKEN, bg = self.couleurAccent, fg = self.couleurTexte2)
        self.boutonActif = choix_bouton

    def creerBtnModule(self, module):
        self.module.config(
            bg=self.couleur500,
            fg = self.couleurTexte1,                            
            font = ("Arial", 15),
            relief="flat",
            activebackground = self.couleurAccent, 
            width = 15, 
            anchor = W)

    def creerBtnEtapeProjet(self,etapeProjet):
        self.etapeProjet.config(
            bg=self.couleur500,
            fg = self.couleurAccent,                            
            justify='left',
            font = ("Arial", 16),
            relief="flat",
            activebackground = self.couleurAccent, 
            width = 15,
            anchor = W)

    def creerInfoProjet(self): 
        self.canevasInfo = Canvas(self.frameInfo, bg=self.couleur500,bd=0, highlightthickness=0, width = 998, height = 800)
        self.canevasInfo.grid(row = 0, column = 0, sticky = "nsew")

        self.nomProjet = "Project name"
        self.date = "2018/12/21"
        self.sprintNumber = 1
        self.timeRemaining = "2 Days 18h"
        nomProjet = self.parent.getNomProjet()

        self.lblNomProjet           = Label(text = nomProjet[0], bg = self.couleur500, fg = self.couleurAccent, font = ("Arial", 25, "bold"))
        self.lblDeadline            = Label(text = "Ajouter: ", fg = self.couleurAccent)
        self.lblDate                = Label(text = self.date, fg = self.couleurTexte1)
        self.lblMember              = Label(text = "Membres du projet:", fg = self.couleurAccent)
        self.lblTimer               = Label(text = "Time left before the end of the Sprint #" + str(self.sprintNumber), fg = self.couleurAccent)
        self.lblTimeLeft            = Label(text = self.timeRemaining, fg = self.couleurTexte1)

        btnCreationP=Button(                                       # CrÃ©ation bouton connection
            text="+",
            bg= self.couleur500,                                        # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1, command=self.frameQuiBougeCreationProjet)
               
        def changerProjet(*args):
            self.nom1=self.v.get()
            #self.nom1=self.nom1[2:-3]
            self.parent.selectionProjet(self.nom1)
          
        self.listeOptions=list()
        tata = self.parent.selectProjetDuMembre()
        for k in tata:
            for g in k:
                self.listeOptions.append(g)
        
        #print (self.listeOptions
        self.v = StringVar()
        x=self.parent.getNomProjet()
        x=x[0]
        self.v.set(x)
        self.v.trace("w", changerProjet)
        self.om = OptionMenu(self.canevasInfo,  self.v, *self.listeOptions)
        self.om.config(font=('calibri',(12)),bg=self.couleurAccent,width=14, highlightcolor = self.couleurAccent )
        
        self.canevasInfo.create_window(870, 102, window = self.om)
        
        self.listeMembres=Listbox(
            bg=self.couleur500,                            #Bleu-gris
            borderwidth=0,
            relief=FLAT,
            width=25,
            height=8,
            fg = self.couleurTexte1,                            #texte blanc
            font = ("Courier New", 12, "bold"),
            highlightthickness = 0,
            highlightcolor = self.couleur500,
            selectbackground = self.couleurAccent)
        
        self.updateListeMembres()
            
        self.entryNomMembreAjout = Entry(                                        
            bg=self.couleurAccent,                                         
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')
        
        self.btnAjouterMembre = Button(                                       # CrÃ©ation bouton connection
                                        text="+",
                                        bg=self.couleur500,                                        # Couleur bouton [cyan]
                                        relief = "flat",
                                        font = ("Courier New", 12, "bold"),
                                        fg = self.couleurTexte1, command=self.ajouterMembre)
        
        self.lblProjectDescription    = Label(text = "Description du projet: ", font = ("Arial", 10),fg = self.couleurAccent,bg=self.couleur500)
        self.lblTeamMsg             = Label(text = "Message de l'equipe: ",font = ("Arial", 10),fg = self.couleurAccent,bg=self.couleur500)
        self.lblUser                = Label(text = '@' + self.parent.monnom, font = ("Arial", 10),fg = self.couleurAccent,bg=self.couleur500)
        self.listeLabelInfo = [self.lblDeadline,self.lblDate,self.lblMember,self.lblTimer,self.lblTimeLeft ] #,self.member1,self.member2,self.member3,self.member4, self.member5,self.member6
        self.canevasInfo.create_window(998/2,45, window = self.lblNomProjet)
        self.canevasInfo.create_window(200,100, window = self.lblMember)
        self.canevasInfo.create_window(200,205, window = self.listeMembres)
        self.canevasInfo.create_window(205,310, window = self.entryNomMembreAjout)
        self.canevasInfo.create_window(315,310, window = self.btnAjouterMembre)
        self.canevasInfo.create_window(205,310, window = self.lblDeadline)
        self.canevasInfo.create_window(110,355, window = self.lblProjectDescription)
        self.canevasInfo.create_window(110,453, window = self.lblTeamMsg)
        self.canevasInfo.create_window(72, 638, window = self.lblUser)

        self.canevasInfo.create_line(40,70,950,70,fill=self.couleurAccent)

        self.btnRefresh = Button(relief = FLAT, bg = self.couleur500)
        self.photoRefresh = PhotoImage(file = "image/refresh.png")
        self.btnRefresh.config(image = self.photoRefresh, width = 15, height = 15, command = self.updateChat)

        #self.canevasInfo.create_window(830,765, window = self.btnRefresh)


        for self.labelInfo in self.listeLabelInfo:
            self.creerLabelInfo(self.labelInfo)

        self.txtDescriptionProjet = Text(self.canevasInfo, width = 900, height = 65, bg =self.couleur500,selectbackground= "#f442e5", fg = self.couleurTexte1)
        self.canevasInfo.create_window(499,400, window = self.txtDescriptionProjet,width = 900,height = 65)
        self.txtDescriptionProjet.insert('end', self.parent.getDescriptionProjet())
        self.txtDescriptionProjet.config(state=DISABLED)
        self.txtTeam = Text(self.canevasInfo, width = 900, height = 65, bg =self.couleur500, selectbackground= "#f442e5", fg = self.couleurTexte1 )
        self.canevasInfo.create_window(499,540, window = self.txtTeam,width = 900,height = 150)
        #self.txtTeam.insert('end', "@John:" + "\n" + "  J'ai terminer la premiere partie du travail." + "\n\n" + "@Sofia:" + "\n" + "  Parfait! Merci John.")
        self.txtUser = Text(self.canevasInfo, width = 900, height = 65, bg =self.couleurTexte1, selectbackground= "#f442e5")
        self.canevasInfo.create_window(499,700, window = self.txtUser,width = 900,height = 100)
        self.txtUser.insert('end', '')
        self.updateChat()
        self.txtTeam.config(state=DISABLED)
        self.btnLeaveMsg = Button(text = "Envoyer",bg=self.couleurAccent,fg = self.couleurTexte1,font = ("Arial", 12), relief="raised", activebackground = self.couleurAccent, width = 12, command=self.insertIntoChat)
        self.canevasInfo.create_window(850,765, window = self.btnLeaveMsg, width = 200, height = 25)
        
        self.canevasInfo.create_window(780,102,window=btnCreationP)
        self.canevasInfo.create_window(185,450, window = self.btnRefresh)

    def creerLabelInfo(self,labelInfo):
        self.labelInfo.config(
            bg=self.couleur500,                            
            justify='left',
            relief="flat",
            font = ("Arial", 12),
            activebackground = self.couleurAccent, 
            width = 35,
            anchor = W)

#===============================================================================
#    Description: vue insertion et select appel controlleur pour chat
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/28 - 21h30
#===============================================================================

    def insertIntoChat(self):
        message=self.txtUser.get("1.0",END)
        self.parent.insertIntoChat(message)
        self.updateChat()
    
    def updateChat(self):
        self.txtTeam.config(state='normal')
        self.txtTeam.delete("1.0",END)
        listeChat=self.parent.getContentChat()

        for i in listeChat:
            print(i)
            self.txtTeam.insert('1.0', '@'+i[1]+" --- " +i[4] + "\n" + i[3] + "\n")
            
        self.txtUser.delete("1.0",END)
        self.txtTeam.config(state=DISABLED)
      
#===============================================================================
#     Description: update listBox liste membre ï¿½cran infoProjet
#     Creator: GuillaumeGeoffroy
#     Last modified: 2018/11/28 - 19h00 
#===============================================================================
     
    def updateListeMembres(self):
        self.listeMembres.delete(0, END)
        for i in self.parent.getListeMembres():
            for n in i:
                self.listeMembres.insert(END, n)   
            
#===============================================================================
#     Description: requette module xyz
#     Creator: GuillaumeGeoffroy
#     Last modified: 2018/11/12 - 10h00 
#===============================================================================

    def requeteModule(self,event):
        mod=event.widget.cget("text")
        self.parent.requetemodule(mod)    
        
    def requeteCrc(self):
        mod="crc"
        self.parent.requetemodule(mod)    

    def requeteCasUsages(self):
        mod="casUsages"
        self.parent.requetemodule(mod)    
    
    def requeteMaquette(self):
        mod="maquettes"
        self.parent.requetemodule(mod)    
    
    def requeteModelisation(self):
        mod="modelisation"
        self.parent.requetemodule(mod)
    
    def requetePlanifGlobale(self):
        mod="planifGlobale"
        self.parent.requetemodule(mod)  
        
    def closeprocess(self):
        self.parent.fermerprocessus()  
              
    def loginclient(self):
        ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
        identifiant=self.nomsplash.get() # noter notre identifiant
        motDePasse = self.loginMDP.get() #Lit le mot de passe

        connexionValide = True #Verifier si les champs sont remplis
        '''Tous les print() qui suivent devrait etre changes pour des Label+createwindow
            a  cote/sous le champ correspondant dans le UI'''

        if not identifiant:
            print("Veuillez entrer un identifiant")
            connexionValide = False
        if not motDePasse:
            print("Veuillez entrer un mot de passe")
            connexionValide = False
        if connexionValide:
            self.parent.loginclient(ipserveur,identifiant, motDePasse)

    def inscrireClient(self):
        if self.validerInformations(): #Si les champs ont ete remplis
            ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
            self.parent.inscrireSiDisponibles(ipserveur, self.identifiant, self.courriel, self.mp1,self.questionSecu,self.reponseSecu )#Envoie a  client_main

#===============================================================================
#     Description: intake outake ajout membre -} a alleger
#     Creator: GuillaumeGeoffroy
#     Last modified: 2018/11/24 - 19h00 
#===============================================================================


    def ajouterMembre(self):
        nom=self.entryNomMembreAjout.get()
        rep=self.parent.ajouterMembre(nom)
        #self.creerInfoProjet()
        self.updateListeMembres()
        self.entryNomMembreAjout.delete(0, END)
        self.entryNomMembreAjout.insert(END, rep)

                  
#########################################################
##
            
    def afficherInscriptionAchevee(self, identifiant, motDePasse):
        self.frameSignIn.destroy() #Faudrait mettre a§a dans le serveur parce que l'inscription n'est peut-etre pas
        self.loginMDP.delete(0, END)
        self.loginMDP.insert(END, motDePasse)
        self.nomsplash.delete(0, END)
        self.nomsplash.insert(END, identifiant)
        self.labelInscrit = Label(self.canevasLogin, text="Vous etes inscrit!", fg= 'green', bg=self.couleur500, font =("Times New Roman", 16) )

        self.canevasLogin.create_window(                        # Dessiner bouton connecter sur canevas
            300,380,window=self.labelInscrit)

    #############################
    ##      Vincent 5 nov - ajout des champs question, reponse + link avec database
    
    def afficherErreurDejaUtilise(self, code):
        if code ==1:
            self.erreurIDDejaUtilise.place(x=5, y=85)
        elif code ==2:
            self.erreurCourrielDejaUtilise.place(x=5, y=215)
        else:
            self.erreurAutre.text = code
            self.erreurCourrielDejaUtilise.place(x=20, y=302)
    
    def validerInformations(self):#S'assure que les champs sont remplis + '@' et '.' ds courriel
        self.identifiant = self.nomUsager.get()
        self.mp1 = self.motDePasse.get()
        self.mp2 = self.confirmationMDP.get()
        self.courriel = self.email.get()
        self.questionSecu = self.questionSecurite.get()
        self.reponseSecu = self.reponseQuestion.get()

        infosValides = True

        print("%r vs %r" % (self.identifiant, self.textNomUsager))
        self.erreurIDDejaUtilise.place_forget()
        self.erreurCourrielDejaUtilise.place_forget()
        self.erreurIDInvalide.place_forget()
        self.erreurPWDifferents.place_forget()
        self.erreurMPInvalide.place_forget()
        self.erreurCourrielInvalide.place_forget()
        self.erreurQSInvalide.place_forget()
        self.erreurRSInvalide.place_forget()
        self.erreurAutre.place_forget()
        
        
        
        if self.identifiant == "" or self.identifiant == self.textNomUsager:
            #print("Veuillez vous choisir un identifiant.")
            infosValides = False
            self.erreurIDInvalide.place(x=50, y=85)
        
        if self.mp1 != self.mp2:
            #print("Les passwords entres sont differents")#Changer ces print pour des Label qui s'affichent a  ca´te/sous les champs
            infosValides = False
            self.erreurPWDifferents.place(x=50, y=130)

        if self.mp2 == "" or self.mp2 == self.textMotDePasse:
            #print("Veuillez saisir un mot de passe.")
            infosValides = False
            self.erreurMPInvalide.place(x=50, y=175)

        if ('@' not in self.courriel) or ("." not in self.courriel) or self.courriel == self.textEmail:
            #print("Veuillez saisir un courriel valide.")
            infosValides = False
            self.erreurCourrielInvalide.place(x=50, y=215)

        if self.questionSecu == "" or self.questionSecu == self.textQuestionSecurite:
            #print("Veuillez saisir une question de securite.")
            infosValides = False
            self.erreurQSInvalide.place(x=50, y=260)

        if self.reponseSecu == "" or self.reponseSecu == self.textReponseQuestion:
            #print("Veuillez saisir une reponse a la question de securite.")
            infosValides = False
            self.erreurRSInvalide.place(x=20, y=302)
        
        return infosValides

    def underConstruction(self):
        self.canevasInfo.delete("all")
        self.lblSorry = Label(
            text = "Desole, cette page est en cours de construction.", 
            bg= self.couleur500,
            fg = self.couleurTexte1,                            
            justify='left',
            relief="flat",
            font = ("Arial", 22),
            activebackground = self.couleurAccent, 
            width = 50)

        self.lblAbonnement = Label(    		
            text = "Pour avoir acces au module lors de leur lancement, abonnez-vous!", 
            bg= self.couleur500,
            fg = self.couleurAccent,                            
            justify='left',
            relief="flat",
            font = ("Arial", 12),
            activebackground = self.couleurAccent, 
            width = 50)

        self.btnAbonnement = Button(
            text = "S'abonner",
            bg= self.couleurAccent,
            font = ("Arial", 12), 
            relief="raised", 
            activebackground = self.couleur500, 
            width = 12,
            command = self.nouvelleAbonnement)

        self.img_UnderConstruction = PhotoImage (file = "image/Under_Construction.png")
        x = 500
        y = 400

        self.canevasInfo.create_window(499, 575, window = self.btnAbonnement,width = 200, height = 35)
        self.canevasInfo.create_window(499,250, window = self.lblSorry)
        self.canevasInfo.create_window(499,520, window = self.lblAbonnement)
        self.canevasInfo.create_image (x, y, image = self.img_UnderConstruction)

    def nouvelleAbonnement(self):      
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 499, 0
        self.frameCreateAbonnement = Frame(
            self.root, 
            bd=1, 
            relief=RIDGE,
            bg= self.couleur500)
        self.frameCreateAbonnement.place(
            x=self.__winX, 
            y=200, 
            width=400, 
            height=360)
        
        self.labelCreateAbonnement = Label(
            self.frameCreateAbonnement, 
            bd=1, 
            relief=RIDGE, 
            text="Abonnement",fg= self.couleurAccent,
            font = ("Courier New", 12, "bold"),
            bg = self.couleur500)
        self.labelCreateAbonnement.pack(fill=X, padx=1, pady=1)
		
        self.canevasAbonnement = Canvas(
            self.frameCreateAbonnement, 
            width=400,
            height=460,
            bg = self.couleur500, 
            bd=0, 
            highlightbackground = self.couleur500)
        self.canevasAbonnement.pack(fill=X, padx=1, pady=1)
		
		## When the button is pressed, make sure we get the first coordinates
        self.labelCreateAbonnement.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelCreateAbonnement.bind('<B1-Motion>', self.MoveWindowAbonnement)
        self.frameCreateAbonnement.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frameCreateAbonnement.bind('<B1-Motion>', self.MoveWindowAbonnement)
        self.compteur = 0
        self.compteurY = 50
              
        #usager, mot de passe, confirmation, email, question de sÃ©curitÃ©, rÃ©ponse sÃ©curitÃ©, btnOk
        self.champNomClient = Entry()
        self.champAddresse = Entry()
        self.champNumeroCarte = Entry()
        self.champExpiration = Entry()
              
        self.btnConfirmerAbonnement = Button(
            text="Creer",
            bg = self.couleur500,
            fg = self.couleurTexte1,#texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = self.couleurAccent,
            command= None)
        
        self.canevasAbonnement.create_window(200,240,window=self.btnConfirmerAbonnement,width=300,height=25)
        self.btnQuitter1 = Button( text='X', command=self.frameCreateAbonnement.destroy, bg= self.couleur500, relief = "flat" )
        self.canevasAbonnement.create_window( 380,-10,window=self.btnQuitter1,width=25,height=21 )
        self.textNomClient = "Nom Prenom"
        self.textAddresse = "Addresse"
        self.textNumeroCarte = "Carte de credit"
        self.textDateExpiration = "Date d'expiration"
      
        self.entryListe = [self.champNomClient, self.champAddresse, self.champNumeroCarte, self.champExpiration]
        self.texteListe = [self.textNomClient, self.textAddresse, self.textNumeroCarte, self.textDateExpiration]
        
        for self.entry in self.entryListe:
            self.champsTexte = self.texteListe[self.compteur]
            self.construitEntryAbonnement(self.entry,self.champsTexte,2)
            self.compteur += 1
            self.compteurY += 43
    
    def construitEntryAbonnement(self, entry, champsTexte, v):
        self.entry.insert(0, champsTexte)
        self.entry.bind('<FocusIn>',lambda event: self.on_entry_click(event,entry,champsTexte))
        self.entry.bind('<FocusOut>',lambda event: self.on_focusout(event,entry,champsTexte))
        self.entry.config(
            bg= self.couleurAccent,                                         # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            justify='center')

        self.canevasAbonnement.create_window(200,self.compteurY,window=self.entry,width=300,height=25)
    
    def MoveWindowAbonnement(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__lastX = event.x_root
        self.frameCreateAbonnement.place_configure(x=self.__winX) 
    



if __name__ == '__main__':
    m=Vue(0,"jmd","127.0.0.1")
    m.root.mainloop()
