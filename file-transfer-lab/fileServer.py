#! /usr/bin/env python3
import sys

sys.path.append("../lib")       # for params

import os, socket, params
import os.path
from os import path


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        fileName = ''
        for x in range(10):
            if not path.exists("file%d.txt" % (x)):
                fileName = "file%d.txt" % (x)
                break

        f = open(fileName,'wb')

        while 1:
            data = framedReceive(sock,debug=1)
            if not data: break
            f = open(fileName,'wb')
            while data != bytes(''.encode()):
                f.write(data)
                print(data.decode())
                data = framedReceive(sock,debug=1)
                print("Received")

        while True:
            payload = framedReceive(sock, debug=1)
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug=1)

