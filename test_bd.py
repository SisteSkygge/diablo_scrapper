import sqlite3
from CONSTANT import *

def test_bd(DB_NAME):
    db = sqlite3.connect(DB_NAME)
    requete = db.execute("SELECT * FROM Objet")
    for res in requete:
        print(res)
    requete = db.execute("SELECT * FROM Propriete")
    for res in requete:
        print(res)
    requete = db.execute("SELECT * FROM Fabrique")
    for res in requete:
        print(res)

if __name__=="__main__":
    test_bd(DB_NAME)
