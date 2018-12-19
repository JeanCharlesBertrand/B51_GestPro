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
        self.root.iconbitmap('image/tk_logo.ico')
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
         # Main Frame
        self.gui_style = ttk.Style()
        self.gui_style.configure('My.TFrame', background='#282E3F', foreground='#dbdbdb')
        self.gui_style.configure('My.TLabel', background='#282E3F', foreground='#4C9689', font = ("Arial", 10))
        self.mainFrame = ttk.Frame(self.root, style='My.TFrame')
        self.mainFrame.pack()
        
        # Frame Title bar
        self.frameTitleBar = ttk.Frame(self.mainFrame)
        self.frameTitleBar.grid(row=0, column=1, pady=10)
        self.labelNomProjet = ttk.Label(self.frameTitleBar, text="ANALYSE TEXTUELLE", font = ("Arial", 30), background='#282E3F', foreground='#4C9689')
        self.labelNomProjet.grid(row=0, column=1)

        # Frame Enonce
        self.leftMargin = Frame(self.mainFrame)
        self.leftMargin.grid(row=1, column=0, padx=25, pady=25)
        self.frameEnonce = Frame(self.mainFrame)
        self.frameEnonce.grid(row=1, column=1, pady=25)
        self.rightMargin = Frame(self.mainFrame)
        self.rightMargin.grid(row=1, column=2, padx=25, pady=25)

        
        # Champ Text de l'enonce Analyse
        self.txtEnonce = Text(self.frameEnonce, width=100, height=15, wrap=WORD)
        self.txtEnonce.grid(row=0, column=1)
        self.enonceScrollb = Scrollbar(self.frameEnonce, command=self.txtEnonce.yview)
        self.enonceScrollb.grid(row=0, column=2, sticky='nsew')
        self.txtEnonce['yscrollcommand'] = self.enonceScrollb.set
        
        
        # Frame boutons Importer Exporter Sauvegarder
        self.frameBtnCentre = ttk.Frame(self.mainFrame, style='My.TFrame')
        self.frameBtnCentre.grid(row=2, column=1, pady=20)
        
        self.btnImportEnonce = Button(self.frameBtnCentre, text="IMPORTER", font = ("Arial", 12), background='#4C9689', foreground='#dbdbdb', command=self.importEnonce)
        self.btnImportEnonce.grid(row=0, column=0, padx=10)
        self.btnSaveEnonce = Button(self.frameBtnCentre, text="SAUVEGARDER", font = ("Arial", 12), background='#4C9689', foreground='#dbdbdb', command=self.parent.insertIntoAnalyse)
        self.btnSaveEnonce.grid(row=0, column=1, padx=10)
        self.btnExportEnonce = Button(self.frameBtnCentre, text="EXPORTER", font = ("Arial", 12), background='#4C9689', foreground='#dbdbdb', command=self.saveToTxtFile)
        self.btnExportEnonce.grid(row=0, column=2, padx=10)
        
            
        # Frame Tableau
        self.frameTableau = ttk.Frame(self.mainFrame, style='My.TFrame')
        self.frameTableau.grid(row=3, column=1, padx=25, pady=10)
       
       # Labels Nom, Verbe, Adjectif
        self.labelNom = ttk.Label(self.frameTableau, text="NOM", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelNom.grid(row=1, column=1, pady=10)
        self.labelVerbe = ttk.Label(self.frameTableau, text="VERBE", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelVerbe.grid(row=1, column=2, pady=10)
        self.labelAdj = ttk.Label(self.frameTableau, text="ADJECTIF", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelAdj.grid(row=1, column=3, pady=10)

        # Labels Nom, Verbe, Adjectif
        self.labelNom = ttk.Label(self.frameTableau, text="IMPLICITE", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelNom.grid(row=2, column=0, padx=10)
        self.labelVerbe = ttk.Label(self.frameTableau, text="EXPLICITE", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelVerbe.grid(row=3, column=0, padx=10)
        self.labelAdj = ttk.Label(self.frameTableau, text="SUPPLEMENTAIRE", font = ("Arial", 12), background='#282E3F', foreground='#4C9689')
        self.labelAdj.grid(row=4, column=0, padx=10)

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
        
        # Frame Marge bas
        self.bottomMargin = Frame(self.mainFrame)
        self.bottomMargin.grid(row=4, column=1, padx=25, pady=25)
        
        
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
        
    def exportEnonce(self):
        pass
        
    def prepaInsertList(self):
        ListInsert = list()
        ListInsert.append(self.txtEnonce.get("1.0", END))
        ListInsert.append(self.tabNomImplicite.get("1.0", END))
        ListInsert.append(self.tabVerbeImplicite.get("1.0", END))
        ListInsert.append(self.tabAdjImplicite.get("1.0", END))
        ListInsert.append(self.tabNomExplicite.get("1.0", END))
        ListInsert.append(self.tabVerbeExplicite.get("1.0", END))
        ListInsert.append(self.tabAdjExplicite.get("1.0", END))
        ListInsert.append(self.tabNomSupp.get("1.0", END))
        ListInsert.append(self.tabVerbeSupp.get("1.0", END))  
        ListInsert.append(self.tabAdjSupp.get("1.0", END)) 
        return ListInsert
    
    def showListeSelect(self):
        self.selectList=self.parent.selectFromAnalyse()
        try:
            print(self.selectList)
            self.txtEnonce.delete("1.0", END)
            self.txtEnonce.insert("1.0", self.selectList[2])
            self.tabNomImplicite.delete("1.0", END)
            self.tabNomImplicite.insert("1.0", self.selectList[3])
            self.tabVerbeImplicite.delete("1.0", END)
            self.tabVerbeImplicite.insert("1.0", self.selectList[4])
            self.tabAdjImplicite.delete("1.0", END)
            self.tabAdjImplicite.insert("1.0", self.selectList[5])
            self.tabNomExplicite.delete("1.0", END)
            self.tabNomExplicite.insert("1.0", self.selectList[6])
            self.tabVerbeExplicite.delete("1.0", END)
            self.tabVerbeExplicite.insert("1.0", self.selectList[7])
            self.tabAdjExplicite.delete("1.0", END)
            self.tabAdjExplicite.insert("1.0", self.selectList[8])
            self.tabNomSupp.delete("1.0", END)
            self.tabNomSupp.insert("1.0", self.selectList[9])
            self.tabVerbeSupp.delete("1.0", END)  
            self.tabVerbeSupp.insert("1.0", self.selectList[10])  
            self.tabAdjSupp.delete("1.0", END)
            self.tabAdjSupp.insert("1.0", self.selectList[11])
        except Exception as e:
            pass

    
    # Importer un fichier texte pour l'enonce
    def readTxtFile(self, filePath):
        try:
            with open(filePath, 'r') as file:
                file = file.read()
                for line in file:
                    self.txtEnonce.insert(END, line)
        except IOError as e:
            print("File not found")
    
    # Sauvegarde l'enonce dans un fichier texte        
    def saveToTxtFile(self):
        file_path = filedialog.asksaveasfile()
        content=self.txtEnonce.get("1.0", END)
        file_path.write(content)
        file_path.close()

    # Fenetre pour sélectionner un fichier à ouvrir
    def openTxtFile(self):
        file_path = filedialog.askopenfilename()
        return file_path
        
    def fermerfenetre(self):
        print("ONFERME la fenetre")
        self.root.destroy()
    