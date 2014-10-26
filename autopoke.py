#!/usr/bin/env python2.7
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import socket
import sys
import time

DEFAULT_INTERVAL = 2
DEFAULT_PORT = 6666

BASE_URL = "http://m.facebook.com/"
LOGIN_INFO_PATH = "testinfo"

def main():

	# Get port
	port = DEFAULT_PORT
	if len(sys.argv) > 1: port = int(sys.argv[1])

	# Get check interval
	interval = DEFAULT_INTERVAL
	if len(sys.argv) > 2: interval = int(sys.argv[2])

	# Get people who can be poked
	allowed_pokes = set()
	print '\n', "Welcome to autopoke.py!"
	print "Before we begin, we need to know who we have permission to poke."
	print "Please enter the full Facebook names of everyone we can poke,"
	print "or the name of a text file containing names a line-delimited"
	print "list of people to poke."
	print "When you are finished, enter a blank line.", '\n'
	while(True):
		name = raw_input("We can poke: ")
		if name == "": break

		# If the "name" is the name of a text file
		if name.endswith(".txt"):
			try:
				text = open(name).read()
				namesset = set(name for name in text.split("\n") if name != "")
				allowed_pokes |= namesset
				print "Read the text file named " + name
			except:
				print "Couldn't read the file called " + name

		else:
			allowed_pokes.add(name)
	print '\n', "Great! We will poke", len(allowed_pokes), "people."
	print "We will check for new pokes every", interval, "second(s)."
	print '\n', "At any point, hit Control-C to stop.", '\n'
	print "Waiting for pokes...", '\n'

	# Start poking
	while(True):
		pokes = pokeBack(port, allowed_pokes)
		if pokes == False:
			print "Poke checking failed."
			return
		time.sleep(interval)

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
	if len(names) > 0: print
	for i in range(len(names)):
		print names[i], "poked you!"
		if names[i] in allowed_pokes:
			getResponse(poke_links[i], port)
			print "Poked", names[i], "back"
		else:
			print "You did not give permission to poke", names[i], "back."
	if len(names) > 0: print


if __name__ == "__main__": main()
