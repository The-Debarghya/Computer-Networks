#!/usr/bin/env python3
import threading
import multiprocessing
from sender import Sender
from receiver import Receiver
from channel import Channel
import walshCode

def simulate_environment(wTable, senderCount):
    writeRecvFd = [] #channel to receiver
    readRecvFd = [] #channel to receiver
    for _ in range(senderCount):
        readhead, writehead = multiprocessing.Pipe()
        readRecvFd.append(readhead) # file descriptor taken by receiver
        writeRecvFd.append(writehead) # file descriptor taken by channel
    readSendFd, writeSendFd = multiprocessing.Pipe() # sender to channel
    senderObjList = []
    receiverObjList = []
    senderThreads = []
    receiverThreads = []
    channel = Channel(senderCount, 0, readSendFd, writeRecvFd)

    for i in range(senderCount):
        sender = Sender(i, wTable[i], writeSendFd)
        senderObjList.append(sender)
        receiver = Receiver(i, wTable[i], readRecvFd[i])
        receiverObjList.append(receiver)
    channelThread = threading.Thread(target=channel.relayThread)
    for i in range(senderCount):
        sthread = threading.Thread(name="sender_thread" + str(i+1), target=senderObjList[i].send_data)
        senderThreads.append(sthread)
        rthread = threading.Thread(name="receiver_thread" + str(i+1), target=receiverObjList[i].receive_data)
        receiverThreads.append(rthread)
    channelThread.start()
    for thread in receiverThreads:
        thread.start()
    for thread in senderThreads:
        thread.start()
    for thread in senderThreads:
        thread.join()
    for thread in receiverThreads:
        thread.join()
    channelThread.join()

if __name__ == "__main__":
    senderCount = int(input("Enter number of senders:"))
    wTable = walshCode.getWalshTable(senderCount)
    with open('logs/log.txt', 'a+', encoding='utf-8') as fd:
        fd.write(f"\n\n----------------------------------------------------------\n Walsh Table For {senderCount} Station environment:{wTable} \
                  \n\n----------------------------------------------------------\n")
    fd.close()
    simulate_environment(wTable, senderCount)