#!/usr/bin/env python3
import sys
import datetime
from packetManager import Packet

class Receiver:
    def __init__(self, id: int, channelToReceiver) -> None:
        self.seq = 0 #must be synced with sender seq
        self.id = id
        self.sender_dict = {} # key value pair of sender_id:outfile_path
        self.channelToReceiver = channelToReceiver

    def write_file(self, filename: str):
        try:
            fd = open(filename, "a+")
        except FileNotFoundError as err:
            current_time = datetime.datetime.now()
            print(f"\n [{current_time.strftime('%d/%m/%Y %H:%M:%S')}] ERROR: {err} File {filename} not found!")
            sys.exit(f"File {filename} Not Found!")
        return fd

    def init_receiver(self):
        while True:
            packet = self.channelToReceiver.recv()
            sender = packet.get_src()
            if sender not in self.sender_dict.keys():
                self.sender_dict[sender] = "./logs/output/output" + str(sender+1) + '.txt'

            outfile = self.sender_dict[sender]
            fd = self.write_file(outfile)
            datastr = packet.get_data()
            fd.write(datastr)
            fd.close()
            current_time = datetime.datetime.now()
            with open("logs/log.txt", "a+") as f:
                f.write(f"\n[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Receiver-{self.id+1} received Packet SUCCESSFULLY!\n")