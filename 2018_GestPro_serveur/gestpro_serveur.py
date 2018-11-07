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
	
	def resetCurseur(self):
		dbUtilisateurs.c=dbUtilisateurs.conn.cursor()	
		
	def loginauserveur(self,nom, motDePasse):
		#SELECT du mot de passe relié à l'identifiant dans la BD, casté dans un object de type cursor
		curseurMdP = dbUtilisateurs.c.execute('SELECT mot_de_passe FROM utilisateurs WHERE identifiant = \'%s\';' % nom)
		#.fetchone() s'applique pour 1 résultat, et comme ici Id:pw est 1:1, ça va tjrs marcher
		motDePasseCorrespondant = curseurMdP.fetchone()
		self.resetCurseur()
		if not motDePasseCorrespondant: #Si l'utilisateur n'est pas dans la bd il n'y aura
			return 0			 #pas de mot de passe correspondant, donc le login de marchera pas

		print("mot de passe: "+list(motDePasseCorrespondant)[0]) #Pour espionner les mots de passe ;)
		'''.fetchone() retourne un tuple avec une valeur Ex: ('aaaa',)
		donc on y accède par [0]
		'''
		if motDePasseCorrespondant[0] == motDePasse:
			return self.modele.creerclient(nom)
		else:
			return 0
		
	def inscrireSiInfosDisponibles(self, identifiant, courriel, mot_de_passe,question,reponse):
		disponibles = True
		messageErreur = ""
		try:
			dbUtilisateurs.c.execute('INSERT INTO utilisateurs(identifiant, courriel, mot_de_passe, question_sec, reponse_ques) VALUES (\'%s\', \'%s\', \'%s\', \'%s\',\'%s\');' % ( identifiant, courriel, mot_de_passe,question,reponse ) )
			dbUtilisateurs.conn.commit()
		except Exception as e:
			if str(e) == "UNIQUE constraint failed: utilisateurs.identifiant":
				messageErreur = "Cet identifiant existe déjà, veuillez en choisir un autre svp"
				disponibles = False
			elif str(e) == "UNIQUE constraint failed: utilisateurs.courriel":
				messageErreur = "Ce courriel a déjà été utilisé, veuillez en choisir un autre svp"
				disponibles = False
			else:
				print(str(e))
				disponibles = False
				messageErreur = str(e)
				print('%r' % e)
		#Ajouter la date id'nscription?
		self.resetCurseur()
		return ([disponibles, messageErreur])

#===============================================================================
#    Description: insert le tuble et appel la fonction d'ajout à la liste de liaison l'association membre-projet
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================

	def creerSiInfosDisponibles(self, nom, identifiant, description, organisation):
		disponibles = True
		messageErreur = ""
		time1 = time.strftime('%Y-%m-%d', time.localtime())
		#curseurIdC = dbUtilisateurs.c.execute('SELECT id FROM utilisateurs WHERE identifiant = ?', nom)
		#createurId = curseurIdC.fetchone()
		try:
			dbUtilisateurs.c.execute('INSERT INTO projet(nom, id_createur, description, nom_organi, date_creation) VALUES (?, ?, ?, ?, ?)', ( nom, identifiant, description, organisation, time1 ) )
			dbUtilisateurs.conn.commit()
		except Exception as e:
			if str(e) == "UNIQUE constraint failed: projet.nom, projet.createurId":
				messageErreur = "Vous avez déjà créer un projet de même nom"
				disponibles = False
			else:
				print(str(e))
				disponibles = False
				messageErreur = str(e)
				print('%r' % e)
		
		self.resetCurseur()
		if disponibles:
			self.ajouterMembre(identifiant, nom)
		
		return ([disponibles, messageErreur])

#( [nom], (identifiant,), [description], [organisation], [time1], [time2] ) )
#===============================================================================
#    Description: retourne le id du membre en fonction de son identifiant
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/05 - 9h00
#===============================================================================
	
	def getIdMembre(self,identifiant):
		curseurID = dbUtilisateurs.c.execute('SELECT id FROM utilisateurs WHERE identifiant = ?', [identifiant])
		idT = curseurID.fetchone()
		self.resetCurseur()
		id=int(idT[0])
		return id
	
#===============================================================================
#    Description: retourne la liste des noms de projets dont fait partie le membre
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================
	
	def selectProjetDuMembre(self,identifiant):
		curseurListe = dbUtilisateurs.c.execute('SELECT nom FROM projet WHERE id IN (SELECT id_projet FROM user_projet WHERE id_user=?)', (identifiant,))
		liste = curseurListe.fetchall()
		self.resetCurseur()
		return liste
	
#===============================================================================
#    Description: insert le tuple d'association membre-projet dans la table de liaison
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================
	
	def ajouterMembre(self,identifiant,nom):
		disponibles = True
		messageErreur = ""
		idProjet=self.getIdProjet(nom)
		try:
			dbUtilisateurs.c.execute('INSERT INTO user_projet(id_user, id_projet) VALUES (?, ?)', (identifiant, idProjet) )
			dbUtilisateurs.conn.commit()
		except Exception as e:
			if str(e) == "UNIQUE constraint failed: user_projet.id_user	, user_projet.id_projet":
				messageErreur = "Déjà membre du projet"

			else:
				print(str(e))
				disponibles = False
				messageErreur = str(e)
				print('%r' % e)
				
		self.resetCurseur()

#===============================================================================
#    Description: retourne l'id d'un projet dont on connait le nom (à ce stade pour la sélection du projet dans lequel le client veut travailler)
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/04 - 12h30
#===============================================================================

	def getIdProjet(self,nom):
		curseurIdProjet = dbUtilisateurs.c.execute('SELECT id FROM projet WHERE nom = ?',[nom])
		idT=curseurIdProjet.fetchone()
		self.resetCurseur()
		id=int(idT[0])
		return id

#===============================================================================

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
