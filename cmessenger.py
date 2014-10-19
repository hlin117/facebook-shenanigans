import requests
import socket

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
