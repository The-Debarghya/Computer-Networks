#!/usr/bin/env python3
import socket

HOST = '127.0.0.1'
PORT = 9999

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print("Waiting for connections")

while True:
    c, addr = s.accept()
    print("Connection from {}".format(addr))
    protocol = c.recv(1024).decode('utf-8')
    if protocol == "1":
        pass
    elif protocol == "2":
        pass
    else:
        pass
    c.close()
