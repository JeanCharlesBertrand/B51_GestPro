# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
import time
class Vue():
	def __init__(self,parent,largeur=800,hauteur=600):
		self.root=tix.Tk()
		self.parent=parent
		self.root.title(self.parent.getNomProjet()) 
		self.root.iconbitmap("Image/tk_logo.ico")
		self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
		
		self.couleur500 = "#344955"
		self.couleur800 = ""
		self.couleur300 = ""
		self.couleurTexte1 = "#FFFFFF"
		self.couleurTexte2 = "#000000"
		self.couleurAccent = "#FAAB1A"
		self.couleurSelection = "#FF4181"
		
		self.modele=None
		self.largeur=largeur
		self.hauteur=hauteur
		self.images={}
		self.cadreactif=None
		self.creercadres()
		self.changecadre(self.cadresplash)
		self.parent.serveur.getTablesMod(self.parent.idProjet)
		self.afficherListeTables()
		
	def afficherListeTables(self):
		self.listTables.delete(0,'end')
		for nomTable in self.parent.serveur.getTablesMod(self.parent.idProjet):
			self.listTables.insert(self.listTables.size(), nomTable)

		
		
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
		
	def deleteTable(self):
		nomTable = self.listTables.get(self.listTables.curselection())[0]
		requete = 'DELETE FROM modelisation WHERE id_projet = ? AND nom_table = ?'
		idProjet = str(self.parent.idProjet)
		self.parent.serveur.entreeGenerique(requete, (idProjet,nomTable) )
		self.clearTable()
		self.afficherListeTables()
		
		
		
	def loadTable(self, event):
		self.clearTable()
		textTable = self.parent.serveur.loadTable( self.listTables.get(self.listTables.curselection())[0], self.parent.idProjet)
		for ligne in textTable[0].split('\n'):
			if ligne!= "":
				words = ligne.split(',')
				for i in range(5):
					self.listBoxes[i].insert(self.listBoxes[i].size(), words[i])
		self.insertNom()
	
	def selectLine(self, event):
		indexLine = self.listNom.nearest(event.y) #determine l'index du texte clique en fonction du y de la souris
		selected = ""
		for i in range(5):
			selected = self.listBoxes[i].get(indexLine) #prend le texte choisi dans la listbox
			self.listBoxes[i].selection_clear(0, END) #annule la selection dans la listbox
			self.listBoxes[i].selection_set(indexLine)#selectionne l'index choisi dans chaque listbox
			self.lineEntries[i].delete(0, 'end') # enleve le text des entries
			self.lineEntries[i].insert(0,selected) #set le text des entries pour le text selectionne
			
		self.entryNumLigne.delete(0, 'end')
		self.entryNumLigne.insert(0, indexLine)
	
	def creercadresplash(self):
		self.cadresplash=Frame(self.root, bg=self.couleur500)
		
		self.frameModNom = Frame(self.cadresplash, bg=self.couleur500)
		self.frameModTables = Frame(self.cadresplash, bg=self.couleur500)
		self.frameModListBox = Frame(self.cadresplash, bg=self.couleur500)
		
		self.frameModNom.grid(column=1, row=0, sticky=W+E)
		self.frameModTables.grid(column=0, row=0, rowspan=10, sticky=N+S+W+E)
		self.frameModListBox.grid(column=1, row=1, sticky=N+S+W+E)

	
		self.listTables = Listbox(self.frameModTables,height=15, width=12, bg="#D3D3D3", font = ('Courier New',13))
		self.listTables.pack(side=LEFT)


		
		self.scroll = Scrollbar(self.frameModListBox,orient=VERTICAL,command=self.monScroll)

		self.listNom = Listbox(self.frameModListBox,  height=20,width=12, bg="#D3D3D3",  font = ('Courier New',13),exportselection=0,yscrollcommand=self.scroll.set)
		self.listType = Listbox(self.frameModListBox,  height=20,width=12, bg="#D3D3D3", font = ('Courier New',13),exportselection=0, yscrollcommand=self.scroll.set)
		self.listKey = Listbox(self.frameModListBox,  height=20,width=12, bg="#D3D3D3", font = ('Courier New',13), exportselection=0, yscrollcommand=self.scroll.set)
		self.listNN = Listbox(self.frameModListBox,  height=20,width=12, bg="#D3D3D3", font = ('Courier New',13),exportselection=0, yscrollcommand=self.scroll.set)
		self.listDefault = Listbox(self.frameModListBox,  height=20,width=12, bg="#D3D3D3", font = ('Courier New',13), exportselection=0, yscrollcommand=self.scroll.set)
		self.listBoxes = [ self.listNom, self.listType, self.listKey, self.listNN, self.listDefault ]
		
		for listbox in self.listBoxes:
			listbox.bind("<Button-1>", self.selectLine)

		
		self.listTables.bind("<Double-Button-1>", self.loadTable)
		
		self.lableMsgErreur = Label(self.frameModListBox, bd=1,text="Message d'erreur : veuillez remplir tous les champs!",fg="red",font = ("Courier New", 12, "bold"),bg=self.couleur500)
		
		self.labelListeTables = Label(self.frameModNom, bd=1,text="Tables",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.labelNomTable = Label(self.frameModNom,bd=1,text="Nom de la nouvelle table: ",fg=self.couleurAccent, font = ("Courier New", 10, "bold"),bg=self.couleur500)
				
		self.labelNTable = Label(self.frameModNom,bd=1,text="",fg='white',font = ("Courier New", 13, "bold"), bg=self.couleur500)
		
		self.entryNumLigne=Entry(self.frameModListBox,bg=self.couleurAccent, relief = "sunken", font = ("Courier New", 12, "bold"), fg = self.couleur500,justify='center')
		
		self.entryNomTable=Entry(self.frameModNom ,bg="#D3D3D3", relief = "sunken", font = ("Courier New", 12, "bold"),justify='center')
			
		btnNew=Button(self.frameModNom, text=" CREATE ",bg=self.couleurAccent, relief = "raised", font = ("Courier New", 14, "bold"), fg = 'Black',command=self.nouvelleTable)
			
		self.labelNomChamp = Label(self.frameModListBox,bd=1,text="Nom ",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.entryNomChamp=Entry(self.frameModListBox, bg=self.couleurAccent, relief = "sunken",font = ("Courier New", 10, "bold"),fg = "#dbdbdb",justify='center', width= 8)

		self.labelTypeChamp = Label(self.frameModListBox,bd=1,text="Type ",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.entryTypeChamp=Entry(self.frameModListBox, bg=self.couleurAccent,	relief = "sunken",font = ("Courier New", 10, "bold"),fg = "#dbdbdb",justify='center', width= 8)

		self.labelKeyChamp = Label(self.frameModListBox,bd=1,text="Cle ",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.entryKeyChamp=Entry(self.frameModListBox, bg=self.couleurAccent,relief = "sunken",font = ("Courier New", 10, "bold"),fg = "#dbdbdb",justify='center', width= 8)
		
		self.labelNNChamp = Label(self.frameModListBox,bd=1,text="Non nul",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.entryNNChamp=Entry(self.frameModListBox, bg=self.couleurAccent,relief = "sunken",font = ("Courier New", 10, "bold"),fg = "#dbdbdb",justify='center', width= 8)
			
		self.labelDefaultChamp = Label(self.frameModListBox,bd=1,text="Defaut ",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
			
		self.entryDefaultChamp=Entry(self.frameModListBox, bg=self.couleurAccent,relief = "sunken",font = ("Courier New", 10, "bold"),fg = "#dbdbdb",justify='center', width= 8)
			
		btnAdd=Button(self.frameModListBox, text="+Ligne", bg=self.couleurAccent,relief = "raised",font = ("Courier New", 12, "bold"),fg = 'black',command=self.insertLineToTable)
			
		btnUpdate=Button(self.frameModListBox, text="UPDATE", bg=self.couleurAccent,relief = "raised",font = ("Courier New", 12, "bold"),fg = "black",command=self.updateLigne)
			
		#btnSave=Button(self.frameModNom,	text=" Save ",bg=self.couleurAccent,relief = "raised",font = ("Courier New", 14, "bold"),fg = "#dbdbdb",command= self.saveTable)  
			
		btnDelete=Button(self.frameModTables, text=" DELETE ",bg=self.couleurAccent,relief = "raised",font = ("Courier New", 14, "bold"),fg = "black", command=self.deleteTable)
			
		self.labelNumLigne = Label(self.frameModListBox,bd=1,text="Ligne:",fg=self.couleurAccent,font = ("Courier New", 10, "bold"),bg=self.couleur500)
			
		self.labelNomCetteTable = Label(self.frameModNom,bd=1,text="Table active: ",fg=self.couleurAccent,font = ("Courier New", 12, "bold"),bg=self.couleur500)
		
		btnDelete.pack( side = BOTTOM)

		self.labelNomTable.grid(column=1, row=1, sticky=N+S+W+E)
		self.entryNomTable.grid(column=2, row=1, sticky=N+S+W+E)
		self.labelNomCetteTable.grid(column=1, row=3, sticky=N+S+W+E)
		self.labelNTable.grid(column=2, row=3, sticky=N+S+W+E)
		btnNew.grid(column=6, row=1, sticky=N+S+W+E)
		self.scroll.grid(column=7, row=0, sticky=N+S+W+E)
		
		
			
		self.listNom.grid(column=0, row=0, sticky=N+S+W+E)
		self.entryNomChamp.grid(column=0, row=1, sticky=N+S+W+E)
		self.listType.grid(column=1, row=0, sticky=N+S+W+E)
		self.entryTypeChamp.grid(column=1, row=1, sticky=N+S+W+E)
		self.listKey.grid(column=2, row=0, sticky=N+S+W+E)
		self.entryKeyChamp.grid(column=2, row=1, sticky=N+S+W+E)
		self.listNN.grid(column=3, row=0, sticky=N+S+W+E)
		self.entryNNChamp.grid(column=3, row=1, sticky=N+S+W+E)
		self.listDefault.grid(column=4, row=0, sticky=N+S+W+E)
		self.entryDefaultChamp.grid(column=4, row=1, sticky=N+S+W+E)
		#self.lableMsgErreur.grid(column=1, row=5, sticky=N+S+W+E)
		btnAdd.grid(column=5, row=1, sticky=N+S+W+E)
		btnUpdate.grid(column=5, row=2, sticky=N+S+W+E)
		

		self.lineEntries = [ self.entryNomChamp, self.entryTypeChamp, self.entryKeyChamp, self.entryNNChamp, self.entryDefaultChamp]


	def verifierMsgErreur(self):
		motEntre = self.entryNomChamp.get()
		if motEntre =="":
			self.lableMsgErreur.grid(column=1, row=5, sticky=N+S+W+E)

	
	
	def monScroll (self, *args):
		
		self.listNom.yview(*args)
		self.listType.yview(*args)
		self.listKey.yview(*args)
		self.listNN.yview(*args)
		self.listDefault.yview(*args)
		
	
	def	updateLigne(self):
		numLigne = int(self.entryNumLigne.get())
		updatedText = ""
		for i in range(5):
			lb = self.listBoxes[i]
			updatedText = self.lineEntries[i].get()
			lb.delete(numLigne)
			lb.insert(numLigne, updatedText)

		
	def insertLineToTable(self):
		line = [entry.get() for entry in self.lineEntries]
		for i in range(5):
			listbox = self.listBoxes[i]
			listbox.insert(listbox.size(), line[i])
	
	def clearTable(self):
		for i in self.listBoxes:
			i.delete(0,'end')

	
	def getShownTableText(self):
		texteDeLaTableAffiche = ""
		for i in range( self.listNom.size() ):
			texteDeLaTableAffiche+= ",".join( [lb.get(i) for lb in self.listBoxes] )
			texteDeLaTableAffiche+='\n'
		return texteDeLaTableAffiche
	
	
	def saveTable(self):
		texteDeLaTable = self.getShownTableText()
		nomTable = self.labelNTable['text']
		requete = 'INSERT INTO modelisation(id_projet, texte_table, nom_table) VALUES (?, ?, ?)'
		params = ( self.parent.idProjet, texteDeLaTable,nomTable )#Changer param3 pour LabelNtable?
		if self.parent.serveur.entreeGenerique( requete, params )!="ok":
			requete = 'UPDATE modelisation SET texte_table = ? WHERE id_projet = ? AND nom_table = ?'
			params = ( texteDeLaTable, self.parent.idProjet,self.labelNTable['text'] )
			self.parent.serveur.entreeGenerique( requete, params )
		#self.afficherListeTables()
		self.selectByName(nomTable, self.listTables)
		
	def selectByName(self, elementName, listbox):
		for i in range(listbox.size()):
			if listbox.get(i)[0]==elementName:
				listbox.selection_set(i)
	
	def nouvelleTable(self):
		self.clearTable()

		nomEntre = self.entryNomTable.get()
		if nomEntre !="":
			requete = 'INSERT INTO modelisation(id_projet, texte_table, nom_table) VALUES (?, ?, ?)'
			params = (self.parent.idProjet, "",nomEntre)
			self.parent.serveur.entreeGenerique(requete, params)
			self.afficherListeTables()
			self.selectByName(nomEntre, self.listTables)
			self.insertNom()
		else :	
			print("champ nom vide") 
	
	def insertNom(self):
		nom = self.listTables.get(self.listTables.curselection())[0]
		self.labelNTable.config(text=nom)
		
	def fermerfenetre(self):
		print("ONFERME la fenetre")
		self.root.destroy()
	