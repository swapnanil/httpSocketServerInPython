from threading import Thread
import socket

class request(Thread) :
	def __init__ (self, csock, connId, timeout) :
		Thread.__init__(self)
		self.csock = csock
		self.connId = connId
		self.timeout = timeout

	def run(self) :
		print "(request) CONNID: " + self.connId + "\n"
		self.csock.sendall("""HTTP/1.0 200 OK
		Content-Type: text/html

		<html>
		<head>
		<title>Success</title>
		</head>
		<body>"""
		"""connId: """ + self.connId +
		"""<br>timeout: """ + self.timeout +
		"""</body>
		</html>
		""")
		self.csock.close()