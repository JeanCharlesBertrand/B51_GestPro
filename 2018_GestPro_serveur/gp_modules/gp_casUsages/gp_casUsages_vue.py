

from tkinter import *

class Vue():
    def __init__(self):
        self.root = Tk()
        self.root.title("Omada")
        self.root.geometry('1200x800')

        self.couleur500 = "#282E3F"
        self.couleur800 = ""
        self.couleur300 = ""
        self.couleurTexte1 = "#FFFFFF"
        self.couleurTexte2 = "#FFFFFF"
        self.couleurAccent = "#4C9689"
        self.couleurSelection = "#FF4181"
        
        self.incrementLabel = 10

        self.creerFrameCasUsage()

    def creerFrameCasUsage(self):
        self.frameModuleCU = Frame(self.root)
        self.frameCasUsage = Frame(self.frameModuleCU,bg=self.couleur500, width = 200, height = 800)
        self.frameScenario = Frame(self.frameModuleCU,bg="#282E3F", width = 998, height = 800)
        self.frameBorder = Frame(self.frameModuleCU,bg = "black", width = 2, height = 800)
        self.canevasCasUsage = Canvas(self.frameCasUsage,bg="#282E3F",bd=0, highlightthickness=0, width = 200, height = 800)
        self.canevasCasUsage.grid(row = 0, column = 0, sticky = "nsew")
        self.canevasScenario = Canvas(self.frameScenario, bg="#282E3F",bd=0, highlightthickness=0, width = 998, height = 800)
        self.canevasScenario.pack()

        self.frameModuleCU.pack()

        self.frameCasUsage.grid(row = 0, column = 1, sticky = "nse")
        self.frameBorder.grid(row = 0, column =2, sticky = "ns")
        self.frameScenario.grid(row = 0, column = 3, sticky = "nse")

        self.frameCasUsage.grid_rowconfigure(60, weight = 0)
        self.frameCasUsage.grid_columnconfigure(1, weight =0)
        
        self.listeCasUsage = Listbox(self.canevasCasUsage)
        self.listeCasUsage.pack()
        
        self.scrollCasUsage = Scrollbar(self.canevasCasUsage)
        self.scrollCasUsage.pack(side = LEFT, fill=Y)
        
        self.listeCasUsage.config(yscrollcommand=self.scrollCasUsage.set)
        self.scrollCasUsage.config(command=self.listeCasUsage.yview)
        
        self.creerScenario()

    def creerLabel(self):
       texte = self.entCasUsage.get()
       self.listeCasUsage.insert(END, texte)


    def creerBtnModule(self, module):
        self.module.config(
            bg="#282E3F",
            fg = "#dbdbdb",                            
            font = ("Arial", 15),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15, 
            anchor = W)

    def creerBtnEtapeProjet(self,etapeProjet):
        self.etapeProjet.config(
            bg="#282E3F",
            fg = "#4C9689",                            
            justify='left',
            font = ("Arial", 16),
            relief="flat",
            activebackground = "#4C9689", 
            width = 15,
            anchor = W)

    def creerScenario(self):
        self.nomFenetre = "Scenario d'utilisation"
        self.lblNomFentre = Label(text = self.nomFenetre, bg = "#282E3F", fg = "#4C9689", font = ("Arial", 25, "bold"))
        self.entCasUsage = Entry(   
            bg=self.couleurAccent,        
            relief = "sunken",
            font = ("Courier New", 12, "bold"),
            fg = self.couleurTexte1,justify='center')


        self.canevasScenario.create_window(400,200, window = self.entCasUsage, width = 700, height = 30)
        self.canevasScenario.create_window(450,50, window = self.lblNomFentre)

        self.btnCommit = Button(text = "Commit",bg="#4C9689",fg = "#dbdbdb",font = ("Arial", 12), relief="raised", activebackground = "#4C9689", width = 12, command = self.creerLabel)
        self.canevasScenario.create_window(850,765, window = self.btnCommit, width = 200, height = 25)



    def creerLabelInfo(self,labelInfo):
        self.labelInfo.config(
            bg="#282E3F",                            
            justify='left',
            relief="flat",
            font = ("Arial", 12),
            activebackground = "#4C9689", 
            width = 35,
            anchor = W)


if __name__ == '__main__':
    m=Vue()
    m.root.mainloop()