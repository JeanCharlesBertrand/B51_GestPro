

class Modele():
    def __init__(self, parent, idProjet):
        self.parent=parent
        self.idProjet=idProjet
        self.listeCas=[]
        
    def creerCas(self, idBD, casUsage):
        rep=self.getCas(casUsage)
        if rep == 0:
            cas=CasUsage(idBD, casUsage)
            self.listeCas.append(cas)
            return cas
        
        return rep
            
        
    def getCas(self, nomCas):
        for i in self.listeCas:
            if nomCas == i.casUsage:
                return i
        
        return 0
    
    
    def inscrireLigne(self, resp, texte, cas):
        rep=self.getCas(cas)
        
        if resp == "usager":
            rep.scenarioUsager.append(texte)
            rep.scenarioOrdi.append("")
            rep.scenarioAutre.append("")
            self.parent.commitLigne(resp, texte, cas)
            
        elif resp == "ordi":
            rep.scenarioUsager.append("")
            rep.scenarioOrdi.append(texte)
            rep.scenarioAutre.append("")
            
        elif resp == "autre":
            rep.scenarioUsager.append("")
            rep.scenarioOrdi.append("")
            rep.scenarioAutre.append(texte)
            
    def inscrireLigneUpload(self, usager, ordinateur, autre):
        
            rep.scenarioUsager.append(usager)
            rep.scenarioOrdi.append(ordinateur)
            rep.scenarioAutre.append(autre)
            self.parent.commitLigne(resp, texte, cas)
        
        
        
        
class CasUsage():
    def __init__(self, idBD, casUsage):
        self.idBD=idBD
        self.casUsage=casUsage
        self.scenarioUsager=[]
        self.scenarioOrdi=[]
        self.scenarioAutre=[]
        self.modifie=0

        
    