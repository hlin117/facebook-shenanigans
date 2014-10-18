import requests
from bs4 import BeautifulSoup
import codecs
import os
import urllib2
import cookielib

EMAIL = 'email'
PASSWORD = 'password'

BASE_URL = "http://m.facebook.com/"

def main():

	login(EMAIL, PASSWORD)

'''
Logs into Facebook with the given email and password.
Returns a Requests session for further requests.
'''
def login(email, password):

	loginURL = BASE_URL + 'login.php'

	# Sent GET Request to get form data
	req = requests.get(loginURL)
	soup = BeautifulSoup(req.text)

	# Add form data to data dictionary
	data = {}
	dataInputs = [tag for tag in soup.form.children if tag.name == 'input']
	for tag in dataInputs:
		name = tag['name']
		data[name] = soup('input', {'name' : name})[0]['value']

	# Add email and password
	data['email'] = email
	data['pass'] = password
	data['login'] = 'Log In'

	# Create session
	session = requests.Session()
	req = session.post(loginURL, data)

	print req.text

	return session





if __name__ == "__main__": main()
