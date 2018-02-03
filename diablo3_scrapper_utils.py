#-*- coding:utf-8 -*-

def select(borne_entree, borne_sortie, file_name):
    """Active l'enregistrement d'un fichier quand le pointeur de fichier se trouvent entre
    2 elements presents dans le texte"""

    #Initialisation de la variable qui servira à stocker le résultat de la fonction
    stockage = ""
    #Iniatialisation d'une variable permettant de déclencher ou non quand l'algorithme doit
    #Rajouter les éléments du fichier dans la variable stockage
    active = 0
    with open(file_name, 'r', encoding="utf-8") as file_handler:
        #line = "a" Pour remplir une premiere la condition de la boucle while pour ne pas
        #sortir directement de la boucle
        line ="a"
        while(line!=""):
            line = file_handler.readline()

            #On supprime les tabulations pour que celles-ci gènent lors de la comparaison
            #de string de même, on oubliera pas dans les arguments le \n s'il est nécessaire
            line = line.replace("\t", "")

            #On active l'enregistrement du fichier dans la variable stockage
            if(line==borne_entree):
                active = 1

            if(active==1):
                #Evite d'enregistrer des lignes vides contenant seulement un "\n"
                if(line=="\n"):
                    pass
                else:
                    stockage += line

            #On désactive l'enregistrement
            if(line==borne_sortie):
                active = 0

        file_handler.close()
        with open(file_name, 'w', encoding="utf-8") as saving_file:
            saving_file.write(stockage)
        saving_file.close()

def remove_balise(file_name):
    """ Cette fonction enlève toutes les balises d'un fichier texte et l'enregistre dans le fichier texte"""

    active = 0
    stockage = ""

    with open(file_name, 'r', encoding="utf-8") as saving_file:
        #Pour que la condition soit validé pour rentrer une premiere fois dans la boucle
        line = " "
        #Variable qui stockera le texte que l'on ré-écrira dans le fichier
        stockage = ""
        #On recupere toutes les lignes du fichier sous forme de list
        line = saving_file.readlines()
        #Une prend une ligne de la liste des lignes du fichier

        for element in line:
            #Init initial de la variable qui indique si l'on se trouve dans une balise ou non
            active = 0
            put_flag = 0
            #Met un repere si le cotenu de la liste correspond au nom d'un item
            if("<h3" in element and "><a href" in element):
                put_flag += 1

            for letter in element:
                #On prend les lettres 1 par 1 et on regarde si la caractere et < ou >
                #Que respectivement signifiront que nous rentrons ou sortons d'une balise
                if(letter=="<"):
                    #NOTE : +1 car une balise peut se trouver dans une autre balise et il faut TOUT supprimer
                    #On comptera donc le nombre de balise dans lequel nous rentrons
                    active += 1
                if(letter==">"):
                    #On est sorti d'une balise
                    active -= 1
                if(active==0):
                    if(put_flag>=1):
                        stockage += "&"
                        put_flag -= 1
                    #active==0 signifie que nous ne sommes pas dans une balises
                    #On sauvegarde donc la lettre
                    stockage += str(letter)

    saving_file.close()
    #On ferme le fichier pour pouvoir le ré-ouvrir en mode écriture
    #On se débarasse des derniers artefacts restants pour que le fichier soit plus lisible pour un humain
    #Les artefacts restant sont des ">" ou des lignes vides avec juste un "\n"
    stockage = stockage.replace(">", "")
    with open(file_name, 'w', encoding="utf-8") as saving_file:
        saving_file.write(stockage)
    saving_file.close()
    #On le ré-ouvre pour récuperer une liste des lignes
    with open(file_name, 'r', encoding="utf-8") as saving_file:
        file_handler = saving_file.readlines()
        stockage=""
        for element in file_handler:
            #On stocke seulement les chaines qui ne sont pas des "\n" vides
            if(element!="\n"):
                for letter in element:
                    stockage += letter
    saving_file.close()
    #On ferme le fichier pour le ré-ouvrir en mode écriture après
    #On sauvegarde le contenu de stockage dans le fichier, cela sera le résultat final de la fonction
    with open(file_name, 'w', encoding="utf-8") as saving_file:
        saving_file.write(stockage)
    saving_file.close()

def remove_int(file_name):
    """ Elimine les INT restant dans les fichiers servant à décrire le numéro de ligne pour le tableau dans lequel les objets étaient stockés"""

    #Pour cela on récupérera les lignes du fichier dans une liste, On regardera si la ligne contient une "," cela signifiera alors que c'est un nombre à virgule donc on ne touche pas.
    #Si la ligne n'en contient pas alors on essaiera de convertir la ligne en INT, si sa fonctionne alors on n'enregistre pas la ligne dans stockage, si cela ne fonctionne pas alors on enregistre la ligne dans stockage
    # REMARQUE : les "\n" ne génent pas à la convertion des string en INT

    stockage =""

    #On ouvre en mode lecture file_name pour mettre dans une liste les lignes du fichier
    with open(file_name, 'r', encoding="utf-8") as saving_file:
        ligne = saving_file.readlines()
    saving_file.close()
    #On navigue dans les éléments
    for element in ligne:
        if("," in element):
            for letter in element:
                stockage += letter
        else:
            try:
                #On essaie de convertir, si sa marche on ne fait rien , si sa échoue alors on enregistre l'élément dans stockage
                int(element)
            except:
                #la convertion en INT à échouer on enregistre l'element dans stockage
                for letter in element:
                    stockage += letter

    #On ouvre le file_name en mode ecriture pour y écrire stockage
    with open(file_name, 'w', encoding="utf-8") as saving_file:
        saving_file.write(stockage)
    saving_file.close()

def remove_first_character_space(file_name):
    stockage = ""
    with open(file_name, 'r', encoding='utf-8') as saving_file:
        ligne = saving_file.readlines()
    saving_file.close()

    for element in ligne:
        #Remplace les , par des . problemes de la version francaise de la page html, comme en France on utilise des virgules à la place des points pour les nombres décimaux
        element = element.replace(",", ".")
        if (element[0]==" "):
            element = element.replace(" ", "", 1)
        for letter in element:
            stockage += letter

    with open(file_name, 'w', encoding="utf-8") as saving_file:
        saving_file.write(stockage)
    saving_file.close()

if "__main__"==__name__:
    print(select("<tbody>", "</tbody>", "bow"))
    print("End")
