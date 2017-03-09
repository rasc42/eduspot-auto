#!/usr/bin/python
from bs4 import BeautifulSoup
import getpass
import requests
import argparse


def connect(username, password):
    # Create a session to store all the needed cookies
    s = requests.session()

    # First, let's try to connect to a sample website
    r = s.get("http://captive.apple.com")
    if "Success" in r.text:
        print("You are already connected to the internet!")
        exit(0)
    # If there is no 'Success', it means we have arrived on the
    # captive portal instead of the website we want

    # Get the authentication token between the Grenoble INP server and the captive portal
    try:
        r = s.get(
            "https://eduspot-ouest.crous-grenoble.fr/sso?entity_id=https://shibboleth.grenoble-inp.fr/idp/shibboleth")
    except requests.exceptions.ConnectionError:
        print("Connection refused. Make sure that you are connected to EDUSPOT @ CROUS Grenoble.")
        exit(1)

    soup = BeautifulSoup(r.text, 'html.parser')
    token1 = soup.find('input')['value']

    # Post it to Grenoble INP server and retrieve Grenoble INP CAS form
    j = s.post("https://shibboleth.grenoble-inp.fr/idp/profile/SAML2/POST/SSO", data={'SAMLRequest': token1})
    soup = BeautifulSoup(j.text, 'html.parser')
    url_post = 'https://cas-inp.grenet.fr' + soup.find('form')['action']

    # Retrieve hidden inputs to post again
    inputs = soup.find_all('input')
    for i in inputs:
        if i['name'] == 'lt':
            lt = i['value']

    # While authentication is not done
    while True:
        if username:
            print("Username : " + username)
        # Ask for username if not given in parameter
        if not username:
            username = input("Login: ")
        # Ask for password if not given in parameter
        if not password:
            password = getpass.getpass('Password: ')

        # Authentication to Grenoble INP CAS
        payload = dict(_eventId='submit', lt=lt, submit='LOGIN', username=username, password=password)
        j = s.post(url_post, data=payload)
        soup = BeautifulSoup(j.text, 'html.parser')

        # Check if the authentication failed or not
        if soup.title and 'CAS' in soup.title.text:
            password = ''
        else:
            break

    # Retrieve the response token to send back to captive portal
    token2 = soup.find('input')['value']

    print('Authentication successful')
    s.post('https://eduspot-ouest.crous-grenoble.fr/authsaml2/singleSignOnPost', {'SAMLResponse': token2})

    # Finally, make a test with a classic test website
    r = s.get('http://captive.apple.com')
    if 'Success' in r.text:
        print('Verification finished: You are connected to EDUSPOT!')


parser = argparse.ArgumentParser(description='Connect to eduspot.')
parser.add_argument('-u', '--username', help='Username of the user')
parser.add_argument('-p', '--password', help='Password of the user')
args = parser.parse_args()

connect(args.username, args.password)
