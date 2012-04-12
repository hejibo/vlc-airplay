from socket import *
from sys import argv

if __name__ == '__main__':
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind( ('192.168.123.3', 56662) )
	args = ''.join(argv[1:])
	if args == '': exit(0)
	
	sock.sendto('IMMA CHARGIN MAH AIRPLAY', ('192.168.123.2', 56662) )
	
	data, addr = sock.recvfrom(64)

	if data == 'START AT PORT 56672':
		stream = socket(AF_INET, SOCK_STREAM)
		stream.connect(('192.168.123.2', 56672))
		print('Connected!')

		buff = open('%s' % args,'r')
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