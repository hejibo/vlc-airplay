#!/usr/bin/env python
from __future__ import with_statement
from socket import *
from daemon import Daemon
import os, sys, json, threading

saveDir = '/home/var1able/airplay/%s'

class dAirplay(Daemon):
	def run(self):
		try:
			sock = socket(AF_INET, SOCK_DGRAM)
			sock.bind( ('0.0.0.0', 56662) )

			strmSock = socket(AF_INET, SOCK_STREAM)
			strmSock.bind( ('0.0.0.0', 56673) )

			while True:
				data, addr = sock.recvfrom(256)
				receiveFile(data, addr, sock, strmSock)
		finally:
			strmSock.close()
			sock.close()

def receiveFile(data, addr, sock, strmSock):
	data = json.loads(data)
	fName, fSize, fType = data['name'], data['size'], data['content']

	with open( saveDir % fName, 'w+' ) as wBuffer:
		wBuffer.seek(0)
		pCount = 0
		sock.sendto('{"response": 200}', addr)

		strmSock.listen(2)
		try:
			conn, addr = strmSock.accept()

			while not False:
				data = conn.recv(2048)
				pCount += 1
				if not data:
					break
				wBuffer.write(data)
				if pCount % 10: wBuffer.flush() 

			wBuffer.flush()

		finally:
			conn.close()

if __name__ == '__main__':
	daemon = dAirplay('/tmp/airplay-daemon.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                        #daemon.run()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)