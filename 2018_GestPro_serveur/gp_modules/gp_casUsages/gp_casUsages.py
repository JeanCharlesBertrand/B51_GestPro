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
        self.vue.root.mainloop()

    def lierServeur(self):
        ad="http://"+self.ipserveur+":"+self.nodeport
        self.serveur=ServerProxy(ad)
        
    def creerCas(self, cas):
        rep=self.modele.creerCas(cas)
        self.vue.inscrireCasUsageEntryDansListe(rep)
        
        
        
    def getNomProjet(self):
        self.nomProjet = self.serveur.getNomProjet(self.idProjet)
        return self.nomProjet

    
if __name__ == '__main__':
    c=Controleur()