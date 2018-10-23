# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import tix
from tkinter import ttk
from PIL import Image,ImageDraw, ImageTk
import os,os.path
import math
from helper import Helper as hlp
import signal

class Vue():
    def __init__(self,parent,monip,largeur=800,hauteur=600):
        self.root=tix.Tk()
        self.root.title(os.path.basename(sys.argv[0]))
        self.root.protocol("WM_DELETE_WINDOW", self.fermerfenetre)
        self.monip=monip
        self.parent=parent
        self.modele=None
        self.nom=None
        self.largeur=largeur
        self.hauteur=hauteur
        self.images={}
        self.modes={}
        self.modecourant=None
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
    
    def chargercentral(self,rep):
        for i in rep:
            self.listemodules.insert(END,i)
        self.changecadre(self.cadrecentral)
        
    def creercadres(self):
        self.creercadresplash()
        self.creercadrecentral()
                
    def creercadresplash(self):
        self.cadresplash=Frame(self.root)
        self.canevasplash=Canvas(self.cadresplash,width=640,height=580,bg="red")
        self.canevasplash.pack()
        self.nomsplash=Entry(bg="pink")
        self.nomsplash.insert(0, "jmd")
        self.ipsplash=Entry(bg="pink")
        self.ipsplash.insert(0, self.monip)
        self.balIp=tix.Balloon(self.cadresplash,state="balloon")
        self.balIp.bind_widget(self.canevasplash,msg="identifiez vous et indiquez l'adresse du serveur")
        btnconnecter=Button(text="Connecter au serveur",bg="pink",command=self.loginclient)
        self.canevasplash.create_window(200,200,window=self.nomsplash,width=100,height=30)
        
        self.canevasplash.create_window(200,250,window=self.ipsplash,width=100,height=30)
        self.canevasplash.create_window(200,400,window=btnconnecter,width=100,height=30)
        
    def closeprocess(self):
        self.parent.fermerprocessus()
    
    def creercadrecentral(self):
        self.cadrecentral=Frame(self.root)
        self.canevacentral=Canvas(self.cadrecentral,width=640,height=580,bg="green")
        self.canevacentral.pack()
        
        self.listemodules=Listbox(bg="lightblue",borderwidth=0,relief=FLAT,width=40,height=6)
        self.ipcentral=Entry(bg="pink")
        self.ipcentral.insert(0, self.monip)
        btnconnecter=Button(text="Requerir module",bg="pink",command=self.requetemodule)
        self.canevacentral.create_window(200,100,window=self.listemodules)
        self.canevacentral.create_window(200,450,window=btnconnecter,width=150,height=30)
        
        btnquitproc=Button(text="Fermer dernier module",bg="red",command=self.closeprocess)
        self.canevacentral.create_window(200,500,window=btnquitproc,width=200,height=30)
        
        
    def requetemodule(self):
        mod=self.listemodules.selection_get()
        if mod:
            self.parent.requetemodule(mod)
        
    def loginclient(self):
        ipserveur=self.ipsplash.get() # lire le IP dans le champ du layout
        nom=self.nomsplash.get() # noter notre nom
        self.parent.loginclient(ipserveur,nom)
                
    def fermerfenetre(self):
        # Ici, on pourrait mettre des actions a faire avant de fermer (sauvegarder, avertir etc)
        self.parent.fermefenetre()

    
if __name__ == '__main__':
    m=Vue(0,"jmd","127.0.0.1")
    m.root.mainloop()
    