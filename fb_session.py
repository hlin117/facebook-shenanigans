import requests
from bs4 import BeautifulSoup
import codecs
import os
import sys
import SocketServer

DEFAULT_PORT = 6666
DEBUG = True

BASE_URL = "http://m.facebook.com/"
LOGIN_INFO_PATH = "testinfo"

global session

def main():

	# Create FB Session and handler
	global session
	session = getSession(DEBUG)

	# Get port
	port = DEFAULT_PORT
	if len(sys.argv) > 1: port = int(sys.argv[1])

	# Start socket server on given port
	try:
		print "Starting socket server on port", port
		server = SocketServer.TCPServer(('localhost', port), FB_Session_Handler)
		server.serve_forever()
	except:
		print "An error has occured."
		print "Server has been shut down."


'''
Class for handling FB Session requests.
'''
class FB_Session_Handler(SocketServer.BaseRequestHandler):

	def handle(self):

		global session

		data = self.request.recv(1024).strip()
		print
		print "Received request from", self.client_address[0]

		# Attempt to load the data as a dictionary and load request type
		req_type = ""
		payload = {}
		try:
			payload = eval(data)
			req_type = payload['type']
		except:
			print "Improperly formatted payload; could not parse."
			return

		# Handle a GET request
		if req_type == 'GET':
			try:
				url = payload['url']
				req = session.get(url)
				response = req.text.encode('utf-8')
				print "Handled GET request."
				self.request.sendall(response)
				return
			except:
			 	print "Failed to handle GET request."
			 	return

'''
Gets the user's email and password.
Uses this information to create and return an FB session.
'''
def getSession(debug = False):

	email = ""
	password = ""

	# Get username and password depending on whether in debug mode or not
	if debug: email, password = getLoginInfo()
	else:
		print '\n', "Please enter your email address:", '\n'
		email = raw_input()
		print '\n', "Please enter your FB password:", '\n'
		password = raw_input()

	# Create FB Session
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

	return session


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

		# Return things
		if "Welcome" in soup.title.text: return -2
		elif "Security" in soup.title.text: return -3
		return session

	except: return -1


################################################################################
# Code for Testing
################################################################################

'''
Reads the testinfo file.

The first two lines of which are the email and 
password used for debugging. 

The third line is ignored.

This information is not hardcoded so as to
keep it private in the repository.
'''
def getLoginInfo():
	f = open(LOGIN_INFO_PATH, 'r')
	email = f.readline().rstrip()
	password = f.readline().rstrip()
	f.close()
	return email, password


if __name__ == "__main__": main()
