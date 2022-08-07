#!/usr/bin/env python3
import socket
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random
import time
import checksum
import lrc
import vrc
import crc
import helper

HOST = 'localhost'
PORT = 9999
PKT_SIZE = 8
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

text = input("Enter data:").encode('utf-8')
res = input("Do you want to insert errors?(Y/n)")
method = input("Detection Method:(CRC/VRC/LRC/Checksum)")
enc_text = bin(bytes_to_long(text))[2:]
actual_len = len(enc_text)

if actual_len/8 == 0:
    pass
else:
    extra = '0'*(8-(actual_len % 8))
    enc_text = enc_text + extra

chunks = [enc_text[i:i+PKT_SIZE] for i in range(0, len(enc_text), PKT_SIZE)]

c.send(long_to_bytes(actual_len))
time.sleep(1)
if method == "CRC":
    c.send(b"CRC")
    time.sleep(1)
    crc_method = input("Give the CRC divisor method:")
    divisor = helper.convToBinary(crc_method)
    c.send(divisor.encode('utf-8'))
    chunks = crc.CRC.encodeData(chunks, divisor)
elif method == "VRC":
    c.send(b"VRC")
    time.sleep(1)
    c.send(vrc.VRC.generate_vrc(chunks).encode('utf-8'))
elif method == "LRC":
    c.send(b"LRC")
    time.sleep(1)
    c.send(lrc.LRC.generate_lrc(chunks).encode('utf-8'))
elif method == "Checksum":
    c.send(b"Checksum")
    time.sleep(1)
    c.send(checksum.Checksum.generate_checksum(chunks).encode('utf-8'))
else:
    print("No such method!")
    c.close()
    exit(1)
for i in chunks:
    time.sleep(1)
    if res == 'y' or res == 'Y':
        j = inject_error(i, random.randint(0, 2))
        c.send(j.encode('utf-8'))
    else:
        c.send(i.encode('utf-8'))

c.send(b'EOF')
print("Sending data", enc_text)
print(chunks)
print(c.recv(1024).decode('utf-8'))
