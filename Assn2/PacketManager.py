#!/usr/bin/env python3

import ErrorDetectingSchemes

divisor = '100000100110000010001110110110111'


class Packet:
    def __init__(self, source: int, destination: int, _type: int, seqNo: int, segmentData: str):
        self.source = source
        self.destination = destination
        self.type = _type
        self.segmentData = segmentData
        self.seqNo = seqNo

    def toBinaryString(self, data_size: int):
        preamble = '01'*28
        sfd = '10101011'
        destAddress = '{0:048b}'.format(self.destination)
        sourceAddress = '{0:048b}'.format(self.source)
        typeToBits = '{0:08b}'.format(self.type)
        seqToBits = '{0:08b}'.format(self.seqNo)
        segmentData = self.segmentData
        if(len(segmentData) < data_size):
            segmentData += '\0'*(data_size-len(segmentData))
        data = ""
        for i in range(0, len(segmentData)):
            character = segmentData[i]
            dataByte = '{0:08b}'.format(ord(character))
            data = data + dataByte
        packet = preamble + sfd + destAddress + \
            sourceAddress + typeToBits + seqToBits + data
        packet = ErrorDetectingSchemes.CRC.generateCRC(packet, divisor)
        self.packet = packet
        return packet

    @classmethod
    def build(cls, packet):
        source = int(packet[64:112], 2)
        destination = int(packet[112:160], 2)
        _type = int(packet[160:168], 2)
        seq_no = int(packet[168:176], 2)
        text = ""
        data = packet[176:-32]
        asciiData = [data[i:i+8] for i in range(0, len(data), 8)]
        for letter in asciiData:
            if(letter == '00000000'):
                continue
            text += chr(int(letter, 2))
        new_packet = cls(source, destination, _type, seq_no, text)
        new_packet.packet = packet
        return new_packet

    def getData(self):
        return self.segmentData

    def getType(self):
        return self.type

    def getSeqNo(self):
        return self.seqNo

    def hasError(self):
        return ErrorDetectingSchemes.CRC.checkCRC(self.packet, divisor)
