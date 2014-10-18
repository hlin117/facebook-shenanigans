import requests
from bs4 import BeautifulSoup
import codecs
import os
import socket
import sys
import time

CHECK_INTERVAL = 2

DEFAULT_PORT = 6666

BASE_URL = "http://m.facebook.com/"
LOGIN_INFO_PATH = "testinfo"

def main():

	# Get port
	port = DEFAULT_PORT
	if len(sys.argv) > 1: port = int(sys.argv[1])

	# Read quick info for testing
	email, password, allowed_pokes = getLoginInfo()

	while(True):

		print "Checking for new pokes..."
		print
		pokes = pokeBack(port, allowed_pokes)
		if pokes == False:
			print "Poke checking failed."
			return
		print

		time.sleep(CHECK_INTERVAL)

'''
Sends a GET request through the session on the given port.
The GET request will carry the provided url.
The text of FB's response is returned.
'''
def getResponse(url, port):

	try: 

		# Connect to fb_session
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(('localhost', port))

		# Send type and url payload
		payload = {}
		payload['type'] = 'GET'
		payload['url'] = url
		sock.sendall(str(payload))

		# Use string buffer to read everything from socket
		buff = ""
		data = True
		while data:
			data = sock.recv(1024)
			buff += data
		return buff

	except:

		print "Could not connect to server on " + str(port)
		return False


'''
Gets the active pokes from the provided FB_Session port.
Returns a list of links to access to poke back everyone.
'''
def pokeBack(port, allowed_pokes):

	pokeURL = BASE_URL + 'pokes'

	# Get data from pokes page
	response = getResponse(pokeURL, port)
	if response == False:
		print "GET request routing failed."
		return False
	soup = BeautifulSoup(response)

	# Filter down to divs of people to poke back
	class_filter = soup.findAll('div', {'class' : 'bd'})
	poke_divs = [div for div in class_filter if 'poked you' in div.text]
	
	# Get people's names
	name_links = [div.findAll('a')[0] for div in poke_divs]
	profile_pics = [a.findAll('img')[0] for a in name_links]
	names = [img['alt'] for img in profile_pics]

	# Get poke back links
	poke_links = [BASE_URL + div.findAll('a')[2]['href'] for div in poke_divs]

	# Poke allowed people back
	if len(names) == 0: print "No one poked you :("
	for i in range(len(names)):
		print names[i], "poked you!"
		if names[i] in allowed_pokes:
			getResponse(poke_links[i], port)
			print "Poked", names[i], "back."
		else:
			print "You did not give permission to poke", names[i], "back."


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
	f = open(LOGIN_INFO_PATH, 'r')
	email = f.readline().rstrip()
	password = f.readline().rstrip()
	allowed = f.readline().rstrip()
	f.close()
	return email, password, eval(allowed)

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
