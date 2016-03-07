import netifaces as nint
import os
import socket

def serveAnImage(filename):
		#hostname = '127.0.0.1'
		port = 5000
		img = open(filename, 'r')
		hostname = nint.ifaddresses('wlan0')[2][0]['addr']

		print hostname

		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#socket handshake
		soc.bind((hostname, port+1)) #part 1
		soc.listen(5)

		#wait for part two on client side

		#ACK - part 3
		clientSoc, addr = soc.accept()
		print "Connected to - ", addr
		
		#send numObject_Payload
		numObject_Payload = 3
		clientSoc.sendall(str(numObject_Payload).encode('utf-8'))
		clientSoc.close()
		print 'Sent numObjects ', numObject_Payload

		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		soc.bind((hostname, port))
		soc.listen(5)
		clientSoc, addr = soc.accept()
		print "Now connected - ", addr
		while (1):
			
			while True:
				# read the image line by line
				strng = img.readline(1024) 	
				
				#reached end of file here, BREAK
				if not strng: 
					break
				clientSoc.send(strng) #send it through the socket
			img.close()
			print "Done"
			return
		soc.close()
		clientSoc.close()
		
			
if __name__ == "__main__":
#	print 'provide filename: '
#	filename = raw_input()
	filename = "image.jpg"
	serveAnImage(filename)
