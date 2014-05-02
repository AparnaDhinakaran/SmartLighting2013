import argparse
import compare_regs as cr
import datetime as dt
import inversemodel_clusters as ic
import math
import matplotlib
import matplotlib.dates as md
import numpy as np
import prediction_clusters as pc
import pylab as pl
import sqlite3
import time

from datetime import date
from matplotlib import pyplot as plt
from matplotlib import ticker

"""
Please note: these are validtimes we have used in the past. They are here for reference:

validtimes = [1339138800000, 1340175600000] #June 8, 2012 to June 20, 2012; exception: 'nasalight3'
validtimes = [1388275200000, 1389312000000] #December 29, 2013 to January 10, 2014
validtimes = [1388534400000, 1389398400000] #January 1, 2014 to January 11, 2014
validtimes = [1390176000000, 1391040000000] #January 20, 2014 to January 30, 2014
"""

# Map testbed to dependent motes
dependentsMap = {'NASA': ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7'],
              'NewNasa': ['nasalight2','nasalight3'],
              'Hesse': ['light2'],
              'NewCitris': ['light5','light6','light7','light9','light10']}

# Map testbed to regressor motes
regressorsMap = {'NASA': ['nasalight1','nasalight4'],
              'NewNasa': ['nasalight4','nasalight1'],
              'Hesse': ['light3','light4'],
              'NewCitris': ['light8']}

def createBestReg(testbed, startValid, endValid, startTrain, endTrain):
    """
    Output the best regressors for the dependent sensors of the testbed TESTBED along with
    the RMS value and percent errors in a file called <testbed>_bestreg.txt.
    
    Use validtimes startValid-endValid.
    
    For NASA testbed:
        Possible dependents: nasalight2,3,5,6,7
        Possible co-regressors: nasalight1,4 or none
        Possible artificial regs: lighta,b,c,d
        Window regressor: nasalight8
        if dependent == 'nasalight3': #only applies for NASA
            validtimes = [1339138800000,1339570800000] #Jun8toJun13(midnight-to-midnight)

    Argument Types:
        testbed - String
        startValid - float
        endValid - float
        startTrain - float
        endTrain - float
    """
    validtimes = [startValid, endValid]
    depmotes = dependentsMap[testbed] 
    regmotes = regressorsMap[testbed] 
    rmserrs = cr.compare_regression(validtimes, testbed, startTrain, endTrain, depmotes,
        regmotes,'all','noaltitude')
    best = open('results/' + testbed + '_bestreg.txt','w')
    for mote in depmotes:
        rmsper = []
        for count in range(len(rmserrs[mote])):
            rmsper.append(rmserrs[mote][count][1])
        min_index = np.argmin(np.array(rmsper))
        best.write('Best regressors for dependent, '+mote+': ' +
            str(rmserrs[mote][min_index][2]) + '\nRMS value error = ' + 
            str(rmserrs[mote][min_index][0]) + ' and RMS percent error = ' + 
            str(rmserrs[mote][min_index][1])+'\n\n')
    best.close()
    print 'Done! Woohoo!'
    print 'See results in: results/' + testbed + '_bestreg.txt'

def plot(testbed, startValid, endValid, startTrain, endTrain):
    """
    Plot the inverse model results for the specified testbed using validtimes
    startValid-endValid.

    Argument Types:
        testbed - String
        startValid - float
        endValid - float
        startTrain - float
        endTrain - float
    """
    # Determine bestreg for each depedent
    f = open('results/' + testbed + '_bestreg.txt','r')
    lines = f.readlines()
    f.close()
    dependents = dependentsMap[testbed]
    regs = dict()
    for dependent in dependents:
        # Populate the regs dictionary
        regs[dependent] = []
        for line in lines:
            words = line.split()
            if len(words) > 4 and words[4] == dependent+':':
                for word in words[5:]:
                    word = word.replace(']','').replace('[','').replace("'",'').replace(',','')
                    regs[dependent].append(word)
        regressors = regs[dependent]
        singlePlot(testbed, dependent, regressors, startValid, endValid, startTrain, endTrain)

def singlePlot(testbed, dependent, regressors, startValid, endValid, startTrain, endTrain):
    """
    Plot the inverse model results for the specified testbed using validtimes, dependent,
    and regressors using the validtimes startValid-endValid.

    Argument Types:
        testbed - String
        dependent - string
        regressors - list of strings
        startValid - float
        endValid - float
        startTrain - float
        endTrain - float
    """
    validtimes = [startValid, endValid]
    ic.inversemodel(testbed,startTrain,endTrain,dependent,regressors)
    ic.inversemodel_hour(testbed,startTrain,endTrain,dependent,regressors)
    a,b,predc,actc,c,d,e,timec=pc.prediction(validtimes,'all',testbed,dependent,regressors)
    a,b,predh,acth,c,d,e,timeh=pc.prediction_hour(validtimes,testbed,dependent,regressors)
    predictedfinal = predc + predh
    actual = actc + acth
    time = timec + timeh
    plotdata = zip(time,actual,predictedfinal)
    plotdata.sort()
    for count in range(len(plotdata)):
        time[count] = plotdata[count][0]
        actual[count] = plotdata[count][1]
        predictedfinal[count] = plotdata[count][2]
    n = 20
    time = [t/1000.0 for t in time]
    duration = max(time) - min(time)
    dates=[dt.datetime.fromtimestamp(ts) for ts in time]
    datenums=md.date2num(dates)
    fig = matplotlib.pyplot.gcf()
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.4)
    xfmt = md.DateFormatter('%Y-%m-%d %H')
    ax.xaxis.set_major_formatter(xfmt)
    ax.plot(datenums,actual,"ro",label='Measured light')
    ax.plot(datenums,predictedfinal,"bo",label='Predicted light')
    ax.set_xlabel('Time of day',fontsize=34)
    ax.set_ylabel('Illuminance (lux)', fontsize=34)
    ax.set_ylim([0, max(int(np.max(actual)), int(np.max(predictedfinal)))])
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(24)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(24)
        tick.label.set_rotation(90)
    legend = ax.legend(loc='upper right')
    for label in legend.get_texts():
        label.set_fontsize(32)
    fig.set_size_inches(10.5,9)
    plt.savefig('plots/' + dependent + '.png', dpi=400)
    plt.show()

def validateInput(args):
    """Validates the user's input arguments."""
    if args.testbed not in ['NASA', 'NewNasa', 'Hesse', 'NewCitris']:
        raise argparse.ArgumentTypeError('No such testbed: ' + args.testbed)
    if args.v1 < time.localtime() and args.v2 < time.localtime():
        if args.v1 > args.v2:
            raise argparse.ArgumentTypeError('Start validtime must be less than end validtime.')
    else:
        raise argparse.ArgumentTypeError('Validtimes must be valid unixtimes less than the ' +
            'current unixtime.')
    if args.t1 < time.localtime() and args.t2 < time.localtime():
        if args.t1 > args.t2:
            raise argparse.ArgumentTypeError('Start traintime must be less than end traintime.')
    else:
        raise argparse.ArgumentTypeError('Traintimes must be valid unixtimes less than the ' +
            'current unixtime.')
    if args.plotSingle:
        if len(args.plotSingle) < 2:
            raise argparse.ArgumentTypeError('Argument -plotSingle requires dependent ' +
                    'mote and atleast one regressor mote.')
        if (args.plotSingle[0] not in dependentsMap[args.testbed]):
            raise argparse.ArgumentTypeError('Invalid dependent mote: ' + args.plotSingle[0] + '.')
        for reg in args.plotSingle[1:]:
            if (reg not in dependentsMap[args.testbed]):
                raise argparse.ArgumentTypeError('Invalid regressor mote: ' + reg + '.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('testbed')
    parser.add_argument('v1', type=int)
    parser.add_argument('v2', type=int)
    parser.add_argument('t1', type=int)
    parser.add_argument('t2', type=int)
    group.add_argument('-plot', action="store_true")
    group.add_argument('-plotSingle', nargs='+')
    args = parser.parse_args()
    validateInput(args)
    if args.plot:
        print "plot!"
        plot(args.testbed, args.v1, args.v2, args.t1, args.t2)
    elif args.plotSingle:
        print "plotSingle!"
        singlePlot(args.testbed, args.plotSingle[0], args.plotSingle[1:], args.v1, args.v2, args.t1, args.t2)
    else:
        print "no plotting!"
        createBestReg(args.testbed, args.v1, args.v2, args.t1, args.t2)
