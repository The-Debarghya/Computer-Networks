#!/usr/bin/env python3

import time
import PacketManager
import threading

WINDOW_SIZE = 8
MAX_SEQUENCE_NUMBER = 16


class Receiver:
    def __init__(self, connection, name: str, senderAddress: int, receiverAddress: int, file: str):
        self.connection = connection
        self.name = name
        self.file_name = file
        self.senderAddress = senderAddress
        self.receiverAddress = receiverAddress
        self.packetType = {'data': 0, 'ack': 1, 'nak': 2}
        self.front = 0
        self.end = WINDOW_SIZE
        self.window = []
        self.filled_up = []
        for index in range(0, MAX_SEQUENCE_NUMBER):
            self.window.append(0)
            self.filled_up.append(False)
        self.NAK_sent = False
        self.ACK_needed = False
        self.recentACK = PacketManager.Packet(
            self.senderAddress, self.receiverAddress, 1, 0, "Acknowledgement Packet")
        self.endReceiving = False
        self.lastACKsent = 'not started'

    def validSEQ(self, seq_no: int):
        if((self.front <= seq_no and seq_no < self.end) or (self.end < self.front and self.front <= seq_no) or (seq_no < self.end and self.end < self.front)):
            return True
        else:
            return False

    def sendAck(self):
        packet = PacketManager.Packet(self.senderAddress, self.receiverAddress,
                                      self.packetType['ack'], self.front, 'acknowledgement Packet')
        self.recentACK = packet
        print('Sent ACK no = ', self.front)
        self.connection.send(str.encode(packet.toBinaryString(22)))
        self.lastACKsent = time.time()

    def sendNak(self):
        packet = PacketManager.Packet(
            self.senderAddress, self.receiverAddress, self.packetType['nak'], self.front, 'No acknowledgement')
        self.connection.send(str.encode(packet.toBinaryString(22)))
        print('Sent NAK no = ', self.front)

    def resendPreviousACK(self):
        while(not self.endReceiving):
            if(self.lastACKsent == 'not started'):
                continue
            current_time = time.time()
            total_spent = (current_time - self.lastACKsent)
            if(total_spent > 1):
                self.connection.send(str.encode(
                    self.recentACK.toBinaryString(22)))
                self.lastACKsent = time.time()

    def startReceiving(self):
        time.sleep(0.4)
        ACKresendingThread = threading.Thread(target=self.resendPreviousACK)
        ACKresendingThread.start()
        data = self.connection.recv(576).decode()
        total_data = ''
        while data != 'end':
            packet = PacketManager.Packet.build(data)
            print("\nPacket Reached")
            if not packet.hasError():
                print("NO ERRORS FOUND")
                seqNo = packet.getSeqNo()
                if(seqNo != self.front and self.NAK_sent is False):
                    self.sendNak()
                    self.NAK_sent = True
                if(self.validSEQ(seqNo) and self.filled_up[seqNo] is False):
                    self.filled_up[seqNo] = True
                    self.window[seqNo] = packet.getData()
                    # print(packet.getData())
                    while(self.filled_up[self.front] is True):
                        total_data += self.window[self.front]
                        self.filled_up[self.front] = False
                        self.front = (self.front + 1) % MAX_SEQUENCE_NUMBER
                        self.end = (self.end + 1) % MAX_SEQUENCE_NUMBER
                        self.ACK_needed = True
                        print('PACKET RECEIVED SUCCESSFULLY')
                    if(self.ACK_needed):
                        self.sendAck()
                        self.ACK_needed = False
                        self.NAK_sent = False
            else:
                print("Packet Dropped")
            data = self.connection.recv(576).decode()
        self.endReceiving = True
        ACKresendingThread.join()
        file = open(self.file_name, 'a')
        file.write(total_data)
        file.close()
