#!/usr/bin/env python3
import validate
from Crypto.Util.number import long_to_bytes

class Packet:
    def __init__(self, _type, seq, segment_data, src, dest) -> None:
        self.type = _type
        self.seq = seq
        self.segment_data = segment_data
        self.src = src
        self.dest = dest
        self.packet = ''

    def generate_packet(self):
        preamble = '01'*28
        sfd = '10101011'
        src_addr = '{0:048b}'.format(int(self.src))
        dest_addr = '{0:048b}'.format(int(self.dest))
        seqbits = '{0:08b}'.format(self.seq)
        length = '{0:08b}'.format(len(self.segment_data))
        data = ''
        for i in range(len(self.segment_data)):
            character = self.segment_data[i]
            data += '{0:08b}'.format(ord(character))
        packet = preamble + sfd + dest_addr + src_addr + seqbits + length + data
        checksum = validate.get_checksum(packet)
        packet += checksum
        self.packet = packet
        return self

    def __str__(self) -> str:
        return str(self.packet)

    def get_datalen(self) -> int:
        return len(self.segment_data)

    def get_type(self) -> int:
        return self.type

    def get_seqno(self) -> int:
        seqbits = self.packet[160:168]
        return int(seqbits, 2)

    def get_src(self) -> int:
        return int(self.packet[112:160], 2)

    def get_dest(self) -> int:
        return int(self.packet[64:112], 2)

    def get_data(self) -> str:
        datastr = ""
        databits = self.packet[176:544]
        datastr = long_to_bytes(int(databits, 2)).decode('utf-8')
        return datastr

    def validate_packet(self) -> bool:
        return validate.validate_checksum(self.packet)
