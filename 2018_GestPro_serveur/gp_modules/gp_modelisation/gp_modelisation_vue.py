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

		
		self.entryNomTable.place(x=320, y= 70)
		self.labelNomTable.place(x=170, y=70)
		self.labelListeTables.place(x= 20, y=70)
		listbox = Listbox(self.cadresplash)
		listbox.place(x= 20, y=100)
		
	def fermerfenetre(self):
		print("ONFERME la fenetre")
		self.root.destroy()
	