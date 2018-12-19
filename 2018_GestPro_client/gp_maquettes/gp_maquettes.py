# -*- coding: utf-8 -*-

import os,os.path
import sys
#import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from gp_maquettes_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy

class Mod_maquette():
    def __init__(self, nomMaquette):
        self.id = None
        self.nom = nomMaquette
        self.formes = []
        
    def ajouteForme(self, forme, couleur, largeur, coordonnee):
        forme = Forme(forme, couleur, largeur, coordonnee)
        self.formes.append(forme)
        
        
class Forme():
    def __init__(self, forme, couleur, largeur, coordonnee):
        self.typeForme = forme
        self.coordonnees = coordonnee
        self.couleur = couleur
        self.largeur = largeur
        

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR",sys.argv)
        self.createurId=Id
        self.modele=None
        self.idProjet=int(sys.argv[4])
        self.ipserveur=sys.argv[2]
        self.nodeport=sys.argv[3]
        self.serveur=None
        self.lierServeur()
        self.vue=Vue(self)
        self.vue.root.mainloop()
        
    def ajouteForme(self, forme, couleur, largeur, coordonnee):
        print("In controleur:", forme, couleur, largeur, coordonnee)
        self.modele.ajouteForme(forme, couleur, largeur, coordonnee)


    def lierServeur(self):
        ad="http://"+self.ipserveur+":"+self.nodeport
        self.serveur=ServerProxy(ad)
        
    def creerMaquette(self, nomMaquette):
        self.modele = Mod_maquette(nomMaquette)



if __name__ == '__main__':
    c=Controleur()