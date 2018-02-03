import os
from shutil import copyfile
from CONSTANT import url_extension

def copy_from_data_storage(dir_name):

    for element in url_extension:
        copyfile(dir_name+"/"+element, "./"+element)

if "__main__"==__name__:
    copie_from_data_storage("html_data")
