  #===============================================================================
#     Nom fichier : gestpro_vue.py
#     OrmÃƒÂ da
#     Creation date: 2018/10/22
#     Description: CrÃƒÂ©ation du GUI et des ÃƒÂ©lÃƒÂ©ments visuel du projet 
#     Creator: Julien DesgagnÃƒÂ©
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
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================

class Vue():
    def __init__(self,parent,monip,largeur=200,hauteur=200):
        self.parent=parent
        self.root=tix.Tk()
        self.root.title("Omada")
        self.root.iconbitmap('image/tk_logo.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.parent.fermefenetre)
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
            bg="#282E3F")
        self.canevasSelectProjet.pack()

        self.listeProjets=Listbox(
            bg="#4C9689",                            #Bleu-gris
            borderwidth=0,
            relief=FLAT,
            width=25,
            height=8,
            fg = "#dbdbdb",                            #texte blanc
            font = ("Courier New", 12, "bold"),
            highlightbackground= "#282E3F")
        
        btnSelection=Button(                                    # CrÃ©ation bouton connection
            text="Selection Projet",
            bg="#4C9689",                                             # Couleur bouton [cyan]
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.requeteProjet)
        
        btnCreation=Button(                                       # CrÃ©ation bouton connection
            text="Creer un projet",
            bg="#282E3F",                                        # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.frameQuiBougeCreationProjet)           # Couleur de texte [blanc]
        
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
            self.parent.creerSiDisponibles(self.nomProjet, self.description, self.nomOrganisation)#Envoie Ã Â  client_main
 
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
            bg="#282E3F")
        self.frameCreateProject.place(
            x=self.__winX, 
            y=20, 
            width=300, 
            height=260)
        
        self.labelCreateProject = Label(
            self.frameCreateProject, 
            bd=1, 
            relief=RIDGE, 
            text="Creation du projet",fg="#4C9689",
            font = ("Courier New", 12, "bold"),
            bg="#282E3F")
        self.labelCreateProject.pack(fill=X, padx=1, pady=1)
        
        self.canevasCreation = Canvas(
            self.frameCreateProject, 
            width=300,
            height=360,
            bg="#282E3F", 
            bd=0, 
            highlightbackground ="#282E3F")
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
            bg="#282E3F",
            fg = "#dbdbdb",                            #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689",
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
#                  par le frame passÃƒÂ© en paramÃƒÂ¨tre.
#     Creator: Julien DesgagnÃƒÂ©
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
#     Description: Affiche la liste des modules prÃƒÂ©sent dans le dossier du projet.
#                  Cette fonction est appelÃƒÂ© dans le controlleur par la fontion
#                  loginclient().
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================

    def chargercentral(self):
        #for i in self.parent.serveur.modulesdisponibles:
        #     self.listemodules.insert(END,i)
        self.changecadre(self.frameAccueil)

#===============================================================================
#     Description: CrÃƒÂ©er les diffÃƒÂ©rents frames utilisÃƒÂ©s dans le projet 
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/10/22 - 21h40 
#===============================================================================
        
    def creercadres(self):
        self.creerFrameLogin()
        #self.creercadresplash()
        self.creerFrameAccueil()
        self.creerFrameSelectProjet()

#===============================================================================
#     Description: Création du frame de login pour l'usager
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/11/05 - 8h00
#===============================================================================

    def creerFrameLogin(self):
        self.frameLogin = Frame(self.root)                          # CrÃƒÂ©ation frameLogin
        self.canevasLogin=Canvas(                                 # Ajout d'un canvas de le frame
            self.frameLogin,
            width=600,
            height=400,
            bg="#282E3F")                                         # Couleur de fond [Bleu-gris]
        self.img_logo2 = PhotoImage (file = "image/logo3.png")      # Importer image logo
        x = 300                                                       # Position x,y de l'image sur canevas
        y = 100 

        self.compteurTexte = 0
        self.compteurLoginY = 175

        self.canevasLogin.create_image (                        # Dessiner logo sur le canevas
            x, y, image = self.img_logo2)
        self.canevasLogin.pack()
        self.nomsplash=Entry(                                     # Champs entrÃƒÂ© no.1
            bg="#4C9689",                                         # Couleur de fond [cyan]
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')                    # Couleur de texte [blanc]
        

        self.loginMDP=Entry(                                    # Champs entrÃƒÂ© no.2
            bg="#4C9689",                                         # Couleur de fond [cyan]
            relief = "sunken",
            show = '*',
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')                    # Couleur de texte [blanc]
            #show="*")                                              # Remplace le texte par des '*'

        #################################
        #Rajouter ip ici
        self.ipsplash=Entry(
            bg="#4C9689",
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        
        #self.ipsplash.insert(0, self.monip)
        #################################
        
                    # Placeholder password
        btnConnecter=Button(                                    # CrÃƒÂ©ation bouton connection
            text="Connecter au serveur",
            bg="#4C9689",                                             # Couleur bouton [cyan]
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.loginclient)            # Couleur de texte [blanc]
            
        btnInscription=Button(                                        # CrÃƒÂ©ation bouton connection
            text="S'inscrire",
            bg="#282E3F",                                         # Couleur bouton [cyan]
            relief = "flat",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",command=self.frameQuiBouge)               # Couleur de texte [blanc]
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
            bg="#4C9689",                                         
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')

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
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/11/05 - 7h25 
#===============================================================================

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

        #usager, mot de passe, confirmation, email, question de sÃƒÂ©curitÃƒÂ©, rÃƒÂ©ponse sÃƒÂ©curitÃƒÂ©, btnOk
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
            bg="#282E3F",
            fg = "#dbdbdb",                               #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689",
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
            
        self.erreurIDInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez vous choisir un identifiant.")
        self.erreurIDDejaUtilise = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Cet identifiant existe dÃƒÂ©jÃƒÂ , veuillez en choisir un autre")
        self.erreurPWDifferents = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Les passwords entres sont diffÃƒÂ©rents.")
        self.erreurCourrielInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir un courriel valide.")
        self.erreurCourrielDejaUtilise = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Cet courriel existe dÃƒÂ©jÃƒÂ , veuillez en choisir un autre")
        self.erreurMPInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir un mot de passe.")
        self.erreurQSInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir une question de sÃƒÂ©curitÃƒÂ©.")
        self.erreurRSInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir une rÃƒÂ©ponse a la question de sÃƒÂ©curitÃƒÂ©.")
        self.erreurAutre = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="")
    
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

    def startMoveWindow(self,event):
        self.__lastX= event.x_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__lastX = event.x_root
        self.frameSignIn.place_configure(x=self.__winX)

#===============================================================================
#     Description: 
#     Creator: Julien DesgagnÃƒÂ©
#     Last modified: 2018/10/23 - 9h15 
#===============================================================================
    
    
    def creerFrameAccueil(self):
        self.frameAccueil = Frame(self.root)
        self.frameModule = Frame(self.frameAccueil,bg="#282E3F", width = 200, height = 800)
        self.frameInfo = Frame(self.frameAccueil,bg="#282E3F", width = 998, height = 800)
        self.frameBorder = Frame(self.frameAccueil,bg = "black", width = 2, height = 800)
        #self.canevasModule = Canvas(self.frameModule,bg="#282E3F",bd=0, highlightthickness=0, width = 200, height = 800)
        #self.canevasModule.grid(row = 0, column = 0, sticky = "nsew")
        #self.canevasInfo = Canvas(self.frameInfo, bg="#282E3F",bd=0, highlightthickness=0, width = 998, height = 800)

        self.frameModule.grid(row = 0, column = 1, sticky = "nse")
        self.frameBorder.grid(row = 0, column =2, sticky = "ns")
        self.frameInfo.grid(row = 0, column = 3, sticky = "nse")
        #self.canevasInfo.grid(row = 0, column = 0, sticky = "nsew")

        self.frameModule.grid_rowconfigure(20, weight = 0)
        self.frameModule.grid_columnconfigure(2, weight =0)
        #self.creerBoutonFrameModule()
    
    def creerBoutonFrameModule(self):       
        self.canevasModule = Canvas(self.frameModule,bg="#282E3F",bd=0, highlightthickness=0, width = 200, height = 800)
        self.canevasModule.grid(row = 0, column = 0, sticky = "nsew")
        
        y=130
        cles=[*self.parent.getModulesDisponibles()]
        
        for cle in cles:
            btnX = Button(text=cle,
                          bg="#282E3F",
                          fg = "#dbdbdb",                            
                          font = ("Arial", 15),
                          relief="flat",
                          activebackground = "#4C9689", 
                          width = 15, 
                          anchor = W)
        
            btnX.bind("<ButtonRelease-1>", self.requeteModule)
            self.canevasModule.create_window(100, y, window=btnX,width=200,height=30)
            y+=(600)/len(cles)
            
        #self.btnAnalyseTxt      = Button(text = "     Analyse textuelle", command = self.requeteAnalyse)
        #self.btnCasUsage        = Button(text = "     Cas d'usage", command = self.requeteCasUsages)
        #self.btnScenario        = Button(text = "     Scenario")
        #self.btnMaquette        = Button(text = "     Maquette", command = self.requeteMaquette)
        #self.btnCRC             = Button(text = "     CRC", command = self.requeteCrc)
        #self.btnDonnee          = Button(text = "     Donnee", command = self.requeteModelisation)
        #self.btnCreationSprint  = Button(text = "     Creation sprint")
        #self.btnScrum           = Button(text = "     Scrum(s)")
        #self.btnProbleme        = Button(text = "     Probleme")
        #self.btnDebriefing      = Button(text = "     Debriefing")
        #self.btnCalendrier      = Button(text = "     Debriefing")
        #self.btnStats           = Button(text = "     Statistique")
        self.btnPlanif          = Button(text = "       Planification", bg="#282E3F",
            fg = "#4C9689",                            
            justify='left',
            font = ("Arial", 16),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15,
            anchor = W)
        #self.btnImplementation  = Button(text = "     Implementation")
        #self.btnSyntheseStats   = Button(text = "     Synthese et stats")
        #self.btnChat            = Button(text = "     Chat")
        
        self.btnQuitter = Button(text = "          Quitter", bg="#282E3F",
            fg = "#4C9689",                            
            justify='left',
            font = ("Arial", 16),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15,
            anchor = W)
        
        self.lblVersion = Label(bd=1, text="Version 1.0",fg="#4C9689",font = ("Arial", 10),bg="#282E3F")

        #self.listeModule = [self.btnAnalyseTxt, self.btnCasUsage, self.btnScenario, self.btnMaquette, 
                            #self.btnCRC, self.btnDonnee,self.btnCreationSprint,self.btnScrum,self.btnProbleme,
                            #self.btnDebriefing,self.btnCalendrier,self.btnStats]

        #self.listeEtapeProjet = [self.btnPlanif, self.btnImplementation, self.btnSyntheseStats, self.btnChat, self.btnQuitter]

        #for self.etapeProjet in self.listeEtapeProjet:
        #    self.creerBtnEtapeProjet(self.etapeProjet)

       # for self.module in self.listeModule:
       #     self.creerBtnModule(self.module)

        #self.canevasModule.create_window(100,55, window=self.btnAnalyseTxt,width=200,height=30)
        #self.canevasModule.create_window(100,85, window=self.btnCasUsage,width=200,height=30)
        #self.canevasModule.create_window(100,115, window=self.btnScenario,width=200,height=30)
        #self.canevasModule.create_window(100,145, window=self.btnMaquette,width=200,height=30)
        #self.canevasModule.create_window(100,175, window=self.btnCRC,width=200,height=30)
        #self.canevasModule.create_window(100,205, window=self.btnDonnee,width=200,height=30)
        #self.canevasModule.create_window(100,280, window=self.btnCreationSprint,width=200,height=30)
        #self.canevasModule.create_window(100,310, window=self.btnScrum,width=200,height=30)
        #self.canevasModule.create_window(100,340, window=self.btnProbleme,width=200,height=30)
        #self.canevasModule.create_window(100,370, window=self.btnDebriefing,width=200,height=30)
        #self.canevasModule.create_window(100,435, window=self.btnCalendrier,width=200,height=30)
        #self.canevasModule.create_window(100,465, window=self.btnStats,width=200,height=30)
        self.canevasModule.create_window(160,790,window=self.lblVersion, width=75, height=30)

        self.canevasModule.create_window(100,75, window=self.btnPlanif,width=200,height=30)
        #self.canevasModule.create_window(100,250, window=self.btnImplementation,width=200,height=30)
        #self.canevasModule.create_window(100,405, window=self.btnSyntheseStats,width=200,height=30)
        #self.canevasModule.create_window(100,510, window=self.btnChat,width=200,height=30)
        self.canevasModule.create_window(100,y, window=self.btnQuitter,width=200,height=30)

    def creerBtnModule(self, module):
        self.module.config(
            bg="#282E3F",
            fg = "#dbdbdb",                            
            font = ("Arial", 15),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15, 
            anchor = W)

    def creerBtnEtapeProjet(self,etapeProjet):
        self.etapeProjet.config(
            bg="#282E3F",
            fg = "#4C9689",                            
            justify='left',
            font = ("Arial", 16),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15,
            anchor = W)

    def creerInfoProjet(self): 
        self.canevasInfo = Canvas(self.frameInfo, bg="#282E3F",bd=0, highlightthickness=0, width = 998, height = 800)
        self.canevasInfo.grid(row = 0, column = 0, sticky = "nsew")

        self.nomProjet = "Project name"
        self.date = "2018/12/21"
        self.sprintNumber = 1
        self.timeRemaining = "2 Days 18h"
        nomProjet = self.parent.getNomProjet()
        self.lblNomProjet           = Label(text = nomProjet[0], bg = "#282E3F", fg = "#4C9689", font = ("Arial", 25, "bold"))
        self.lblDeadline            = Label(text = "Add: ", fg = "#4C9689")
        self.lblDate                = Label(text = self.date, fg = "#dbdbdb")
        self.lblMember              = Label(text = "Member:", fg = "#4C9689")
        self.lblTimer               = Label(text = "Time left before the end of the Sprint #" + str(self.sprintNumber), fg = "#4C9689")
        self.lblTimeLeft            = Label(text = self.timeRemaining, fg = "#dbdbdb")
               
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
        self.om.config(font=('calibri',(12)),bg="#4C9689",width=14)
        
        self.canevasInfo.create_window(870, 102, window = self.om)
        
        self.listeMembres=Listbox(
            bg="#282E3F",                            #Bleu-gris
            borderwidth=0,
            relief=FLAT,
            width=25,
            height=8,
            fg = "#dbdbdb",                            #texte blanc
            font = ("Courier New", 12, "bold"))
        
        self.updateListeMembres()
            
        self.entryNomMembreAjout = Entry(                                        
            bg="#4C9689",                                         
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        
        self.btnAjouterMembre = Button(                                       # CrÃ©ation bouton connection
                                        text="+",
                                        bg="#282E3F",                                        # Couleur bouton [cyan]
                                        relief = "flat",
                                        font = ("Courier New", 12, "bold"),
                                        fg = "#dbdbdb", command=self.ajouterMembre)
        
        self.lblProjectDescription    = Label(text = "Description du projet: ", font = ("Arial", 10),fg = "#4C9689",bg="#282E3F")
        self.lblTeamMsg             = Label(text = "Message de l'equipe: ",font = ("Arial", 10),fg = "#4C9689",bg="#282E3F")
        self.lblUser                = Label(text = '@' + self.parent.monnom, font = ("Arial", 10),fg = "#4C9689",bg="#282E3F")
        self.listeLabelInfo = [self.lblDeadline,self.lblDate,self.lblMember,self.lblTimer,self.lblTimeLeft ] #,self.member1,self.member2,self.member3,self.member4, self.member5,self.member6
        self.canevasInfo.create_window(998/2,45, window = self.lblNomProjet)
        self.canevasInfo.create_window(200,100, window = self.lblMember)
        self.canevasInfo.create_window(177,205, window = self.listeMembres)
        self.canevasInfo.create_window(205,310, window = self.entryNomMembreAjout)
        self.canevasInfo.create_window(315,310, window = self.btnAjouterMembre)
        self.canevasInfo.create_window(205,310, window = self.lblDeadline)
        self.canevasInfo.create_window(110,355, window = self.lblProjectDescription)
        self.canevasInfo.create_window(110,453, window = self.lblTeamMsg)
        self.canevasInfo.create_window(72, 638, window = self.lblUser)
        self.canevasInfo.create_line(40,70,950,70,fill="#4C9689")

        for self.labelInfo in self.listeLabelInfo:
            self.creerLabelInfo(self.labelInfo)

        self.txtDescriptionProjet = Text(self.canevasInfo, width = 900, height = 65, bg ="#282E3F",selectbackground= "#f442e5", fg = "#dbdbdb")
        self.canevasInfo.create_window(499,400, window = self.txtDescriptionProjet,width = 900,height = 65)
        self.txtDescriptionProjet.insert('end', self.parent.getDescriptionProjet())
        self.txtDescriptionProjet.config(state=DISABLED)
        self.txtTeam = Text(self.canevasInfo, width = 900, height = 65, bg ="#282E3F", selectbackground= "#f442e5", fg = "#dbdbdb" )
        self.canevasInfo.create_window(499,540, window = self.txtTeam,width = 900,height = 150)
        #self.txtTeam.insert('end', "@John:" + "\n" + "  J'ai terminer la premiere partie du travail." + "\n\n" + "@Sofia:" + "\n" + "  Parfait! Merci John.")
        self.txtUser = Text(self.canevasInfo, width = 900, height = 65, bg ="#dbdbdb", selectbackground= "#f442e5")
        self.canevasInfo.create_window(499,700, window = self.txtUser,width = 900,height = 100)
        self.txtUser.insert('end', '')
        self.updateChat()
        self.txtTeam.config(state=DISABLED)
        self.btnLeaveMsg = Button(text = "Envoyer",bg="#4C9689",fg = "#dbdbdb",font = ("Arial", 12), relief="raised", activebackground = "#4C9689", width = 12, command=self.insertIntoChat)
        self.canevasInfo.create_window(850,765, window = self.btnLeaveMsg, width = 200, height = 25)

    def creerLabelInfo(self,labelInfo):
        self.labelInfo.config(
            bg="#282E3F",                            
            justify='left',
            relief="flat",
            font = ("Arial", 12),
            activebackground = "#4C9689", 
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

        connexionValide = True #VÃƒÂ©rifier si les champs sont remplis
        '''Tous les print() qui suivent devrait etre changes pour des Label+createwindow
            ÃƒÂ  cote/sous le champ correspondant dans le UI'''

        if not identifiant:
            print("Veuillez entrer un identifiant")
            connexionValide = False
        if not motDePasse:
            print("Veuillez entrer un mot de passe")
            connexionValide = False
        if connexionValide:
            self.parent.loginclient(ipserveur,identifiant, motDePasse)

    def inscrireClient(self):
        if self.validerInformations(): #Si les champs ont ÃƒÂ©tÃƒÂ© remplis
            ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
            self.parent.inscrireSiDisponibles(ipserveur, self.identifiant, self.courriel, self.mp1,self.questionSecu,self.reponseSecu )#Envoie ÃƒÂ  client_main

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
        self.frameSignIn.destroy() #Faudrait mettre ÃƒÂ§a dans le serveur parce que l'inscription n'est peut-ÃƒÂªtre pas
        self.loginMDP.delete(0, END)
        self.loginMDP.insert(END, motDePasse)
        self.nomsplash.delete(0, END)
        self.nomsplash.insert(END, identifiant)
        self.labelInscrit = Label(self.canevasLogin, text="Vous ÃƒÂªtes inscrit!", fg= 'green', bg="#282E3F", font =("Times New Roman", 16) )

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
            #print("Les passwords entres sont differents")#Changer ces print pour des Label qui s'affichent ÃƒÂ  cÃƒÂ´tÃƒÂ©/sous les champs
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
    



if __name__ == '__main__':
    m=Vue(0,"jmd","127.0.0.1")
    m.root.mainloop()
