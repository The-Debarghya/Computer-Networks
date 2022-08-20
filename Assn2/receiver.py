#!/usr/bin/env python3
import socket


HOST = 'localhost'
PORT = 9999

c = socket.socket()

c.connect((HOST, PORT))

text = input("Enter data:").encode('utf-8')
c.send(text)
print(c.recv(1024).decode('utf-8'))
