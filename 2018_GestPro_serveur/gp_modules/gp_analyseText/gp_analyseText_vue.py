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
        #self.changecadre(self.cadresplash)
        
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
        self.mainWindow()
        #self.creercadresplash()
        #self.cadrejeu=Frame(self.root,bg="blue")
        #self.modecourant=None
                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=640,height=480,bg="#4C9689")
        self.canevasplash.pack()
        print("creer splash screen")
        
        btnTest = Button(
            text="Test",
            bg="#282E3F",
            fg = "#dbdbdb",                            #texte blanc
            justify='right',
            font = ("Courier New", 12, "bold"),
            relief="flat",
            overrelief = "raised",
            activebackground = "#4C9689")
        
        self.canevasplash.create_window(80,10,window=btnTest, width=150, height=15)
        
        self.champIdentifiant = Entry()
        
        self.champIdentifiant.config(
            bg="#4C9689",
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = "#dbdbdb",justify='center')
        
        self.canevasplash.create_window(80,60,window=self.champIdentifiant, width=150, height=15)
        
    
    def mainWindow(self):
        #self.window=Tk()
        #self.topFrame=Frame(self.root)

        lblAnalyse=Label(self.root, text='ANALYSE')
        lblAnalyse.grid(row=0, column=1)
        
        lblTableau=Label(self.root, text='TABLEAU')
        lblTableau.grid(row=0, column=2)
        
        txtEnonce = StringVar()
        champEnonce=Entry(self.root, textvariable=txtEnonce)
        champEnonce.grid(row=3, column=1, columnspan=3, rowspan=5)
        
        lblImplicite=Label(self.root, text='IMPLICITE')
        lblImplicite.grid(row=10, column=1)
        
        lblExplicite=Label(self.root, text='EXPLICITE')
        lblExplicite.grid(row=10, column=4)
        
        lblSupp=Label(self.root, text='SUPPLÉMENTAIRE')
        lblSupp.grid(row=10, column=7)
        
        test=Text(self.root)
        test.grid(row=11, column=2)
        

        
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    