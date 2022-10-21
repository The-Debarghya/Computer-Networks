#!/usr/bin/env pytgon3
import sys
import threading
import multiprocessing
from sender import Sender
from receiver import Receiver
from channel import Channel

def simulate_environment(method: int, senderCount: int):
    writeFdChannelToSender = []
    readFdChannelToSender = []

    writeFdChannelToReceiver = []
    readFdChannelToReceiver = []

    readFdReceiverToChannel = []

    for _ in range(senderCount):
        readFd, writeFd = multiprocessing.Pipe()
        readFdChannelToSender.append(readFd) # taken by sender
        writeFdChannelToSender.append(writeFd) # taken by channel
    
    for _ in range(senderCount):
        readFd, writeFd = multiprocessing.Pipe()
        readFdChannelToReceiver.append(readFd) # taken by sender
        writeFdChannelToReceiver.append(writeFd) # taken by channel
    
    readFdSenderToChannel, writeFdSenderToChannel = multiprocessing.Pipe()
    senderList = []
    receiverList = []
    senderThreads = []
    receiverThreads = []

    channelObj = Channel(senderCount, readFdSenderToChannel, writeFdChannelToSender, readFdReceiverToChannel, writeFdChannelToReceiver)
    for i in range(senderCount):
        sender = Sender(i, "logs/input/input"+str(i+1)+".txt", writeFdSenderToChannel, readFdChannelToSender[i], method, senderCount)
        senderList.append(sender)
        receiver = Receiver(i, readFdChannelToReceiver[i])
        receiverList.append(receiver)
    
    channel_thread = threading.Thread(target=channelObj.init_channel)
    for i in range(senderCount):
        sthread = threading.Thread(target=senderList[i].init_sender)
        senderThreads.append(sthread)
        rthread = threading.Thread(target=receiverList[i].init_receiver)
        receiverThreads.append(rthread)

    channel_thread.start()
    for thread in receiverThreads:
        thread.start()
    for thread in senderThreads:
        thread.start()
    for thread in senderThreads:
        thread.join()
    for thread in receiverThreads:
        thread.join()
    channel_thread.join()

if __name__ == "__main__":
    method = int(input("1.One Persistent\n2.Non Persistent\n3.p-Persistent\nEnter choice of CSMA method:"))
    if method == 1:
        choice = "One"
    elif method == 2:
        choice = "Non"
    elif method == 3:
        choice = "p"
    else:
        print("Choose properly!")
        sys.exit(1)
    senderCount = int(input("Number of senders:"))
    with open('logs/log.txt', 'a+', encoding='utf-8') as fp: 
        fp.write("\n\n+------------------------------------------------------------+\n\n" + \
            f"\tLogs For the CSMA Method:{choice}-persistent, Sender Count:{senderCount}\n"+ \
                "\n+------------------------------------------------------------+\n\n")
    with open('logs/analysis.txt', 'a+', encoding='utf-8') as fp: 
        fp.write("\n\n+------------------------------------------------------------+\n\n" + \
            f"\tStats For the CSMA Method:{choice}-persistent, Sender Count:{senderCount}\n"+ \
                "\n+------------------------------------------------------------+\n\n")
    simulate_environment(method, senderCount)

