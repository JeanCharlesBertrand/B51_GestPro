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
            fg = "#dbdbdb")
			#command=self.loginclient)  

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
            fg = "#dbdbdb")
			#command=self.loginclient) 
			
		btnSave=Button(                                    
            text=" Save ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb")
			#command=self.loginclient)  
			
		btnDelete=Button(                                    
            text=" DELETE ",
            bg="#4C9689",                                             
            relief = "raised",
            font = ("Courier New", 14, "bold"),
            fg = "#dbdbdb")
			#command=self.loginclient)  

		self.entryDefaultChamp.place(x=500, y= 400)
		self.labelDefaultChamp.place(x=500, y=150)
		self.entryNNChamp.place(x=420, y= 400)
		self.labelNNChamp.place(x=412, y=150)
		self.entryKeyChamp.place(x=340, y= 400)
		self.labelKeyChamp.place(x=353, y=150)
		self.entryNomChamp.place(x=180, y= 400)
		self.labelNomChamp.place(x=190, y=150)
		self.entryTypeChamp.place(x=260, y= 400)
		self.labelTypeChamp.place(x=270, y=150)

			
		self.canevasplash.create_window(580,80,window=btnNew,width=60,height=30)
		self.canevasplash.create_window(602,412,window=btnAdd,width=30,height=30)
		self.canevasplash.create_window(580,120,window=btnSave,width=60,height=30)
		self.canevasplash.create_window(80,450,window=btnDelete,width=120,height=30)

		self.entryNomTable.place(x=320, y= 70)
		self.labelNomTable.place(x=170, y=70)
		self.labelListeTables.place(x= 20, y=70)
		listTables = Listbox(self.cadresplash,height=20, bg="#002887")
		listTables.place(x= 20, y=100)
		listNom = Listbox(self.cadresplash,  height=500, bg="#002887")
		listNom.place(x= 180, y=170,width=65, height=225)
		listType = Listbox(self.cadresplash, width=20, bg="#002887")
		listType.place(x= 260, y=170,width=65, height=225)
		listKey = Listbox(self.cadresplash, width=20, bg="#002887")
		listKey.place(x= 340, y=170,width=65, height=225)
		listNN = Listbox(self.cadresplash, width=20, bg="#002887")
		listNN.place(x= 420, y=170,width=65, height=225)
		listDefault = Listbox(self.cadresplash, width=20, bg="#002887")
		listDefault.place(x= 500, y=170,width=65, height=225)
		
		
		
	def fermerfenetre(self):
		print("ONFERME la fenetre")
		self.root.destroy()
	