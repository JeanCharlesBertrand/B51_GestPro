# -*- encoding: utf-8 -*-

#import Pyro4
from xmlrpc.server import SimpleXMLRPCServer

import xmlrpc.client

import os,os.path
from threading import Timer
import sys
import socket
import time
import random
from DBUtilisateurs import * #inclut sqlite3 et la classe dbUtilisateurs
dbUtilisateurs = DbUtilisateurs()





# Pour statut_confirmation, 0 = pas confirmé, 1 confirmé
# Pour type_acces, 0 = viewer, 1 = full
# Mettre dans une fonction éventuellement


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
monip=s.getsockname()[0]
print("MON IP SERVEUR",monip)
s.close()

#daemon = Pyro4.core.Daemon(host=monip,port=9999) 
daemon= SimpleXMLRPCServer((monip,9999))

#class Client(object):
#	def __init__(self,nom):
#		self.nom=nom
		
class ModeleService(object):
	def __init__(self,parent,rdseed):
		self.parent=parent
		self.rdseed=rdseed
		self.modulesdisponibles={"projet":"gp_projet",
								 "sql":"gp_sql",
								 "login":"gp_login"}
		self.clients={}

	def creerclient(self,nom):
		#if nom in self.clients.keys(): # on assure un nom unique
		#	return [0,"Erreur de nom"]
		# tout va bien on cree le client et lui retourne la seed pour le random
		#c=Client(nom)
		#self.clients[nom]=c
		return [1,"Bienvenue",list(self.modulesdisponibles.keys())]
			
class ControleurServeur(object):
	def __init__(self):
		rand=random.randrange(1000)+1000
		self.modele=ModeleService(self,rand)
		
	def loginauserveur(self,nom, motDePasse):
		#SELECT du mot de passe relié à l'identifiant dans la BD, casté dans un object de type cursor
		curseurMdP = dbUtilisateurs.c.execute('SELECT mot_de_passe FROM utilisateurs WHERE identifiant = \'%s\';' % nom)
		#.fetchone() s'applique pour 1 résultat, et comme ici Id:pw est 1:1, ça va tjrs marcher
		motDePasseCorrespondant = curseurMdP.fetchone()
		if not motDePasseCorrespondant: #Si l'utilisateur n'est pas dans la bd il n'y aura
			return 0			 #pas de mot de passe correspondant, donc le login de marchera pas

		#print(list(motDePasseCorrespondant)[0]) #Pour espionner les mots de passe ;)
		'''.fetchone() retourne un tuple avec une valeur Ex: ('aaaa',)
		donc on y accède par [0]
		'''
		if motDePasseCorrespondant[0] == motDePasse:
			return self.modele.creerclient(nom)
		else:
			return 0
		
	def inscrireSiInfosDisponibles(self, identifiant, courriel, mot_de_passe):
		disponibles = True
		messageErreur = ""
		try:
			dbUtilisateurs.c.execute('INSERT INTO utilisateurs(identifiant, courriel, mot_de_passe) VALUES (\'%s\', \'%s\', \'%s\');' % ( identifiant, courriel, mot_de_passe ) )
			dbUtilisateurs.conn.commit()
		except Exception as e:
			if str(e) == "UNIQUE constraint failed: utilisateurs.identifiant":
				messageErreur = "Cet identifiant existe déjà, veuillez en choisir un autre svp"
				disponibles = False
			if str(e) == "UNIQUE constraint failed: utilisateurs.courriel":
				messageErreur = "Ce courriel a déjà été utilisé, veuillez en choisir un autre svp"
				disponibles = False
			if messageErreur == "":
				print(str(e))
				print('%r' % e)
		#Ajouter la date id'nscription?
		return ([disponibles, messageErreur])

	def requetemodule(self,mod):
		if mod in self.modele.modulesdisponibles.keys():
			cwd=os.getcwd()
			if os.path.exists(cwd+"/gp_modules/"):
				dirmod=cwd+"/gp_modules/"+self.modele.modulesdisponibles[mod]+"/"
				if os.path.exists(dirmod):
					listefichiers=[]
					for i in os.listdir(dirmod):
						if os.path.isfile(dirmod+i):
							val=["fichier",i]
						else:
							val=["dossier",i]
							
						listefichiers.append(val)
					return [mod,dirmod,listefichiers]
			
			
			
	def requetefichier(self,lieu):
		fiche=open(lieu,"rb")
		contenub=fiche.read()
		fiche.close()
		return xmlrpc.client.Binary(contenub)
			
		
	def quitter(self):
		t=Timer(1,self.fermer)
		t.start()
		return "ferme"
	
	def jequitte(self,nom):
		del self.modele.clients[nom]
		del self.modele.cadreDelta[nom]
		if not self.modele.clients:
			self.quitter()
		return 1
	
	def fermer(self):
		print("FERMETURE DU SERVEUR")
		daemon.shutdown()

controleurServeur=ControleurServeur()
daemon.register_instance(controleurServeur)	 
 
print("Serveur XML-RPC actif")
daemon.serve_forever()