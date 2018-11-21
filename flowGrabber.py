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
    firstRun = True
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if row[4] == 'UDP':
                if firstRun:
                    firstRun = False
                    continue
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                try:
                    dPort = (row[-1].split('  >  '))[1].split(' ')[0]
                    sPort = (row[-1].split('  >  '))[0].split(' ')[-1]
                except:
                    continue

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

# For TCP packets, in the addition to the total byte sum, calculate the overhead
# ratio as the sum of all headers (including TCP, IP, and Ethernet) divided by
# the total size of  the data  that is  transferred by  the  flow. If  the  flow
# did  not  transfer any data  (e.g.,  the connection did not stablish 
# successfully), use the number 9999 instead to represent infinity. Now draw the
# CDF of hit ratio. What can you say about TCP overhead base on this chart?
def overHead():
    pass

# - Inter Packet Arrival time --------------------------------------------------

def interPacketArrival():
    flows = []
    firstRun = True
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if True:#row[4] == 'UDP':
                if firstRun:
                    firstRun = False
                    continue
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                try:
                    dPort = (row[-1].split('  >  '))[1].split(' ')[0]
                    sPort = (row[-1].split('  >  '))[0].split(' ')[-1]
                except:
                    continue

                #Go through previous flows, determine if an already existing flow
                for flow in flows:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        flow[3] += 1 #packet count
                        #duration = previous duration + (current time - time of last packet in flow)
                        flow[1] = str(float(flow[1]) + (float(row[1]) - float(flow[2])))
                        flow[2] = row[1] #Time this packet was captured
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([[source, destination, sPort, dPort], float(row[1]), float(row[1]), 1])

    for flow in flows:
        #Divide total interpacket time with total number of packets in flow
        flow = [flow[0], float(flow[1]) / int(flow[3])]
    saveToCSV(flows)

# Request (only the initial SYN packet)
# Reset (the connection terminated after one side sent a reset signal) 
# Finished (the connection is successfully terminated after each side sent the FIN message and the other side acknowledged it)
# Ongoing (if the last packet was sent during the 5 minutes of the trace file) 
def TCPState():
    flows = []
    firstRun = True
    with open('tcpPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #Ensures that we skip the first iteration
            if firstRun:
                    firstRun = False
                    continue

            #If in a flow, perform for loop, else the if(not)
            inFlows = False 
            #Get
            source = row[2]
            destination = row[3]
            dPort = (row[-1].split('  >  '))[1].split(' ')[0]
            sPort = (row[-1].split('  >  '))[0].split(' ')[-1]

            #Go through previous flows, determine if an already existing flow
            for flow in flows:
                #Check if IP in flow
                if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                    extract = ''.join([i for i in row[-2] if not i.isdigit()]).replace('\\', '')
                    flow[1].append(extract)
                    inFlows = True

            if not(inFlows):
                extract = ''.join([i for i in row[-2] if not i.isdigit()]).replace('\\', '')
                flows.append([[source, destination, sPort, dPort], [extract]])

    counter = [['Request', 0], ['Reset', 0], ['Finished', 0], ['Ongoing', 0]]

    for flow in flows:

        #This is a hack, to check if second to last packet has 'F' flag in it
        finished = False
        if len(flow[1]) > 1:
            if 'F' in flow[1][-2]:
                finished = True

        #If the flow has been reset
        if 'R' in flow[1][-1]:
            counter[1][1] += 1
        
        #If the flow has succesfully ended
        elif ('F' in flow[1][-1]) or finished:
            counter[2][1] += 1

        #If the flow is ongoing
        elif 'A' in flow[1][-1]:
            counter[3][1] += 1

        #Else, it's a request or identify it
        else:
            notS = False
            for element in flow[1]:
                if element != 'S':
                    print(flow[1])
                    notS = True
                    break
            if not(notS):
                counter[0][1] += 1

    print(counter) 

#getNumFlows()
#getFlowDuration()
#getSizeFlows()
#overHead()
#interPacketArrival()
TCPState()
