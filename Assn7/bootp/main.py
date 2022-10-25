#!/usr/bin/env python3

import argparse, socket
import random
from time import time
BUFSIZE = 65535

def nextPowerOf2(num: int):
    n = 1
    power = 0
    while(n < num):
        n *= 2
        power += 1
    return power


def calculateSubnetMaskv4(n: int) -> str:
    x = nextPowerOf2(n)
    mask = "1"*(32-x) + "0"*x
    subnet = [str(int(mask[i:i+8], 2)) for i in range(0, 32, 8)]
    return ".".join(subnet)


def server(interface, port, ndevices):
    taken_ips = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    #print(f"Current subnet mask is (for {ndevices}):", calculateSubnetMaskv4(ndevices))
    print(f"Listening for requests at {sock.getsockname()}")
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print(f"The client at ('255.255.255.255', {address[1]}) is: {text}")
        s = text.split(":")[1]
        if s in taken_ips:
            sock.sendto(b"Declined Request", address)
            print("Declined Request")
        else:
            taken_ips.append(s)
            sock.sendto(f"{s},{calculateSubnetMaskv4(ndevices)},{interface}".encode("ascii"), address)


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("192.168.101.6", 40400)
    sock.bind(addr)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    text = f"Requesting for IP, subnet mask, default gateway, previous IP:{addr[0]}"
    s = network.split(".")
    netw_list = [".".join(s[:3])+"."+str(int(i)) for i in range(256)]
    print("Requested for private IP, subnet-mask, gateway")
    for netw in netw_list:
        try:
            sock.sendto(text.encode("ascii"), (netw, port))
        except Exception:
            pass
    prev = addr[0]
    while True:
        random.seed(time())
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        if "Declined" in text:
            print(text)
            print("Requesting again...")
            l = prev.split(".")
            new = ".".join(l[:3]) + "." + str(random.randint(1, 254))
            prev = new
            sock.sendto(f"Requesting for IP:{new}".encode('ascii'), address)
        else:
            print("Reply from BOOTP server:")
            addrs = text.split(",")
            print(f"Assigned IP: {addrs[0]}")
            print(f"Subnet Mask of network: {addrs[1]}")
            print(f"Default gateway: {address[0]}")
            sock.close()
            break


if __name__ == "__main__":
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;' ' network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='UDP port (default 1060)')
    parser.add_argument('-n', metavar='ndevices', type=int, default=256, help="Number of devices in current network(Max supported=254)")
    args = parser.parse_args()
    function = choices[args.role]
    if function == client:
        function(args.host, args.p)
    else:
        function(args.host, args.p, args.n)
