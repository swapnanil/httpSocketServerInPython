import socket

def request(caddr, connId, timeout) :
	csock
	print "CONNID: " + connId + "\n"
	csock.sendall("""HTTP/1.0 200 OK
	Content-Type: text/html
	<html>
	<head>
	<title>Success</title>
	</head>
	<body>"""
	"""connId: """ + connId +
	"""<br>timeout: """ + timeout +
	"""</body>
	</html>
	""")
	csock.close()