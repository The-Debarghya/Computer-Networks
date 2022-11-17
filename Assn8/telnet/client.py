#!/usr/bin/env python3
import socket
from threading import Thread

HOST = "localhost"
PORT = 9999
def sendProcess(sock: socket.socket) -> None:
    while True:
        msg = input()
        msg = msg.encode()
        sock.send(msg)
        if msg == "exit".encode('utf-8'):
            break

def receiveProcess(sock: socket.socket) -> None:
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode())

if __name__ == "__main__":
    s = socket.socket()
    s.connect((HOST, PORT))

    sendThread = Thread(target=sendProcess, args=[s])
    receiveThread = Thread(target=receiveProcess, args=[s])

    sendThread.start()
    receiveThread.start()

    sendThread.join()
    receiveThread.join()