#!/usr/bin/env python3
import threading
import sys 
import time
from datetime import datetime

class Sender:
    def __init__(self, name, walshCode, senderToChannel) -> None:
        self.name = name 
        self.walshCode = walshCode
        self.senderToChannel = senderToChannel
        self.start = 0
        self.bitcount = 0
        self.delay = 0

    def read_file(self, sender):
        try:
            filename = "./logs/input/" + 'input' + str(sender+1) + '.txt'
            fd = open(filename, 'r', encoding='utf-8')
        except FileNotFoundError as err:
            curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{curr_datetime}] EXCEPTION AT: {err}")
            sys.exit(f"File with name {filename} is not found!")
        return fd

    def send_data(self):
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/log.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n[{curr_datetime}] SENDER-{self.name+1} Started Sending To RECEIVER-{self.name+1}")
        self.start = time.time()
        file = self.read_file(self.name)
        dataByte = file.read(1)
        while dataByte:
            dataBits = '{0:08b}'.format(ord(dataByte))
            for i in range(len(dataBits)):
                dataToSend = []
                bit = int(dataBits[i])
                if bit == 0:
                    bit = -1
                for j in self.walshCode:
                    dataToSend.append(j*bit)
                self.senderToChannel.send(dataToSend)
                self.bitcount += 1
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                with open('logs/log.txt', 'a+', encoding='utf-8') as f:
                    f.write(f"\n[{curr_datetime}] SENDER-{self.name+1} Data Bit Sent {bit}")
                time.sleep(0.3)
            dataByte = file.read(1)
            self.delay = round((time.time()-self.start), 2)
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/analysis.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n\n+--------- {curr_datetime} SENDER-{self.name+1} Statistics ---------+\n" + \
                            f"[+] Total Bits Transferred: {self.bitcount}\n" + \
                            f"[+] Total Time Taken: {self.delay} seconds\n" + \
                            f"[+] Throughput: {round(self.bitcount/self.delay, 3)} bps\n" + \
                            "+" + "-"*54 + '+\n\n\n')
        curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open('logs/log.txt', 'a+', encoding='utf-8') as f:
            f.write(f"\n[{curr_datetime}] SENDER-{self.name+1} Ended Sending Data")

    def initSender(self):
        sender_thread = threading.Thread(name="sender_thread" + str(self.name+1), target=self.send_data)
        sender_thread.start()
        sender_thread.join()