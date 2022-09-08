#!/usr/bin/env python3

import socket
from threading import Thread, Lock
import ErrorInsertion
import random
import time

client_map = {}
my_lock = Lock()


def process_packet(packet: str):
    flag = random.randint(0, 100)
    if(flag >= 0 and flag < 65):
        return packet
    elif(flag >= 65 and flag < 80):
        return ErrorInsertion.Error.injectError(packet)
    elif(flag >= 80 and flag < 90):
        time.sleep(0.5)
        return packet
    else:
        return ''


class ConnectionHandler (Thread):
    def __init__(self, clientSocket, clientAddress) -> None:
        Thread.__init__(self)
        self.csocket = clientSocket
        self.caddr = clientAddress
        print(f'\nGot new connection from {clientAddress}')

    def setConnection(self):
        availableClients = []
        availableClientNames = []
        for address in client_map:
            if address != self.caddr and client_map[address][2] is None:
                availableClients.append(address)
                availableClientNames.append(client_map[address][1])
        if (len(availableClients) == 0):
            self.csocket.send(bytes("No client is available", 'utf-8'))
        else:
            self.csocket.send(bytes(','.join(availableClientNames), 'utf-8'))
            choice = int(self.csocket.recv(1024).decode())
            my_lock.acquire()
            raddr = availableClients[choice]
            if (client_map[raddr][2] is None):
                rsocket = client_map[raddr][0]
                client_map[raddr][2] = self.caddr
                client_map[raddr][3] = 384
                client_map[self.caddr][2] = raddr
                client_map[self.caddr][3] = 576
                self.csocket.send(bytes(str(raddr[1]), 'utf-8'))
                rsocket.send(bytes(str(self.caddr[1]), 'utf-8'))
                print(self.caddr, "is sending data to", raddr)
            else:
                print("receiver is busy")
            my_lock.release()

    def revokeConnection(self) -> None:
        my_lock.acquire()
        raddr = client_map[self.caddr][2]
        client_map[raddr][2] = None
        client_map[self.caddr][2] = None
        client_map[raddr][3] = client_map[self.caddr][3] = 1024
        self.csocket.send(str.encode("Sending completed"))
        print(self.caddr, ' ended transferring data to ', raddr)
        my_lock.release()

    def run(self) -> None:
        self.csocket.send(b"You are now connected to server.\nClient Name: ")
        name = self.csocket.recv(1024).decode()
        self.csocket.send(bytes(str(self.caddr[1]), 'utf-8'))
        client_map[self.caddr] = [self.csocket, name, None, 1024]
        data = "open"
        while data != "close":
            inputBuffer = client_map[self.caddr][3]
            data = self.csocket.recv(inputBuffer).decode()
            if (client_map[self.caddr][2] is None):
                if data == "request for sending":
                    self.setConnection()
                else:
                    pass
            else:
                rsocket = client_map[client_map[self.caddr][2]][0]
                if data == "start":
                    rsocket.send(str.encode(data))
                elif data == "end":
                    rsocket.send(str.encode(data))
                    self.revokeConnection()
                else:
                    newData = process_packet(data)
                    if(newData != ''):
                        rsocket.send(str.encode(newData))
        self.csocket.close()
        print("Client at", self.caddr, "disconnected")
        client_map.pop(self.caddr)


def server():
    HOST = '127.0.0.1'
    PORT = 9999
    MAX_LIMIT = 5
    with socket.socket() as server:
        print("Server started")
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        print(f"Server socket bound to {PORT}")
        server.listen(MAX_LIMIT)
        print("Server is waiting for client request...")
        while True:
            conn, addr = server.accept()
            newThread = ConnectionHandler(conn, addr)
            newThread.start()


if __name__ == '__main__':
    server()
