import sqlite3



class DbUtilisateurs:
	def __init__(self):
		self.conn = sqlite3.connect("inscription.bd")
		self.c = self.conn.cursor()
		self.creationInscription()
		self.creationProjet()
		self.creationUserProjet()

	def creationInscription(self):
		self.c.execute(''' CREATE TABLE IF NOT EXISTS utilisateurs(
				id				INTEGER		PRIMARY KEY AUTOINCREMENT,
				identifiant		TEXT		NOT NULL,
				courriel		TEXT		NOT NULL,
				statut_conf		INTEGER		DEFAULT 0,
				mot_de_passe	TEXT		NOT NULL,
				type_acces		INTEGER		DEFAULT 1,
				question_sec	TEXT		NOT NULL,
				reponse_ques 	TEXT		NOT NULL,

				CONSTRAINT uc_user_courriel		UNIQUE(courriel),
				CONSTRAINT uc_user_identifiant	UNIQUE(identifiant)
														) ''') 
	
	def creationProjet(self):
		self.c.execute(''' CREATE TABLE IF NOT EXISTS projet(
				id				INTEGER		PRIMARY KEY AUTOINCREMENT,
				nom				TEXT		NOT NULL,
				id_createur		INTEGER		NOT NULL,
				description 	TEXT,
				nom_organi		TEXT,
				date_creation	TEXT		NOT NULL,

				CONSTRAINT uc_createur_nom UNIQUE(nom,id_createur),
				CONSTRAINT fk_pro_id_createur FOREIGN KEY (id_createur) REFERENCES utilisateurs(id)

														) ''') 
	def creationUserProjet(self):
		self.c.execute(''' CREATE TABLE IF NOT EXISTS user_projet(
				id_user			INTEGER		NOT NULL,
				id_projet		INTEGER		NOT NULL,		

				CONSTRAINT pk_user_projet PRIMARY KEY(id_user,id_projet),
				CONSTRAINT fk_userPro_iduser FOREIGN KEY (id_user) REFERENCES utilisateurs(id),
				CONSTRAINT fk_userPro_idpro FOREIGN KEY (id_projet) REFERENCES projet(id)
														) ''')