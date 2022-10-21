#!/usr/bin/env python3
import time
import threading
import datetime

channel_propagation_delay = 0.8

class Channel:
    def __init__(self, senderToChannel, channelToSender: list, receiverToChannel: list, channelToReceiver: list) -> None:
        self.active = False
        self.current_time = datetime.datetime.now()
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
