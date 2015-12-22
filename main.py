import socket
import re
import sys
import threading
import time

import request                                                  # request.py to create new request
import serverStatus                                             # serverStatus.py to get list of active requests
import kill                                                     # kill.py for kill requests

host = ''
port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

while True:
    csock, caddr = sock.accept()
    # print "Connection from: " + `caddr`
    req = csock.recv(1024)
    r_match = re.match('GET /api/request\?connId=(\d+)&timeout=(\d+)\sHTTP/1', req)
    s_match = re.match('GET /api/serverStatus\sHTTP/1', req)
    k_match = re.match('GET /api/kill\?connId=(\d+)\sHTTP/1', req)
    if r_match:
        connId = r_match.group(1)
        timeout = r_match.group(2)
        r_thread = request.request(csock, connId, timeout)
        r_thread.setName('r_' + `time.time()`)                 # name request thread as r_<start time>
        r_thread.start()
    elif s_match :
        s_thread = serverStatus.serverStatus(csock)
        s_thread.start()
    elif k_match :
        connId = k_match.group(1)
        k_thread = kill.kill(csock, connId)
        k_thread.start()
    else:                                                       # invalid request
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