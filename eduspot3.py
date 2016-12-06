#!/usr/bin/python
# (c) Phoenix, All rights reserved
from bs4 import BeautifulSoup
import getpass
from time import sleep
import requests

def cookiesjoin(cj1, cj2):
    k = requests.utils.dict_from_cookiejar(cj2)
    return requests.utils.add_dict_to_cookiejar(cj1, k)

print("Récupération du premier token")
r = requests.get("https://univnautes.ensiie.fr/sso?entity_id=https://shibboleth.ensiie.fr/idp/shibboleth")
soup = BeautifulSoup(r.text, 'html.parser')
token1 = soup.find('input')['value']

cookies = r.cookies

sleep(1)
print("Envoi du premier token à l'ENSIIE")

j = requests.post("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO", data = {"SAMLRequest": token1}, cookies = cookies)

cookies = cookiesjoin(cookies, j.cookies)

print("Récupération du formulaire de connexion")
sleep(1)
r = requests.get("https://cas.ensiie.fr/login?service=https://shibboleth.ensiie.fr/idp/Authn/RemoteUser", cookies = cookies)
soup = BeautifulSoup(r.text, 'html.parser')
urlpost = "https://cas.ensiie.fr" + soup.find('form')['action']

cookies = cookiesjoin(cookies, r.cookies)

sleep(1)
print(urlpost)
print("Remplissage du formulaire de connexion")
password = getpass.getpass("Entrez votre mot de passe : ")

j = requests.post(urlpost, data={"username": "eliah.rebstock", "password": password}, cookies=cookies)

cookies = cookiesjoin(cookies, j.cookies)
print(cookies)
sleep(1)
r = requests.get("https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO", cookies=cookies)
print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
token2 = soup.find('input')['value']

cookies = cookiesjoin(cookies, r.cookies)

sleep(1)
print(token2)
print("Authentification finale")
requests.post("https://univnautes.ensiie.fr/authsaml2/singleSignOnPost", {"SAMLResponse", token2}, cookies=cookies)

sleep(1)
print("Vous êtes sensé être connecté à eduspot !")
