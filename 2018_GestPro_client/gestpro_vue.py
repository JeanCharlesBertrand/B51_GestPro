  #===============================================================================
#	 Nom fichier : gestpro_vue.py
#	 Orm√†da
#	 Creation date: 2018/10/22
#	 Description: Cr√©ation du GUI et des √©l√©ments visuel du projet 
#	 Creator: Julien Desgagn√©
#	 Version 1.0
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
#	 Description: Classe principale d'affichage
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/22 - 21h40 
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

#===============================================================================
#	 Description: cadre temporaire pour tester les fonctionnalitÈs
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30
#===============================================================================	

	def creerFrameSelectProjet(self):
		self.frameSelectProjet = Frame(self.root)						 # CrÈation frameSelectProjet
		self.canevasSelectProjet=Canvas(								# Ajout d'un canvas de le frame
			self.frameSelectProjet,
			width=600,
			height=400,
			bg="#282E3F")
		self.canevasSelectProjet.pack()

		self.listeProjets=Listbox(
			bg="#4C9689",							#Bleu-gris
			borderwidth=0,
			relief=FLAT,
			width=25,
			height=8,
			fg = "#dbdbdb",							#texte blanc
			font = ("Courier New", 12, "bold"),
			highlightbackground= "#282E3F")
		
		btnSelection=Button(									# CrÈation bouton connection
			text="Selection Projet",
			bg="#4C9689",											 # Couleur bouton [cyan]
			relief = "raised",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.requeteProjet)
		
		btnCreation=Button(									   # CrÈation bouton connection
			text="Creer un projet",
			bg="#282E3F",										# Couleur bouton [cyan]
			relief = "flat",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.frameQuiBougeCreationProjet)		   # Couleur de texte [blanc]
		
		self.canevasSelectProjet.create_window(
			300,
			150,
			window=self.listeProjets)
		
		self.canevasSelectProjet.create_window(						   # Dessiner bouton connecter sur canevas
			300,270,window=btnSelection,width=250,height=40)
		
		self.canevasSelectProjet.create_window(						   # Dessiner bouton connecter sur canevas
			300,315,window=btnCreation,width=250,height=40)

#===============================================================================
#	 Description: valider et get infos pour creation projet
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30
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
		#	 if self.parent.serveur.inscrireSiDisponibles(self.identifiant, self.courriel):
		#		 self.parent.serveur.setMotDePasse(self.identifiant, self.mp1)
		#		 print("Inscrit!")

#===============================================================================
#	 Description: valide infos et send modele qui send au serveur
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30
#===============================================================================	
	
	def creerProjet(self):
		if self.validerInformationsCreationProjet(): #Si les champs ont ÈtÈ remplis
			self.parent.creerSiDisponibles(self.nomProjet, self.description, self.nomOrganisation)#Envoie ‡† client_main
 
#===============================================================================
#	 Description: Temporaire fenetre pop pour creer projet
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30
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
		
		#usager, mot de passe, confirmation, email, question de sÈcuritÈ, rÈponse sÈcuritÈ, btnOk
		self.champnomProjet = Entry()
		self.champnomOrganisation = Entry()
		self.champdescription = Entry()
		
		btnConfirmerCreation = Button(
			text="Creer",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
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
#	 Description: prend en selection le nom de projet over dans la liste
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30 
#===============================================================================

	def requeteProjet(self):
		if self.listeProjets.size() > 0:
			pro=self.listeProjets.selection_get()
			if pro:
				self.parent.selectionProjet(pro)
	
#===============================================================================
#	 Description: change le cadre et insËre la liste des projets associÈs au membre dans la fenÍtre de sÈlection d'un projet
#	 Creator: Guillaume Geoffroy
#	 Last modified: 2018/11/04 - 12h30
#===============================================================================	
	
	def chargerSelectProjet(self, liste):
		self.listeProjets.delete(0,'end')
		for i in liste:
			self.listeProjets.insert(END,i)
		self.changecadre(self.frameSelectProjet)

#===============================================================================
#	 Description: Change le frame actif. Efface le frame actuel et le remplace
#				  par le frame pass√© en param√®tre.
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/22 - 21h48 
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
#	 Description: Affiche la liste des modules pr√©sent dans le dossier du projet.
#				  Cette fonction est appel√© dans le controlleur par la fontion
#				  loginclient().
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/22 - 21h40 
#===============================================================================

	def chargercentral(self):
		#for i in self.parent.serveur.modulesdisponibles:
		#	 self.listemodules.insert(END,i)
		self.changecadre(self.cadrecentral)

#===============================================================================
#	 Description: Cr√©er les diff√©rents frames utilis√©s dans le projet 
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/22 - 21h40 
#===============================================================================
		
	def creercadres(self):
		self.creerFrameLogin()
		#self.creercadresplash()
		self.creercadrecentral()
		self.creerFrameSelectProjet()

#===============================================================================
#	 Description: Cr√©ation du frame de login pour l'usager
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/11/05 - 8h00
#===============================================================================

	def creerFrameLogin(self):
		self.frameLogin = Frame(self.root)						  # Cr√©ation frameLogin
		self.canevasLogin=Canvas(								 # Ajout d'un canvas de le frame
			self.frameLogin,
			width=600,
			height=400,
			bg="#282E3F")										 # Couleur de fond [Bleu-gris]
		self.img_logo2 = PhotoImage (file = "image/logo3.png")	  # Importer image logo
		x = 300													   # Position x,y de l'image sur canevas
		y = 100 

		self.compteurTexte = 0
		self.compteurLoginY = 175

		self.canevasLogin.create_image (						# Dessiner logo sur le canevas
			x, y, image = self.img_logo2)
		self.canevasLogin.pack()
		self.nomsplash=Entry(									 # Champs entr√© no.1
			bg="#4C9689",										 # Couleur de fond [cyan]
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')					# Couleur de texte [blanc]
		

		self.loginMDP=Entry(									# Champs entr√© no.2
			bg="#4C9689",										 # Couleur de fond [cyan]
			relief = "sunken",
			show = '*',
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')					# Couleur de texte [blanc]
			#show="*")											  # Remplace le texte par des '*'

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
		btnConnecter=Button(									# Cr√©ation bouton connection
			text="Connecter au serveur",
			bg="#4C9689",											 # Couleur bouton [cyan]
			relief = "raised",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.loginclient)			# Couleur de texte [blanc]
			
		btnInscription=Button(										# Cr√©ation bouton connection
			text="S'inscrire",
			bg="#282E3F",										 # Couleur bouton [cyan]
			relief = "flat",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.frameQuiBouge)			   # Couleur de texte [blanc]
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			300,300,window=btnConnecter,width=250,height=40)
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			300,350,window=btnInscription,width=250,height=40)
			
		######	AJOUT IP 
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
#	 Description: 
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/11/05 - 7h25 
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

		#usager, mot de passe, confirmation, email, question de s√©curit√©, r√©ponse s√©curit√©, btnOk
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
			fg = "#dbdbdb",							   #texte blanc
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

	def construitEntry(self, entry, champsTexte, v):
		self.entry.insert(0, champsTexte)
		self.entry.bind('<FocusIn>',lambda event: self.on_entry_click(event,entry,champsTexte))
		self.entry.bind('<FocusOut>',lambda event: self.on_focusout(event,entry,champsTexte))
		self.entry.config(
			bg="#4C9689",										 # Couleur de fond [cyan]
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
#	 Description: 
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/23 - 9h15 
#===============================================================================
	
	def creercadrecentral(self):
		self.cadrecentral=Frame(self.root)
		self.canevacentral=Canvas(
			self.cadrecentral,
			width=1200,
			height=800,
			bg="#282E3F")							 #Bleu-gris
		self.canevacentral.pack()
		
		self.cadreChat=Frame(self.cadrecentral, 
			width=450,
			height=200,
			bg="#4C9689")
		
		self.cadreChat.place(x=600,y=350)
		
		self.cadreEntree=Frame(self.cadrecentral, 
			width=450,
			height=45,
			bg="#387c70")
		
		self.cadreEntree.place(x=600,y=550)
						
		btnquitproc=Button(
			text="Fermer dernier module",
			bg="#4C9689",							 #Cyan
			fg = "#dbdbdb",							   #texte blanc
			justify='center',
			font = ("Courier New", 12, "bold"),
			command=self.closeprocess)

		btnAjouterMembre = Button(
			text="+Membre",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 30, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689",
			command=self.ajouterMembrePop)
		
		btnMandat = Button(
			text="Mandat",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnAnalyse = Button(
			text="Analyse",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689",
			command=self.requeteAnalyse)
		btnCasUsage = Button(
			text="Cas usage",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnScenario = Button(
			text="Scenario",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnInventaire = Button(
			text="Inventaire",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command= null)
		btnMaquette = Button(
			text="Maquette",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnCRC = Button(
			text="CRC",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnModelisation = Button(
			text="Modelisation",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnTimePlaner = Button(
			text="Time planner",
			bg="#282E3F",
			fg = "#dbdbdb",							   #texte blanc
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
		self.canevacentral.create_window(200,200,window=btnAjouterMembre,width=150,height=15)

	def ajouterMembrePop(self):
		self.__winX, self.__winY = 200, 20
		self.frameAjouterMembre = Frame(
			self.root, 
			bd=1, 
			relief=RIDGE,
			bg="#282E3F")
		self.frameAjouterMembre.place(
			x=self.__winX, 
			y=20, 
			width=300, 
			height=260)
		
		self.labelAjouterMembre = Label(
			self.frameAjouterMembre, 
			bd=1, 
			relief=RIDGE, 
			text="Ajouter un membre au projet",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
		self.labelAjouterMembre.pack(fill=X, padx=1, pady=1)
		
		self.canevasAjouterMembre = Canvas(
			self.frameAjouterMembre, 
			width=300,
			height=360,
			bg="#282E3F", 
			bd=0, 
			highlightbackground ="#282E3F")
		self.canevasAjouterMembre.pack(fill=X, padx=1, pady=1)
		
		## When the button is pressed, make sure we get the first coordinates
		self.labelAjouterMembre.bind('<ButtonPress-1>', self.startMoveWindow)
		self.labelAjouterMembre.bind('<B1-Motion>', self.MoveWindow2)
		self.frameAjouterMembre.bind('<ButtonPress-1>', self.startMoveWindow)
		self.frameAjouterMembre.bind('<B1-Motion>', self.MoveWindow2)

		self.compteur = 0
		self.compteurY = 50
		
		#usager, mot de passe, confirmation, email, question de sÈcuritÈ, rÈponse sÈcuritÈ, btnOk
		self.champIdentifiant = Entry()
		
		btnConfirmerAjout = Button(
			text="Creer",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 12, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689",
			command=self.ajouterMembre)
		
		self.canevasAjouterMembre .create_window(						 
			50,180,window=btnConfirmerAjout,width=200,height=25)
		
		self.textIdentifiant = "Identifiant"
		
		self.entryListe = [self.champIdentifiant]
		self.texteListe = [self.textIdentifiant]
		
		for self.entry in self.entryListe:
			self.champsTexte = self.texteListe[self.compteur]
			self.construitEntry(self.entry,self.champsTexte,3)
			self.compteur += 1
			self.compteurY += 43
		
	def MoveWindow2 (self, event):
		self.root.update_idletasks()
		self.__winX += event.x_root - self.__lastX
		self.__lastX = event.x_root
		self.frameAjouterMembre.place_configure(x=self.__winX)

		
#===============================================================================
#	 Description: 
#	 Creator: Julien Desgagn√©
#	 Last modified: 2018/10/22 - 21h40 
#===============================================================================

	def closeprocess(self):
		self.parent.fermerprocessus()

	def requeteAnalyse(self):
		mod="analyseText"
		self.parent.requetemodule(mod)		  
		
	def loginclient(self):
		ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
		identifiant=self.nomsplash.get() # noter notre identifiant
		motDePasse = self.loginMDP.get() #Lit le mot de passe

		connexionValide = True #V√©rifier si les champs sont remplis
		'''Tous les print() qui suivent devrait etre changes pour des Label+createwindow
			√† cote/sous le champ correspondant dans le UI'''

		if not identifiant:
			print("Veuillez entrer un identifiant")
			connexionValide = False
		if not motDePasse:
			print("Veuillez entrer un mot de passe")
			connexionValide = False
		if connexionValide:
			self.parent.loginclient(ipserveur,identifiant, motDePasse)

	def inscrireClient(self):
		if self.validerInformations(): #Si les champs ont √©t√© remplis
			ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
			self.parent.inscrireSiDisponibles(ipserveur, self.identifiant, self.courriel, self.mp1,self.questionSecu,self.reponseSecu )#Envoie √† client_main

	def ajouterMembre(self):
		if self.validerAjoutMembre():
			self.parent.ajouterMembre(self.nomMembreAjout)
			
#########################################################
##
			
	def afficherInscriptionAchevee(self, identifiant, motDePasse):
		self.frameSignIn.destroy() #Faudrait mettre √ßa dans le serveur parce que l'inscription n'est peut-√™tre pas
		self.loginMDP.delete(0, END)
		self.loginMDP.insert(END, motDePasse)
		self.nomsplash.delete(0, END)
		self.nomsplash.insert(END, identifiant)
		self.labelInscrit = Label(self.canevasLogin, text="Vous etes inscrit!")
		#A COMPLETER: Envoyer id et mdp dans les champs texte
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			100,100,window=self.labelInscrit)

	#############################
	##	  Vincent 5 nov - ajout des champs question, reponse + link avec database
			
	def validerInformations(self):#S'assure que les champs sont remplis + '@' et '.' ds courriel
		self.identifiant = self.nomUsager.get()
		self.mp1 = self.motDePasse.get()
		self.mp2 = self.confirmationMDP.get()
		self.courriel = self.email.get()
		self.questionSecu = self.questionSecurite.get()
		self.reponseSecu = self.reponseQuestion.get()


		self.erreurIDInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez vous choisir un identifiant.")
		self.erreurPWDifferents = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Les passwords entres sont differents.")
		self.erreurCourrielInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir un courriel valide.")
		self.erreurMPInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir un mot de passe.")
		self.erreurQSInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir une question de securite.")
		self.erreurRSInvalide = Label(self.frameSignIn, fg="red", bg="#282E3F", height=1, text="Veuillez saisir une reponse a la question de securite.")
		
		self.erreurIDInvalide.place(x=50, y=85)
		self.erreurPWDifferents.place(x=50, y=130)
		self.erreurMPInvalide.place(x=50, y=175)
		self.erreurCourrielInvalide.place(x=50, y=215)
		self.erreurQSInvalide.place(x=50, y=260)
		self.erreurRSInvalide.place(x=20, y=302)
		
		self.erreurIDInvalide.visible = False
		self.erreurPWDifferents.visible = False
		self.erreurCourrielInvalide.visible = False
		self.erreurMPInvalide.visible = False
		self.erreurQSInvalide.visible = False
		self.erreurRSInvalide.visible = False

		infosValides = True

		print("%r vs %r" % (self.identifiant, self.textNomUsager))

		if self.identifiant == "" or self.identifiant == self.textNomUsager:
			#print("Veuillez vous choisir un identifiant.")
			infosValides = False
			self.erreurIDInvalide.visible = True
		
		if self.mp1 != self.mp2:
			#print("Les passwords entres sont differents")#Changer ces print pour des Label qui s'affichent √† c√¥t√©/sous les champs
			infosValides = False
			self.erreurPWDifferents.visible = True

		if self.mp2 == "" or self.mp2 == self.textMotDePasse:
			#print("Veuillez saisir un mot de passe.")
			infosValides = False
			self.erreurMPInvalide.visible = True

		if ('@' not in self.courriel) or ("." not in self.courriel) or self.courriel == self.textEmail:
			#print("Veuillez saisir un courriel valide.")
			infosValides = False
			self.erreurCourrielInvalide.visible = True

		if self.questionSecu == "" or self.questionSecu == self.textQuestionSecurite:
			#print("Veuillez saisir une question de securite.")
			infosValides = False
			self.erreurQSInvalide.visible = True

		if self.reponseSecu == "" or self.reponseSecu == self.textReponseQuestion:
			#print("Veuillez saisir une reponse a la question de securite.")
			infosValides = False
			self.erreurRSInvalide.visible = True
		
		return infosValides	   
	
	
	def validerAjoutMembre(self):#S'assure que les champs sont remplis + '@' et '.' ds courriel
		self.nomMembreAjout = self.champIdentifiant.get()

		infosValides = True

		if self.nomMembreAjout == "" or self.nomMembreAjout == self.textIdentifiant:
			#print("Veuillez vous choisir un identifiant.")
			infosValides = False
		
		return infosValides 
	
	def afficherErreurAjoutMembre(self,message):
		if self.afficher:
			self.erreurAjout = Label(self.frameAjouterMembre, fg="red", bg="#282E3F", height=1, text=message)
			self.erreurAjout.place(x=50, y=85)
	
	



if __name__ == '__main__':
	m=Vue(0,"jmd","127.0.0.1")
	m.root.mainloop()