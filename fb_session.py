#!/usr/bin/env python2.7

import requests
from bs4 import BeautifulSoup
import sys
import SocketServer
import getpass

DEFAULT_PORT = 6666

BASE_URL = "http://m.facebook.com/"
LOGIN_INFO_PATH = "testinfo"

global session

def main():

	# Create FB Session and handler
	global session
	session = getSession()
	if session == False:
		print "Session aborted.", '\n'
		return

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
		sender = ""
		url = ""
		payload = {}
		try:
			payload = eval(data)
			req_type = payload['type']
			sender = payload['sender']
			url = payload['url']
			print "Processing", req_type, "request from", sender
			print "Destination:", '\t', url
		except:
			print "Improperly formatted payload; could not parse."
			return

		# Handle a GET request
		if req_type == 'GET':
			try:
				req = session.get(url)
				response = req.text.encode('utf-8')
				print "Handled GET request successfully."
				self.request.sendall(response)
				return
			except:
			 	print "Failed to handle GET request."
			 	return

		# Handle POST request
		if req_type == 'POST':

			try:

				# Attempt to parse headers and data
				headers = {}
				try: headers = eval(payload['headers'])
				except: print "Could not parse headers."
				data = {}
				try: data = eval(payload['data'])
				except: print "Could not parse data."

				# Send POST request
				req = session.post(url, data = data, headers = headers)
				response = req.text.encode('utf-8')
				print "Handled POST request successfully."
				self.request.sendall(response)
				return
				
			except:
				print "Failed to handle POST request."
				return

		# Unknown request
		else:
			print "Request type", req_type, "not recognized. Reponse aborted."

'''
Gets the user's email and password.
Uses this information to create and return an FB session.
'''
def getSession(debug = False):

	email = ""
	password = ""

	# Get username and password depending on whether in debug mode or not
	print '\n', "Please provide your Facebook credentials."
	email = raw_input("Email Address: ")
	password = getpass.getpass("FB Password: ")
	print

	# Create FB Session
	session = login(email, password)
	if session == -1:
		print "Connection failed."
		return False
	elif session == -2:
		print "Authentication failed."
		return False
	elif session == -3:
		print "Security check was given."
		return False

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


if __name__ == "__main__": main()
