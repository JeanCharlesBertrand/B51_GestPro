

from tkinter import *

class Vue():
    def __init__(self):
        self.root = Tk()
        self.root.title("Omada")
        #self.root.geometry('1200x800')

        self.couleur500 = "#282E3F"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#FFFFFF"
        self.couleurAccent = "#4C9689"
        self.couleurSelection = "#FF4181"
   
        self.creerFrameCasUsage()
        
        
    def creerFrameCasUsage(self):
        
        self.frameModuleCU = Frame(self.root, bg="red")
        
        self.listeCas = Frame(self.frameModuleCU)
        self.infoCas = Frame(self.frameModuleCU)
        self.scenario = Frame(self.frameModuleCU, bg="blue")
        
        self.listeCas.grid(column=0, row=0, rowspan=2, sticky=N+S+W+E)
        self.infoCas.grid(column=1, row=0, sticky=N+S+W+E)
        self.scenario.grid(column=1, row=1, sticky=N+S+W+E)
        
        ##    Liste cas d'usage    ##
        
        self.listeCasUsage = Listbox(self.listeCas, background="lightgreen",height=30)
        self.listeCasUsage.pack(side=LEFT, expand=1, fill=BOTH)
        
        for i in range(500):
            self.listeCasUsage.insert(END, i)
        
        self.scrollCasUsage = Scrollbar(self.listeCas)
        self.scrollCasUsage.pack(side=LEFT, fill=Y)
        self.listeCasUsage.config(yscrollcommand=self.scrollCasUsage.set)
        self.scrollCasUsage.config(command=self.listeCasUsage.yview)
        
        self.frameModuleCU.columnconfigure(0, weight=1)
        self.frameModuleCU.columnconfigure(1, weight=3)
        
        self.frameModuleCU.rowconfigure(0, weight=1)
        self.frameModuleCU.rowconfigure(1, weight=3)
        
        
        ##    Cas d'usage entry    ##
        
        self.infoCas.rowconfigure(0, weight=1)
        self.infoCas.rowconfigure(1, weight=1)
        
        self.labelTitreModule = Label(self.infoCas, text="Scénario d'utilisation", font=("Arial", 25, "bold"))
        self.labelTitreModule.grid(row=0, column=0)
        
        self.entryCas = Entry(self.infoCas)
        self.entryCas.grid(row=1, column=0)
  
       
       ##    Scénario    ##
       
        self.scenario.columnconfigure(0, weight=1)
        self.scenario.columnconfigure(1, weight=1)
        self.scenario.columnconfigure(2, weight=1)
        
        self.scenario.rowconfigure(0, weight=1)
        self.scenario.rowconfigure(1, weight=1)
        self.scenario.rowconfigure(2, weight=5)
        
        
            #Label
        self.labelUsager = Label(self.scenario, text="Usager", font=("Arial", 12, "bold"))
        self.labelUsager.grid(row=0, column=0)
        
        self.labelOrdinateur = Label(self.scenario, text="Ordinateur", font=("Arial", 12, "bold"))
        self.labelOrdinateur.grid(row=0, column=1)
        
        self.labelAutre = Label(self.scenario, text="Autre", font=("Arial", 12, "bold"))
        self.labelAutre.grid(row=0, column=2)
        
            #Entry
        self.entryUsager = Entry(self.scenario)
        self.entryUsager.grid(row=1, column=0)
        
        self.entryOrdi = Entry(self.scenario)
        self.entryOrdi.grid(row=1, column=1)
        
        self.entryAutre = Entry(self.scenario)
        self.entryAutre.grid(row=1, column=2)
        
        self.entryUsager = Entry(self.scenario)
        self.entryCas.grid(row=1, column=0)
        
            #ListBox
            
                #Usager
        self.listeUsager = Listbox(self.scenario, background="red")
        self.listeUsager.grid(row=2, column=0, sticky=N+S+W+E)
    
        self.scrollUsager = Scrollbar(self.listeUsager)
        self.scrollUsager.pack(side=LEFT, fill=Y)
        self.listeUsager.config(yscrollcommand=self.scrollUsager.set)
        self.scrollUsager.config(command=self.listeUsager.yview)
        
                #Ordi
        self.listeOrdi = Listbox(self.scenario, background="red")
        self.listeOrdi.grid(row=2, column=1, sticky=N+S+W+E)

        self.scrollOrdi = Scrollbar(self.listeOrdi)
        self.scrollOrdi.pack(side=LEFT, fill=Y)
        self.listeOrdi.config(yscrollcommand=self.scrollOrdi.set)
        self.scrollOrdi.config(command=self.listeOrdi.yview)
        
                #Autre
        self.listeAutre = Listbox(self.scenario, background="red")
        self.listeAutre.grid(row=2, column=2, sticky=N+S+W+E)
    
        self.scrollAutre = Scrollbar(self.listeAutre)
        self.scrollAutre.pack(side=LEFT, fill=Y)
        self.listeAutre.config(yscrollcommand=self.scrollAutre.set)
        self.scrollAutre.config(command=self.listeAutre.yview)
        
        
        
        ###
        
        self.frameModuleCU.columnconfigure(0, weight=1)
        self.frameModuleCU.columnconfigure(1, weight=3)
                
        self.frameModuleCU.pack(expand=1,fill=BOTH)
        
        

    def inscrireCasUsageEntryDansListe(self):
        self.texteCas = self.entryCas.get()
        
        



if __name__ == '__main__':
    m=Vue()
    m.root.mainloop()