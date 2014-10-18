import requests
from bs4 import BeautifulSoup
import codecs
import os
import urllib2
import cookielib

BASE_URL = "http://m.facebook.com/"

def main():

	# Get test email and password from local file
	email, password, allowed_pokes = getLoginInfo()

	# Get FB session
	session = login(email, password)
	if session == -1:
		print "Connection failed."
		return
	elif session == -2:
		print "Authentication failed."
		return
	elif session == -3:
		print "Security check was given."
		return

	# Check for recent pokes
	pokes = checkForPokes(session, allowed_pokes)
	if pokes == -1:
		print "Connection failed."
		return
	elif pokes == -2:
		print "Authentication failed."

	print pokes

################################################################################
# Facebook Functions
################################################################################


'''
Logs into Facebook with the given email and password.
Returns a Requests session for further requests.
Returns error code -1 for failed connection and -2 for bad login credentials.
Returns -3 if a security check was given.
'''
def login(email, password):

	try:

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
		soup = BeautifulSoup(req.text)


		if "Welcome" in soup.title: return -2
		elif "Security" in soup.title: return -3
		return session

	except: return -1


'''
Gets the active pokes from the provided FB session.
Returns a list of links to access to poke back everyone.
Returns error code -1 for failed connection and -2 for bad login credentials.
'''
def checkForPokes(session, allowed_pokes):

	pokeURL = BASE_URL + 'pokes'

	# Navigate to the pokes page
	req = session.get(pokeURL)
	soup = BeautifulSoup(req.text)

	#showHTML(req)

	# Get links to poke people back
	class_filter = soup.findAll('div', {'class' : 'bd'})
	poke_divs = [div for div in class_filter if 'poked you' in div.text]
	pokes = [pokeURL + tag.find_all('a')[0]['href'] for tag in poke_divs]

	# Filter out links by people the code is allowed to poke
	final_pokes = []
	for poke in pokes:
		print poke
		name = poke.split('/')
		print name
		if name[-1] in allowed_pokes:
			final_pokes.append(poke)

	return final_pokes


################################################################################
# Code for Testing
################################################################################

'''
Reads the testinfo file.

The first two lines of which are the email and 
password used for debugging. 

The third line is the list of allowed pokes.

This information is not hardcoded so as to
keep it private in the repository.
'''
def getLoginInfo():
	f = open('testinfo', 'r')
	return f.readline(), f.readline(), eval(f.readline())

'''
Takes a request and opens the returned HTML in Firefox.
This function was written specifically for my machine running Ubuntu.
It will likely fail in other environments.
'''
def showHTML(request):
	f = codecs.open('output.html', 'w', 'utf-8')
	f.write(request.text)
	f.close()
	os.system('firefox output.html')


if __name__ == "__main__": main()
