#!/usr/bin/env python3
import socket
import random
import time
from Crypto.Util.number import long_to_bytes

HOST = '127.0.0.1'
PORT = 9999
DATA_SIZE = 46
c = socket.socket()
random.seed(time.time())


def inject_error(text: str, number: int) -> str:
    if number == 0:
        return text
    for _ in range(number):
        x = random.randint(0, len(text)-1)
        if text[x] == '0':
            text = text[:x]+'1'+text[x+1:]
        else:
            text = text[:x]+'0'+text[x+1:]
    return text


c.connect((HOST, PORT))
with open("test.txt", "r") as f:
    text = f.read()

protocol = input(
    "Select the Protocol:\n[1]Stop and Wait ARQ\n[2]Go Back N\n[3]Selective Repeat\nYour choice:")
if protocol not in ["1", "2", "3"]:
    print("Not a valid option!")
    exit(2)
c.send(protocol.encode('utf-8'))
