

from tkinter import *
from tkinter import *
import random

class Vue():
    def __init__(self, parent):
        self.root = Tk()
        self.parent=parent
        self.root.title(self.parent.getNomProjet())
        self.root.geometry('1200x800')

        self.couleur500 = "#282E3F"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#FFFFFF"
        self.couleurAccent = "#4C9689"
        self.couleurSelection = "#FF4181"
   
        self.creerFrameCasUsage()
        
        
    def creerFrameCasUsage(self):
        
        self.frameModuleCU = Frame(self.root, bg=self.couleur500)
        
        self.frameModuleCU.columnconfigure(0, weight=5)
        self.frameModuleCU.columnconfigure(1, weight=1)
        self.frameModuleCU.columnconfigure(2, weight=9)
    
        self.frameModuleCU.rowconfigure(0, weight=1)
        self.frameModuleCU.rowconfigure(1, weight=3)
        
        self.listeCas = Frame(self.frameModuleCU)
        self.bordure = Frame(self.frameModuleCU, background=self.couleur500)
        self.infoCas = Frame(self.frameModuleCU, background=self.couleur500)
        self.scenario = Frame(self.frameModuleCU, background=self.couleur500)
        
        self.listeCas.grid(column=0, row=0, rowspan=2, sticky=N+S+W+E)
        self.bordure.grid(column=1, row=0, rowspan=2, sticky=N+S+W+E)
        self.infoCas.grid(column=2, row=0, sticky=N+S+W+E)
        self.scenario.grid(column=2, row=1, sticky=N+S+W+E)
        
        
        ##    Liste cas d'usage    ##
        
        self.listeCas.columnconfigure(0, weight=1)
        self.listeCas.columnconfigure(1, weight=1)
        
        self.listeCasUsage = Listbox(self.listeCas, background=self.couleurAccent, height=30)
        self.listeCasUsage.grid(column=0, sticky=N+S+W+E)
        
        self.scrollCasUsage = Scrollbar(self.listeCas)
        self.scrollCasUsage.grid(column=1, sticky=N+S+E)
        self.listeCasUsage.config(yscrollcommand=self.scrollCasUsage.set)
        self.scrollCasUsage.config(command=self.listeCasUsage.yview)
        
        
        ##    Cas d'usage entry    ##
        
        self.infoCas.rowconfigure(0, weight=1)
        self.infoCas.rowconfigure(1, weight=1)
       
        self.infoCas.columnconfigure(0, weight=5)
        self.infoCas.columnconfigure(1, weight=1)
        
        self.labelTitreModule = Label(self.infoCas, text="Scénario d'utilisation", font=("Arial", 25, "bold"))
        self.labelTitreModule.grid(row=0, column=0, sticky=S+W+E)
        
        self.entryCas = Entry(self.infoCas)
        self.entryCas.grid(row=1, column=0, sticky=W+E)
        
        self.boutonCasUsage = Button(self.infoCas, text="+", command=self.ajoutCas)
        self.boutonCasUsage.grid(row=1, column=1)
  
       
       ##    Scénario    ##
       
        self.scenario.columnconfigure(0, weight=1)
        self.scenario.columnconfigure(1, weight=1)
        self.scenario.columnconfigure(2, weight=1)
        self.scenario.columnconfigure(3, weight=1)
        
        self.scenario.rowconfigure(0, weight=1)
        self.scenario.rowconfigure(1, weight=1)
        self.scenario.rowconfigure(2, weight=1)
        self.scenario.rowconfigure(3, weight=5)
        self.scenario.rowconfigure(4, weight=2)
        self.scenario.rowconfigure(5, weight=1)
        
            #Label
        self.labelUsager = Label(self.scenario, text="Usager", font=("Arial", 12, "bold"), background=self.couleurAccent)
        self.labelUsager.grid(row=0, column=0, sticky=W+E)
        
        self.labelOrdinateur = Label(self.scenario, text="Ordinateur", font=("Arial", 12, "bold"), background=self.couleurAccent)
        self.labelOrdinateur.grid(row=0, column=1, sticky=W+E)
        
        self.labelAutre = Label(self.scenario, text="Autre", font=("Arial", 12, "bold"), background=self.couleurAccent)
        self.labelAutre.grid(row=0, column=2, sticky=W+E)
        
            #Entry
        self.entryUsager = Entry(self.scenario)
        self.entryUsager.grid(row=1, column=0, sticky=N+S+W+E)
        
        self.entryOrdi = Entry(self.scenario)
        self.entryOrdi.grid(row=1, column=1, sticky=N+S+W+E)
        
        self.entryAutre = Entry(self.scenario)
        self.entryAutre.grid(row=1, column=2, sticky=N+S+W+E)
        
        
        
            #Bouton
        self.boutonLigneUsager = Button(self.scenario, text="+", command=self.inscrireLigneUsager)
        self.boutonLigneUsager.grid(row=2, column=0, sticky=W+E)    
        
        self.boutonLigneOrdi = Button(self.scenario, text="+", command=self.inscrireLigneOrdi)
        self.boutonLigneOrdi.grid(row=2, column=1, sticky=W+E)    
        
        self.boutonLigneAutre = Button(self.scenario, text="+", command=self.inscrireLigneAutre)
        self.boutonLigneAutre.grid(row=2, column=2, sticky=W+E)    
    
        
            #ListBox
            
                #ScrollBar 
        self.scrollScenario = Scrollbar(self.scenario, command=self.scrollListes)
        self.scrollScenario.grid(row=3,column=3, sticky=N+S+W)
            
                #Usager
        self.listeUsager = Listbox(self.scenario, background=self.couleurAccent, yscrollcommand=self.scrollScenario.set)
        self.listeUsager.grid(row=3, column=0, sticky=N+S+W+E)
    
                #Ordi
        self.listeOrdi = Listbox(self.scenario, background=self.couleurAccent, yscrollcommand=self.scrollScenario.set)
        self.listeOrdi.grid(row=3, column=1, sticky=N+S+W+E)

                #Autre
        self.listeAutre = Listbox(self.scenario, background=self.couleurAccent, yscrollcommand=self.scrollScenario.set)
        self.listeAutre.grid(row=3, column=2, sticky=N+S+W+E)
        
        
        
        self.boutonCommit = Button(self.scenario, text="commit", command=self.sauveCasUsage)
        self.boutonCommit.grid(row=4, column=0, columnspan=3, sticky=W+E)
        
        
        
        self.boutonEffacerLigne = Button(self.scenario, text="Effacer ligne", command=self.effacerLigne)
        self.boutonEffacerLigne.grid(row=5, column=0, sticky=W+E)
        
        self.boutonEffacerListe = Button(self.scenario, text="Effacer tableau", command=self.effacerListBox)
        self.boutonEffacerListe.grid(row=5, column=2, sticky=W+E)
        
        self.pseudodata()
       
        

                ################
        
        self.frameModuleCU.columnconfigure(0, weight=1)
        self.frameModuleCU.columnconfigure(1, weight=3)
                
        self.frameModuleCU.pack(expand=1,fill=BOTH)
        
    def scrollListes(self, *args):
        self.listeUsager.yview(*args)
        self.listeOrdi.yview(*args)
        self.listeAutre.yview(*args)
     

    def pseudodata(self):
        test=["ok","jim","bill","joe","sam","chan",
              "bat","spidey","ironman","pete","carl","bob",]
        for i in range(200):
            self.listeUsager.insert(END,random.choice(test))
            self.listeOrdi.insert(END,random.choice(test))
            self.listeAutre.insert(END,random.choice(test))
  

    def inscrireCasUsageEntryDansListe(self, texte):
        self.listeCasUsage.insert(END, texte)
        self.entryCas.delete(0, END)
        
    def inscrireLigneUsager(self):
        self.texteLigne = self.entryUsager.get()
        self.listeUsager.insert(END, self.texteLigne)
        self.listeOrdi.insert(END, "")
        self.listeAutre.insert(END, "")
        self.entryUsager.delete(0, END)
        
    def inscrireLigneOrdi(self):
        self.texteLigne = self.entryOrdi.get()
        self.listeOrdi.insert(END, self.texteLigne)
        self.listeUsager.insert(END, "")
        self.listeAutre.insert(END, "")
        self.entryOrdi.delete(0, END)
        
    def inscrireLigneAutre(self):
        self.texteLigne = self.entryAutre.get()
        self.listeAutre.insert(END, self.texteLigne)
        self.listeOrdi.insert(END, "")
        self.listeUsager.insert(END, "")
        self.entryAutre.delete(0, END)
        
    def effacerLigne(self):
        self.listeUsager.delete(END, END)
        self.listeOrdi.delete(END, END)
        self.listeAutre.delete(END, END)
        
    def effacerListBox(self):
        self.listeUsager.delete(0, END)
        self.listeOrdi.delete(0, END)
        self.listeAutre.delete(0, END)
 
    def sauveCasUsage(self):
        self.texteCas = self.entryCas.get()
        
        self.UsagerListe = self.listeUsager.get(0, END)
        self.OrdiListe = self.listeOrdi.get(0, END)
        self.AutreListe = self.listeAutre.get(0, END)
        
        listeScenario = []
        
        for i in range(len(self.UsagerListe)):
            ligne=[]
            ligne.append(self.UsagerListe[i])
            ligne.append(self.OrdiListe[i])
            ligne.append(self.AutreListe[i])
            listeScenario.append([ligne])
        
        self.parent.sauveCasUsageModele(self.texteCas, listeScenario)
        
        
           
    def ajoutCas(self):
        texteCas = self.entryCas.get()
        self.parent.creerCas(texteCas)
        
        
        
            
        
