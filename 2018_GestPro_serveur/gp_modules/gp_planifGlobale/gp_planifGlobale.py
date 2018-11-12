# -*- coding: utf-8 -*-

import os,os.path
import sys
#import Pyro4
import socket
from subprocess import Popen 
import math
#from sm_projet_modele import *
from gp_implementation_vue import *
from helper import Helper as hlp
from IdMaker import Id
from xmlrpc.client import ServerProxy

class Controleur():
    def __init__(self):
        print("IN CONTROLEUR",sys.argv)
        self.createurId=Id
        self.modele=None
        self.vue=Vue(self)
        self.vue.root.mainloop()
        self.idProjet=int(sys.argv[4])
        self.ipserveur=sys.argv[2]
        self.nodeport=sys.argv[3]
        self.serveur=None
        self.lierServeur()

    def lierServeur(self):
        ad="http://"+self.ipserveur+":"+self.nodeport
        self.serveur=ServerProxy(ad) 
        
if __name__ == '__main__':
    c=Controleur()