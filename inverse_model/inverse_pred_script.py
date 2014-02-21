#datetime.datetime.fromtimestamp(unixtime)
import numpy as np
from matplotlib import pyplot as plt
import math
import sqlite3
import compare_regs as cr
import inversemodel_clusters as ic
import prediction_clusters as pc
import datetime

#comment this section below out if you do not need to create a new bestreg file

def createBestReg(testbed):

    if testbed == 'NASA':
        #possible dependents: nasalight2,3,5,6,7
        #possible co-regressors: nasalight1,4 or none
        #possible artificial regs: lighta,b,c,d
        #NASA always uses nasalight8 as window regressor
        depmotes = ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7']
        #regmotes = ['nasalight4','nasalight1'] #noartificial
        regmotes = ['nasalight1','nasalight4','lighta','lightb','lightc','lightd'] #yesartificial
        validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('bestreg.txt','w')
        for mote in depmotes:
            rmsper = []
            for count in range(len(rmserrs[mote])):
                rmsper.append(rmserrs[mote][count][1])
            min_index = np.argmin(np.array(rmsper))
            best.write('Best regressors for dependent, '+mote+': '+str(rmserrs[mote][min_index][2])+'\nRMS value error = '+str(rmserrs[mote][min_index][0])+' and RMS percent error = '+str(rmserrs[mote][min_index][1])+'\n\n')
        best.close()
    elif testbed == 'Hesse':
        #possible dependents: light2
        #possible co-regressors: light3,4 or none
        #NASA always uses light1 as window regressor
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
        #possible dependents: light2
        #possible co-regressors: light3,4 or none
        #NASA always uses light1 as window regressor
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
        #possible dependents: nasalight2,3,5,6,7
        #possible co-regressors: nasalight1,4 or none
        #possible artificial regs: lighta,b,c,d
        #NASA always uses nasalight8 as window regressor
        depmotes = ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7']
        #regmotes = ['nasalight4','nasalight1'] #noartificial
        regmotes = ['nasalight1','nasalight4','lighta','lightb','lightc','lightd'] #yesartificial
        validtimes = [1386033540000,1391559480000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
        rmserrs = cr.compare_regression(validtimes,testbed,depmotes,regmotes,'all','noaltitude')
        best = open('newnasa.txt','w')
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
    lines = f.readlines()
    if testbed == 'NASA':
        dependents = ['nasalight2','nasalight3','nasalight5','nasalight6','nasalight7']
        validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
    elif testbed == 'Hesse':
        dependents = ['light2']
        validtimes = [1363417200000,1364281200000] #Mar16toMar26(midnight-to-midnight)
    elif testbed == 'NewCitris':
        dependents = ['light5', 'light6', 'light7', 'light9', 'light10']
        validtimes = [1377887460000, 1382563860000]
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
        if dependent == 'nasalight3': #only applies for NASA
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
        if testbed == 'NASA':
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

def single(testbed,dependent,regressors):
    
    # single case
    if testbed == 'NASA':
        validtimes = [1339138800000,1340175600000] #Jun8toJun20(midnight-to-midnight) exception: 'nasalight3'
    elif testbed == 'Hesse':
        validtimes = [1363417200000,1364281200000] #Mar16toMar26(midnight-to-midnight)
    elif testbed == 'NewCitris':
        validtimes = [1377887460000, 1382563860000]
    ic.inversemodel(testbed,dependent,regressors)
    ic.inversemodel_hour(testbed,dependent,regressors)
    if dependent == 'nasalight3': #only applies for NASA
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
    if testbed == 'NASA':
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


createBestReg('NewNasa')

