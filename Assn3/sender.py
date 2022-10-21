#!/usr/bin/env python3
import sys
import time
import random
import threading
from packetManager import Packet
import datetime


class Sender:
    def __init__(self, id: int, filename: str, senderToChannel, channelToSender, method: int, senderCount:int) -> None:
        self.start = 0
        self.seq = 0
        self.packetCount = 0
        self.collisionCount = 0
        self.senderCount = senderCount
        self.busy = False
        self.id = id
        self.filename = filename
        self.senderToChannel = senderToChannel
        self.channelToSender = channelToSender
        self.method = method
        self.packet_type = {'data': 0, 'ack': 1}
        self.dest = self.id

    def read_file(self, filename: str):
        try:
            fd = open(filename, "r", encoding='utf-8')
        except FileNotFoundError as err:
            current_time = datetime.datetime.now()
            print(f"\n [{current_time.strftime('%d/%m/%Y %H:%M:%S')}] ERROR: {err} File {filename} not found!")
            sys.exit(f"File {filename} Not Found!")
        return fd

    def one_persistent(self, packet):
        while True:
            if not self.busy:
                f = self.read_file("./logs/collide.txt")
                collision = f.read()
                f.close()
                if collision == '1':
                    self.collisionCount += 1
                    current_time = datetime.datetime.now()
                    with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                        fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} encounters COLLISION.")
                    time.sleep(0.1) # wait after collision
                else:
                    current_time = datetime.datetime.now()
                    with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                        fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} sent Packet {self.packetCount+1} to Channel\n")
                    f = open('logs/collide.txt', "w", encoding='utf-8')
                    f.write(str(1))
                    f.close()
                    time.sleep(0.1) # vulnerable time
                    f = open('logs/collide.txt', "w",  encoding='utf-8')
                    f.write(str(0))
                    f.close()
                    self.senderToChannel.send(packet) 
                    time.sleep(1) # propagation time
                    break
            else:
                current_time = datetime.datetime.now()
                with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                    fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} finds Channel is BUSY.")
                time.sleep(0.5)
                continue

    def non_persistent(self, packet):
        while True:
            if not self.busy:
                f = self.read_file("./logs/collide.txt")
                collision = f.read()
                f.close()
                if collision == '1':
                    self.collisionCount += 1
                    current_time = datetime.datetime.now()
                    with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                        fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} encounters COLLISION.")
                    time.sleep(0.1) # wait after collision
                else:
                    current_time = datetime.datetime.now()
                    with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                        fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} sent Packet {self.packetCount+1} to Channel\n")
                    f = open('logs/collide.txt', "w", encoding='utf-8')
                    f.write(str(1))
                    f.close()
                    time.sleep(0.1) # vulnerable time
                    f = open('logs/collide.txt', "w",  encoding='utf-8')
                    f.write(str(0))
                    f.close()
                    self.senderToChannel.send(packet) 
                    time.sleep(1) # propagation time
                    break
            else:
                random.seed(time.time())
                current_time = datetime.datetime.now()
                with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                    fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} finds Channel is BUSY.")
                time.sleep(random.randint(1, 5))
                continue

    def p_persistent(self, packet):
        while True:
            if not self.busy:
                x = random.random()
                p = 1/self.senderCount
                if x <= p:
                    f = self.read_file("./logs/collide.txt")
                    collision = f.read()
                    f.close()
                    if collision == '1':
                        self.collisionCount += 1
                        current_time = datetime.datetime.now()
                        with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                            fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} encounters COLLISION.")
                        time.sleep(0.1) # wait after collision
                    else:
                        current_time = datetime.datetime.now()
                        with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                            fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} sent Packet {self.packetCount+1} to Channel\n")
                        f = open('logs/collide.txt', "w", encoding='utf-8')
                        f.write(str(1))
                        f.close()
                        time.sleep(0.1) # vulnerable time
                        f = open('logs/collide.txt', "w",  encoding='utf-8')
                        f.write(str(0))
                        f.close()
                        self.senderToChannel.send(packet) 
                        time.sleep(1) # propagation time
                        break
                else:
                    current_time = datetime.datetime.now()
                    with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                        fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} is WAITING, wait period:0.25secs.\n")
                    time.sleep(0.25) # wait a certain time
            else:
                current_time = datetime.datetime.now()
                with open("logs/log.txt", "a+", encoding="utf-8") as fp:
                    fp.write(f"[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} finds Channel is BUSY.")
                time.sleep(0.5)
                continue

    def carrier_sense(self):
        while True:
            if self.channelToSender.recv() == '1':
                self.busy = True
            else:
                self.busy = False

    def transfer_data(self):
        current_time = datetime.datetime.now()
        with open("logs/log.txt", "a+", encoding="utf-8") as fp:
            fp.write(f"\n[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} Starts sending to Receiver {self.dest+1}.\n")
        self.start = time.time()
        fd = self.read_file(self.filename)
        data = fd.read(46)
        self.seq = 0
        while data:
            packet = Packet(self.packet_type['data'], self.seq, data, self.id, self.dest).generate_packet()
            if self.method == 1:
                self.one_persistent(packet)
            elif self.method == 2:
                self.non_persistent(packet)
            else:
                self.p_persistent(packet)
            self.packetCount += 1
            data = fd.read(46)
            if len(data) == 0:
                break
            if len(data) < 46:
                l = len(data)
                for _ in range(46-l): data += ' '
        fd.close()
        current_time = datetime.datetime.now()
        with open("logs/log.txt", "a+", encoding="utf-8") as fp:
            fp.write(f"\n\n**********[{current_time.strftime('%d/%m/%Y %H:%M:%S')}] Sender {self.id+1} FINISHES sending data*********\n\n")
        with open('logs/analysis.txt', 'a+', encoding='utf-8') as fp:
            fp.write(f"\n\n+---------- {current_time} SENDER-{self.id+1} STATS ----------+" + '\n' + \
                            "[*]\tTotal packets: {}".format(self.packetCount) + '\n' + \
                            "[*]\tTotal Delay: {} secs".format(round(time.time() - self.start, 2)) + '\n' + \
                            "[*]\tTotal collisions: {}".format(self.collisionCount) + '\n' + \
                            "[*]\tThroughput: {}".format(round(self.packetCount/(self.packetCount + self.collisionCount), 3)) + '\n' + \
                            "+------------------------------------------------------+\n\n")
        
    def init_sender(self):
        sender_thread = threading.Thread(name="sender_thread", target=self.transfer_data)
        sensing_thread = threading.Thread(name="sensing_thread", target=self.carrier_sense)
        sender_thread.start()
        sensing_thread.start()
        sender_thread.join()
        sensing_thread.join()
                    
