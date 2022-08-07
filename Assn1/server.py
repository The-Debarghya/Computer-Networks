#!/usr/bin/env python3
import socket
from Crypto.Util.number import long_to_bytes, bytes_to_long
import checksum
import lrc
import vrc
import crc 

s = socket.socket()

s.bind(('localhost', 9999))

s.listen(1)
print("Waiting for connections")

while True:
    c, addr = s.accept()
    print("Connection from {}".format(addr))
    size = bytes_to_long(c.recv(1024))
    method = c.recv(1024).decode('utf-8')
    data = c.recv(1024).decode('utf-8')
    li = []
    while 1:
        text = c.recv(1024).decode('utf-8')
        if 'EOF' in text:
            li.append(text.replace("EOF", ""))
            break
        li.append(text)
    received_text = ''.join(li)[:size]
    print("Data size:{}, detection method:{}".format(size, method))
    print("Received Data={}".format(received_text))
    if method == "CRC":
        if crc.CRC.checkRemainder(li, data):
            c.send(b"Received Text, No errors found by CRC")
        else:
            c.send(b"Error detected by CRC")
    elif method == "VRC":
        if vrc.VRC.check_vrc(li, data):
            c.send(b"Received Text, No errors found by VRC")
        else:
            c.send(b"Error detected by VRC")
    elif method == "LRC":
        if lrc.LRC.check_lrc(li, data):
            c.send(b"Received Text, No errors found by LRC")
        else:
            c.send(b"Error detected by LRC")
    elif method == "Checksum":
        if checksum.Checksum.check_checksum(li, data):
            c.send(b"Received Text, No errors found by Checksum")
        else:
            c.send(b"Error detected by Checksum")
    else:
        raise Exception("An error occurred while parsing data")
    c.close()
