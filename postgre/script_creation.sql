------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------



------------------------------------------------------------
-- Table: Utilisateur
------------------------------------------------------------
CREATE TABLE public.Utilisateur(
	Pseudo   VARCHAR (30) NOT NULL ,
	mdp      VARCHAR (30) NOT NULL  ,
	CONSTRAINT Utilisateur_PK PRIMARY KEY (Pseudo)
)WITHOUT OIDS;


------------------------------------------------------------
-- Table: Potin
------------------------------------------------------------
CREATE TABLE public.Potin(
	ID_Potin       INT  NOT NULL ,
	Titre          VARCHAR (10000) NOT NULL ,
	Nombre_likes   INT  NOT NULL ,
	has_liked      BOOL  NOT NULL ,
	Pseudo         VARCHAR (30) NOT NULL  ,
	CONSTRAINT Potin_PK PRIMARY KEY (ID_Potin)

	,CONSTRAINT Potin_Utilisateur_FK FOREIGN KEY (Pseudo) REFERENCES public.Utilisateur(Pseudo)
)WITHOUT OIDS;



