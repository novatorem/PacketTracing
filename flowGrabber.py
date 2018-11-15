import os
import re
import csv

#Helper function to save to CSV for easier readability
def saveToCSV(data, directory = 'output', name = 'data.csv'):
    with open(os.path.join(os.path.dirname(__file__), directory + "/" + name),
            'w') as f:
        for row in data:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator = '\n')
            writer.writerows([row])

# - Get the number of TCP/UDP flows --------------------------------------------
def getNumFlows():
    flows = []
    flows.append([0])
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if row[4] == 'TCP':
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                dPort = (row[-2].split('  >  '))[1].split(' ')[0]
                sPort = (row[-2].split('  >  '))[0].split(' ')[-1]

                #Go through previous flows, determine if an already existing flow
                for flow in flows[1:]:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        #Increase number of packets belonging to the flow
                        inFlows = True
                        flow[1] += 1
                        break
                
                #If not already in a flow, create a new one
                if not(inFlows):
                    flows[0][0] += 1
                    flows.append([[source, destination, sPort, dPort], 1])

    saveToCSV(flows)

def test():
    flows = 0
    with open('udpConversations.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            flows += 1
    print(flows - 1)

# - Get the duration of unique flows -------------------------------------------
def getFlowDuration():
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if row[4] == 'TCP':
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                dPort = (row[-2].split('  >  '))[1].split(' ')[0]
                sPort = (row[-2].split('  >  '))[0].split(' ')[-1]

                #Go through previous flows, determine if an already existing flow
                for flow in flows:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        flow[1] = float(row[1]) - float(flow[2])
                        flow[3] += 1
                        inFlows = True
                        break
                if not(inFlows):
                    #Flow[1] will be total time of last recieved packet in flow
                    #Flow[2] will be start time of first recieved packet in flow
                    flows.append([[source, destination, sPort, dPort], row[1], row[1], 0])

    for flow in flows:
        if flow[-1] < 1:
            flow[1] = float(0)
        del flow[-1]
        del flow[-2]

    saveToCSV(flows)

# - Get the size of flows ------------------------------------------------------
def getSizeFlows():
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if row[4] == 'TCP':
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                dPort = (row[-2].split('  >  '))[1].split(' ')[0]
                sPort = (row[-2].split('  >  '))[0].split(' ')[-1]

                #Go through previous flows, determine if an already existing flow
                for flow in flows:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        flow[1] = flow[1] + 1 #packet count
                        flow[2] = str(int(flow[2]) + int(row[5])) #length of packet
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([[source, destination, sPort, dPort], 1, row[5]])
    saveToCSV(flows)

# For TCP packets, in the addition to the total byte sum, calculate 
# the overhead ratio as the sum of all headers (including TCP, IP, and Ethernet) divided by the total 
# size of  the data  that is  transferred by  the  flow. If  the  flow did  not  transfer any data  (e.g.,  the 
# connection did not stablish successfully), use the number 9999 instead to represent infinity. Now 
# draw the CDF of hit ratio. What can you say about TCP overhead base on this chart?
def overHead():
    pass

# - Inter Packet Arrival time --------------------------------------------------

def interPacketArrival():
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if row[4] == 'TCP':
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                dPort = (row[-2].split('  >  '))[1].split(' ')[0]
                sPort = (row[-2].split('  >  '))[0].split(' ')[-1]

                #Go through previous flows, determine if an already existing flow
                for flow in flows:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        flow[2] = int(flow[2]) + 1 #packet count
                        flow[1] = str(float(flow[1]) + float(row[7])) #length of packet
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([[source, destination, sPort, dPort], float(row[7]), 1])

    for flow in flows:
        flow = [flow[0], float(flow[1]) / int(flow[2])]
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
    #i = 0
    flows = []
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #i += 1
            #if i > 100:
                #break
            if row[4] == 'TCP':
                inFlows = False
                source = row[2]
                destination = row[3]
                for flow in flows:
                    if source in flow and destination in flow:
                        if 'ACK' in row[6]:
                                flow[2].append('ACK')
                        if 'ACK, SYN' in row[6]:
                            flow[2].append('ACK, SYN')
                        if 'FIN' in row[6]:
                                flow[2].append('FIN')
                        if 'RST' in row[6]:
                                flow[2].append('RST')
                        inFlows = True
                        break
                if not(inFlows):
                    flow = [source, destination, []]
                    if 'ACK' in row[6]:
                        flow[2].append('ACK')
                    if 'SYN' in row[6]:
                        flow[2].append('SYN')
                    if 'FIN' in row[6]:
                        flow[2].append('FIN')
                    if 'RST' in row[6]:
                        flow[2].append('RST')
                    flows.append(flow)

    saveToCSV(flows)
    tally = [['ACK', 0], ['SYN', 0], ['FIN', 0], ['RST', 0], ['SYN, ACK']]
    for flow in flows:
        
        if ''.join(flow).rfind('FIN') < ''.join(flow).rfind('RST'):
            tally[3][1] += 1
        elif flow[-2] == 'FIN' and flow[-1] == 'ACK':
            tally[2][1] += 1
    print(tally)

#getNumFlows()
#getFlowDuration()
#getSizeFlows()
#overHead()
interPacketArrival()
#TCPState()
