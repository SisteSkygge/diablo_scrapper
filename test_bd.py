import sqlite3
from CONSTANT import *

def test_bd(db_var):
    requete = db_var.execute("SELECT * FROM Objet")
    for res in requete:
        print(res)
    requete = db_var.execute("SELECT * FROM Propriete")
    for res in requete:
        print(res)
    requete = db_var.execute("SELECT * FROM Fabrique")
    for res in requete:
        print(res)

if __name__=="__main__":
    db = sqlite3.connect(DB_NAME)
    test_bd(db)
    db.close()
