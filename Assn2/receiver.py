#!/usr/bin/env python3

import socket
import select
import SenderSW
import ReceiverSW
import SenderGBN
import ReceiverGBN
import SenderSR
import ReceiverSR


senderList = [SenderSW, SenderGBN, SenderSR]
receiverList = [ReceiverSW, ReceiverGBN, ReceiverSR]


def my_receiver():
    print('Select Protocol-----')
    print('1.Stop and wait\n2.Go back N\n2.Selective repeat\n')
    protocol = int(input('Enter choice: '))
    if(protocol > 3 or protocol < 1):
        protocol = 1
    protocol -= 1
    HOST = '127.0.0.1'
    PORT = 9999
    with socket.socket() as client:
        client.connect((HOST, PORT))
        msg = client.recv(1024).decode()
        print(msg, end='')
        name = input()
        client.sendall(bytes(name, 'UTF-8'))
        address = client.recv(1024).decode()
        senderAddress = int(address)
        while(True):
            print('Input options-----\n1.Receive data\n2.Close\n')
            choice = int(input('Enter option : '))
            if(choice != 1):
                client.send(str.encode("close"))
                break
            inputs = [client]
            output = []
            readable, writable, exceptionals = select.select(
                inputs, output, inputs, 3600)
            for s in readable:
                data = s.recv(1024).decode()
                if(data == "No client is available"):
                    print(data)
                    break
                elif(choice == 1):
                    print('Receiving data-----')
                    file_name = ''
                    if protocol == 0:
                        file_name = 'StopWait_rec.txt'
                    elif protocol == 1:
                        file_name = 'GoBack_rec.txt'
                    else:
                        file_name = 'SelectiveRepeat_rec.txt'
                    receiverAddress = int(data)
                    s.send(bytes("start", 'utf-8'))
                    my_receiver = receiverList[protocol].Receiver(
                        client, name, senderAddress, receiverAddress, file_name)
                    my_receiver.startReceiving()
            if not (readable or writable or exceptionals):
                continue


if __name__ == '__main__':
    my_receiver()
