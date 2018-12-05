# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from tkinter import filedialog
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp

class Vue():
    def __init__(self,parent,largeur=800,hauteur=600):
        #self.root=tix.Tk()
        self.root=Tk()
        self.parent=parent
        #self.root.title(os.path.basename(sys.argv[0]))
        self.root.title(self.parent.getNomProjet())
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
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
        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TButton', foreground='#4C9689')
        self.gui_style.configure('My.TFrame', background='#4C9689')

         # Main Frame
        self.mainFrame = ttk.Frame(self.root)
        self.mainFrame.pack()
        
        # Frame Title bar
        self.frameTitleBar = ttk.Frame(self.mainFrame)
        self.frameTitleBar.pack()
        self.labelNomProjet = ttk.Label(self.frameTitleBar, text="Nom du projet", justify = LEFT)
        self.labelNomProjet.grid(row=0, column=0)

        # Frame Enonce
        self.frameEnonce = ttk.Frame(self.mainFrame)
        self.frameEnonce.pack()
        
        # Champ Text de l'enonce Analyse
        self.txtEnonce = Text(self.frameEnonce, width=100, height=20, wrap=WORD)
        self.txtEnonce.grid(row=0, column=0)
        self.enonceScrollb = ttk.Scrollbar(self.frameEnonce, command=self.txtEnonce.yview)
        self.enonceScrollb.grid(row=0, column=1, sticky='nsew')
        self.txtEnonce['yscrollcommand'] = self.enonceScrollb.set
        
        # Frame boutons Importer Exporter Sauvegarder
        self.frameBtnCentre = ttk.Frame(self.mainFrame, style='My.TFrame')
        self.frameBtnCentre.pack(pady=20)
        
        self.btnImportEnonce = ttk.Button(self.frameBtnCentre, text="Importer", command=self.importEnonce)
        self.btnImportEnonce.grid(row=0, column=0)
        self.btnSaveEnonce = ttk.Button(self.frameBtnCentre, text="Sauvegarder")
        self.btnSaveEnonce.grid(row=0, column=1)
        self.btnExportEnonce = ttk.Button(self.frameBtnCentre, text="Exporter", command=self.getSelectedText)
        self.btnExportEnonce.grid(row=0, column=2)
        
                
        # Frame Tableau
        self.frameTableau = ttk.Frame(self.mainFrame)
        self.frameTableau.pack()
       
       # Labels Nom, Verbe, Adjectif
        self.labelNom = ttk.Label(self.frameTableau, text="NOM")
        self.labelNom.grid(row=1, column=1)
        self.labelVerbe = ttk.Label(self.frameTableau, text="VERBE")
        self.labelVerbe.grid(row=1, column=2)
        self.labelAdj = ttk.Label(self.frameTableau, text="ADJECTIF")
        self.labelAdj.grid(row=1, column=3)

        # Labels Nom, Verbe, Adjectif
        self.labelNom = ttk.Label(self.frameTableau, text="IMPLICITE")
        self.labelNom.grid(row=2, column=0)
        self.labelVerbe = ttk.Label(self.frameTableau, text="EXPLICITE")
        self.labelVerbe.grid(row=3, column=0)
        self.labelAdj = ttk.Label(self.frameTableau, text="SUPPLEMENTAIRE")
        self.labelAdj.grid(row=4, column=0)

        self.tabNomImplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabNomImplicite.grid(row=2, column=1)
        self.tabVerbeImplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabVerbeImplicite.grid(row=2, column=2)
        self.tabAdjImplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabAdjImplicite.grid(row=2, column=3)

        self.tabNomExplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabNomExplicite.grid(row=3, column=1)
        self.tabVerbeExplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabVerbeExplicite.grid(row=3, column=2)
        self.tabAdjExplicite = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabAdjExplicite.grid(row=3, column=3)

        self.tabNomSupp = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabNomSupp.grid(row=4, column=1)
        self.tabVerbeSupp = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabVerbeSupp.grid(row=4, column=2)
        self.tabAdjSupp = Text(self.frameTableau, width=30, height=10, wrap=WORD)
        self.tabAdjSupp.grid(row=4, column=3)
        
    def getSelectedText(self):
        if self.txtEnonce.tag_ranges("sel"):
            selected=self.txtEnonce.selection_get()
            print(selected)
            if len(self.tabNomImplicite.get("1.0", END)) == 1:
                self.tabNomImplicite.insert(END, selected)
            else:
                self.tabNomImplicite.insert(END, "\n"+selected)
        else:
            pass
        
    def importEnonce(self):
        filePath = self.openTxtFile()
        txtContent = self.readTxtFile(filePath)

    def getTxtField(self):
        #input = self.txtEnonce.get("1.0", END)
        #print(input)
        pass

    def readTxtFile(self, filePath):
        fileReader = open(filePath, 'r')
        for line in fileReader:
            print(line)
            self.txtEnonce.insert(END, line)
        fileReader.close()

    def openTxtFile(self):
        file_path = filedialog.askopenfilename()
        #print(file_path)
        return file_path

    def saveToTxtFile(self):
        pass
        
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    