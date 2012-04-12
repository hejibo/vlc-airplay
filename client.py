from socket import *
from subprocess import Popen

accepted = ['192.168.123.3']
waiter_addr = ('192.168.123.2', 56662)
stream_addr = ('192.168.123.2', 56672)

if __name__ == '__main__':
	sWaiter = socket(AF_INET, SOCK_DGRAM)
	sWaiter.bind( waiter_addr )
	data, addr = sWaiter.recvfrom(256)
	
	if addr[0] in accepted:
		print(data)
		filename = 'file.mp4'

		stream = socket(AF_INET, SOCK_STREAM)
		buff = open('/tmp/%s' % filename,'w+')
		buff.seek(0)

		stream.bind( stream_addr )
		sWaiter.sendto('START AT PORT 56672', (addr[0],56662))
		print('Everything should start right now')

		stream.listen(1) #We wait here
		conn, addr = stream.accept() #Accepting connection
		dCount = 0
		while True:
			frame = conn.recv(2048)
			if not frame: break
			dCount+=1
			buff.write(frame)
			if dCount % 10 ==0: buff.flush()
			if dCount == 20: Popen(['vlc', '/tmp/file.mp4'])

		buff.close()  #Cleaning up
		conn.close()
		stream.close()
		print

	sWaiter.close()
