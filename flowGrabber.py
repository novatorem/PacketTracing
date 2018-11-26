import os
import re
import csv
import statistics

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
            #if row[4] == 'TCP':
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
    firstRun = True
    with open('allPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if firstRun:
                    firstRun = False
                    continue
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

def overHead():
    flows = []
    firstRun = True
    with open('packetLengths.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            if firstRun:
                firstRun = False
                continue
            inFlows = False #If in a flow, perform for loop, else the if(not)
            source = row[2]
            destination = row[3]
            dPort = (row[-1].split('  >  '))[1].split(' ')[0]
            sPort = (row[-1].split('  >  '))[0].split(' ')[-1]

            #Go through previous flows, determine if an already existing flow
            for flow in flows:
                #Check if IP in flow
                if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                    flow[1] = str(int(flow[1]) + (int(row[-3]) - int(row[-2]))) #total packet length
                    flow[2] = str(int(flow[2]) + int(row[-2])) #tcp data length
                    inFlows = True
                    break
            if not(inFlows):
                flows.append([[source, destination, sPort, dPort], 1, row[-2]])
    
    for flow in flows:
        if flow[2] == '0':
            flow[1] = 9999
            del flow[2]
        else:
            flow[1] = int(flow[1]) / int(flow[2])
            del flow[-1]

    saveToCSV(flows)

# - Inter Packet Arrival time --------------------------------------------------

def interPacketArrival():
    flows = []
    firstRun = True
    with open('bothPackets.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #if (row[4] == 'UDP') or (row[4] == 'TCP'):
                if firstRun:
                    firstRun = False
                    continue
                inFlows = False #If in a flow, perform for loop, else the if(not)
                source = row[2]
                destination = row[3]
                dPort = (row[-1].split('  >  '))[1].split(' ')[0]
                sPort = (row[-1].split('  >  '))[0].split(' ')[-1]

                #Go through previous flows, determine if an already existing flow
                for flow in flows:
                    #Check if IP in flow
                    if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                        flow[3] += 1 #packet count
                        flow[2] = float(row[1])
                        inFlows = True
                        break
                if not(inFlows):
                    flows.append([[source, destination, sPort, dPort], float(row[1]), float(row[1]), 1])

    for flow in flows:
        totalTime = flow[2] - flow[1]
        averageTime = totalTime / flow[3]
        del flow[-1]
        del flow[-1]
        flow[1] = averageTime
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

def rto():
    RTTS = rtt()
    time = rttTime()
    RTOS = [1]
    SRTT = RTTS[0]
    RTTVAR = RTTS[0]/2
    RTOS.append(SRTT + max(0.001, 4 * RTTVAR))
    SRTTS = [SRTT]
    for RTT in RTTS[1:]:
        RTTVAR = (1 - 1/4) * RTTVAR + 1/4 * abs(SRTT - RTT)
        SRTT = (1 - 1/8) * SRTT + 1/8 * RTT
        SRTTS.append(SRTT)
        RTOS.append(SRTT + max(0.001, 4 * RTTVAR))
    i = 0
    results = []
    while i < len(RTTS):
        temp = [time[i], RTTS[i], SRTTS[i]]
        results.append(temp)
        i += 1
    saveToCSV(results)

def rtt(data = 'flow1.csv'):
    results = []
    firstRun = True
    with open(data) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #Ensures that we skip the first iteration
            if firstRun:
                    firstRun = False
                    continue

            if row[-2] != "":
                results.append(float(row[-2]))
    return(results)

def rttTime():
    results = []
    firstRun = True
    with open('flow1.csv') as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #Ensures that we skip the first iteration
            if firstRun:
                    firstRun = False
                    continue

            if row[-2] != "":
                results.append(int(float(row[1])))
    return(results)

def rttEstimation(data = 'rtt3.csv'):
    flows = []
    firstRun = True
    with open(data) as csv_file:
        csvReader = csv.reader(csv_file, delimiter=',')
        for row in csvReader:
            #Ensures that we skip the first iteration
            if firstRun:
                    firstRun = False
                    continue
            #If in a flow, perform for loop, else the if(not)
            inFlows = False 
            #Get the flow by isolating for IP/Port
            source = row[2]
            destination = row[3]
            dPort = (row[-1].split('  >  '))[1].split(' ')[0]
            sPort = (row[-1].split('  >  '))[0].split(' ')[-1]

            #Go through previous flows, determine if in an already existing flow
            for flow in flows:
                #Check if IP/Port in flow
                if source in flow[0] and destination in flow[0] and dPort in flow[0] and sPort in flow[0]:
                    #Add the packet to an existing flow
                    flow[1].append(row)
                    inFlows = True
                    break

            #Create a new flow
            if not(inFlows):
                flows.append([[source, destination, sPort, dPort], [row], row[1]])

    #All the RTTs of all the flows
    RTTSflows = []
    #For each flow in the host, get the RTTs and add them
    for flow in flows:
        temp = []
        for row in flow[1]:
                if row[-2] != "":
                    temp.append(float(row[-2]))
        RTTSflows.append(temp)
    medians = []
    #Go through all the RTTs of each flow
    for RTTS in RTTSflows:
        #SRTT formula to get the estimation
        SRTT = RTTS[0]
        SRTTS = [SRTT]
        for RTT in RTTS:
            SRTT = (1 - 1/8) * SRTT + 1/8 * RTT
            SRTTS.append(SRTT)
        #Append all the median SRTTS
        medians.append(statistics.median(SRTTS))

    #Send to csv a list of [TIME, MEDIAN SRTT]
    timeMedian = []
    i = 0
    while i < len(flows):
        timeMedian.append([flows[i][-1], medians[i]])
        i += 1
    saveToCSV(timeMedian)

#getNumFlows()
#getFlowDuration()
#getSizeFlows()
#overHead()
#interPacketArrival()
#TCPState()
#rto()
rttEstimation()
