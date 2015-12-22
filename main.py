import socket
import re
import sys
import threading
import time

import request
import serverStatus
import kill


port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1) # don't queue up any requests

# Loop forever, listening for requests:
while True:
    csock, caddr = sock.accept()
    # print "Connection from: " + `caddr`
    req = csock.recv(1024) # get the request, 1kB max
    r_match = re.match('GET /api/request\?connId=(\d+)&timeout=(\d+)\sHTTP/1', req)
    s_match = re.match('GET /api/serverStatus\sHTTP/1', req)
    if r_match:
        connId = r_match.group(1)
        timeout = r_match.group(2)
        r_thread = request.request(csock, connId, timeout)
        millis = time.time()
        r_thread.setName('r_' + `millis`)
        r_thread.start()
    elif s_match :
        s_thread = serverStatus.serverStatus(csock)
        s_thread.start()
    else:
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