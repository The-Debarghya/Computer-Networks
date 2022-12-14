#!/usr/bin/env python3
import threading
from datetime import datetime
import walshCode

class Channel:
    def __init__(self, senderCount, name, senderToChannel, channelToReceiver) -> None:
        self.name = name
        self.senderCount = senderCount
        self.senderToChannel = senderToChannel
        self.channelToReceiver = channelToReceiver
        self.channelData = [0 for _ in range(walshCode.nextPowerOf2(senderCount))]
        self.syncVal = 0

    def relayThread(self):
        while True:
            num = walshCode.nextPowerOf2(self.senderCount)
            for _ in range(self.senderCount):
                data = self.senderToChannel.recv()
                curr_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                with open('logs/log.txt', 'a+', encoding='utf-8') as f:
                    f.write(f"\n[{curr_datetime}] CHANNEL Passed {data}")
                for j in range(num):
                    #print(self.channelData, data, i, j)
                    self.channelData[j] += data[j]
                self.syncVal += 1
                if self.syncVal == self.senderCount:
                    for receiver in range(self.senderCount): # receiverCount = senderCount
                        self.channelToReceiver[receiver].send(self.channelData)
                    self.syncVal = 0
                    self.channelData = [0 for _ in range(walshCode.nextPowerOf2(self.senderCount))]
    
    def initChannel(self):
        channelThread = threading.Thread("channel_thread", target=self.relayThread)
        channelThread.start()
        channelThread.join()