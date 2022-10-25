#!/usr/bin/env python3

import argparse, socket
BUFSIZE = 65535

def server(interface, port):
    #taken_ips = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    #print(f"Current subnet mask is (for {ndevices}):", calculateSubnetMaskv4(ndevices))
    print(f"Listening for requests at {sock.getsockname()}")
    while True:
        data, address = sock.recvfrom(BUFSIZE)
        text = data.decode('ascii')
        print(f"The client at {address} is: {text}")


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = ("192.168.101.6", 40400)
    sock.bind(addr)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 0)
    text = f"Requesting for IP, subnet mask, default gateway, previous IP:{addr[0]}"
    sock.sendto(text.encode("ascii"), (network, port))
    

if __name__ == "__main__":
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send, receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;' ' network the client sends to')
    parser.add_argument('-p', metavar='port', type=int, default=1060, help='UDP port (default 1060)')
    #parser.add_argument('-n', metavar='ndevices', type=int, default=256, help="Number of devices in current network(Max supported=256)")
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
