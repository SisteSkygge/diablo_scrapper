import sqlite3
import os
from CONSTANT import *

def create_database():
    """
        L'utilisation de ce scrypt EFFACE l'ancienne base de données et en créer une nouvelle,
        elle efface donc les données déjà enregistrés.
        Il permet aussi d'apporter des modifications à la structure de la base de données

        Le choix de sqlite3 est voulu, je souhaite une base de données légère et locale
        pour ceux souhaitant utiliser un SGBD de type Mysql, PostGreSQL, ...;
        voici la structure de la base de données
    """

    #Détecte si dans le fichier ou s'éxécute le script se trouve la base de données
    if(DB_NAME in os.listdir(".")):
        print("La base de données a été trouvé")
        print("Suppression en cours...")
        os.remove(DB_NAME)
        print("Base de données supprimé")
    else:
        print("La base de données n'a pas été trouvé")

    print("Création d'une nouvelle base de données en cours...")

    #On créer la base de données
    db = sqlite3.connect(DB_NAME)

    #On execute le code SQL permettant de créer la structure de la table
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

def add_data_to_database(DB_NAME, file_name):
    """ Cette fonction sert à lire les file_name, traité par un programme précédent, de lire les lignes et suivant les elements de la ligne lu décidé, si on créer un nouvel item, propriete, fabrique etc..."""

    #Un enregistrement commence
    #Après la catégorie il y a un nombre seul, celui-ci est lié à la ligne qui suit
    with open(file_name, 'r', encoding="utf-8") as saving_file:
        ligne = saving_file.readlines()
    saving_file.close()

    db = sqlite3.connect(DB_NAME)
    property_list = []
    primary = 1
    phase = 0
    account_bound = 0
    nom = ""
    categorie = ""
    qualite = ""
    fabricant = ""

    for i in range(len(ligne)-1):
        if("Aucun objet à afficher" in ligne[i]):
            #On est à la fin du fichier et le programme POURRA PEUT ETRE crash en faisant un overflow si on ne lui indique pas de s'arrêter avant.
            break
        elif("&" in ligne[i]):
            #New section
            #S'il y a des enregistrements alors on les sauvegarde
            if(nom!=""):
                db.execute("""INSERT INTO Objet(name, categorie, qualite, account_bound) VALUES(?, ?, ?, ?);""", (nom, categorie, qualite, account_bound))
                #On recupere l'id de l'objet rajouter pour pouvoir l'utiliser en clé étrangère dans les requètes suivantes
                id_max = int(db.execute("""SELECT max(id) FROM Objet""").fetchone()[0])
                for element in property_list:
                    ligne_buffer = element.split("\t")
                    db.execute("""INSERT INTO Propriete(id_objet, intitule, primary_prop) VALUES(?, ?, ?);""", (id_max, ligne_buffer[0], ligne_buffer[1]))
                if(fabricant!=""):
                    db.execute("""INSERT INTO Fabrique(id_objet, fabriquant) VALUES(?, ?);""", (id_max, fabricant))

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
            ligne_buffer = ligne[i].split(" ")
            if(len(ligne_buffer)==1):
                qualite = "Normal"
                categorie = ligne_buffer[0].replace("\n", "")
            else:
                #On fait un replace "d'" dans le cas ou la qualite de l'item est "d'ensemble" car le split se fait au niveau des espaces
                qualite = ligne_buffer[len(ligne_buffer)-1].replace("d'", "").replace("\n", "")
                for j in range(len(ligne_buffer)-2):
                    if(j!=len(ligne_buffer)-2):
                        categorie += ligne_buffer[j]+" "
                    else:
                        categorie += ligne_buffer[j]
            phase = 2
        else:
            #On recupere la caracteristique principal -> Armure, dégâts par seconde, ces données sont positionnés sur deux lignes
            #Pas besoin de s'occuper du fait que certains items n'en possèdent pas car si il n'en possède pas alors cette enregistrement est un nom d'item et la premiere condition du if s'en occupe
            if(ligne[i]=="Armure\n" or ligne[i]=="Primaires\n"):
                pass
            elif(ligne[i]=="Secondaires\n"):
                primary = 0
            elif("Account Bound" in ligne[i]):
                account_bound = 1
            elif("Crée par" in ligne[i]):
                ligne_buffer = ligne[i].split(" ")
                fabricant = str(ligne_buffer[len(ligne_buffer)-1]).replace("\n", "")
                i += 1
                #On increment I pour passer la ligne indiquant le niveau d'artisanat requis pour créer l'item
            elif("Armure" in ligne[i+1] or "Dégâts par seconde" in ligne[i+1]):
                #On est dans le cas de la propriete sur 2 lignes
                property_list.append(str(str(ligne[i]).replace("\n", " ")+str(ligne[i+1])+"\t"+str(primary)))
                i += 1
                #On incremente de 1 i pour passer la ligne qu'on a noté en avance
            else:
                property_list.append(str(str(ligne[i]).replace("\n", "")+"\t"+str(primary)))
    db.commit()
    db.close()


if (__name__ == "__main__"):
    create_database()
