# -*- coding:utf-8 -*-
""" Ce programme n'est compatible qu'avec python 3 et avec l'installation de la librairie requests
Installation de requests : pip install requests
"""

from CONSTANT import *
from diablo3_scrapper_utils import *
from clean import *
from get_page import *
from copy_paste import *
from create_database import *
from get_categorie import *
from test_bd import *
import sqlite3

#De-commente pour retelecharger les pages en cas de mises a jour de Diablo et de changements dans les items
get_page(dir_storage)

#DEBUG supprime les fichiers temporaires se trouvant dans le repertoire d'execution
clean(".", True)
#On copie les fichiers d'un repertoire de stockage des pages HTML pour eviter de faire trop de requetes aupres
#du serveur de blizzard
copy_from_data_storage(dir_storage)
#On cree la base de donnees
create_database()

#On cree une connection vers la base de donnees pour ne pas que les
#fonctions ouvrent et ferment plusieurs dizaines de fois une connection
db = sqlite3.connect(DB_NAME)

for element in url_extension:

    #On selectionne seulemnt le contenu entre les balises <tbody> et </tbody>
    #Le contenu entre ces lignes est le detail et le nom des items
    select("<tbody>\n","</tbody>\n", element)
    #On retire toutes les balises pour pouvoir effectuer le traitement et la detection de texte pour le mettre dans la base de donnees
    remove_balise(element)
    #Dernier artefact a retirer pour que la detection des elements soit operationnels
    #Ces artefacts sont des INT dans le fichier qui servent dans le code source de la page HTML a referencer le numero de case
    remove_int(element)
    #Retire les espaces en position 0 dans les lignes
    remove_first_character_space(element)
    #Amelioration -> Faire les operations suivantes en faisant moins d'ouverture d'un même fichier

#Recolte et cree le nom des differentes categories d'item different,
#Cela sera utile lors du traitement pour les enregistrements dans la base de donnees
#Pour les noms de categories composes de plusieurs mots comme "Hache a deux mains"
#Il cree aussi un fichier appele "categorie_file" qui se fait supprimer dans clean()
categorie_list = get_categorie(file_with_categorie)

#On rajoute les donnees de tous les fichiers dans la base de donnees
#cette fonction assure la reconnaissance des lignes et l'ajout dans la base de donnees
for element in url_extension:
    #TODO modifier la fonction pour qu'elle compare les categories qu'elle obtient avec les
    #categorie contenu dans cette variable categorie_list
    add_data_to_database(db, element, categorie_list)

#De-commente pour supprimer les fichiers traites des pages HTML
clean(".", False)
#DEBUG enlever le dossier de stockage des pages html forcera le retelechargement
clean_dir("html_data/")
#DEBUG enleve le fichier creer par python contenant des .pyc
clean_dir("__pycache__/")
#Essaie de la base de donnees en copiant toutes les tables se trouvant dans la base de donnees
#DEBUG
test_bd(db)
#Ferme la connection
db.close()
