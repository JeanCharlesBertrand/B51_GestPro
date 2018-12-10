# -*- coding: utf-8 -*-

import os,os.path
import sys
#import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from gp_crc_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy


class Controleur():
    def __init__(self):
        print("IN CONTROLEUR",sys.argv)
        self.createurId=Id
        self.modele=None
        #self.vue=Vue(self)
        #self.vue.root.mainloop()
        self.idProjet=int(sys.argv[4])
        self.ipserveur=sys.argv[2]
        self.nodeport=sys.argv[3]
        self.serveur=None
        self.lierServeur()
        self.vue=Vue(self)
        self.vue.root.mainloop()

    def lierServeur(self):
        ad="http://"+self.ipserveur+":"+self.nodeport
        self.serveur=ServerProxy(ad)

    def getNomProjet(self):
        self.nomProjet = self.serveur.getNomProjet(self.idProjet)
        return self.nomProjet
    
    def insertIntoCRC(self,idFiche,classe,proprietaire,collaboration,responsabilites,parametres):
        print("enregistrer Fiche")
        #print(idFiche,classe,proprietaire,collaboration,responsabilites,parametres)
        self.serveur.insertIntoCRC(self.idProjet,idFiche,classe,proprietaire,collaboration,responsabilites,parametres)
        
    def selectFromCRC(self):
        print("lire dans BD")
        #return self.serveur.selectFromCRC(self,self.NomProjet())

    def getFiche(self, idProjet,NomFiche):
        print("lire dans BD par Fiche")
        #return self.serveur.getFiche(self.NomProjet,self.NomFiche)
    
"""
    def modifierFiche(self, idProjet,NomFiche):
        print("ecrire dans BD par Fiche")
        return self.serveur.modifierFiche(self.NomProjet,self.NomFiche)
"""

     
if __name__ == '__main__':
    c=Controleur()
