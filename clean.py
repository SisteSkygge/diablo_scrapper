import os
from CONSTANT import *

def clean(dir_name, bool_del_DB):

    for element in os.listdir(dir_name):
        if (str(element).replace(".html", "") in url_extension):
            os.remove(element)
        else:
            pass
        if(element==file_with_categorie):
            os.remove(element)
        if(element==DB_NAME and bool_del_DB==True):
            os.remove(DB_NAME)

if "__main__" == __name__:
    clean(".", True)
