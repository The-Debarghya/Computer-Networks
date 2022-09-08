#!/usr/bin/env python3

import time
import PacketManager


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
            senderAddress, receiverAddress, 1, 0, "Acknowledgement Packet")

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
            print("\nPacket Received")
            if not packet.hasError():
                print("NO ERROR FOUND")
                seqNo = packet.getSeqNo()
                if self.seqNo == seqNo:
                    data = packet.getData()
                    total_data += data
                    self.seqNo = (self.seqNo+1) % 2
                    self.sendAck()
                    print("ACK Sent By Receiver\n")
                else:
                    self.resendPreviousACK()
                    print("ACK Resent")
            else:
                print("Packet Dropped")

            data = self.connection.recv(576).decode()

        file = open(self.file_name, 'a')
        file.write(total_data)
        file.close()
