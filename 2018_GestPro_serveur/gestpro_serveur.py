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
daemon= SimpleXMLRPCServer((monip,9999), allow_none=True)

#class Client(object):
#   def __init__(self,nom):
#       self.nom=nom
        
class ModeleService(object):
    def __init__(self,parent,rdseed):
        self.parent=parent
        self.rdseed=rdseed
        self.modulesdisponibles={   "analyseText":     ["gp_analyseText",0.1],
                                      "casUsages":       ["gp_casUsages",0.1], 
                                            "crc":             ["gp_crc",0.1],
                                   "modelisation":    ["gp_modelisation",0.1],
                                      "maquettes":       ["gp_maquettes",0.1],
                                  "planifGlobale":   ["gp_planifGlobale",0.1]                                                             
                                }
        self.clients={}

    def requeteAnalyse(self):
        mod="analyseText"
        self.parent.requetemodule(mod)  

    def creerclient(self,nom):
        #if nom in self.clients.keys(): # on assure un nom unique
        #   return [0,"Erreur de nom"]
        # tout va bien on cree le client et lui retourne la seed pour le random
        #c=Client(nom)
        #self.clients[nom]=c
        return [1,"Bienvenue",list(self.modulesdisponibles.keys())]
            
class ControleurServeur(object):
    def __init__(self):
        rand=random.randrange(1000)+1000
        self.modele=ModeleService(self,rand)

#===============================================================================
#    Description: appelé une fois le curseur utilisé en transposé dans une variable intermédiaire pour réutilisation du curseur
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/07 - 18h30
#===============================================================================
    
    def resetCurseur(self):
        dbUtilisateurs.c=dbUtilisateurs.conn.cursor()   
        
    def getDicoModules(self):
        return self.modele.modulesdisponibles
        
    def loginauserveur(self,nom, motDePasse):
        #SELECT du mot de passe relié à l'identifiant dans la BD, casté dans un object de type cursor
        curseurMdP = dbUtilisateurs.c.execute('SELECT mot_de_passe FROM utilisateurs WHERE identifiant = \'%s\';' % nom)
        #.fetchone() s'applique pour 1 résultat, et comme ici Id:pw est 1:1, ça va tjrs marcher
        motDePasseCorrespondant = curseurMdP.fetchone()
        self.resetCurseur()
        if not motDePasseCorrespondant: #Si l'utilisateur n'est pas dans la bd il n'y aura
            return 0             #pas de mot de passe correspondant, donc le login de marchera pas

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
        messageErreur = None
        try:
            dbUtilisateurs.c.execute('INSERT INTO utilisateurs(identifiant, courriel, mot_de_passe, question_sec, reponse_ques) VALUES (\'%s\', \'%s\', \'%s\', \'%s\',\'%s\');' % ( identifiant, courriel, mot_de_passe,question,reponse ) )
            dbUtilisateurs.conn.commit()
        except Exception as e:
            if str(e) == "UNIQUE constraint failed: utilisateurs.identifiant":
                messageErreur = 1
                disponibles = False
            elif str(e) == "UNIQUE constraint failed: utilisateurs.courriel":
                messageErreur = 2
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
            rep2=self.ajouterMembre(identifiant, nom)
        
        return ([disponibles, messageErreur])

#( [nom], (identifiant,), [description], [organisation], [time1], [time2] ) )
#===============================================================================
#    Description: retourne le id du membre en fonction de son identifiant 2)son identifiant
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/05 - 9h00
#===============================================================================
    
    def getIdMembre(self,identifiant):
        curseurID = dbUtilisateurs.c.execute('SELECT id FROM utilisateurs WHERE identifiant = ?', [identifiant])
        idT = curseurID.fetchone()
        self.resetCurseur()
        id=int(idT[0])
        return id
        
    def getIdentifiantMembre(self,id):
        curseurIDM = dbUtilisateurs.c.execute('SELECT identifiant FROM utilisateurs WHERE id = ?', (id,))
        identifiant = curseurIDP.fetchone()
        self.resetCurseur()
        return identifiant
    
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


    def requeteGenerique(self,requete):
        curseurListe = dbUtilisateurs.c.execute(requete)
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste
        
#===============================================================================
#    Description: fonction entree recoit string requete sql pour entree des éléments dans la bd et fonction sortie recoit string requete sql pour sortir des éléments de la bd
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/12/12 - 9h40
#===============================================================================
    
    def entreeGenerique1(self,requete):
        try:
            dbUtilisateurs.c.execute(requete)
            dbUtilisateurs.conn.commit()
        except Exception as e:
            self.trace = str(e)
        self.resetCurseur()
        return self.trace

    def sortieGenerique(self,requete):
        try:
            curseurListe = dbUtilisateurs.c.execute(requete)
        except Exception as e:
            print(str(e))
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste
        
#===============================================================================
#    Description: retourne la liste de tout les usagers inscrits 
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/28 - 19h00
#===============================================================================
    
    def getListeUsagers(self):
        curseurListe = dbUtilisateurs.c.execute('SELECT identifiant FROM utilisateurs WHERE id IN (SELECT id FROM utilisateurs)')
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste
    
#===============================================================================
#    Description: 1)retourne le nom du projet selon id 2)la description 3)la liste de membres
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/28 - 10h20
#===============================================================================
    
    def getNomProjet(self, idProjet):
        curseurIDP = dbUtilisateurs.c.execute('SELECT nom FROM projet WHERE id = ?', (idProjet,))
        nomP = curseurIDP.fetchone()
        self.resetCurseur()
        return nomP
    
    def getDescriptionProjet(self,idProjet):
        curseurIDP = dbUtilisateurs.c.execute('SELECT description FROM projet WHERE id = ?', (idProjet,))
        description = curseurIDP.fetchone()
        self.resetCurseur()
        return description
    
    def getListeMembres(self,id):
        curseurListe = dbUtilisateurs.c.execute('SELECT identifiant FROM utilisateurs WHERE id IN (SELECT id_user FROM user_projet WHERE id_projet=?)', (id,))
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
        if type(nom) is str:
            idProjet=self.getIdProjet(nom)
        else:
            idProjet=nom
        try:
            dbUtilisateurs.c.execute('INSERT INTO user_projet(id_user, id_projet) VALUES (?, ?)', (identifiant, idProjet) )
            dbUtilisateurs.conn.commit()
        except Exception as e:
            if str(e) == "UNIQUE constraint failed: user_projet.id_user , user_projet.id_projet":
                messageErreur = "Déjà membre du projet"

            else:
                print(str(e))
                disponibles = False
                messageErreur = str(e)
                print('%r' % e)
        
        self.resetCurseur()
        return messageErreur
                
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
#     Description: insert d'une nouvelle table a partir de Modelisation vers la BD
#     Creator: Vincent Trudel et Yasmine Kaddouri
#     Last modified: 2018/12/10 - 10h00
#===============================================================================
    


    def getTablesMod(self, id):
        curseurListe = dbUtilisateurs.c.execute('SELECT nom_table FROM modelisation WHERE id_projet = ?', (id,))
        liste = curseurListe.fetchall()
        self.resetCurseur()
        print(str(liste))
        return liste
    
    def loadTable(self, nomTable, idProjet):
        print(nomTable+", "+str(idProjet))
        curseurListe = dbUtilisateurs.c.execute('SELECT texte_table FROM modelisation WHERE id_projet = ? AND nom_table = ?', (str(idProjet),nomTable))
        texte_table = curseurListe.fetchall()[0]
        self.resetCurseur()
        return texte_table
        
    def entreeGenerique(self,requete, params):
        self.trace = "ok"
        try:
            dbUtilisateurs.c.execute(requete, params)
            dbUtilisateurs.conn.commit()
        except Exception as e:
            self.trace = str(e)
        self.resetCurseur()
        return self.trace

    def sortieGenerique(self,requete):
        self.trace = "Good!"
        try:
            curseurListe = dbUtilisateurs.c.execute(requete)
        except Exception as e:
            print(str(e))
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste
        
#===============================================================================
#    Description: server insertion et select pour chat
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/11/28 - 21h30
#===============================================================================

    def insertIntoChat(self,identifiant, idProjet, message, time):
        if(message is not ""):
            dbUtilisateurs.c.execute('INSERT INTO chat(identifiant, id_projet, message, time) VALUES (?, ?, ?, ?)', (identifiant, idProjet,message,time) )
            dbUtilisateurs.conn.commit()
        self.resetCurseur()
        
    def getContentChat(self, id):
        curseurListe = dbUtilisateurs.c.execute('SELECT * FROM chat WHERE id_projet = ?', (id,))
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste
        
#===============================================================================
#    Description: server insertion et select pour analyse
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/12/03 - 11h00
#===============================================================================

    def insertIntoAnalyse(self, list, idProjet):
            dbUtilisateurs.c.execute('UPDATE analyse SET fichierMandat = ?, fichNomExp = ?, fichVerbeExp = ?, fichAdjExp = ?, fichNomImp = ?, fichVerbeImp = ?, fichAdjImp = ?, fichNomSupp = ?, fichVerbeSupp = ?, fichAdjSupp = ? WHERE id_projet = ?', (list[0],list[1],list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], idProjet,))
            self.resetCurseur()
            dbUtilisateurs.conn.commit()
            ok = dbUtilisateurs.c.execute('SELECT * FROM analyse WHERE id_projet = ?', (idProjet,))
            rows = ok.fetchone()
            self.resetCurseur()
            if rows is None:
                dbUtilisateurs.c.execute('INSERT INTO analyse(id_projet, fichierMandat, fichNomExp, fichVerbeExp, fichAdjExp, fichNomImp, fichVerbeImp, fichAdjImp, fichNomSupp, fichVerbeSupp, fichAdjSupp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (idProjet, list[0],list[1],list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9]) )
                dbUtilisateurs.conn.commit()
                self.resetCurseur()
            
        
    def selectFromAnalyse(self, id):
        curseurListe = dbUtilisateurs.c.execute('SELECT * FROM analyse WHERE id_projet = ?', (id,))
        liste = curseurListe.fetchone()
        self.resetCurseur()
        return liste

#===============================================================================
#    Description: server insertion et select pour planif
#    Creator: Guillaume Geoffroy
#    Last modified: 2018/12/19 - 10h30
#===============================================================================

    def insertIntoPlanif(self, idProjet, list):
        dbUtilisateurs.c.execute('DELETE FROM planif WHERE id_projet = ?', (idProjet,))
        dbUtilisateurs.conn.commit()
        self.resetCurseur()
        c=0
        for i in list:
            dbUtilisateurs.c.execute('INSERT INTO planif (id_projet, nom) VALUES (?, ?)', (idProjet, list[c]))
            dbUtilisateurs.conn.commit()
            self.resetCurseur()  
            c+=1  

    def selectFromPlanif(self, id):
        curseurListe = dbUtilisateurs.c.execute('SELECT nom FROM planif WHERE id_projet = ?', (id,))
        liste = curseurListe.fetchall()
        self.resetCurseur()
        return liste 

#===============================================================================
#    Description: server insertion et select pour CRC -Lynda - 2018/12/13
#
#===============================================================================

    def insertIntoCRC(self,idProjet,idFiche,classe,proprietaire,collaboration,responsabilites,parametres):
        try:
            test = dbUtilisateurs.c.execute('SELECT * FROM crc WHERE id_projet = ? AND id_fiche = ? AND classe = ?', (idProjet,idFiche,classe))
            crcrows = test.fetchone()
            self.resetCurseur()

            if crcrows is None:
                print("Fiche "+classe+" ajoutée")
                dbUtilisateurs.c.execute('INSERT INTO crc(id_projet,id_fiche,classe,proprietaire,collaboration,responsabilites,parametres) VALUES (?, ?, ?, ?, ?, ?, ?)',(idProjet,idFiche,classe,proprietaire,collaboration,responsabilites,parametres,))
                dbUtilisateurs.conn.commit()
                self.resetCurseur()
            else:
                print("Fiche "+classe+" modifiée")
                dbUtilisateurs.c.execute('UPDATE crc SET  classe = ?, proprietaire = ?, collaboration = ?, responsabilites = ?, parametres = ? WHERE id_projet = ? AND id_fiche = ? ', (classe,proprietaire,collaboration,responsabilites,parametres,idProjet,idFiche))
                self.resetCurseur()
                dbUtilisateurs.conn.commit()
                
        except Exception as e:
                print(str(e))
        
    def selectFromCRC(self, idProjet):
        try:
            curseurListe = dbUtilisateurs.c.execute('SELECT * FROM crc WHERE id_projet = ?', (idProjet,))
            liste = curseurListe.fetchall()
            self.resetCurseur()
            return liste
        except Exception as e:
            print(str(e))
            
    def deleteFromCRC(self,idProjet,idFiche,classe,proprietaire,collaboration,responsabilites,parametres):
        try:
            test = dbUtilisateurs.c.execute('DELETE FROM crc WHERE id_projet = ? AND id_fiche = ? AND classe = ?', (idProjet,idFiche,classe))
            crcrows = test.fetchone()
            self.resetCurseur()
            dbUtilisateurs.conn.commit()

        except Exception as e:
                print(str(e))

#===============================================================================

    def requetemodule(self,mod):
        if mod in self.modele.modulesdisponibles.keys():
            cwd=os.getcwd()
            if os.path.exists(cwd+"/gp_modules/"):
                lieuApp="/gp_"+mod
                dirmod=cwd+"/gp_modules/"+lieuApp+"/"
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
