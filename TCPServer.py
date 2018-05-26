#TCPServer.py
import os
import sys
from socket import socket, SOCK_STREAM, AF_INET

def openTcpSocket(serverPort):
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	return serverSocket

def sendFile(connectionSocket, filename, contentType):
	
	file = open(filename, 'rU').read()
	fileSize = os.path.getsize(filename)
	buffer = open(filename, 'rU').read()
	connectionSocket.send("HTTP/1.1 200 OK\n")
	connectionSocket.send("Content-Length: %d\n" % fileSize)
	connectionSocket.send("Content-Type: %s\n\n" % contentType)
	connectionSocket.send(buffer)
	
	#extension = filename.split()[1].partition(".")[2]

def sendError(connectionSocket, num, error):
	connectionSocket.send('HTTP/1.1 404 Not Found')

def main():
	serverSocket = openTcpSocket(1122)
	serverSocket.listen(1)
	while True:
		try:
			#Establish the connection
			print 'Ready to serve...'
			connectionSocket, addr = serverSocket.accept()
			message = connectionSocket.recv(4096)
			print message
			filename = message.split()[1].partition("/")[2]
			#statusLine = message.split()[2]
			#print statusLine
			sendFile(connectionSocket, filename, "text/plain")
			connectionSocket.close()
		except IOError:
			print "Not found %s" % filename
			sendError(connectionSocket, '404', 'Not Found')
			connectionSocket.close()
		except KeyboardInterrupt:
			print "\nInterrupted by CTRL-C"
			break
	serverSocket.close()

if __name__== '__main__':
	main()
