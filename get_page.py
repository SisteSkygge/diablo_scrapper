import requests
import os
from CONSTANT import url_extension

def get_page(dir_storage):

    try:
        os.mkdir(dir_storage)
    except:
        pass

    for element in url_extension:
        #On recupere la page HTML
        file_handler = requests.get("https://eu.battle.net/d3/fr/item/"+str(element)+"/", stream=True)
        #On affiche le code de status apres avoir recuperer la page HTML voir si il y a une erreur ou non
        print(str(element)+" : "+str(file_handler))
        #On sauvegarde la page HTML dans un fichier
        with open(dir_storage+"/"+element, 'wb') as saving_file:
            for chunk in file_handler.iter_content(chunk_size=128):
                saving_file.write(chunk)
        saving_file.close()

if __name__=="__main__":
    get_page("html_data")
