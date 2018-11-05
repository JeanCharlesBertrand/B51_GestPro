#===============================================================================
#	Nom fichier : gestpro_vue.py
#	Ormàda
#	Creation date: 2018/10/22
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
#	Description: Classe principale d'affichage
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
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

#===============================================================================
#	Description: Change le frame actif. Efface le frame actuel et le remplace
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
#	Description: Affiche la liste des modules présent dans le dossier du projet.
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
#	Description: Créer les différents frames utilisés dans le projet 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================
		
	def creercadres(self):
		self.creerFrameLogin()
		#self.creercadresplash()
		self.creercadrecentral()

#===============================================================================
#	Description: Création du frame de login pour l'usager
#	Creator: Julien Desgagné
#	Last modified: 2018/11/05 - 8h00
#===============================================================================

	def creerFrameLogin(self):
		self.frameLogin = Frame(self.root)						# Création frameLogin
		self.canevasLogin=Canvas(								# Ajout d'un canvas de le frame
			self.frameLogin,
			width=600,
			height=400,
			bg="#282E3F")										# Couleur de fond [Bleu-gris]
		self.img_logo2 = PhotoImage (file = "image/logo3.png")	# Importer image logo
		x = 300													# Position x,y de l'image sur canevas
		y = 100 

		self.compteurTexte = 0
		self.compteurLoginY = 175

		self.canevasLogin.create_image (						# Dessiner logo sur le canevas
			x, y, image = self.img_logo2)
		self.canevasLogin.pack()
		self.nomsplash=Entry(									# Champs entré no.1
			bg="#4C9689",										# Couleur de fond [cyan]
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')					# Couleur de texte [blanc]
		

		self.loginMDP=Entry(									# Champs entré no.2
			bg="#4C9689",										# Couleur de fond [cyan]
			relief = "sunken",
			show = '*',
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')					# Couleur de texte [blanc]
			#show="*")											# Remplace le texte par des '*'

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
		btnConnecter=Button(									# Création bouton connection
			text="Connecter au serveur",
			bg="#4C9689",											# Couleur bouton [cyan]
			relief = "raised",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.loginclient)			# Couleur de texte [blanc]
			
		btnInscription=Button(									  # Création bouton connection
			text="S'inscrire",
			bg="#282E3F",										# Couleur bouton [cyan]
			relief = "flat",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",command=self.frameQuiBouge)			 # Couleur de texte [blanc]
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			300,300,window=btnConnecter,width=250,height=40)
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			300,350,window=btnInscription,width=250,height=40)
			
		######  AJOUT IP 
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
#	Description: Creation de nouveau projet
#	Creator: Julien Desgagné
#	Last modified: 2018/10/22 - 21h40 
#===============================================================================

#===============================================================================
#	Description: 
#	Creator: Julien Desgagné
#	Last modified: 2018/11/05 - 7h25 
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

		#usager, mot de passe, confirmation, email, question de sécurité, réponse sécurité, btnOk
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
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 12, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689",
			command=self.inscrireClient)

		self.canevasSignIn.create_window(						 
			150,310,window=self.btnConfirmerInscription,width=200,height=25)

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
			self.construitEntry(self.entry,self.champsTexte)
			self.compteur += 1
			self.compteurY += 43


	def construitEntry(self, entry, champsTexte):
		self.entry.insert(0, champsTexte)
		self.entry.bind('<FocusIn>',lambda event: self.on_entry_click(event,entry,champsTexte))
		self.entry.bind('<FocusOut>',lambda event: self.on_focusout(event,entry,champsTexte))
		self.entry.config(
			bg="#4C9689",										# Couleur de fond [cyan]
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')

		self.canevasSignIn.create_window(						 
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
#	Description: 
#	Creator: Julien Desgagné
#	Last modified: 2018/10/23 - 9h15 
#===============================================================================
	
	def creercadrecentral(self):
		self.cadrecentral=Frame(self.root)
		self.canevacentral=Canvas(
			self.cadrecentral,
			width=1200,
			height=800,
			bg="#282E3F")							#Bleu-gris
		self.canevacentral.pack()
		
		self.listemodules=Listbox(
			bg="#282E3F",							#Bleu-gris
			borderwidth=0,
			relief=FLAT,
			width=20,
			height=6,
			fg = "#dbdbdb",							#texte blanc
			font = ("Courier New", 12, "bold"),
			highlightbackground= "#282E3F")			#Contour bleu-gris
		self.ipcentral=Entry(bg="pink")
		self.ipcentral.insert(0, self.monip)
		btnConnecter=Button(
			text="Requerir module",
			bg="#4C9689",							#Cyan
			fg = "#dbdbdb",							#texte blanc
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
			bg="#4C9689",							#Cyan
			fg = "#dbdbdb",							#texte blanc
			justify='center',
			font = ("Courier New", 12, "bold"),
			command=self.closeprocess)

		btnMandat = Button(
			text="Mandat",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnAnalyse = Button(
			text="Analyse",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnCasUsage = Button(
			text="Cas usage",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnScenario = Button(
			text="Scenario",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnInventaire = Button(
			text="Inventaire",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command= null)
		btnMaquette = Button(
			text="Maquette",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnCRC = Button(
			text="CRC",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnModelisation = Button(
			text="Modelisation",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
			justify='right',
			font = ("Courier New", 15, "bold"),
			relief="flat",
			overrelief = "raised",
			activebackground = "#4C9689")
			#command=none)
		btnTimePlaner = Button(
			text="Time planner",
			bg="#282E3F",
			fg = "#dbdbdb",							#texte blanc
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
#	Description: 
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
		motDePasse = self.loginMDP.get() #Lit le mot de passe

		connexionValide = True #Vérifier si les champs sont remplis
		'''Tous les print() qui suivent devrait etre changes pour des Label+createwindow
			à cote/sous le champ correspondant dans le UI'''

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
			self.parent.inscrireSiDisponibles(ipserveur, self.identifiant, self.courriel, self.mp1,self.questionSecu,self.reponseSecu )#Envoie à client_main

#########################################################
##
			
	def afficherInscriptionAchevee(self, identifiant, motDePasse):
		self.frameSignIn.destroy() #Faudrait mettre ça dans le serveur parce que l'inscription n'est peut-être pas
		self.loginMDP.delete(0, END)
		self.loginMDP.insert(END, motDePasse)
		self.nomsplash.delete(0, END)
		self.nomsplash.insert(END, identifiant)
		self.labelInscrit = Label(self.canevasLogin, text="Vous etes inscrit!")
		#A COMPLETER: Envoyer id et mdp dans les champs texte
		self.canevasLogin.create_window(						# Dessiner bouton connecter sur canevas
			100,100,window=self.labelInscrit)

	#############################
	##	Vincent 5 nov - ajout des champs question, reponse + link avec database
			
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
			#print("Les passwords entres sont differents")#Changer ces print pour des Label qui s'affichent à côté/sous les champs
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
	
if __name__ == '__main__':
	m=Vue(0,"jmd","127.0.0.1")
	m.root.mainloop()
	
