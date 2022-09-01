#!/usr/bin/env python3
import crc

divisor = '100000100110000010001110110110111'


class Packet:
    def __init__(self, src: list, dest: list, _type: int, seqNo: int, segmentData: str):
        self.src = src
        self.dest = dest
        self.type = _type
        self.segmentData = segmentData
        self.seqNo = seqNo

    def toBinaryString(self, data_size: int):
        preamble = '01'*28
        sfd = '10101011'

        destAddress = ''.join(['{0:08b}'.format(int(i)) for i in self.dest[0].split(
            '.')]) + '{0:016b}'.format(self.dest[1])
        srcAddress = ''.join(['{0:08b}'.format(int(i)) for i in self.src[0].split(
            '.')]) + '{0:016b}'.format(self.src[1])

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
            srcAddress + typeToBits + seqToBits + data

        packet = crc.CRC.encodeData(packet, divisor)
        self.packet = packet

        return packet

    @classmethod
    def build(cls, packet):

        shost = [packet[64:96][i:i+8] for i in range(0, 32, 8)]
        shost = '.'.join([str(int(i, 2)) for i in shost])
        source = [shost, int(packet[96:112], 2)]
        dhost = [packet[112:144][i:i+8] for i in range(0, 32, 8)]
        dhost = '.'.join([str(int(i, 2)) for i in dhost])
        destination = [dhost, int(packet[144:160], 2)]

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
        return crc.CRC.checkRemainder(self.packet, divisor)
