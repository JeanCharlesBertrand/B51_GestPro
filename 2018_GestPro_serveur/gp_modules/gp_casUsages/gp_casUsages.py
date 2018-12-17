# -*- coding: utf-8 -*-

import os,os.path
import sys
import socket
from subprocess import Popen 
import math
from gp_casUsages_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy


class Controleur():
    def __init__(self):
        self.createurId=Id
        self.modele=None
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
        
    def commitCasUsageBD(self, texte):
        self.requete="INSERT INTO cas_usage(description) VALUES ('"+texte+"')"
        rep = self.serveur.entreeGenerique(self.requete)
        self.select="SELECT description FROM cas_usage WHERE id = 1"
        repo = self.serveur.sortieGenerique(self.select)
        print(repo)
        
        
     

    
if __name__ == '__main__':
    c=Controleur()