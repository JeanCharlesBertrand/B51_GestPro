import sqlite3

'''On pourrait faire une classe plus générique et passer le path de
la DB en paramètre au constructeur, ça pourrait être pratique si on fait plusieurs BD,
ce qui serait pratique à mon avis, pour pas que ça overload si
y'en a une seule, mais c'est débattable
'''

class DbUtilisateurs:
	def __init__(self):
		self.conn = sqlite3.connect("inscription.bd")
		self.c = self.conn.cursor()
		self.c.execute(''' CREATE TABLE IF NOT EXISTS utilisateurs(
				id				INTEGER		PRIMARY KEY AUTOINCREMENT,
				identifiant		TEXT		NOT NULL,
				courriel		TEXT		NOT NULL,
				statut_conf		INTEGER		DEFAULT 0,
				mot_de_passe	TEXT		NOT NULL,
				type_acces		INTEGER		DEFAULT 1,

				CONSTRAINT uc_courriel		UNIQUE(courriel),
				CONSTRAINT uc_identifiant	UNIQUE(identifiant)
														) ''') #Mettre dans une fonction? (C'est JM qui m'a dit ça)

		
