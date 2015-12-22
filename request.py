from threading import Thread
import socket
import time
import threading

class request(Thread) :
	def __init__ (self, csock, connId, timeout) :
		Thread.__init__(self)
		self.csock = csock
		self.connId = connId
		self.timeout = timeout
		self.killed = False

	def run(self) :
		print "(request) CONNID: " + self.connId + "\n"

		start_time = float(threading.current_thread().getName()[2: ])
		while float(self.timeout) - (time.time() - start_time) > 0 :            # check for time remaining
			if self.killed :												    # if killed in kill.py
				self.csock.sendall("""HTTP/1.0 200 OK
				Content-Type: text/json\r\n
				{status : "killed"}""")
				self.csock.close()
				return

		self.csock.sendall("""HTTP/1.0 200 OK
		Content-Type: text/json\r\n
		{status : "ok"}""")
		self.csock.close()