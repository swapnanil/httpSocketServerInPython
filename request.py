from threading import Thread
import socket
import time

class request(Thread) :
	def __init__ (self, csock, connId, timeout) :
		Thread.__init__(self)
		self.csock = csock
		self.connId = connId
		self.timeout = timeout

	def run(self) :
		print "(request) CONNID: " + self.connId + "\n"
		time.sleep(int(self.timeout))
		self.csock.sendall("""HTTP/1.0 200 OK
		Content-Type: text/html

		<html>
		<head>
		<title>Success</title>
		</head>
		<body>
		{success : "ok"}
		</body>
		</html>
		""")
		self.csock.close()