#!/usr/bin/env python3
import socket
import os
from threading import Thread
import subprocess

HOST = "localhost"
PORT = 9999

def exec_cmd(command: str, path: str) -> str:
    out = subprocess.run(command, capture_output=True, shell=True, cwd=path)
    if out.returncode == 0:
        return out.stdout.decode("utf-8")
    else:
        return out.stderr.decode("utf-8")

def handleNewClient(conn: socket.socket, addr: socket._Address) -> None:
    path = os.getcwd()
    while True:
        data = conn.recv(1024)
        res = "".encode()
        if not data:
            break
        data = data.decode().strip()
        if data == "exit":
            break
        elif data.startswith("cd"):
            requiredPath = data.split(" ")[1].strip()
            tmpPath = os.path.join(path, requiredPath)
            resTerminal = exec_cmd("cd "+ tmpPath, path)
            path = requiredPath
            res = resTerminal.encode()
        else:
            print(data)
            resTerminal = exec_cmd(data, path)
            res = resTerminal.encode()
        conn.send(res)
    conn.close()

def init_server() -> None:
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    processes = []
    while True:
        conn, addr = s.accept()
        t = Thread(target=handleNewClient, args=[conn, addr])
        t.start()
        processes.append(t)

        for x in processes:
            x.join()

if __name__ == "__main__":
    init_server()