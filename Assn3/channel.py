#!/usr/bin/env python3
import time
import threading
import datetime

channel_propagation_delay = 0.8

class Channel:
    def __init__(self, sendercnt: int, senderToChannel, channelToSender: list, receiverToChannel: list, channelToReceiver: list) -> None:
        self.active = False
        self.sendercnt = sendercnt 
        self.senderToChannel = senderToChannel
        self.channelToSender = channelToSender
        self.receiverToChannel = receiverToChannel
        self.channelToReceiver = channelToReceiver

    def transfer_data_pkts(self):
        '''Sending data packets from Sender to Receiver through the channel'''
        while True:
            packet = self.senderToChannel.recv()
            self.active = True
            time.sleep(channel_propagation_delay)
            self.active = False
            dest = packet.get_dest()
            self.channelToReceiver[dest].send(packet)

    def transfer_response(self, sender: int):
        while True:
            if self.active:
                self.channelToSender[sender].send(str(1)) #denoting channel busy
            else:
                self.channelToSender[sender].send(str(0)) #denoting channel idle

    def init_channel(self):
        curr_time = datetime.datetime.now()
        with open("logs/log.txt", "a+") as f:
            f.write(f"\n[{curr_time.strftime('%d/%m/%Y %H:%M:%S')}] Channel initialized.\n")
        channelToReceiverThreads = []
        channelToSenderThreads = []
        sender = 0
        dataThread = threading.Thread(name="DataThread-"+str(sender+1), target=self.transfer_data_pkts)
        channelToReceiverThreads.append(dataThread)
        for _ in range(self.sendercnt):
            respThread = threading.Thread(name="RespThread-"+str(sender+1), target=self.transfer_response, args=(sender,))
            channelToSenderThreads.append(respThread)
            sender += 1

        for thread in channelToReceiverThreads:
            thread.start()
        for thread in channelToSenderThreads:
            thread.start()
        for thread in channelToReceiverThreads:
            thread.join()
        for thread in channelToSenderThreads:
            thread.join()
