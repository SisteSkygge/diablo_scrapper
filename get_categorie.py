from CONSTANT import url_extension, file_with_categorie

def get_categorie(saving_file_name):
    categorie_list = ""
    for element in url_extension:
        with open(element, 'r', encoding="utf-8") as saving_file:
            ligne = saving_file.readlines()
        saving_file.close()
        categorie_list += ligne[1].replace(" rare", "").replace(" magique", "").replace(" legendaire", "")

    with open(saving_file_name, 'w', encoding="utf-8") as saving_file:
        saving_file.write(categorie_list)
    saving_file.close()

    return categorie_list

if __name__=="__main__":
    get_categorie(file_with_categorie)
