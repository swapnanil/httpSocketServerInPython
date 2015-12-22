from threading import Thread
import socket
import time
import threading

class serverStatus(Thread) :
	def __init__(self, csock) :
		Thread.__init__(self)
		self.csock = csock
	def run(self) :
		ss = '{'
		for t in threading.enumerate() :
		    	r_name = t.getName()
		    	if r_name[0 : 2] == 'r_' :
		    		remaining_time = float(t.timeout) - ( time.time() - float(r_name[2 : ]) )
		    		if remaining_time > 0 :
		    			ss += '"' + t.connId + '" : "' + `int(round(remaining_time))` + '", '
		ss = ss[0 : -2]
		if ss :
			ss += '}'
		else :
			ss = 'No active requests!'
		self.csock.sendall("""HTTP/1.0 200 OK
			Content-Type: text/html

			<html>
			<head>
			<title>Server Status</title>
			</head>
			<body>"""
			+ ss +
			"""</body>
			</html>""")
		self.csock.close()