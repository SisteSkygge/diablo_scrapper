# -*- coding:utf-8 -*-
from CONSTANT import *
from diablo3_scrapper_utils import *
from clean import *
from get_page import *
from copy_paste import *
from create_database import *
from get_categorie import *
from test_bd import *

#Dé-commenté pour retélécharger les pages en cas de mises à jour de Diablo et de changements dans les items
get_page(dir_storage)

#DEBUG supprime les fichiers temporaires se trouvant dans le repertoire d'execution
clean(".", True)
copy_from_data_storage(dir_storage)
create_database()

for element in url_extension:

    #On selectionne seulemnt le contenu entre les balises <tbody> et </tbody>
    #Le contenu entre ces lignes est le détail et le nom des items
    select("<tbody>\n","</tbody>\n", element)
    #On retire toutes les balises pour pouvoir effectuer le traitement et la detection de texte pour le mettre dans la base de données
    remove_balise(element)
    #Dernier artefact à retirer pour que la detection des elements soit opérationnels
    #Ces artefacts sont des INT dans le fichier qui servent dans le code source de la page HTML à référencer le numéro de case
    remove_int(element)
    #Retire les espaces en position 0 dans les lignes
    remove_first_character_space(element)
    #Amélioration -> Faire les opérations suivantes en faisant moins d'ouverture d'un même fichier
    add_data_to_database(DB_NAME, element)

#Pas d'utilité pour le moment mais il est la
#get_categorie(file_with_categorie)

#clean(".", False)
#Essaie de la base de données
#test_bd(DB_NAME)
clean(".", False)
