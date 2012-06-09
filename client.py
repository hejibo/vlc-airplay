#!/usr/bin/env python
from __future__ import with_statement
import os
from socket import *
from sys import argv

remoteAddr = '192.168.123.2'
udpAddr = ( remoteAddr, 56662 )
tcpAddr = ( remoteAddr, 56673 )

def sendFile(path, content):
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.settimeout(16)
	sock.bind( ('0.0.0.0', 56662) )

	fName = path.split('/')[-1]
	fSize = os.path.getsize(path)

	header = '{"name": "%s", "size": %s, "content": "%s"}' % (fName, fSize, content)
	print('Trying to connect, header: %s' % header)
	sock.sendto( header, udpAddr )

	try:
		data, addr = sock.recvfrom(64)
	except:
		print('Connection timed out')
		return
	
	if data == '{"response": 200}':
		with open( path, 'r' ) as rBuffer:
			try:
				strmSock = socket(AF_INET, SOCK_STREAM)
				strmSock.connect( tcpAddr )
				rBuffer.seek(0)

				while not False:
					data = rBuffer.read(2048)
					if not data: 
						break
					strmSock.send(data)

			finally:
				strmSock.close()

if __name__ == '__main__':
	fVideo = argv[1]
	fSubtitle = argv[2] if len(argv) > 2 else ''

	if os.path.isfile(fSubtitle):
		sendFile(path = fSubtitle, content = 'subtitle')

	if os.path.isfile(fVideo):
		sendFile(path = fVideo, content = 'video')