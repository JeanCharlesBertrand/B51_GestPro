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
		self.root.title(os.path.basename(sys.argv[0]))
		self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
		self.parent=parent
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
		indexLine = self.listNom.nearest(event.y) #détermine l'index du texte cliqué en fonction du y de la souris
		selected = ""
		for i in range(5):
			selected = self.listBoxes[i].get(indexLine) #prend le texte choisi dans la listbox
			self.listBoxes[i].selection_clear(0, END) #annule la sélection dans la listbox
			self.listBoxes[i].selection_set(indexLine)#selectionne l'index choisi dans chaque listbox
			self.lineEntries[i].delete(0, 'end') # enleve le text des entries
			self.lineEntries[i].insert(0,selected) #set le text des entries pour le text selectionné
			
		self.entryNumLigne.delete(0, 'end')
		self.entryNumLigne.insert(0, indexLine)
	
	def creercadresplash(self):
		self.cadresplash=Frame(self.root)
		self.canevasplash=Canvas(self.cadresplash,width=640,height=480,bg="#282E3F")
		self.canevasplash.pack()
		self.listTables = Listbox(self.cadresplash,height=15, width=12, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listTables.place(x= 20, y=100)

		self.scrollbar = Scrollbar(orient="vertical")
	
		
		self.listNom = Listbox(self.cadresplash,  height=500, bg="#002887", font = ('Courier New',13), fg = 'white', exportselection=0, yscrollcommand=self.scrollbar.set)
		self.listNom.place(x= 150, y=160,width=65, height=235)
		self.listType = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white', exportselection=0, yscrollcommand=self.scrollbar.set)
		self.listType.place(x= 230, y=160,width=65, height=235)
		self.listKey = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white', exportselection=0, yscrollcommand=self.scrollbar.set)
		self.listKey.place(x= 310, y=160,width=65, height=235)
		self.listNN = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white', exportselection=0, yscrollcommand=self.scrollbar.set)
		self.listNN.place(x= 390, y=160,width=65, height=235)
		self.listDefault = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white', exportselection=0, yscrollcommand=self.scrollbar.set)
		self.listDefault.place(x= 470, y=160,width=65, height=235)
		self.listBoxes = [ self.listNom, self.listType, self.listKey, self.listNN, self.listDefault ]
		

		for listbox in self.listBoxes:
			listbox.bind("<Button-1>", self.selectLine)
		
		self.listTables.bind("<Double-Button-1>", self.loadTable)
		self.canevasplash.create_line(0, 50, 640, 50, fill="black")
		
		self.labelListeTables = Label(
			self.cadresplash, 
			bd=1,
			text="Tables",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.labelNomTable = Label(
			self.cadresplash,
			bd=1,
			text="Nom de la nouvelle table: ",fg="#4C9689",
			font = ("Courier New", 10, "bold"),
			bg="#282E3F")
				
		self.labelNTable = Label(
			self.cadresplash,
			bd=1,
			text="",fg="#4C9689",
			font = ("Courier New", 13, "bold"),
			bg="#282E3F")
		
		self.entryNumLigne=Entry(
			bg="#4C9689",
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')
		
		self.entryNomTable=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')
			
		btnNew=Button(                                    
            text=" CREATE ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb",
			command=self.nouvelleTable)
			
		#btnClear=Button(                                    
        #    text=" CLEAR ",
        #    bg="#4C9689",                                             
        #    relief = "raised",
        #    font = ("Courier New", 14, "bold"),
        #    fg = "#dbdbdb",
		#	command=self.clearTable)  

		self.labelNomChamp = Label(
			self.cadresplash,
			bd=1,
			text="Nom ",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.entryNomChamp=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 10, "bold"),
			fg = "#dbdbdb",justify='center', width= 8)

		self.labelTypeChamp = Label(
			self.cadresplash,
			bd=1,
			text="Type ",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.entryTypeChamp=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 10, "bold"),
			fg = "#dbdbdb",justify='center', width= 8)

		self.labelKeyChamp = Label(
			self.cadresplash,
			bd=1,
			text="Clé ",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.entryKeyChamp=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 10, "bold"),
			fg = "#dbdbdb",justify='center', width= 8)
		
		self.labelNNChamp = Label(
			self.cadresplash,
			bd=1,
			text="Non nul",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.entryNNChamp=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 10, "bold"),
			fg = "#dbdbdb",justify='center', width= 8)
			
		self.labelDefaultChamp = Label(
			self.cadresplash,
			bd=1,
			text="Défaut ",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		self.entryDefaultChamp=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 10, "bold"),
			fg = "#dbdbdb",justify='center', width= 8)
			
		btnAdd=Button(                                    
            text="+Ligne",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",
			command=self.insertLineToTable)
			
		btnUpdate=Button(                                    
            text="UPDATE",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",
			command=self.updateLigne)
			
		btnSave=Button(                                    
            text=" Save ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb",
			command= self.saveTable)  
			
		btnDelete=Button(                                    
            text=" DELETE ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb", command=self.deleteTable)
			
		self.labelNumLigne = Label(
			self.cadresplash,
			bd=1,
			text="Ligne:",fg="#4C9689",
			font = ("Courier New", 10, "bold"),
			bg="#282E3F")
			
		self.labelNomCetteTable = Label(
			self.cadresplash,
			bd=1,
			text="Table active: ",fg="#4C9689",
			font = ("Courier New", 12, "bold"),
			bg="#282E3F")
			
		
		self.labelDefaultChamp.place(x=470, y=140)
		self.entryDefaultChamp.place(x=470, y= 400)
		self.labelDefaultChamp.place(x=470, y=140)
		self.entryNNChamp.place(x=390, y= 400)
		self.labelNNChamp.place(x=382, y=140)
		self.entryKeyChamp.place(x=310, y= 400)
		self.labelKeyChamp.place(x=323, y=140)
		self.entryNomChamp.place(x=150, y= 400)
		self.labelNomChamp.place(x=160, y=140)
		self.entryTypeChamp.place(x=230, y= 400)
		self.labelTypeChamp.place(x=240, y=140)

		self.lineEntries = [ self.entryNomChamp, self.entryTypeChamp, self.entryKeyChamp, self.entryNNChamp, self.entryDefaultChamp]


		self.canevasplash.create_window(605,80,window=btnNew,width=70,height=30)
		self.canevasplash.create_window(605,115,window=btnSave,width=70,height=30)
		#self.canevasplash.create_window(605,150,window=btnClear,width=70,height=30)

		self.entryNumLigne.place(x=588, y=372, width=28)
		self.labelNumLigne.place(x=537, y=372)
		self.canevasplash.create_window(580, 437,window=btnAdd,width=75,height=25)
		self.canevasplash.create_window(580, 412,window=btnUpdate,width=75,height=25)
		self.canevasplash.create_window(80,450,window=btnDelete,width=120,height=30)
		self.entryNomTable.place(x=363, y= 70)
		self.labelNomTable.place(x=160, y=70)
		self.labelNTable.place(x=320,y=100)
		self.labelNomCetteTable.place(x=160, y=100)
		self.labelListeTables.place(x= 20, y=70)
		
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
	
	def insertNom(self):
		nom = self.listTables.get(self.listTables.curselection())[0]
		self.labelNTable.config(text=nom)
		
	def fermerfenetre(self):
		print("ONFERME la fenetre")
		self.root.destroy()
	