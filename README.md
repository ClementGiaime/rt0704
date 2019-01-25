# Valerian-QCM

Conception d'un application de solution de QCM

## Requirement

Python version 3.7 doit être utilisé pour lancer les applications, de plus des modules sont nécéssaires pour le bon fonctionnement de l'app :

Module flask

```bash
pip3 install flask==1.0.2
```

Module lxml

```bash
pip3 install lxml==4.2.5
```

Module requests

```bash
pip3 install requests==2.21.0
```

## Pourquoi Python et flask ?

1°/ Parce qu'on m'a dit "tiens essaie python c'est pas mal", j'ai essayé, et j'ai adopté... `Ref. openclassrooms.com`

2°/ Python possède un nombre incalculable de librairie aussi utilie que inutile ! dans le cas de Valerian-QCM le module lxml est utilisé pour gérer la lecture, l'extration des informations et l'écriture dans des fichiers XML.

3°/ Flask est un framework open-source de développement web en Python, c'est un ensemble de modules qui facilite la programmation de sites web dynamiques. et ainsi cela permet de ne pas re-créer ce qui à déjà été fait.

## Pourquoi le nom Valerian ?

C'est une longue explication...

## Installation et lancement de l'application Valerian

### Via docker (Simple)

L'avantage de docker étant que vous n'avez pas besoin d'installé les prés-requis pyhton, de plus l'installation et le lancement de Valerian-QCM et plus simple.

Il existe 3 version de Valerian-QCM dockeriser :

* valerian-dev
* valerian-prod
* valerian-nginx

#### valerian-dev

valerian-dev utilise le cgi fourni par flask, or d'après la documentation de flask, ce cgi doit uniquement être utilisé dans un environement de developpement/test.

**Exemple 1 :**

```bash
docker run -d -p 5000:5000 -p 5002:5002 -e GLOBAL_IP="192.168.168.143" clementgiaime/valerian-dev
```

La variable GLOBAL_IP doit être indiqué lors de la commande docker run, l'adresse IP doit correspondre à l'adresse IP qui héberge le conteneur.

Pour accéder à l'application il suffit de se connecté sur l'adresse : http://GLOBAL_IP:5000/

**Exemple 2 :**

```bash
docker run -d -p 80:5003 -p 8080:5004 -e GLOBAL_IP="192.168.168.143" \
   -e BIND_PORT_QCM="5003" \
   -e BIND_PORT_CORRECTOR="5004" \
   -e PORT_SERVER_QCM="80" \
   -e PORT_SERVER_CORRECTOR="8080" clementgiaime/valerian-dev
```

Dans ce cas l'adresse de connection est  http://GLOBAL_IP/
Correspondance :

| VARIABLE ENVIRONEMENT    | DESCRIPTION                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| GLOBAL_IP                | doit être indiqué lors de la commande docker run, l'adresse IP doit correspondre à l'adresse IP qui héberge le conteneur. |
| BIND_PORT_QCM            | Correspond au port d'écoute du serveur QCM                                                                                |
| BIND_PORT_CORRECTOR      | Correspond au port d'écoute du Corrector QCM                                                                              |
| BIND_PORT_AUTHENTICATION | Correspond au port d'écoute du authentification QCM                                                                       |
| PORT_SERVER_QCM          | Correspond au port le hôte sur lequel BIND_PORT_QCM est mappé                                                             |
| PORT_SERVER_CORRECTOR    | Correspond au port le hôte sur lequel BIND_PORT_CORRECTOR est mappé                                                       |

Bien sur les port mappés `-p 80:5003 -p 8080:5004` doivent correspondre avec les variables `PORT_SERVER_QCM` `BIND_PORT_QCM` `BIND_PORT_CORRECTOR` `BIND_PORT_AUTHENTICATION`

#### valerian-prod

Version de valerian déployé selon les best pratices, en utilisant Gunicorn. Gunicorn est un serveur web HTTP WSGI écrit en Python.

> While lightweight and easy to use, Flask’s built-in server is not suitable for production as it doesn’t scale well. Some of the options available for properly running Flask in production are documented here.

http://flask.pocoo.org/docs/1.0/deploying/

**Exemple 1 :**

```bash
docker run -d -p 5000:5000 -p 5002:5002 -e GLOBAL_IP="192.168.168.143" clementgiaime/valerian-dev
```

La variable GLOBAL_IP doit être indiqué lors de la commande docker run, l'adresse IP doit correspondre à l'adresse IP qui héberge le conteneur.

Pour accéder à l'application il suffit de se connecté sur l'adresse : http://GLOBAL_IP:5000/

**Exemple 2 :**

```bash
docker run -d -p 80:5003 -p 8080:5004 -e GLOBAL_IP="192.168.168.143" \
   -e BIND_PORT_QCM="5003" \
   -e BIND_PORT_CORRECTOR="5004" \
   -e PORT_SERVER_QCM="80" \
   -e PORT_SERVER_CORRECTOR="8080" clementgiaime/valerian-dev
```

Dans ce cas l'adresse de connection est  http://GLOBAL_IP/
Correspondance :

| VARIABLE ENVIRONEMENT    | DESCRIPTION                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| GLOBAL_IP                | doit être indiqué lors de la commande docker run, l'adresse IP doit correspondre à l'adresse IP qui héberge le conteneur. |
| BIND_PORT_QCM            | Correspond au port d'écoute du serveur QCM                                                                                |
| BIND_PORT_CORRECTOR      | Correspond au port d'écoute du Corrector QCM                                                                              |
| BIND_PORT_AUTHENTICATION | Correspond au port d'écoute du authentification QCM                                                                       |
| PORT_SERVER_QCM          | Correspond au port le hôte sur lequel BIND_PORT_QCM est mappé                                                             |
| PORT_SERVER_CORRECTOR    | Correspond au port le hôte sur lequel BIND_PORT_CORRECTOR est mappé                                                       |

Bien sur les port mappés `-p 80:5003 -p 8080:5004` doivent correspondre avec les variables `PORT_SERVER_QCM` `BIND_PORT_QCM` `BIND_PORT_CORRECTOR` `BIND_PORT_AUTHENTICATION`

#### valerian-nginx (The best)

Valerian-nginx est la version la plus abouti. En plus de respecter les bests practices, elle intègre un reverse proxy (merci le titre) qui ne requis aucune configuration de la part de l'utilisateur.

```bash
docker run -d -p 80:80 clementgiaime/valerian-nginx
```

### Via le pull de l'application (Expert++)

**1°/** Installer les modules manquants

**2°/** Si les services sont lancer sur des machines différentes il faut modifier pour sur chaque service le fichier `configuration` présent à la racine du dossier. Sinon si les services sont sur la même machine, ne rien faire (c'est facile)

**3°/** sourcer le fichier de configuration avec la commande `source ./configuration`

**4°/** Lancer les services

```bash
cd Corrector-QCM/
python3.7 app.py &
cd ..
cd Authentication-QCM/
python3.7 app.py &
cd ..
cd Server-QCM/
python3.7 app.py &
```

## Architecture logiciels

![image](image.jpg)

## Utilisation

### Les utilisateurs

Il existe deux type d'utilisateur les étudiants et les professeurs

**Profil etudiant :**

* Voir la liste des QCM qu'il peut faire
* Peut faire un QCM
* Peut voir la correction du QCM une fois celui fait

Exemple de profil utilisateur :

* GIAIME
* GULDNER

**Profil Professeur :**

* Voir la liste de ces QCM
* Supprimer un QCM
* Ajouter un nouveau QCM

> Un QCM est assosié à une matiere, mais elle peut-être assosié à plusieur formation. Par exemple GIAIME et GULDNER ont comme matiere commune RT0701 et AN0701. Un QCM peut-être créé pour la matiere et ainsi être assosié à la formation AN0701. Dans ce cas GIAIME et GULDNER veron tout deux le QCM.

Exemple de profil professeur :

* FLAUZAC
* BELLECAVE
* STEFFENEL

### Les menus

## Problèmes connue dans le developpement

* Lors de la création d'un QCM, il est possible d'accosier une matiere avec une mauvaise formation

## Amélioration

* Enregistrement des notes des QCM effectués par les étudiants
* Affichage de tous les resultats des QCM effectués par les étudiants
* Ajout d'un file de message pour la correction des QCM

## Conseil

Ne pas chercher à corriger les fautes dans les commantaires du codes, j'ai mon correcteur qui a pris congé, il a attrapé la grippe. Et surtout utiliser l'application avec le conteneur valerian-nginx
