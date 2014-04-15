import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import ticker
import math
import sqlite3
import compare_regs as cr
import inversemodel_clusters as ic
import prediction_clusters as pc
from datetime import date
import pylab as pl

import matplotlib.dates as md
import datetime as dt
import time

#comment this section below out if you do not need to create a new bestreg file

def createBestReg(testbed):

    if testbed == 'NASA':
        #possible dependents: nasalight2,3,5,6,7
        #possible co-regressors: nasalight1,4 or none
        #possible artificial regs: lighta,b,c,d
        # This is for winter-summer data
        depmotes = ['nasalight2','nasalight3']
        regmotes = ['nasalight4','nasalight1'] #noartificial
        #NASA always uses nasalight8 as window regressor
        depmotes = ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7']
        regmotes = ['nasalight1','nasalight4']#'lighta','lightb','lightc','lightd'] #yesartificial
        validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
        #validtimes = [1388275200000,1389312000000]
        #validtimes = [1388534400000, 1389398400000] #Jan 1, 2014 to Jan 11, 2014
        #validtimes = [1390176000000, 1391040000000] # Jan 20, 2014 to Jan 30, 2014
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('bestreg.txt','w')
        for mote in depmotes:
            rmsper = []
            for count in range(len(rmserrs[mote])):
                rmsper.append(rmserrs[mote][count][1])
            min_index = np.argmin(np.array(rmsper))
            best.write('Best regressors for dependent, '+mote+': '+str(rmserrs[mote][min_index][2])+'\nRMS value error = '+str(rmserrs[mote][min_index][0])+' and RMS percent error = '+str(rmserrs[mote][min_index][1])+'\n')#\n')
            #best.write(rmserrs[mote][min_index] + '\n\n')
            print rmserrs[mote][min_index],  '\n\n'
        best.close()
    elif testbed == 'Hesse':
        depmotes = ['light2']
        regmotes = ['light3','light4']
        validtimes = [1363417200000,1364281200000] #Mar16toMar26(midnight-to-midnight)
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('bestreg.txt','w')
        for mote in depmotes:
            rmsper = []
            for count in range(len(rmserrs[mote])):
                rmsper.append(rmserrs[mote][count][1])
            min_index = np.argmin(np.array(rmsper))
            best.write('Best regressors for dependent, '+mote+': '+str(rmserrs[mote][min_index][2])+'\nRMS value error = '+str(rmserrs[mote][min_index][0])+' and RMS percent error = '+str(rmserrs[mote][min_index][1])+'\n\n')
        best.close()
    elif testbed == 'NewCitris':
        depmotes = ['light5','light6','light7','light9','light10']
        regmotes = ['light8']
        validtimes = [1377887460000, 1382563860000] #Mar16toMar26(midnight-to-midnight)
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('bestreg.txt','w')
        for mote in depmotes:
            rmsper = []
            for count in range(len(rmserrs[mote])):
                rmsper.append(rmserrs[mote][count][1])
            min_index = np.argmin(np.array(rmsper))
            best.write('Best regressors for dependent, '+mote+': '+str(rmserrs[mote][min_index][2])+'\nRMS value error = '+str(rmserrs[mote][min_index][0])+' and RMS percent error = '+str(rmserrs[mote][min_index][1])+'\n\n')
        best.close()
        
    elif testbed == 'NewNasa':
        depmotes = ['newnasalight2','newnasalight4','newnasalight5','newnasalight6','newnasalight7']
        regmotes = ['newnasalight1','newnasalight3'] # noartificial? yesartificial
        validtimes = [1388275200000,1389312000000]
        #validtimes = [1386033540000,1387070340000]
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('newnasa_reg.txt','w')
        for mote in depmotes:
            rmsper = []
            for count in range(len(rmserrs[mote])):
                rmsper.append(rmserrs[mote][count][1])
            min_index = np.argmin(np.array(rmsper))
            best.write('Best regressors for dependent, '+mote+': '+str(rmserrs[mote][min_index][2])+'\nRMS value error = '+str(rmserrs[mote][min_index][0])+' and RMS percent error = '+str(rmserrs[mote][min_index][1])+'\n\n')
        best.close()

    print 'Done! Woohoo!'

#comment this section above out if you do not need to create a new bestreg file

def plot(testbed):

    #determine bestreg for each depedent
    f = open('bestreg.txt','r')
    #f = open('bestreg_newNasa.txt','r')
    lines = f.readlines()
    if testbed == 'NASA':
        dependents = ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7']
        validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
        #validtimes = [1388275200000,1389312000000]
        #validtimes = [1388534400000, 1389398400000] #Jan 1, 2014 to Jan 11, 2014
        #validtimes = [1390176000000, 1391040000000] # Jan 20, 2014 to Jan 30, 2014
    elif testbed == 'Hesse':
        dependents = ['light2']
        validtimes = [1363417200000,1364281200000] #Mar16toMar26(midnight-to-midnight)
    elif testbed == 'NewCitris':
        dependents = ['light5', 'light6', 'light7', 'light9', 'light10']
        validtimes = [1377887460000, 1382563860000]
    elif testbed == 'NewNasa':
        dependents = ['newnasalight2','newnasalight4','newnasalight5','newnasalight6','newnasalight7']
        #validtimes = [1386033540000,1391559480000]
        #validtimes = [1386033540000,1387070340000]
        validtimes = [1388275200000,1389312000000]
    regs = dict()
    for dependent in dependents:
        regs[dependent] = []
        for line in lines:
            words = line.split()
            if len(words) > 4 and words[4] == dependent+':':
                for word in words[5:]:
                    word = word.replace(']','').replace('[','').replace("'",'').replace(',','')
                    regs[dependent].append(word)
    f.close()

    #retrieve time,actual,predictedfinal data
    for dependent in dependents:        
        regressors = regs[dependent]
        ic.inversemodel(testbed,dependent,regressors)
        ic.inversemodel_hour(testbed,dependent,regressors)
        #if dependent == 'nasalight3': #only applies for NASA
        #    validtimes = [1339138800000,1339570800000] #Jun8toJun13(midnight-to-midnight)
        a,b,predc,actc,c,d,e,timec=pc.prediction(validtimes,'all',testbed,dependent,regressors)
        a,b,predh,acth,c,d,e,timeh=pc.prediction_hour(validtimes,testbed,dependent,regressors)
        predictedfinal = predc+predh
        print "predictedfinal: ", predictedfinal
        actual = actc+acth
        print "actual: ", actual
        time = timec+timeh
        print "time: ", time
        plotdata = zip(time,actual,predictedfinal)
        plotdata.sort()
        for count in range(len(plotdata)):
            time[count]=plotdata[count][0]
            actual[count]=plotdata[count][1]
            predictedfinal[count]=plotdata[count][2]

        #plot
        if testbed == 'NASA':
            yaxislim = (0,1000)
            xaxislim = (0*pow(10,9)+1.339*pow(10,12),1.4*pow(10,9)+1.339*pow(10,12))
            if dependent == 'nasalight3': #only applies for NASA
                xaxislim = (0.1*pow(10,9)+1.339*pow(10,12),0.6*pow(10,9)+1.339*pow(10,12))
        elif testbed == 'NewNasa':
            yaxislim = (0,1000)
            #xaxislim = (0*pow(10,9)+1.386*pow(10,12),1.4*pow(10,9)+1.386*pow(10,12))
            xaxislim = (0*pow(10,9)+1.388*pow(10,12),1.4*pow(10,9)+1.388*pow(10,12))
        elif testbed == 'Hesse' or testbed == 'NewCitris':
            yaxislim = (0,1500)
            xaxislim = (0.3*pow(10,9)+1.363*pow(10,12),1.4*pow(10,9)+1.363*pow(10,12))
        #print "plotting a figure!!"
        #print dependent
        #print "time: ", time
        #print "predictedfinal: ", predictedfinal
        #plt.figure()
        #plt.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        #plt.plot(time,predictedfinal,'r',time,actual,'b')
        ##plt.xlim(xaxislim)
        ##plt.ylim(yaxislim)
        #plt.xlabel('Date')
        #plt.ylabel('Illuminance (Lux)')
        #plt.savefig(dependent+'line')
        #plt.close()
        #plt.figure()
        #plt.scatter(time,predictedfinal,c='r',edgecolor='r')
        #plt.scatter(time,actual,c='b',edgecolor='b')
        ##plt.xlim(xaxislim)
        ##plt.ylim(yaxislim)
        #plt.xlabel('Date')
        #plt.ylabel('Illuminance (Lux)')
        #plt.show()
        #plt.savefig(dependent+'scatter')
        #plt.close()
        print dependent
        n=20
        time = [t/1000.0 for t in time]
        duration = max(time) - min(time)
        now = min(time) 
        #insert the actual unixtimes in place of now,now+duration,n in the next line
        dates=[dt.datetime.fromtimestamp(ts) for ts in time]
        datenums=md.date2num(dates)
        #put measured and predicted in place of values1 and values2
        values1 = actual 
        values2 = predictedfinal 
        fig=matplotlib.pyplot.gcf()
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.4)
        xfmt = md.DateFormatter('%Y-%m-%d %H')
        ax.xaxis.set_major_formatter(xfmt)
        ax.plot(datenums,values1,"ro",label='Measured light')
        ax.plot(datenums,values2,"bo",label='Predicted light')
        ax.set_xlabel('Time of day',fontsize=34)
        ax.set_ylabel('Illuminance (lux)', fontsize=34)
        ax.set_ylim([0, max(int(np.max(values1)), int(np.max(values2)))])
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(24)
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(24)
            tick.label.set_rotation(90)
        legend = ax.legend(loc='upper right')
        for label in legend.get_texts():
            label.set_fontsize(32)
        #fig.set_size_inches(20,10.5)
        fig.set_size_inches(10.5,9)
        plt.savefig(dependent + '.png',dpi=400)
        plt.show()

def formate_date(x, pos=None):
    return pyplt.num2date(x).strftime('%Y-%m-%d')

def single(testbed,dependent,regressors):
    
    # single case
    if testbed == 'NASA':
        #validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
        #validtimes = [1388275200000,1389312000000]
        validtimes = [1388534400000, 1389398400000] #Jan 1, 2014 to Jan 11, 2014
    elif testbed == 'Hesse':
        validtimes = [1363417200000,1364281200000] #Mar16toMar26(midnight-to-midnight)
    elif testbed == 'NewCitris':
        validtimes = [1377887460000, 1382563860000]
    elif testbed == 'NewNasa':
        #validtimes = [1386033540000,1391559480000]
        #validtimes = [1386033540000,1387070340000]
        validtimes = [1388275200000,1389312000000]
    ic.inversemodel(testbed,dependent,regressors)
    ic.inversemodel_hour(testbed,dependent,regressors)
    if dependent == 'nasalight3' and testbed == 'NASA': #only applies for NASA
        validtimes = [1339138800000,1339570800000] #Jun8toJun13(midnight-to-midnight)
    a,b,predc,actc,c,d,e,timec=pc.prediction(validtimes,'all',testbed,dependent,regressors)
    a,b,predh,acth,c,d,e,timeh=pc.prediction_hour(validtimes,testbed,dependent,regressors)
    predictedfinal = predc+predh
    actual = actc+acth
    time = timec+timeh
    plotdata = zip(time,actual,predictedfinal)
    plotdata.sort()
    for count in range(len(plotdata)):
        time[count]=plotdata[count][0]
        actual[count]=plotdata[count][1]
        predictedfinal[count]=plotdata[count][2]

    #plot
    if testbed == 'NASA' or testbed == 'NewNasa':
        yaxislim = (0,1000)
        xaxislim = (0*pow(10,9)+1.339*pow(10,12),1.4*pow(10,9)+1.339*pow(10,12))
        if dependent == 'nasalight3': #only applies for NASA
            xaxislim = (0.1*pow(10,9)+1.339*pow(10,12),0.6*pow(10,9)+1.339*pow(10,12))
    elif testbed == 'Hesse' or testbed == 'NewCitris':
        yaxislim = (0,1500)
        xaxislim = (0.3*pow(10,9)+1.363*pow(10,12),1.4*pow(10,9)+1.363*pow(10,12))
    plt.figure()
    plt.plot(time,predictedfinal,'r',time,actual,'b')
    plt.xlim(xaxislim)
    plt.ylim(yaxislim)
    plt.xlabel('unixtime')
    plt.ylabel('Illuminance (Lux)')
    plt.savefig(dependent+'line')
    plt.close()
    plt.figure()
    plt.scatter(time,predictedfinal,c='r',edgecolor='r')
    plt.scatter(time,actual,c='b',edgecolor='b')
    plt.xlim(xaxislim)
    plt.ylim(yaxislim)
    plt.xlabel('unixtime')
    plt.ylabel('Illuminance (Lux)')
    plt.savefig(dependent+'scatter')
    plt.close()


createBestReg('NASA')
#createBestReg('NewCitris')
#plot('NewNasa')
plot('NASA')
