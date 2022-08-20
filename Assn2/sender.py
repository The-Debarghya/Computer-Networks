#!/usr/bin/env python3
import socket

HOST = 'localhost'
PORT = 9999
s = socket.socket()

s.connect((HOST, PORT))
if s.recv(1024).decode('utf-8') == "ACK":
    s.send(b"Data")
