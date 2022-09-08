#!/usr/bin/env python3

bandwidth = 4000


def generateReport(senderName, receiverName, analysis_file_name, effectivePkt, totalPkt, totalTime, rttStore: list):
    file = open(analysis_file_name, 'a')
    successfullTransmissionTime = (totalTime/effectivePkt)
    file.writelines("\n"+senderName+' is sending data to '
                    + receiverName+"--------------------\n")
    file.writelines('Total packet sent = {}\n'.format(totalPkt))
    file.writelines('Effective packet sent = {}\n'.format(effectivePkt))
    file.writelines(
        'Total time taken = {:6.6f} minutes\n'.format((totalTime/60)))
    throughput = (effectivePkt*72*8)/totalTime
    file.writelines(
        'Receiver Throughput = {:6d} bps\n'.format(int(throughput)))
    efficiency = (throughput/bandwidth)
    file.writelines(
        'Utilization percentage = {:6.2f} %\n'.format((efficiency*100)))
    file.writelines(
        'Average Successful Transmission time of a packet = {:6.6f} seconds/packet\n'.format(successfullTransmissionTime))
    file.writelines("\n")
    file.close()
