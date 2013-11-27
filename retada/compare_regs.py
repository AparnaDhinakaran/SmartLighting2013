import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import math
import prediction_clusters as pc
import inversemodel_clusters as ic
#import isthereclusterdata as cd
import time
import itertools

def record_error(tt,testbed,dep,regs,clust_type,option):

    #determine tt in real local time
    start = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(float(tt[0]/1000)))
    end = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(float(tt[1]/1000)))
    
    #initialize
    if type(tt[0]) != list:
        tt = [tt]
    
    #open files
    if testbed == 'NASA':
        savefile = open('results_NASA.txt','a')
        f = open('compreg_NASA.txt','a')
    if testbed == 'Hesse':
        savefile = open('results_Hesse.txt','a')
        f = open('compreg_Hesse.txt','a')
    if testbed == 'NewCitris':
        savefile = open('results_NewCitris.txt','a')
        f = open('compreg_NewCitris.txt','a')


    #head files
    savefile.write('\n\n From '+start+' to '+end+'\n Testbed: '+str(testbed)+' Dependents: '+str(dep)+' Regressors: '+str(regs)+'\n')
    savefile.close()
    f.write('\n\n From '+start+' to '+end+'\n Testbed: '+str(testbed)+' Dependents: '+str(dep)+' Regressors: '+str(regs)+'\n')

    #clust type option (no option for a single cluster yet)
    if clust_type == 'interval':
        tts = open('training_times.txt','a')
        t = [6.25+0.5*i for i in range(24)]
        rmsval = []
        rmsper = []
        intervals = [[3*i] for i in range(24)]
        for i in range(len(intervals)):
            intervals[i].append(intervals[i][0]+2)
        for traintimes in tt:
            count = 0
            for cluster in intervals:
                timed = t[count]        
                val,per,pred,act,ct,uct,ctl,ti = pc.prediction(traintimes,cluster,testbed,dep,regs)
                count+=1
                f.write(str(timed)+'  '+str(len(pred))+'  '+str(len(act))+'  '+str(val)+'  '+str(per)+'  '+str(ct)+'  '+str(uct)+'  '+str(ctl)+'\n')
                rmsval.append(val)
                rmsper.append(per)
        rmsvalnum = [rmsval[i] for i in range(len(rmsval)) if rmsval[i]>0]
        if len(rmsval) == len(rmsvalnum):
            tts.write('THIS IS GOOD'+str(tt[0])+' '+start+' to '+end+'\n')
            f.write('RMSval of rmsval: '+str(round(np.sqrt(np.mean(np.array(rmsval)**2)),2))+' and RMSval of rmsper: '+str(round(np.sqrt(np.mean(np.array(rmsper)**2)),2))+'\n')
            f.write('Mean of rmsval: '+str(round(np.mean(rmsval),2))+' and Mean of rmsper: '+str(round(np.mean(rmsper),2))+'\n')
        tts.close()
    elif clust_type == 'all':
        for traintimes in tt:
            val,per,pred,act,ct,uct,ctl,ti = pc.prediction(traintimes,'all',testbed,dep,regs,option)
            f.write('Hours 6 to 18'+'  '+str(len(pred))+'  '+str(len(act))+'  '+str(val)+'  '+str(per)+'  '+str(ct)+'  '+str(uct)+'  '+str(ctl)+'\n')
    f.close()
    return val,per
        
def compare_regression(tt,testbed,depmotes,regmotes,clust_type='interval',option='altitude'):

    #open files
    if testbed == 'NASA':
        savefile = open('results_NASA.txt','a')
        f = open('compreg_NASA.txt','a')
    if testbed == 'Hesse':
        savefile = open('results_Hesse.txt','a')
        f = open('compreg_Hesse.txt','a')
    if testbed == 'NewCitris':
        savefile = open('results_NewCitris.txt','a')
        f = open('compreg_NewCitris.txt','a')
    savefile.write('\n/////START COMPARE REGRESSION/////\n')
    savefile.close()
    f.write('\n/////START COMPARE REGRESSION/////\n')
    f.close()

    #compare regressions using itertools    
    rmserrs=dict()
    if testbed == 'NASA':
        window = ['nasalight8']
    elif testbed == 'Hesse':
        window = ['light1']
    elif testbed == 'NewCitris':
        window = ['light8']
    in_list = regmotes
    out_list = []
    for i in range(0,len(in_list)+1):
        out_list.extend(itertools.combinations(in_list,i))
    for dmote in depmotes:
        validtimes = tt
        if dmote == 'nasalight3':
            validtimes = [1339138800000,1339570800000] #Jun8toJun13(midnight-to-midnight)
        print dmote
        rmserrs[dmote]=[]
        combo = 0
        for reg in out_list:
            combo+=1
            allregs = window + list(reg)
            if combo == int(pow(2,len(regmotes))/2):
                print '...Halfway through Combinations...'
            ic.inversemodel(testbed,dmote,allregs,option)
            val,per = record_error(validtimes,testbed,dmote,allregs,clust_type,option)
            rmserrs[dmote].append([val,per,allregs])
        print 'Number of Regressor Combinations: '+str(combo)

    #close files
    if testbed == 'NASA':
        savefile = open('results_NASA.txt','a')
        f = open('compreg_NASA.txt','a')
    if testbed == 'Hesse':
        savefile = open('results_Hesse.txt','a')
        f = open('compreg_Hesse.txt','a')
    if testbed == 'NewCitris':
        savefile = open('results_NewCitris.txt', 'a')
        f = open('compreg_NewCitris.txt', 'a')
    savefile.write('\n/////COMPLETED COMPARE REGRESSION/////\n')
    savefile.close()
    f.write('\n/////COMPLETED COMPARE REGRESSION/////\n')
    f.close()
    return rmserrs
