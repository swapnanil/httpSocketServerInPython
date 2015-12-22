from threading import Thread
import socket
import time
import threading

class kill(Thread) :
	def __init__(self, csock, connId) :
		Thread.__init__(self)
		self.csock = csock
		self.connId = connId
	def run(self) :
		found = False
		for t in threading.enumerate() :
		    	r_name = t.getName()
		    	if r_name[0 : 2] == 'r_' :                                  # if this is a request thread
		    		if int(t.connId) == int(self.connId) :
		    			found = True
		    			t.killed = True                                     # set t's killed attribute as true
		    			break
		if found :
			ss = '{"status":"ok"}'
		else :
			ss = '{"status":"invalid connection Id : ' + `self.connId` + '"}'
		self.csock.sendall("""HTTP/1.0 200 OK
			Content-Type: text/json\r\n
			""" + ss)
		self.csock.close()