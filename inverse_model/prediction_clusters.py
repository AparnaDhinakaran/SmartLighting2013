import dataProcessing as dP
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

windowsMap = {'NASA': 'nasalight8',
              'Hesse': 'light1',
              'NewCitris': 'light8',
              'NewNasa': 'newnasalight1'}

def prediction(traintimes, cluster, testbed, dependent, regressors, option = 'noaltitude'):

    # Keep track of data
    counted = 0
    uncounted = 0
    countedlim = 0

    # Connect db
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
            
    # Retrieve all regressors and dependent data
    allmotes = [dependent] + regressors
    all_light = dict()
    for mote in allmotes:
        all_light[mote] = []
        if cluster == 'all':
            cursor.execute('SELECT average, unixtime, cluster, altitude FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster>=0' %(mote, traintimes[0], traintimes[1]))
        elif type(cluster) == int:
            cursor.execute('SELECT average, unixtime, cluster, altitude FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster=%d' %(mote, traintimes[0], traintimes[1], cluster))
        else:
            cursor.execute('SELECT average, unixtime, cluster, altitude FROM %s WHERE unixtime>=%f AND unixtime<=%f AND cluster>=%d AND cluster<=%d' %(mote, traintimes[0], traintimes[1], cluster[0], cluster[1]))
        temp = cursor.fetchall()
        for j in temp:
            all_light[mote].append(j)
    alldata = dP.process(all_light, 'all')

    # win_reg data depending on testbed
    win_reg = windowsMap[testbed]
    data = alldata[win_reg]

    # Initialize
    light = []
    unixtime = []
    clust = []
    alt = []
    predicted = []
    actual = []
    time = []
    error = []
    errorper = []
    errorsq = []
    errorpersq = []
    
    # Store data
    for i in data:
        if i[2] != None:
            light.append(i[0])
            unixtime.append(i[1])
            clust.append(i[2])
            alt.append(i[3])

    # Prediction
    countfix=0 #correct predicted appending index when no matches are made
    for count in range(len(light)):
        uncounted+=1 #track
        match = 0
        nomatch = 0
        coeff=[9000000]*len(regressors) #if uncounted (arbitrary large number)
        constant=9000000 #if uncounted  (so that error can be detected when data is uncounted for)
        loc_altA=[] #for when clust matches, but alt is out of range

        # Access coefficients and constants
        openfile = open('results/inverse_model_coefficients_' + testbed + '.txt')
        getdata=openfile.readlines()

        # Option
        if option == 'altitude':
            # Retrieve through looping
            for n in range(len(getdata)):
                dat = str.split(getdata[n])
                if int(round(alt[count])) == int(float(dat[-2])) and int(clust[count]) == int(dat[-1]):
                    counted += 1 #track
                    uncounted -= 1 #track
                    match = 1
                    coeff = [] #reinitialize
                    for k in range(len(dat)-3):
                        coeff.append(float(dat[k]))
                    constant=float(dat[-3])
                elif int(clust[count])==int(dat[-1]):
                    loc_altA.append(int(float(dat[-2])))
            if match == 1:
                loc_altA.append(1000000) #arbitrary large number
                loc_altA.append(-1000000) #so that condition will not be satisfied
            elif len(loc_altA) == 0:
                nomatch = 1
                loc_altA.append(1000000) #arbitrary large number
                loc_altA.append(-1000000) #so that condition will not be satisfied
                
            #regressor data
            regsave=[]
            for reg in regressors:
                regsave.append(alldata[reg][count][0])

            #if uncounted or counted (not for countedlim)
            y=constant
            for m in range(len(regsave)):
                y+=coeff[m]*float(regsave[m])

            #prediction for altitudes greater or less than training altitude range (or out of range for a clust)
            if int(round(alt[count]))>np.max(loc_altA) or int(round(alt[count]))<np.min(loc_altA):
                countedlim+=1 #track
                uncounted-=1 #track
                if len(predicted) == 0:
                    if int(round(alt[count]))>np.max(loc_altA):
                        altlim = np.max(loc_altA)
                    elif int(round(alt[count]))<np.min(loc_altA):
                        altlim = np.min(loc_altA)
                    for n in range(len(getdata)):
                        dat=str.split(getdata[n])
                        if int(altlim)==int(float(dat[-2])) and int(clust[count])==int(dat[-1]):
                            coeff=[]
                            for k in range(len(dat)-3):
                                coeff.append(float(dat[k]))
                            constant=float(dat[-3])
                    y=constant
                    for m in range(len(regsave)):
                        y+=coeff[m]*float(regsave[m])
                else:
                    y=predicted[count-1-countfix]

            #resultant
            if nomatch == 0:
                predicted.append(float(y))
                actual.append(float(alldata[dependent][count][0]))
                time.append(float(alldata[dependent][count][1]))
            elif nomatch == 1:
                uncounted-=1 #track
                countfix+=1 #correct predicted indexing
            openfile.close()
            
        #option
        elif option == 'noaltitude':

            #retrieve coeffs and constant
            for n in range(len(getdata)):
                dat=str.split(getdata[n])
                if int(clust[count])==int(dat[-1]): #get exact (counted)
                    if match == 1:
                        countedlim-=1 #track
                        uncounted+=1 #track
                    counted+=1 #track
                    uncounted-=1 #track
                    match=1
                elif np.floor(int(clust[count])/3) == np.floor(int(dat[-1])/3) and match == 0: #get within half hour (countedlim)
                    countedlim+=1 #track
                    uncounted-=1 #track
                    match=1                
                if match == 1:
                    coeff=[] #reinitialize
                    for k in range(len(dat)-3):
                        coeff.append(float(dat[k]))
                    constant=float(dat[-3])
            if match == 0: #get closest (uncounted decimal)
                curr_diff = float('inf')
                for n in range(len(getdata)):
                    dat=str.split(getdata[n])
                    if abs(int(clust[count])-int(dat[-1])) < curr_diff:
                        line_num = n
                dat=str.split(getdata[line_num])                        
                uncounted+=.0001 #track
                uncounted-=1 #track
                coeff=[] #reinitialize
                for k in range(len(dat)-3):
                    coeff.append(float(dat[k]))
                constant=float(dat[-3])

            #regressor data
            regsave=[]
            for reg in regressors:
                regsave.append(alldata[reg][count][0])

            #if counted
            y=constant
            for m in range(len(regsave)):
                y+=coeff[m]*float(regsave[m])

            #resultant
            predicted.append(float(y))
            actual.append(float(alldata[dependent][count][0]))
            time.append(float(alldata[dependent][count][1]))
            openfile.close()
    
    #smoothing (3 point averaging)
    predictedfinal=list(predicted)
    subsect = [[] for i in range(len(predicted)-2)]
    for count in range(len(subsect)):
        for it in range(3):
            subsect[count].append(predicted[count+it])
        subsect[count] = np.mean(subsect[count])
        predictedfinal[count+1] = subsect[count]

    #errors
    for count in range(len(actual)):
        #print "actual[count], predicted[count]:", actual[count], ", ", predicted[count]
        e=actual[count]-predicted[count]
        eper=e/actual[count]
        error.append(e)
        errorper.append(eper)
        errorsq.append(math.pow(e,2))
        errorpersq.append(math.pow(eper,2))
    rmsvalue=math.sqrt(np.mean(errorsq))
    rmspercent=math.sqrt(np.mean(errorpersq))
    savefile = open('results/results_' + testbed + '.txt', 'a')
    text='\nRMS value error is '+str(rmsvalue)+' and RMS percent error is '+str(rmspercent)+' for '+dependent+' using '+option+' and '+str(regressors)+'\n'
    savefile.write(text)
    savefile.close()
    return round(rmsvalue,2),round(rmspercent,2),predictedfinal,actual,counted,uncounted,countedlim,time


def prediction_hour(traintimes, testbed, dependent, regressors, option='noaltitude'):
    #keep track of data
    counted = 0
    uncounted = 0
    countedlim = 0

    #connect db
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
            
    #retrieve all regressors and dependent data
    allmotes = [dependent] + regressors
    all_light = dict()
    for mote in allmotes:
        all_light[mote] = []
        cursor.execute('SELECT average,unixtime,altitude,hour FROM %s WHERE unixtime>=%f AND unixtime<=%f AND (hour>=18 OR hour<6)' %(mote, traintimes[0],traintimes[1]))
        temp=cursor.fetchall()
        for j in temp:
            all_light[mote].append(j)
    alldata = dP.process(all_light,'all')
    
    #win_reg data depending on testbed
    win_reg = windowsMap[testbed]
    data = alldata[win_reg]

    #initialize
    light = []
    unixtime = []
    hour = []
    alt = []
    predicted = []
    actual = []
    time = []
    error = []
    errorper = []
    errorsq = []
    errorpersq = []

    #store data
    for i in data:
        light.append(i[0])
        unixtime.append(i[1])
        alt.append(i[2])
        hour.append(i[3])

    #prediction
    countfix=0 #correct predicted appending index when no matches are made
    for count in range(len(light)):
        uncounted+=1 #track
        match = 0
        nomatch = 0
        coeff=[1000000]*len(regressors) #if uncounted (arbitrary large number)
        constant=1000000 #if uncounted  (so that error can be detected when data is uncounted for)
        loc_altA=[] #for when hour matches, but alt is out of range

        #access coefficients and constants
        openfile = open('results/inverse_model_coefficients_' + testbed + '.txt')
        getdata=openfile.readlines()

        #option
        if option == 'altitude':

            #retrieve through looping
            for n in range(len(getdata)):
                dat=str.split(getdata[n])
                if int(round(alt[count]))==int(float(dat[-2])) and int(hour[count])==int(dat[-1]):
                    counted+=1 #track
                    uncounted-=1 #track
                    match=1
                    coeff=[] #reinitialize
                    for k in range(len(dat)-3):
                        coeff.append(float(dat[k]))
                    constant=float(dat[-3])
                elif int(hour[count])==int(dat[-1]):
                    loc_altA.append(int(float(dat[-2])))
            if match==1:
                loc_altA.append(1000000) #arbitrary large number
                loc_altA.append(-1000000) #so that condition will not be satisfied
            elif len(loc_altA) == 0:
                nomatch = 1
                loc_altA.append(1000000) #arbitrary large number
                loc_altA.append(-1000000) #so that condition will not be satisfied
                
            #regressor data
            regsave=[]
            for reg in regressors:
                regsave.append(alldata[reg][count][0])

            #if uncounted or counted (not for countedlim)
            y=constant
            for m in range(len(regsave)):
                y+=coeff[m]*float(regsave[m])

            #prediction for altitudes greater or less than training altitude range (or out of range for hour)
            if int(round(alt[count]))>np.max(loc_altA) or int(round(alt[count]))<np.min(loc_altA):
                countedlim+=1 #track
                uncounted-=1 #track
                if len(predicted) == 0:
                    if int(round(alt[count]))>np.max(loc_altA):
                        altlim = np.max(loc_altA)
                    elif int(round(alt[count]))<np.min(loc_altA):
                        altlim = np.min(loc_altA)
                    for n in range(len(getdata)):
                        dat=str.split(getdata[n])
                        if int(altlim)==int(float(dat[-2])) and int(hour[count])==int(dat[-1]):
                            coeff=[]
                            for k in range(len(dat)-3):
                                coeff.append(float(dat[k]))
                            constant=float(dat[-3])
                    y=constant
                    for m in range(len(regsave)):
                        y+=coeff[m]*float(regsave[m])
                else:
                    y=predicted[count-1-countfix]

            #resultant
            if nomatch == 0:
                predicted.append(float(y))
                actual.append(float(alldata[dependent][count][0]))
                time.append(float(alldata[dependent][count][1]))
            elif nomatch == 1:
                uncounted-=1 #track
                countfix+=1 #correct predicted indexing
            openfile.close()
            
        #option
        elif option == 'noaltitude':

            #retrieve coeffs and constant
            for n in range(len(getdata)):
                dat=str.split(getdata[n])
                if int(hour[count])==int(dat[-1]):
                    counted+=1 #track
                    uncounted-=1 #track
                    match=1
                    coeff=[] #reinitialize
                    for k in range(len(dat)-3):
                        coeff.append(float(dat[k]))
                    constant=float(dat[-3])

            #regressor data
            regsave=[]
            for reg in regressors:
                regsave.append(alldata[reg][count][0])

            #if counted
            y=constant
            for m in range(len(regsave)):
                y+=coeff[m]*float(regsave[m])

            #resultant
            predicted.append(float(y))
            actual.append(float(alldata[dependent][count][0]))
            time.append(float(alldata[dependent][count][1]))
            openfile.close()

    #smoothing (3 point averaging)
    predictedfinal=list(predicted)
    subsect = [[] for i in range(len(predicted)-2)]
    for count in range(len(subsect)):
        for it in range(3):
            subsect[count].append(predicted[count+it])
        subsect[count] = np.mean(subsect[count])
        predictedfinal[count+1] = subsect[count]

    #errors
    for count in range(len(actual)):
        e=actual[count]-predicted[count]
        eper=e/actual[count]
        error.append(e)
        errorper.append(eper)
        errorsq.append(math.pow(e,2))
        errorpersq.append(math.pow(eper,2))
    rmsvalue=math.sqrt(np.mean(errorsq))
    rmspercent=math.sqrt(np.mean(errorpersq))
    savefile = open('results/results_' + testbed + '_hour.txt', 'a')
    text='\nRMS value error is '+str(rmsvalue)+' and RMS percent error is '+str(rmspercent)+' for '+dependent+' using '+option+' and '+str(regressors)+'\n'
    savefile.write(text)
    savefile.close()
    return round(rmsvalue,2),round(rmspercent,2),predictedfinal,actual,counted,uncounted,countedlim,time       
