# -*- coding: utf-8 -*-

import os,os.path
import sys
from xmlrpc.client import ServerProxy
import socket
from subprocess import Popen 
import math
from gestpro_modele import *
from gestpro_vue import *
from helper import Helper as hlp
from IdMaker import Id

class Controleur():
	def __init__(self):
		print("IN CONTROLEUR")
		self.createurId=Id
		self.modele=None
		self.serveur=None
		self.monip=self.trouverIP()
		self.nodeport="9999"
		self.vue=Vue(self,self.monip)
		self.vue.root.mainloop()
		self.idProjet=None
		self.identifiant=None
		
	def trouverIP(self): # fonction pour trouver le IP en 'pignant' gmail
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # on cree un socket
		s.connect(("gmail.com",80))	   # on envoie le ping
		monip=s.getsockname()[0] # on analyse la reponse qui contient l'IP en position 0 
		s.close() # ferme le socket
		return monip
	
	def inscrireSiDisponibles(self,ipserveur, identifiant, courriel, motDePasse, question, reponse):
		if ipserveur and identifiant and courriel and motDePasse:
			ad="http://"+ipserveur+":"+self.nodeport
			self.serveur=ServerProxy(ad)
			reponseInscription=self.serveur.inscrireSiInfosDisponibles(identifiant, courriel, motDePasse, question, reponse)# on averti le serveur de nous inscrire
			if reponseInscription[0]:# reponseInscription[0] == True/False (succes de l'inscription) et reponseInscription[1] = messageErreur si [0] == False
				print("Inscrit!") #À CHANGER POUR UN LABEL+CREATEWINDOW DANS LA VUE
				self.vue.afficherInscriptionAchevee(identifiant, motDePasse)
			else:
				print(reponseInscription[1])
	
	
	def loginclient(self,ipserveur,identifiant, motDePasse):
		if ipserveur and identifiant and motDePasse:
			ad="http://"+ipserveur+":"+self.nodeport
			self.serveur=ServerProxy(ad)
			self.monnom=identifiant
			rep=self.serveur.loginauserveur(identifiant, motDePasse)	# on averti le serveur de nous inscrire
			print(str(rep))
			#C'est dans le serveur que se passent les vérifications dans la BD
			if rep!=0: # Rep sera 0 si l'utilisateur n'est pas trouvé ou si le pw ne match pas
				self.identifiant=self.serveur.getIdMembre(identifiant) #sauvegarde du côté client le id de utilisateur
				self.vue.chargerSelectProjet(self.selectProjetDuMembre()) #charge fenêtre intermédiaire de sélection/création de projet
			else:
				print("Nous n'avons pas réussi à vous connecter avec ces informations")
				#À CHANGER POUR UN LABEL+CREATEWINDOW DANS LA VUE
				
	
#===============================================================================
#    Description: creer projet si non existant+appel pour ajout du membre table liaison user/projet+retourne fenetre de selection des projets/option de creation
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================				
				
	def creerSiDisponibles(self, nom, description, organisation):
		if nom:# and description and organisation and dateButoir:
			reponseCreation=self.serveur.creerSiInfosDisponibles(nom, self.identifiant, description, organisation)# on averti le serveur de créer le projet
			if reponseCreation[0]:# reponseInscription[0] == True/False (succes de l'inscription) et reponseInscription[1] = messageErreur si [0] == False
				print("Projet Creer") #À CHANGER POUR UN LABEL+CREATEWINDOW DANS LA VUE
				self.vue.frameCreateProject.destroy()
				self.vue.chargerSelectProjet(self.selectProjetDuMembre()) #retourner fenetre d'affichage des projets du membre
			else:
				print(reponseCreation[1])	

#===============================================================================
#    Description: retourne la liste des projets du client à partir de son identifiant conserver localement
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================
					
	def selectProjetDuMembre(self):
		return self.serveur.selectProjetDuMembre(self.identifiant)
		 
#===============================================================================
#    Description: permet de configurer le main pour qu'une fois un projet selectionner on ait son identifiant pour aller chercher les bonnes data dans nos tables de module
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================
		
	def selectionProjet(self,nom):
		if nom:
			self.idProjet=self.serveur.getIdProjet(nom) #set le idProjet du client pour qu'on puisse aller chercher les bonnes infos pour nos modules
			self.vue.chargercentral() #Load le main frame

#===============================================================================

	def requetemodule(self,mod):
		rep=self.serveur.requetemodule(mod)
		if rep:
			print(rep[0])
			cwd=os.getcwd()
			lieuApp="/gp_"+rep[0]
			lieu=cwd+lieuApp
			print(lieu)
			if not os.path.exists(lieu):
				os.mkdir(lieu) #plante s'il exist deja
			reso=rep[1]
			print(rep[1])
			for i in rep[2]:
				if i[0]=="fichier":
					nom=reso+i[1]
					rep=self.serveur.requetefichier(nom)
					fiche=open(lieu+"/"+i[1],"wb")
					fiche.write(rep.data)
					fiche.close()
			chaineappli="."+lieuApp+lieuApp+".py"

			self.pid = Popen([sys.executable, chaineappli,self.monnom,self.monip,self.nodeport],shell=0) 
		else:
			print("RIEN")
			
	def fermerprocessus(self):
		self.pid.kill()
		
	def connecteservice(self,rep):	# initalisation locale de la simulation, creation du modele, generation des assets et suppression du layout de lobby
		if rep[1][0][0]=="connecte":
			#print("REP",rep)
			self.modele=Modele(self,rep[1][0][1],rep[1][0][2]) # on cree le modele
			self.vue.afficherinitpartie(self.modele)

			
	def fermeserveur(self):
		if self.serveur:
			self.serveur.jequitte(self.monnom)
	
	def fermefenetre(self):
		print("Client GestPro quitte")
		self.vue.root.destroy()
		
		
if __name__=="__main__":
	c=Controleur()
	print("End GestPro")
