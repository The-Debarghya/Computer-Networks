#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 9999
ch = socket.socket()

ch.bind((HOST, PORT))

ch.listen(1)
print("Waiting for server to connect")
s, addr1 = ch.accept()
print(f"Connected to Server {addr1}")
s.send(b"ACK")
data = s.recv(1024)
s.close()

while True:
    c, addr = ch.accept()
    print("Connection from {}".format(addr))
    print(c.recv(1024).decode('utf-8'))
    c.send(data)
    c.close()
