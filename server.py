#!/usr/bin/python
from daemon import Daemon
from socket import *
from subprocess import Popen
import threading
import sys, re

accepted = ['192.168.123.3']
waiter_addr = ('192.168.123.2', 56663)
stream_addr = ('192.168.123.2', 56672)
defaultPath = '/home/var1able/%s'
rFileName = re.compile('[^/]*.[a-zA-Z]{2,3}$')

class dAirplay(Daemon):
	def run(self):
		sWaiter = socket(AF_INET, SOCK_DGRAM)
		sWaiter.bind(waiter_addr)
		while 1:
			data, addr = sWaiter.recvfrom(256)

			receiveStream(sWaiter, addr, data)

	def receiveStream(sWaiter, addr, data):
		if addr[0] in accepted:
			filename = re.findall(rFileName, data)[0]	
			print data[15:27]
			subtitle = 'subs.srt' if data[15:27] == 'y, subtitles' else ''
			try:
				stream = socket(AF_INET, SOCK_STREAM) #Creating streaming socket
				stream.bind( stream_addr ) # Binding socket
				sWaiter.sendto('Start, port 56672', (addr[0], 56662))
				if subtitle:
					print('Receiving subs')
					stream.listen(1)
					conn, addr = stream.accept() # Accepting connection
					buff = open(defaultPath % subtitle, 'w+')
					buff.seek(0)
					while True:
						frame = conn.recv(2048)
						if not frame: break
						buff.write(frame)
						buff.flush()
					buff.close()
					conn.close()
				conn, addr = stream.accept() # Accepting connection
				buff = open(defaultPath % filename, 'w+')
				buff.seek(0)
				dCount = 0
				while True:
					frame = conn.recv(2048)
					if not frame: break
					dCount += 1
					buff.write(frame)
					if dCount % 10 == 0: buff.flush()
					if dCount == 200: Popen(['vlc', defaultPath % filename, 
						'--sub-file=%s' % (defaultPath % subtitle)])

			except:
				sWaiter.sendto('Something bad happend, try again', (addr[0], 56662))
				buff.close()
				conn.close()
				stream.close()


class tReceive(threading.Thread):
	def run(self):
		pass

if __name__ == '__main__':
	daemon = dAirplay('/tmp/airplay-daemon.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        #daemon.start()
                        daemon.run()
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
