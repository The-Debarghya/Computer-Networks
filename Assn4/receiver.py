#!/usr/bin/env python3
import threading
import sys
from datetime import datetime

class Receiver:
    def __init__(self, name, wTable, channelToReceiver) -> None:
        self.name = name
        self.wTable = wTable
        self.channelToReceiver = channelToReceiver
        self.codeLength = len(wTable)
        self.senderToReceiver = name

    def getByte(self, dataBits):
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/log.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n[{curr_datetime}] Data : {str(dataBits)}")
        sum = 0
        for i in range(8): 
            sum += pow(2,i) * dataBits[7-i]
        byte = chr(sum)
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/log.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n[{curr_datetime}] Char Received: {byte}\n")
        return byte

    def read_file(self, sender):
        try:
            filename = "./logs/output/" + 'output' + str(sender+1) + '.txt'
            fd = open(filename, 'a+', encoding='utf-8')
        except FileNotFoundError as err:
            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{curr_datetime}] EXCEPTION AT: {str(err)}")
            sys.exit(f"No file exists with name {filename}!")
        return fd

    def receive_data(self):
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/log.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n[{curr_datetime}] RECEIVER-{self.name+1} Receives Data from SENDER-{self.senderToReceiver+1}")
        entiredata = []
        while True:
            channeldata = self.channelToReceiver.recv()
            sum = 0
            for i in range(len(channeldata)):
                sum += channeldata[i] * self.wTable[i]
            sum /= self.codeLength
            if sum == 1:
                bit = 1
            elif sum == -1:
                bit = 0
            else:
                bit = -1
            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open('logs/log.txt', 'a+', encoding='utf-8') as f:
                f.write(f"\n[{curr_datetime}] RECEIVER-{self.name+1} Bit Received: {bit}")

            if len(entiredata) < 8 and bit != -1: 
                entiredata.append(bit)

            if len(entiredata) == 8:
                byte = self.getByte(entiredata)
                output_file = self.read_file(self.senderToReceiver)
                output_file.write(byte)
                output_file.close()
                entiredata = []

    def initReceiver(self):
        receiver_thread = threading.Thread("receiver_thread" + str(self.name+1), target=self.receive_data)
        receiver_thread.start()
        receiver_thread.join()