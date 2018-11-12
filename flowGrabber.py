import os
import csv

def getNumFlows():
    #i = 0
    flows = []
    flows.append([0])
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #i += 1
            #if i > 100:
            #    break
            if row[4] == 'UDP':
                inFlows = False
                source = row[2]
                destination = row[3]
                for flow in flows:
                    if source in flow and destination in flow:
                        flow[2] = flow[2] + 1
                        inFlows = True
                        break
                if not(inFlows):
                    flows[0][0] = flows[0][0] + 1
                    flows.append([source, destination, 1])

    print(flows)

def saveToCSV(data, directory = 'output', name = 'data.csv'):
    with open(os.path.join(os.path.dirname(__file__), directory + "/" + name),
            'w') as f:
        for row in data:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator = '\n')
            writer.writerows([row])

#Needs revision, forgot to account for ports!
def getFlowDuration():
    #i = 0
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        firstRun = True
        for row in csvReader:
            if firstRun:
                firstRun = False
                continue
            #i += 1
            #if i > 100:
            #    break
            #if row[4] == 'UDP': #Remove comment when trying to find specific
            if True:
                inFlows = False
                source = row[2]
                destination = row[3]
                for flow in flows:
                    if source in flow and destination in flow:
                        if row[1] > flow[3]:
                            flow[3] = row[1]
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([source, destination, row[1], row[1]])

    for flow in flows:
        start = flow[2]
        end = flow[3]
        del flow[-1]
        flow[2] = str(round(float(end) - float(start), 6))

    saveToCSV(flows)


# For TCP packets, in the addition to the total byte sum, calculate 
# the overhead ratio as the sum of all headers (including TCP, IP, and Ethernet) divided by the total 
# size of  the data  that is  transferred by  the  flow. If  the  flow did  not  transfer any data  (e.g.,  the 
# connection did not stablish successfully), use the number 9999 instead to represent infinity. Now 
# draw the CDF of hit ratio. What can you say about TCP overhead base on this chart?
def getSizeFlows():
    #i = 0
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #i += 1
            #if i > 100:
            #    break
            if row[4] == 'TCP':
                inFlows = False
                source = row[2]
                destination = row[3]
                for flow in flows:
                    if source in flow and destination in flow:
                        flow[2] = flow[2] + 1 #packet count
                        flow[3] = str(int(flow[3]) + int(row[5])) #length of packet
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([source, destination, 1, row[5]])
    saveToCSV(flows)

# Inter‐packet arrival  time: Calculate  the arrival  time between consecutive packets in each  flow. 
# Then draw the CDF of inter‐arrival time between packets for all flows, TCP flows, and UDP flows. 
# Is  there any  specific inter‐arrival  time  that appears more commonly? If yes, is it present in all 
# flows, TCP flows, or UDP flows? Do you see any difference between TCP and UDP flows? 

def interPacketArrival():
    #i = 0
    flows = []
    with open('allPacketsTime.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #i += 1
            #if i > 100:
            #    break
            if row[4] == 'TCP':
                inFlows = False
                source = row[2]
                destination = row[3]
                for flow in flows:
                    if source in flow and destination in flow:
                        flow[3] = int(flow[3]) + 1 #packet count
                        flow[2] = str(float(flow[2]) + float(row[7])) #length of packet
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([source, destination, float(row[7]), 1])
    for flow in flows:
        flow = [flow[0], flow[1], float(flow[2]) / int(flow[3])]
    saveToCSV(flows)

# TCP State: For each TCP  flow,  determine  the  final  state  of  the  connection. You  can  do  this  by 
# checking the TCP header flags. To simplify, assign each connection to one of these classes: Request 
# (only the initial SYN packet), Reset (the connection terminated after one side sent a reset signal), 
# Finished (the connection is successfully terminated after each side sent the FIN message and the 
# other side acknowledged it), Ongoing (if the last packet was sent during the 5 minutes of the trace 
# file), and Failed (if the last packets was sent before the last 5 minutes of the trace file and the 
# connection is not terminated by a reset or FIN message. This case usually represents connections 
# that suddenly disconnected, e.g., when one side is disconnected from the Internet). 

def TCPState():
    pass

#getNumFlows()
#getFlowDuration()
#getSizeFlows()
interPacketArrival()
#TCPState()

#info = row[6].split(' ')
#print(info[9][4:])