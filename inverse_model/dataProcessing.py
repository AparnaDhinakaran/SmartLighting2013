#!/usr/bin/python

#input: 1.dataDict, dictionary of lists of tuples: (data, unixtime stamp), where keys are motenumbers
#       2.option, 'light' returns only data and 'all' returns data, unixtime stamp, etc
#       3.intervalSize, which is 300000 (5 minutes) by default.
#output: finaldataDict, lists of data points whose unixtimes match within intervalSize
#USAGE: import dataProcessing as dP
#       dP.process(dataDict)

import math
import numpy as np

def process(dataDict, option='light', intervalSize=300000):
    # Initialize
    finaldataDict = dict()
    for mote in dataDict.keys():
        finaldataDict[mote] = []
    empties = 0 #track
    unixtimes = []
	
    # Retrieve unixtimes of the first mote
    key = dataDict.keys()[0]
    for ind in range(len(dataDict[key])):
        unixtime = dataDict[key][ind][1]
        unixtimes.append(unixtime)

    # Match unixtimes to that of first mote
    i = 0
    for unixtime in unixtimes:
        timepointData = dict()
        Uwindow = math.ceil(unixtime+0.5*(intervalSize))
        Dwindow = math.floor(unixtime-0.5*(intervalSize))
        for moteNum in dataDict.keys():
            timepointData[moteNum] = []

            #relevant is a list of datapoints that is within time window
            relevant=[datum for datum in dataDict[moteNum] if Dwindow<=datum[1]<Uwindow and datum[0]!=1.0]

            #retrieve the closest (by time) matching datapoint
            if len(relevant)==1:
                datum = relevant[0]
            elif len(relevant)>1: #more than one data point in current 5 minute window
                i = -1
                t = 'inf'
                for datum in relevant:
                    tdif = abs(datum[1]-unixtime)
                    t = min(t,tdif)
                    if t == tdif:
                        i+=1
                datum = relevant[i]
            else:
                empties+=1 #track
                datum = [] #empty datum
            if datum != []:
                if option=='light':                
                    timepointData[moteNum].append(datum[0])
                elif option=='all':
                    #print "appending"
                    #print "datum: ", datum
                    timepointData[moteNum].append([d for d in datum])

        #check matches        
        minlen=min([len(timepointData[moteNum]) for moteNum in timepointData.keys()])
        if minlen>0: #there is data for every single mote within the time interval window
            i+=1
            for moteNum in dataDict.keys():
                for ind in range(minlen):
                    finaldataDict[moteNum].append(timepointData[moteNum][ind])

    #result
    if len(finaldataDict)==0: 
        print 'FAILURE: no matching datapoints'
    return finaldataDict
