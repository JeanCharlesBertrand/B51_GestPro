

class Modele():
    def __init__(self, parent, idProjet):
        self.parent=parent
        self.idProjet=idProjet
        self.listeCas=[]
        
    def creerCas(self, casUsage):
        rep=self.getCas(casUsage)
        if rep == 0:
            cas=CasUsage(casUsage)
            self.listeCas.append(cas)
            return cas
        
        return rep
            
        
    def getCas(self, nomCas):
        for i in self.listeCas:
            if nomCas == i.casUsage:
                return i
        
        return 0
        
        
        
class CasUsage():
    def __init__(self, casUsage):
        self.casUsage=casUsage
        self.scenarioUsager=[]
        self.scenarioOrdi=[]
        self.scenarioAutre=[]

        
    