#!/usr/bin/python
from bs4 import BeautifulSoup
import getpass
import requests
import argparse

def connect(username, password):
    s = requests.session()

    print("Récupération du premier token")

    r = s.get("https://univnautes.ensiie.fr/sso?entity_id=https://shibboleth.ensiie.fr/idp/shibboleth")
    soup = BeautifulSoup(r.text, 'html.parser')
    token1 = soup.find('input')['value']

    print("Envoi du premier token à l'ENSIIE")

    j = s.post("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO", data = {"SAMLRequest": token1})

    print("Récupération et analyse du formulaire de connexion")

    r = s.get("https://cas.ensiie.fr/login?service=https://shibboleth.ensiie.fr/idp/Authn/RemoteUser")
    soup = BeautifulSoup(r.text, 'html.parser')
    urlpost = "https://cas.ensiie.fr" + soup.find('form')['action']

    inputs = soup.find_all('input')
    for i in inputs:
        if (i['name'] == 'lt'):
            lt = i['value']
        if (i['name'] == 'execution'):
            execution = i['value']

    print("Fin de l'analyse")

    print("Remplissage du formulaire de connexion")
    if not password:
        password = getpass.getpass("Entrez votre mot de passe : ")

    payload = {'_eventId': 'submit', 'lt': lt, 'execution':execution, 'submit': 'LOGIN', 'username': username, 'password': password}
    j = s.post(urlpost, data=payload)

    soup = BeautifulSoup(j.text, 'html.parser')
    token2 = soup.find('input')['value']

    print("Authentification finale au portail captif")
    s.post("https://univnautes.ensiie.fr/authsaml2/singleSignOnPost", {"SAMLResponse": token2})

    print("Vous êtes sensé être connecté à eduspot !")
    print("Vérification avec captive.apple.com")
    r = s.get("http://captive.apple.com")
    if "Success" in r.text:
        print("Vérification terminée : vous êtes connecté à eduspot !")

parser = argparse.ArgumentParser(description='Connect to eduspot.')

parser.add_argument("username", help="username of the user")

parser.add_argument("-p", "--password", help="password of the user")

args = parser.parse_args()

connect(args.username, args.password)
