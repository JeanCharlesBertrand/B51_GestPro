# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
import math
from gp_casUsages_vue import *
from gp_casUsages_modele import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy


class Controleur():
    def __init__(self):
        self.createurId=Id
        self.modele=Modele(self, int(sys.argv[4]))
        self.idProjet=int(sys.argv[4])
        self.ipserveur=sys.argv[2]
        self.nodeport=sys.argv[3]
        self.serveur=None
        self.lierServeur()
        self.vue=Vue(self)
        self.uploadBD(self.idProjet)
        self.vue.root.mainloop()

    def lierServeur(self):
        ad="http://"+self.ipserveur+":"+self.nodeport
        self.serveur=ServerProxy(ad)
        
    def creerCas(self, cas):
        requete="INSERT INTO cas_usage (id_projet, description) VALUES('"+str(self.idProjet)+"', '"+cas+"');"
        self.serveur.entreeGenerique(requete)
        nbCas=self.serveur.entreeGenerique("SELECT COUNT(*) FROM cas_usage WHERE id_projet = '"+str(self.idProjet)+"';")
        rep=self.modele.creerCas(nbCas, cas)
        self.vue.inscrireCasUsageEntryDansListe(rep)
        
    def chercherCas(self, cas):
        rep=self.modele.getCas(cas)
        return rep
    
    def inscrireLigne(self, resp, texte, cas):
        self.modele.inscrireLigne(resp,texte,cas)
        
    def commitLigne(self, resp, texte, cas):
        rep=self.modele.getCas(cas)
        requete="INSERT INTO ligne_cas (id_cas, type, description)  VALUES('"+str(rep.idBD)+"', '"+str(resp)+"', '"+str(texte)+"');"
        self.serveur.entreeGenerique(requete)
        print(self.serveur.entreeGenerique("SELECT * FROM ligne_cas WHERE id_cas = '"+str(rep.idBD)+"';"))
        
        
    def sauveCasUsageModele(self,texteCas, listeScenario):
        print("ini sauve")
        
    def getNomProjet(self):
        self.nomProjet = self.serveur.getNomProjet(self.idProjet)
        return self.nomProjet[0]
    
    def uploadBD(self, idProjet):
        requete="SELECT * FROM cas_usage WHERE id_projet = '"+str(idProjet)+"';"
        rep=self.serveur.entreeGenerique(requete)
        nbCas=self.serveur.entreeGenerique("SELECT COUNT(*) FROM cas_usage WHERE id_projet = '"+str(self.idProjet)+"';")
        
        for i in range(nbCas[0][0]):
            cas=self.modele.creerCas(rep[i][0], rep[i][2])
            self.vue.inscrireCasUsageEntryDansListe(cas)
            nbLignes=self.serveur.entreeGenerique("SELECT COUNT(*) FROM ligne_cas WHERE id_cas = '"+str(rep[i][0])+"';")
            lignes=self.serveur.entreeGenerique("SELECT * FROM ligne_cas WHERE id_cas = '"+str(rep[i][0])+"';")
            print(lignes)
            
            for j in range(nbLignes[0][0]):
                casTexte=self.serveur.entreeGenerique("SELECT description FROM cas_usage WHERE id = '"+str(lignes[j][1])+"';")
                print(casTexte)
                self.modele.inscrireLigne(lignes[j][2], lignes[j][3], casTexte[0][0])
            

    
if __name__ == '__main__':
    c=Controleur()