#!/usr/bin/env python3
import socket
import packet

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
        filename = "StopWait_rec.txt"
        f = open(filename, "a")
        while True:
            pkt = c.recv(4096).decode('utf-8')
            if pkt == '':
                break
            pkt = packet.Packet.build(pkt)
            f.write(pkt.getData())
        f.close()
    elif protocol == "2":
        pass
    else:
        pass
    c.close()
