with open("categorie_file", "r", encoding="utf-8") as categorie_file:
    categorie = categorie_file.readlines()
categorie_file.close()

print(categorie)
print(categorie[0])
