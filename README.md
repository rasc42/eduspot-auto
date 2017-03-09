# Connection script to 'eduspot' wireless hotspot for Grenoble INP students #

Connection script to log faster to eduspot captive portal with GET and POST requests to the right urls. Actually the script works only for Grenoble INP students.

## Dependencies ##

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/master/)

## Usage ##

```
    $ eduspot.py [-h] [-u USERNAME] [-p PASSWORD]
```

If no username or password is given to the script, it will be asked during runtime.

* * *

# Script de connexion automatique à eduspot - Grenoble INP #

Script de connexion rapide au portail captif de eduspot en envoyant des requêtes GET et POST aux bonnes urls. Ce script gère uniquement la connexion pour les étudiants du Grenoble INP.

## Dépendances ##

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/master/)

## Utilisation ##

```
    $ eduspot.py [-h] [-u USERNAME] [-p PASSWORD]
```

Si le nom d'utilisateur ou le mot de passe n'est pas donné au script, il sera demandé à l'exécution.
