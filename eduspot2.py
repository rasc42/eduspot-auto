#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib.request as url
from urllib.parse import urlencode
import getpass
from time import sleep

print("Récupération du premier token")
with url.urlopen("https://univnautes.ensiie.fr/sso?entity_id=https://shibboleth.ensiie.fr/idp/shibboleth") as page1:
    soup = BeautifulSoup(page1.read(), 'html.parser')
    token1 = soup.find('input')['value']

sleep(1)
print(token1)
print("Envoi du premier token à l'ENSIIE")
url.urlopen("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO", urlencode({"SAMLRequest": token1}).encode())

print("Récupération du formulaire de connexion")
sleep(1)
with url.urlopen("https://cas.ensiie.fr/login?service=https://shibboleth.ensiie.fr/idp/Authn/RemoteUser") as page2:
    soup = BeautifulSoup(page2.read(), 'html.parser')
    urlpost = "https://cas.ensiie.fr" + soup.find('form')['action']

sleep(1)
print(urlpost)
print("Remplissage du formulaire de connexion")
password = getpass.getpass("Entrez votre mot de passe : ")

url.urlopen(urlpost, urlencode({"username": "eliah.rebstock", "password": password}).encode())

with url.urlopen("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO") as page3:
    print(page3.read())
    soup = BeautifulSoup(page3.read(), 'html.parser')
    token2 = soup.find('input')['value']

sleep(1)
print(token2)
print("Authentification finale")
url.urlopen("https://univnautes.ensiie.fr/authsaml2/singleSignOnPost", urlencode({"SAMLResponse", token2}).encode())

sleep(1)
print("Vous êtes sensé être connecté à eduspot !")
