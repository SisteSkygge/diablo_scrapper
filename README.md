# diablo_scrapper

EXPLICATIONS POUR L'EXECUTION DU PROGRAMME :

Ce programme nécessite :
  -Python 3 (problème de compatibilité avec les mots-clefs utilisés en argument dans open qui ne sont pas disponible sur une version de python antérieur à la version 3.x
  -La librairie "requests" pour l'installer : pip install requests
  
Pour éxécuter le programme il suffit de lancer "diablo3_scrapper.py", tel qu'il est configuré le programme devrait sortir uniquement une base de données "diablo3_object.bd" qui est une base de données sqlite3.
Toutefois il est possible de modifier quelques arguments des fonctions pour garder les fichiers html de base traités par le programme dans un répertoire, il est possible de gardé les fichiers html une fois traitée (donc une fois que tout le code html et les parties inintéressantes supprimées), 

il est possible de ne pas re-télécharger à chaque fois les fichiers html ce qui prend le plus de temps lors de l'éxécution du programme du programme pour cela il suffit de mettre en commentaire la fonction "get_page()" et de mettre en commentaire à la fin du fichier principal la ligne "clean_dir('html_data/')"

--------------------------------------------------------------

EXPLICATION DE L'UTILISATION DE CHAQUE FICHIER :

diablo3_scrapper.py : Fichier principal d'éxécution
diablo3_scrappre_utils.py : Fournit des fonctions pour l'éxécution du fichier principal
CONSTANT.PY : Fournit des constantes lié à l'éxécution du programme
create_database.py : Fournit les fonctions permettant de créer la base de données et d'insérer des valeurs à l'intérieur
get_categorie.py : Fournit une fonction retournant un fichier avec le nom de chaque catégorie d'item dans le jeu //Inutilisé
get_page.py : Fournit des fonctions permettant de télécharger et stocker les pages html depuis le site officiel du jeu
copy_paste.py : Fournit une fonction permettant de copier les fichiers d'un dossier dans le répertoire courant
clean.py : Fournit des fonctions permettant de nettoyer le répertoire d'éxécution de différents dossiers/fichiers
test_db.py : Fournit une fonction affichant toutes les lignes de la base de données

--------------------------------------------------------------

MOT DU DÉVELOPPEUR : 

Le projet est terminé, toutefois il reste quelques améliorations possible sur plusieurs points :
  -Le traitement des fichiers html, le programme ouvre, ferme et recrée les fichiers beaucoup trop de fois pour être appeler "optimisé" néanmoins cela fonctionne sans provoquer une augmentation du temps d'éxécution significative.
  -La création des valeurs dans la base des données dans la partie catégorie(phase==1), suite à plusieurs problèmes avec les catégories notamment le mot "d'ensemble" j'ai du écrire un code immonde pour corriger ce problème, je pense que des améliorations sont aussi possible sur ce point.
  
D'autres améliorations sont aussi possible un peu partout dans le programme,
je ne souhaite pas continuer de l'améliorer pour plusieurs raisons :
  -Le manque de temps
  -Le manque d'envie, ce projet ne me fait plus envie je l'ai juste fini pour qu'il soit fonctionnel et dire qu'il marche même si il marche de façons assez hideuses.
  
Je m'excuse par avance à toutes les personnes qui liront et développeront à partir de ce code source je n'ai pas été rigoureux sur le nommage des différentes variables, fonction, etc... et supprimés certains commentaires qui n'ont plus de sens au point de développement actuel du projet, je ne prend pas le temps de corriger tout cela par manque d'envie comme citer plus haut car pour moi cela n'a plus d'importance, ce projet ne m'intéresse plus, j'en ai tiré les enseignements que je recherchais en le commançant avant de l'avoir terminé.
  
---------------------------------------------------------------

DÉVELOPPEUR :

GILLES Marco

Temps de développement : Janvier-Février 2018
Actuellement en 1er année d'IUT Informatique à l'université Nice Côte d'Azur (année scolaire 2017-2018)

----------------------------------------------------------------

COPYRIGHT

Creative Commons BY NC SA
©2018 GILLES MARCO
