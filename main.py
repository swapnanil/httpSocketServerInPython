import socket
import re
import sys
from threading import Thread
from time import sleep
import request
import serverStatus
import kill
# Standard socket stuff:
host = '' # do we need socket.gethostname() ?
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1) # don't queue up any requests

# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    # print "Connection from: " + `caddr`
    req = csock.recv(1024) # get the request, 1kB max
    match = re.match('GET /api/request\?connId=(\d+)&timeout=(\d+)\sHTTP/1', req)
    if match:
        connId = match.group(1)
        timeout = match.group(2)
        r_thread = Thread(target = request.request, args = (csock, connId, timeout))
        r_thread.start()
    else:
        # If there was no recognised command then return a 404 (page not found)
        # print "Returning 404"
        csock.sendall("""HTTP/1.0 200 OK
                    Content-Type: text/html
                    <html>
                    <head>
                    <title> Invalid </title>
                    </head>
                    <body>
                    The request was not recognised
                    </body>
                    </html>""")
        csock.close()