------------------------------------------------------------
--        Script Postgre 
------------------------------------------------------------

------------------------------------------------------------
-- Table: Potin
------------------------------------------------------------
CREATE TABLE public.Potin(
	ID_Potin       INT  NOT NULL ,
	Titre          VARCHAR (10000) NOT NULL ,
	Nombre_likes   INT  NOT NULL ,
	Pseudo         VARCHAR (30) NOT NULL  ,
	Anonyme 	   BOOLEAN NOT NULL ,
	CONSTRAINT Potin_PK PRIMARY KEY (ID_Potin)
)WITHOUT OIDS;



