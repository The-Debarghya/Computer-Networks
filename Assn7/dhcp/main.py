#!/usr/bin/env python3

import argparse
import socket
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


def server(interface, port, ndevices, dns, timeout, gateway):
    taken_ips = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    #print(f"Current subnet mask is (for {ndevices}):", calculateSubnetMaskv4(ndevices))
    print(f"Listening for requests at {sock.getsockname()}")
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print(f"The client at ('0.0.0.0', {address[1]}) sent: {text}")
        if address[0] not in taken_ips:
            addr = address[0]
            taken_ips.append(address[0])
        else:
            random.seed(time())
            addr_blocks = address[0].split(".")
            addr = ".".join(addr_blocks[:3]) + "." + str(random.randint(1, 254))
            taken_ips.append(addr)
        print(f"Sent the following Offer:\nIP-{addr},\nGateway-{gateway},\
        \nSubnet Mask-{calculateSubnetMaskv4(ndevices)},\nDNS Server-{dns},\nTime To Live-{timeout} mins")
        config = f"{addr},{gateway},{calculateSubnetMaskv4(ndevices)},{dns},{timeout}".encode('ascii')
        sock.sendto(config, address)
        config, address = sock.recvfrom(BUFSIZE)
        print(f"Received request from:0.0.0.0, {address[1]}")
        sock.sendto("OK".encode('ascii'), address)



def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("172.28.1.211", 40400)
    sock.bind(addr)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    text = f"Discover request for IP, subnet mask, default gateway, DNS server, Timeout, previous IP:{addr[0]}"
    s = network.split(".")
    netw_list = [".".join(s[:3])+"."+str(int(i)) for i in range(256)]
    print("Broadcasted for private IP, subnet-mask, gateway(Discover)")
    for netw in netw_list:
        try:
            sock.sendto(text.encode("ascii"), (netw, port))
        except Exception:
            pass
    while True:
       config, address = sock.recvfrom(BUFSIZE)
       config_list = config.decode('ascii').split(",")
       print(f"Offer from server:IP-{config_list[0]},Default Gateway-{config_list[1]},Subnet Mask-{config_list[2]},DNS Server-{config_list[3]},Time To Live:{config_list[4]} mins")
       print("Request for the offer...")
       for netw in netw_list:
        try:
            sock.sendto(config, (netw, port))
        except Exception:
            pass
       
       resp, address = sock.recvfrom(BUFSIZE)
       if resp.decode('ascii') == 'OK':
        print(f"Reply from server:\nIP-{config_list[0]},\nDefault Gateway-{config_list[1]},\nSubnet Mask-{config_list[2]},\nDNS Server-{config_list[3]},\nTime To Live:{config_list[4]} mins")
       break
       
       #sock.close()


if __name__ == "__main__":
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument(
        'host', help='interface the server listens at;' ' network the client sends to')
    parser.add_argument('-p', metavar='port', type=int,
                        default=1060, help='UDP port (default 1060)')
    parser.add_argument('-n', metavar='ndevices', type=int, default=256,
                        help="Number of devices in current network(Max supported=254)")
    parser.add_argument('-dns', metavar='dns', type=str,
                        default='8.8.8.8', help="manually set the dns server")
    parser.add_argument('-t', metavar='time', type=int,
                        default=30, help="Set TimeOut for an IP")
    parser.add_argument('-gateway', metavar='gateway', type=str,
                        default='192.168.101.6', help='Manually set the default gateway')
    args = parser.parse_args()
    function = choices[args.role]
    if function == client:
        function(args.host, args.p)
    else:
        function(args.host, args.p, args.n, args.dns, args.t, args.gateway)
