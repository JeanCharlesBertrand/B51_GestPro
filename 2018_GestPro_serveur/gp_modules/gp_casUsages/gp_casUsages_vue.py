

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
        self.scenario = Frame(self.frameModuleCU)
        
        self.listeCas.grid(column=0, row=0, rowspan=2, sticky=E)
        self.infoCas.grid(column=1, row=0, sticky=N)
        self.scenario.grid(column=1, row=1, sticky=N)
        
        self.listeCasUsage = Listbox(self.listeCas, background="#4C9689", bd=0, height=50)
        self.listeCasUsage.grid(row = 0, column = 0, sticky = "nsew")
        
        for i in range(500):
            self.listeCasUsage.insert(END, i)
        
        self.scrollCasUsage = Scrollbar(self.listeCas)
        self.scrollCasUsage.grid(row = 0, column = 1, sticky = "nsew")
        
        self.listeCasUsage.config(yscrollcommand=self.scrollCasUsage.set)
        self.scrollCasUsage.config(command=self.listeCasUsage.yview)
        
        self.frameModuleCU.columnconfigure(0, weight=1)
        self.frameModuleCU.columnconfigure(1, weight=3)
        
        self.frameModuleCU.rowconfigure(0, weight=1)
        self.frameModuleCU.rowconfigure(1, weight=2)
        
   
        
        
        self.labelTitreModule = Label(self.infoCas, text="Scénario d'utilisation", font=("Arial", 25, "bold"))
        self.labelTitreModule.grid(row=0, column=0, sticky=N)
        
        self.entryCas = Entry(self.infoCas, width=75)
        self.entryCas.grid(row=1, column=0, sticky=S)

        self.scenario.columnconfigure(0, weight=1)
        self.scenario.columnconfigure(1, weight=1)
        self.scenario.columnconfigure(2, weight=1)

        
        self.labelUsager = Label(self.scenario, text="Usager", font=("Arial", 12, "bold"))
        self.labelUsager.grid(row=0, column=0)
        
        self.labelOrdinateur = Label(self.scenario, text="Ordinateur", font=("Arial", 12, "bold"))
        self.labelOrdinateur.grid(row=0, column=1)
        
        self.labelAutre = Label(self.scenario, text="Autre", font=("Arial", 12, "bold"))
        self.labelAutre.grid(row=0, column=2)
                
        self.frameModuleCU.pack()
        
        

    def creerFrameCasUsage1(self):
        self.frameModuleCU = Frame(self.root, bg="red")
        
        self.frameCasUsage = Frame(self.frameModuleCU,bg=self.couleur500)
        self.frameScenario = Frame(self.frameModuleCU,bg=self.couleur500)


        self.frameModuleCU.pack
        self.frameCasUsage.place
        self.frameScenario.grid(row = 0, column = 1, sticky = "nse")

        
        
        
        self.listeCasUsage = Listbox(self.frameCasUsage, background="#4C9689", bd=0, height=50)
        self.listeCasUsage.grid(row = 0, column = 0, sticky = "nsew")
        
        self.scrollCasUsage = Scrollbar(self.frameCasUsage)
        self.scrollCasUsage.grid(row = 0, column = 1, sticky = "nsew")
        
        self.listeCasUsage.config(yscrollcommand=self.scrollCasUsage.set)
        self.scrollCasUsage.config(command=self.listeCasUsage.yview)
        
        self.creerScenario()
        
        

    #def creerLabel(self):
       #texte = self.entCasUsage.get()
       #self.listeCasUsage.insert(END, texte)





if __name__ == '__main__':
    m=Vue()
    m.root.mainloop()