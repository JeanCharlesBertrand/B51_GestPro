# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp

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
				
	def creercadresplash(self):
		self.cadresplash=Frame(self.root)
		self.canevasplash=Canvas(self.cadresplash,width=640,height=480,bg="#282E3F")
		self.canevasplash.pack()
		
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
			text="Nom de la table: ",fg="#4C9689",
			font = ("Courier New", 10, "bold"),
			bg="#282E3F")
				
		self.labelNTable = Label(
			self.cadresplash,
			bd=1,
			text="",fg="#4C9689",
			font = ("Courier New", 13, "bold"),
			bg="#282E3F")
			
		self.entryNomTable=Entry(
			bg="#4C9689",		
			relief = "sunken",
			font = ("Courier New", 12, "bold"),
			fg = "#dbdbdb",justify='center')
			
		btnNew=Button(                                    
            text=" NEW ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb",
			command=self.insertNom)  

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
            text=" + ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb",
			command=self.insertLineToTable) 
			
		btnSave=Button(                                    
            text=" Save ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb",
			command=self.insertNom)  
			
		btnDelete=Button(                                    
            text=" DELETE ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb")
			#command=self.loginclient)  

			
		self.labelNomCetteTable = Label(
			self.cadresplash,
			bd=1,
			text="Votre table: ",fg="#4C9689",
			font = ("Courier New", 10, "bold"),
			bg="#282E3F")
		self.labelDefaultChamp.place(x=500, y=140)
		self.entryDefaultChamp.place(x=500, y= 400)
		self.labelDefaultChamp.place(x=500, y=140)
		self.entryNNChamp.place(x=420, y= 400)
		self.labelNNChamp.place(x=412, y=140)
		self.entryKeyChamp.place(x=340, y= 400)
		self.labelKeyChamp.place(x=353, y=140)
		self.entryNomChamp.place(x=180, y= 400)
		self.labelNomChamp.place(x=190, y=140)
		self.entryTypeChamp.place(x=260, y= 400)
		self.labelTypeChamp.place(x=270, y=140)

		self.lineEntries = [ self.entryNomChamp, self.entryTypeChamp, self.entryKeyChamp, self.entryNNChamp, self.entryDefaultChamp]


		self.canevasplash.create_window(580,80,window=btnNew,width=60,height=30)
		self.canevasplash.create_window(602,412,window=btnAdd,width=30,height=30)
		self.canevasplash.create_window(580,120,window=btnSave,width=60,height=30)
		self.canevasplash.create_window(80,450,window=btnDelete,width=120,height=30)

		self.entryNomTable.place(x=320, y= 70)
		self.labelNomTable.place(x=160, y=70)
		self.labelNTable.place(x=320,y=100)
		self.labelNomCetteTable.place(x=160, y=100)
		self.labelListeTables.place(x= 20, y=70)
		self.listTables = Listbox(self.cadresplash,height=20, bg="#002887")
		self.listTables.place(x= 20, y=100)
		self.listNom = Listbox(self.cadresplash,  height=500, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listNom.place(x= 180, y=160,width=65, height=235)
		self.listType = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listType.place(x= 260, y=160,width=65, height=235)
		self.listKey = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listKey.place(x= 340, y=160,width=65, height=235)
		self.listNN = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listNN.place(x= 420, y=160,width=65, height=235)
		self.listDefault = Listbox(self.cadresplash, width=20, bg="#002887", font = ('Courier New',13), fg = 'white')
		self.listDefault.place(x= 500, y=160,width=65, height=235)
		
		self.listBoxes = [ self.listNom, self.listType, self.listKey, self.listNN, self.listDefault  ]
		
	def insertLineToTable(self):
		line = [entry.get() for entry in self.lineEntries]
		for i in range(5):
			listbox = self.listBoxes[i]
			listbox.insert(listbox.size(), line[i])
		
		#print(line)
	def insertNom(self):
		nom = self.entryNomTable.get()
		print("monNom", nom)
		self.labelNTable.config(text=nom)
		print(nom)
		
	def fermerfenetre(self):
		print("ONFERME la fenetre")
		self.root.destroy()
	