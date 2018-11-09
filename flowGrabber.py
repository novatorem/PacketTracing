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
            #if row[4] == 'UDP':
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

#getNumFlows()
getFlowDuration()
#info = row[6].split(' ')
#print(info[9][4:])