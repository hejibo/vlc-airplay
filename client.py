#!/usr/bin/python
from socket import *
from sys import argv

udpAddr = ('192.168.123.2', 56662)
tcpAddr = ('192.168.123.2', 56672)

if __name__ == '__main__':
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind( ('192.168.123.3', 56662) )
	filename = argv[1]
	subtitles = argv[2] if len(argv) == 3 else ''
	if filename == '': exit(0)
	
	if subtitles == '': 
		sock.sendto('Starting airplay: %s' % filename, udpAddr )
	else:
		sock.sendto('Starting airplay, subtitles: %s' % filename, udpAddr )
	
	data, addr = sock.recvfrom(64)

	if data == 'Start, port 56672':
		if subtitles != '':
			stream = socket(AF_INET, SOCK_STREAM)
			stream.connect(tcpAddr)
			buff = open('%s' % subtitles, 'r')
			buff.seek(0)

			while 1:
				frame = buff.read(2048)
				if not frame: break
				stream.send(frame)

			buff.close()
			stream.close()

		stream = socket(AF_INET, SOCK_STREAM)
		stream.connect(tcpAddr) 
		buff = open('%s' % filename,'r')
		buff.seek(0)
		print('File opened, starting upload...')
		while 1:
			frame = buff.read(2048)
			if not frame: break
			stream.send(frame)

		stream.close()
		buff.close()
		print('Upload finished!')

	sock.close()