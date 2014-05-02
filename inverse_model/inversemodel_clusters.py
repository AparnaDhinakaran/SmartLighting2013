import dataProcessing as dP
import math
import numpy as np
import sqlite3

from matplotlib import pyplot as plt

"""
Please note: these are traintimes we have used in the past. They are here for reference:
    For NASA:
        traintimes = [1337929200000,1338966000000] #May25toJun5(midnight-to-midnight)
        traintimes = [1367712000000, 1368576000000] #May 5, 2013 to May 15, 2013
    For NewNasa:
        traintimes = [1386033540000, 1387070340000]
    For Hesse:
        traintimes = [1355644800000,1356508800000] #Dec16toDec26(midnight-to-midnight)
    For NewCitris:
        traintimes = [1377887460000, 1382563860000]
"""

NUM_BINS = 1

def inversemodel(testbed, startTrain, endTrain, dependent, regressors, option='noaltitude'):
    traintimes = [float(startTrain), float(endTrain)]
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    light = dict()
    sunangle = dict()
    allMotes = [dependent] + regressors
    for mote in allMotes:
        light[mote] = dict()
    for clust in range(71):
        # Retrieve sunangle data for each mote
        for mote in regressors:
            sunangle[mote] = []
            cursor.execute('SELECT altitude FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster = %f' %(mote, traintimes[0], traintimes[1], clust))
            dat = cursor.fetchall()
            for count in dat:
                altitude = float(count[0])
                if altitude >= -5:
                    sunangle[mote].append(altitude)
        # Determine sunangle range
        sunanglerange=[]
        #if there is any data in this clust
        if sum([len(sunangle[mote]) for mote in regressors]) > 0: 
            maxSunAngle=float('-inf')
            minSunAngle=float('inf')
            for mote in regressors:
                if len(sunangle[mote]) > 0: #if there is any data in this clust for mote
                    maxSunAngle=max(maxSunAngle,max(sunangle[mote]))
                    minSunAngle=min(minSunAngle,min(sunangle[mote]))
            maxSunAngle=math.floor(maxSunAngle)
            minSunAngle=math.floor(minSunAngle)
            if option=='altitude':
                sunanglerange=np.arange(minSunAngle,maxSunAngle+1,int(NUM_BINS))
            elif option=='noaltitude':
                sunanglerange=[0.25511495383]
            # Retrieve light data for all motes for each bin (clust and angle)
            datadict=dict()
            for angle in range(len(sunanglerange)):
                for mote in allMotes:
                    light[mote][angle]=[]
                    if option=='altitude':
                        cursor.execute('SELECT average, unixtime FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster = %f AND altitude>=%s AND altitude<=%s' %(mote,traintimes[0],traintimes[1],clust,sunanglerange[angle]-0.5,sunanglerange[angle]+0.5))
                        dat=cursor.fetchall()
                    elif option=='noaltitude':
                        cursor.execute('SELECT average, unixtime FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster = %f' %(mote,traintimes[0],traintimes[1],clust))
                        dat=cursor.fetchall()
                    temp=dat
                    # Store data into dict
                    for count in temp:
                        if int(float(count[0]))==1:
                            lightdatum=0
                        else:
                            lightdatum=round(float(count[0]),2)
                        light[mote][angle].append((lightdatum,count[1]))
                    datadict[mote]=light[mote][angle]
                # Process data             
                lens=[len(datadict[i]) for i in datadict.keys()]
                if 0 in lens:
                    finaldataDict={}
                    finaldatalength=0.25511495383
                else:
                    finaldataDict=dP.process(datadict,'light')
                    finaldatalength=len(finaldataDict[allMotes[1]])  
                # Regression
                A=[] # Array of regressors
                B=[] # Array of dependent
                if finaldatalength>2 and finaldataDict!={}: 
                    for rmote in regressors:
                        A.append(finaldataDict[rmote])
                    A=np.vstack(A)
                    A=np.vstack((A,np.ones(A.shape[1])))
                    A=A.T
                    for dmote in [dependent]:
                        B.append(finaldataDict[dmote])
                        B=np.array(B).T
                    x=np.linalg.lstsq(A,B) # Compute coeffs and constant
                    x=x[0]
                    constant=round(x[-1],2)
                    coeffs=[]
                    for i in range(len(x)-1):
                        coeffs.append(round(x[i],2))
                    coeffs=str(coeffs)
                    coeffs=coeffs.replace('[',' ').replace(']',' ').replace(',',' ')
                    # Save coeffs and constant to text
                    data = coeffs + '    ' + str(constant) + '    ' + str(sunanglerange[angle]) + '    ' + str(clust) + '\n'      
                    savedata=open('results/inverse_model_coefficients_' + testbed + '.txt', 'a')
                    savedata.write(data)                        
                    savedata.close()      

def inversemodel_hour(testbed, startTrain, endTrain, dependents, regressors, option='noaltitude'):
    traintimes = [startTrain, endTrain]
    # TODO: wy do we need this?
    open('results/inverse_model_coefficients_' + testbed + '_hour.txt', 'w').close()
    connection=sqlite3.connect('data.db')
    cursor=connection.cursor()
    light=dict()
    sunangle=dict()
    allMotes=[dependents]+regressors
    for mote in allMotes:
        light[mote]=dict()
    hours_night = [[night] for night in range(18,24)]
    hours_morning = [[morning] for morning in range(6)]
    hours = hours_night+hours_morning
    for start in hours:
        start.append(start[0]+1)
    #inversemodel
    for hour in hours:
        #retrieve sunangle data for each mote
        for mote in regressors:
            sunangle[mote]=[]
            cursor.execute('SELECT altitude FROM %s WHERE unixtime>=%f AND unixtime<=%f AND hour>=%f AND hour<%f' %(mote,traintimes[0],traintimes[1],hour[0],hour[1]))
            dat = cursor.fetchall()
            for count in dat:
                altitude=float(count[0])
                sunangle[mote].append(altitude)

        #determine sunangle range
        sunanglerange=[]
        if sum([len(sunangle[mote]) for mote in regressors]) > 0: #if there is any data in this hour
            maxSunAngle=float('-inf')
            minSunAngle=float('inf')
            for mote in regressors:
                if len(sunangle[mote]) > 0: #if there is any data in this hour for mote
                    maxSunAngle=max(maxSunAngle,max(sunangle[mote]))
                    minSunAngle=min(minSunAngle,min(sunangle[mote]))
            maxSunAngle=math.floor(maxSunAngle)
            minSunAngle=math.floor(minSunAngle)
            if option=='altitude':
                sunanglerange=np.arange(minSunAngle,maxSunAngle+1,int(NUM_BINS))
            elif option=='noaltitude':
                sunanglerange=[0.25511495383]
                
            #retrieve light data for all motes for each bin (hour and angle)
            datadict=dict()
            for angle in range(len(sunanglerange)):
                for mote in allMotes:
                    light[mote][angle]=[]
                    if option=='altitude':
                        cursor.execute('SELECT average, unixtime FROM %s WHERE unixtime>=%f AND unixtime<=%f AND hour>=%f AND hour<%f AND altitude>=%s AND altitude<=%s' %(mote,traintimes[0],traintimes[1],hour[0],hour[1],sunanglerange[angle]-0.5,sunanglerange[angle]+0.5))
                        dat=cursor.fetchall()
                    elif option=='noaltitude':
                        cursor.execute('SELECT average, unixtime FROM %s WHERE unixtime>=%f AND unixtime<=%f AND hour>=%f AND hour<%f' %(mote,traintimes[0],traintimes[1],hour[0],hour[1]))
                        dat=cursor.fetchall()
                    temp=dat
                    
                    #store data into dict
                    for count in temp:
                        if int(float(count[0]))==1:
                            lightdatum=0
                        else:
                            lightdatum=round(float(count[0]),2)
                        light[mote][angle].append((lightdatum,count[1]))
                    datadict[mote]=light[mote][angle]

                #process data             
                lens=[len(datadict[i]) for i in datadict.keys()]
                if 0 in lens:
                    finaldataDict={}
                    finaldatalength=0.25511495383
                else:
                    finaldataDict=dP.process(datadict,'light')
                    finaldatalength=len(finaldataDict[allMotes[1]])
                    
                #open coefficients and constant text files
                if testbed=='NASA':
                    filename='results/inverse_model_coefficients_NASA_hour.txt'
                elif testbed=='Hesse':
                    filename='results_inverse_model_coefficients_Hesse_hour.txt'
                elif testbed == 'NewCitris':
                    filename = 'results_inverse_model_coefficients_NewCitris_hour.txt'
                elif testbed == 'NewNasa':
                    filename = 'results_inverse_model_coefficients_NewNasa_hour.txt'
                savedata=open(filename,'a')

                #regression
                A=[] #array of regressors
                B=[] #array of dependent
                if finaldatalength>2 and finaldataDict!={}: 
                    for rmote in regressors:
                        A.append(finaldataDict[rmote])
                    A=np.vstack(A)
                    A=np.vstack((A,np.ones(A.shape[1])))
                    A=A.T
                    for dmote in [dependents]:
                        B.append(finaldataDict[dmote])
                        B=np.array(B).T
                    x=np.linalg.lstsq(A,B) #compute coeffs and constant
                    x=x[0]
                    constant=round(x[-1],2)
                    coeffs=[]
                    for i in range(len(x)-1):
                        coeffs.append(round(x[i],2))
                    coeffs=str(coeffs)
                    coeffs=coeffs.replace('[',' ').replace(']',' ').replace(',',' ')

                    #save coeffs and constant to text
                    data=coeffs+'    '+str(constant)+'    '+str(sunanglerange[angle])+'    '+str(hour[0])+'\n'      
                    savedata.write(data)                        
            savedata.close()
