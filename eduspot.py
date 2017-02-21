#!/usr/bin/python
from bs4 import BeautifulSoup
import getpass
import requests
import argparse
import sys

def connect(username, password):
    # Create a session to store all the needed cookies
    s = requests.session()

    # Get the authentication token between the ENSIIE server and the captive portal
    try:
        r = s.get('https://univnautes.ensiie.fr/sso?entity_id=https://shibboleth.ensiie.fr/idp/shibboleth')
    except requests.exceptions.ConnectionError:
        print("Connexion refusée. Êtes-vous bien connecté à eduspot @ ENSIIE ?")
        exit(1)

    soup = BeautifulSoup(r.text, 'html.parser')
    token1 = soup.find('input')['value']

    # Post it to ENSIIE server and retrieve ENSIIE CAS form
    j = s.post('https://shibboleth.ensiie.fr/idp/profile/SAML2/POST/SSO', data = {'SAMLRequest': token1})
    soup = BeautifulSoup(j.text, 'html.parser')
    urlpost = 'https://cas.ensiie.fr' + soup.find('form')['action']

    # Retrieve hidden inputs to post again
    inputs = soup.find_all('input')
    for i in inputs:
        if (i['name'] == 'lt'):
            lt = i['value']
        if (i['name'] == 'execution'):
            execution = i['value']

    # While authentication is not done
    while (True):
        if username:
            print("Username : " + username)
        # Ask for username if not given in parameter
        if not username:
            username = input("Nom d'utilisateur : ")
        # Ask for password if not given in parameter
        if not password:
            password = getpass.getpass('Entrez votre mot de passe ENSIIE : ')

        # Authentication to ENSIIE CAS
        payload = {'_eventId': 'submit', 'lt': lt, 'execution':execution, 'submit': 'LOGIN', 'username': username, 'password': password}
        j = s.post(urlpost, data=payload)
        soup = BeautifulSoup(j.text, 'html.parser')

        # Check if the authentication failed or not
        if soup.title and 'CAS' in soup.title.text:
            password = ''
        else:
            break

    # Retrieve the response token to send back to captive portal
    token2 = soup.find('input')['value']

    print('Authentification réussie')
    s.post('https://univnautes.ensiie.fr/authsaml2/singleSignOnPost', {'SAMLResponse': token2})

    # Finally, make a test with a classic test website
    sys.stdout.write('Vérification de la connexion')
    r = s.get('http://captive.apple.com')
    if 'Success' in r.text:
        sys.stdout.write('\rVérification terminée : vous êtes connecté à eduspot !\n')

parser = argparse.ArgumentParser(description='Connect to eduspot.')
parser.add_argument('-u', '--username', help='Username of the user')
parser.add_argument('-p', '--password', help='Password of the user')
args = parser.parse_args()

connect(args.username, args.password)
