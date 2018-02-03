import sqlite3
import os

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
            qualite VARCHAR(100),
            account_bound INT,
            check (account_bound=1 or account_bound=0));""")

    db.execute("""
        CREATE TABLE Propriete(
            id_objet INTEGER,
            type VARCHAR(25),
            intitule VARCHAR(250),
            PRIMARY KEY (id_objet, type),
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
    buffer_cat = []
    primary = 1
    phase = 0
    account_bound = 0
    categorie = ""
    fabricant = ""

    for element in ligne:
        #Le nom des items ont maintenant un repere, il est plus facile de découper le fichier dans les bonnes sections
        pass
        #TODO

if (__name__ == "__main__"):
    create_database()
