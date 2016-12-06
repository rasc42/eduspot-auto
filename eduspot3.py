#!/usr/bin/python
# (c) Phoenix, All rights reserved
from bs4 import BeautifulSoup
import getpass
from time import sleep
import requests

s = requests.session()

print("Récupération du premier token")

r = s.get("https://univnautes.ensiie.fr/sso?entity_id=https://shibboleth.ensiie.fr/idp/shibboleth")
soup = BeautifulSoup(r.text, 'html.parser')
token1 = soup.find('input')['value']

sleep(1)
print("Envoi du premier token à l'ENSIIE")

j = s.post("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO", data = {"SAMLRequest": token1})


print("Récupération du formulaire de connexion")
sleep(1)
r = s.get("https://cas.ensiie.fr/login?service=https://shibboleth.ensiie.fr/idp/Authn/RemoteUser")
soup = BeautifulSoup(r.text, 'html.parser')
urlpost = "https://cas.ensiie.fr" + soup.find('form')['action']

inputs = soup.find_all('input')
for i in inputs:
    if (i['name'] == 'lt'):
        lt = i['value']
    if (i['name'] == 'execution'):
        execution = i['value']

print("fin de l'analyse")

sleep(1)
print("Remplissage du formulaire de connexion")
password = getpass.getpass("Entrez votre mot de passe : ")

payload = {'_eventId': 'submit', 'lt': lt, 'execution':execution, 'submit': 'LOGIN', 'username': 'eliah.rebstock', 'password': password}
j = s.post(urlpost, data=payload)

print(j.text)
sleep(1)
soup = BeautifulSoup(j.text, 'html.parser')
token2 = soup.find('input')['value']

sleep(1)
print(token2)
print("Authentification finale")
s.post("https://univnautes.ensiie.fr/authsaml2/singleSignOnPost", {"SAMLResponse": token2})

sleep(1)
print("Vous êtes sensé être connecté à eduspot !")
