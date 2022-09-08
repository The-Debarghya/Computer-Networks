#!/usr/bin/env python3

import time
import PacketManager

WINDOW_SIZE = 8


class Receiver:
    def __init__(self, connection, name: str, senderAddress: int, receiverAddress: int, file: str):
        self.connection = connection
        self.name = name
        self.file_name = file
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.packetType = {'data': 0, 'ack': 1}
        self.seqNo = 0
        self.recentACK = PacketManager.Packet(
            self.senderAddress, self.receiverAddress, 1, 0, "Acknowledgement Packet")

    def sendAck(self):
        packet = PacketManager.Packet(self.senderAddress, self.receiverAddress,
                                      self.packetType['ack'], self.seqNo, 'acknowledgement Packet')
        self.recentACK = packet
        self.connection.send(str.encode(packet.toBinaryString(22)))

    def resendPreviousACK(self):
        self.connection.send(str.encode(self.recentACK.toBinaryString(22)))

    def startReceiving(self):
        time.sleep(0.4)
        data = self.connection.recv(576).decode()
        total_data = ''
        while data != 'end':
            packet = PacketManager.Packet.build(data)
            print("\nPACKET RECEIVED")
            if not packet.hasError():
                print("No Error Found")
                seqNo = packet.getSeqNo()
                if self.seqNo == seqNo:
                    data = packet.getData()
                    print(data)
                    total_data += data
                    self.seqNo = ((self.seqNo+1) % WINDOW_SIZE)
                    self.sendAck()
                    print("ACK Sent From Receiver\n")
                else:
                    self.resendPreviousACK()
                    print("ACK Resent")
            else:
                print("Packet Dropped")
            data = self.connection.recv(576).decode()
        file = open(self.file_name, 'a')
        file.write(total_data)
        file.close()
