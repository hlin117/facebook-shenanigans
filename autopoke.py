import requests
from bs4 import BeautifulSoup
import codecs
import os
import urllib2
import cookielib

BASE_URL = "http://m.facebook.com/"

def main():

	# Get test email and password from local file
	email, password = getLoginInfo()

	# Get FB session
	session = login(email, password)
	if session == -1:
		print "Connection failed."
		return
	elif session == -2:
		print "Bad email / password combination."
		return

	# Test if the session can get to the pokes page
	showHTML(session.get(BASE_URL + 'pokes'))


'''
Logs into Facebook with the given email and password.
Returns a Requests session for further requests.
Returns error code -1 for failed connection and -2 for bad login credentials.
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
		return session

	except: return -1

#########################
# Code for Testing
#########################

'''
Reads the testinfo file, the first two lines of which are the email and 
password used for debugging. This information is not hardcoded so as to
keep it private in the repository.
'''
def getLoginInfo():
	f = open('testinfo', 'r')
	return f.readline(), f.readline()

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
