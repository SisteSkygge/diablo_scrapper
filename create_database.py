#-*- coding:utf-8 -*-
import sqlite3
import os
from CONSTANT import *

def create_database():
    """
        L'utilisation de ce scrypt EFFACE l'ancienne base de donnees et en creer une nouvelle,
        elle efface donc les donnees deja enregistres.
        Il permet aussi d'apporter des modifications a la structure de la base de donnees

        Le choix de sqlite3 est voulu, je souhaite une base de donnees legere et locale
        pour ceux souhaitant utiliser un SGBD de type Mysql, PostGreSQL, ...;
        voici la structure de la base de donnees
    """

    #Detecte si dans le fichier ou s'execute le script se trouve la base de donnees
    if(DB_NAME in os.listdir(".")):
        print("La base de donnees a ete trouve")
        print("Suppression en cours...")
        os.remove(DB_NAME)
        print("Base de donnees supprime")
    else:
        print("La base de donnees n'a pas ete trouve")

    print("Creation d'une nouvelle base de donnees en cours...")

    #On cree la base de donnees
    db = sqlite3.connect(DB_NAME)

    #On execute le code SQL permettant de creer la structure de la table
    db.execute("""
        CREATE TABLE Objet(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(150),
            categorie VARCHAR(25) NOT NULL,
            qualite VARCHAR(100) NOT NULL,
            account_bound INT NOT NULL,
            check (account_bound=1 or account_bound=0));""")

    db.execute("""
        CREATE TABLE Propriete(
            id_prop INTEGER PRIMARY KEY AUTOINCREMENT,
            id_objet INTEGER,
            intitule VARCHAR(250),
            primary_prop INTEGER,
            FOREIGN KEY (id_objet) REFERENCES Objet(id));""")

    db.execute("""
        CREATE TABLE Fabrique(
            id_objet INTEGER,
            fabriquant VARCHAR(50),
            PRIMARY KEY (id_objet, fabriquant),
            FOREIGN KEY (id_objet) REFERENCES Objet(id));""")

    db.commit()
    db.close()

def add_data_to_database(db_var, file_name, categorie_list):
    """ Cette fonction sert a lire les file_name, traite par un programme precedent, de lire les lignes et suivant les elements de la ligne lu decide, si on creer un nouvel item, propriete, fabrique etc..."""

    #Un enregistrement commence
    #Apres la categorie il y a un nombre seul, celui-ci est lie a la ligne qui suit
    with open(file_name, 'r', encoding="utf-8") as saving_file:
        ligne = saving_file.readlines()
    saving_file.close()

    property_list = []
    primary = 1
    phase = 0
    account_bound = 0
    nom = ""
    categorie = ""
    qualite = ""
    fabricant = ""

    quality_possible = ["rares","rare", "legendaire", "legendaires", "ensemle", "ensembles", "d'ensembles", "d'ensemble", "magique", "magiques"]

    for i in range(len(ligne)-1):
        if("Aucun objet a afficher" in ligne[i]):
            #On est a la fin du fichier et le programme POURRA PEUT ETRE crash en faisant un overflow si on ne lui indique pas de s'arreter avant.
            break
        elif("&" in ligne[i]):
            #New section
            #S'il y a des enregistrements alors on les sauvegarde
            if(nom!=""):
                db_var.execute("""INSERT INTO Objet(name, categorie, qualite, account_bound) VALUES(?, ?, ?, ?);""", (nom, categorie, qualite, account_bound))
                #On recupere l'id de l'objet rajouter pour pouvoir l'utiliser en cle etrangere dans les requetes suivantes
                id_max = int(db_var.execute("""SELECT max(id) FROM Objet""").fetchone()[0])
                for element in property_list:
                    ligne_buffer = element.split("\t")
                    db_var.execute("""INSERT INTO Propriete(id_objet, intitule, primary_prop) VALUES(?, ?, ?);""", (id_max, ligne_buffer[0], ligne_buffer[1]))
                if(fabricant!=""):
                    db_var.execute("""INSERT INTO Fabrique(id_objet, fabriquant) VALUES(?, ?);""", (id_max, fabricant))

                #On a fini on reset tout
                primary = 1
                property_list = []
                account_bound = 0
                fabricant = ""
                categorie = ""
            nom = ligne[i].replace("&", "").replace("\n", "")
            #On enleve le repere comme il ne nous ait plus utile
            phase = 1
        elif(phase==1):
            #si la phase==1 alors on est sur la ligne de la categorie
            ligne_buffer = ligne[i].replace("\n", "").replace("d'", "").split(" ")
            if(len(ligne_buffer)==1):
                qualite = "Normal"
                categorie = ligne_buffer[0]
            else:
                qualite = ligne_buffer[len(ligne_buffer)-1]
                for j in range(len(ligne_buffer)-2):
                    categorie += ligne_buffer[j]+" "
                if(qualite not in quality_possible):
                    categorie += qualite
                    qualite = "Normal"
            phase = 2
        else:
            #On recupere la caracteristique principal -> Armure, degats par seconde, ces donnees sont positionnes sur deux lignes
            #Pas besoin de s'occuper du fait que certains items n'en possedent pas car si il n'en possede pas alors cette enregistrement est un nom d'item et la premiere condition du if s'en occupe
            if(ligne[i]=="Armure\n" or ligne[i]=="Primaires\n" or "(Niveau" in ligne[i]):
                pass
            elif(ligne[i]=="Secondaires\n"):
                primary = 0
            elif("Account Bound" in ligne[i]):
                account_bound = 1
            elif("Cree par" in ligne[i]):
                ligne_buffer = ligne[i].split(" ")
                fabricant = str(ligne_buffer[len(ligne_buffer)-1]).replace("\n", "")
                i += 1
                #On increment I pour passer la ligne indiquant le niveau d'artisanat requis pour creer l'item
            elif("Armure" in ligne[i+1] or "Degâts par seconde" in ligne[i+1]):
                #On est dans le cas de la propriete sur 2 lignes
                property_list.append(str(str(ligne[i]).replace("\n", " ")+str(ligne[i+1])+"\t"+str(primary)))
                i += 1
                #On incremente de 1 i pour passer la ligne qu'on a note en avance
            else:
                property_list.append(str(str(ligne[i]).replace("\n", "")+"\t"+str(primary)))

    db_var.commit()


if (__name__ == "__main__"):
    create_database()
