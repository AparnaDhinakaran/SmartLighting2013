import numpy as np
import os
import sqlite3
import datetime
from time import strftime
from dateutil.parser import parse
from collections import Counter
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.integrate import simps

MILLISECONDS_IN_ONE_DAY = 86400000
MILLISECONDS_IN_THIRTY_MINUTES = 1800000
UPPER_THRESHOLD = 600
LOWER_THRESHOLD = 300

def approxEnergy(xvalues, yvalues):
    adjustedValues = []
    for value in yvalues:
        if value > UPPER_THRESHOLD:
            adjustedValues.append(UPPER_THRESHOLD)
        if value < LOWER_THRESHOLD:
            adjustedValues.append(LOWER_THRESHOLD)
        else:
            adjustedValues.append(value)
    xbar = xvalues[1] - xvalues[0]
    predArea = simps(adjustedValues, dx=xbar) #Probably need to change later, unknown dx
    return predArea
    
def energyError(predx, predy, realx, realy):
    predArea = approxEnergy(predx, predy)
    realArea = approxEnergy(realx, realy)
    return float(abs(predArea - realArea)) / realArea

def gaussPullData(todayUnixTime, table, days):
    # The unixtime from seven DAYS days before TODAYUNIXTIME
    beforeUnixTime = todayUnixTime - (MILLISECONDS_IN_ONE_DAY * days)
    
    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    # Execute a database query which returns rows of data from past seven days
    cursor.execute('SELECT unixtime, light, cluster FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster >= %d' %(table, todayUnixTime, beforeUnixTime, 0))
    
    # pastValues is a list of data tuples from the last seven days.
    # Each tuple looks like: (unixtime, light, cluster)
    pastValues = cursor.fetchall()
    
    if pastValues != None:
        del pastValues[0]
    else:
        raise Exception("EMPTY PAST DATA!")
    
    all_x_data = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    all_x_data = (all_x_data - beforeUnixTime)/100000 # scales unixtimes
    
    all_y_data = np.array([value[1] for value in pastValues]) # gets light values as y values
    
#     plt.plot(all_x_data, all_y_data, color = 'red')
#     plt.show()
    
    #return a list of lists of xdata and ydata (each list is a segment of total data)
    return all_x_data, all_y_data
    
    
def gaussPullDataWithSplit(todayUnixTime, table, days):
    """
    Usage:
    >>> gaussPullData(1338966000000, 'nasalight2')
    
    This function pulls light data from the database table TABLE starting DAYS days 
    before TODAYUNIXTIME. It then segments the data if there are sharp drops in
    light values and returns a list of lists of unixtimes (the x values) and a list 
    of lists of light values (the y values).
    
    NOTE: We intend to run the day ahead predictions once a day starting at midnight.
    """
    
    # The unixtime from seven days before TODAYUNIXTIME
    beforeUnixTime = todayUnixTime - (MILLISECONDS_IN_ONE_DAY * days)
    
    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    # Execute a database query which returns rows of data from past seven days
    cursor.execute('SELECT unixtime, light, cluster FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster >= %d' %(table, todayUnixTime, beforeUnixTime, 0))
    
    # pastValues is a list of data tuples from the last seven days.
    # Each tuple looks like: (unixtime, light, cluster)
    pastValues = cursor.fetchall()
    
    if pastValues != None:
        del pastValues[0]
    else:
        raise Exception("EMPTY PAST DATA!")
    
    all_x_data = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    all_x_data = (all_x_data - beforeUnixTime)/100000 # scales unixtimes
    
    all_y_data = np.array([value[1] for value in pastValues]) # gets light values as y values
    
    xdata = []
    ydata = []
    xdata.append([])
    ydata.append([])
    
    runningAverage = all_y_data[0]
    
    for i in range(len(all_x_data)):
        x = all_x_data[i]
        y = all_y_data[i]
        if y < 0.5*runningAverage:
#             print "splitting data!"
            xdata.append([])
            ydata.append([])
            runningAverage = y
        else:
            runningAverage = (runningAverage + y) / 2
        xdata[len(xdata) - 1].append(x)
        ydata[len(ydata) - 1].append(y)
        
#     print len(xdata)
#     print len(ydata)
        
#     for i in range(len(xdata)):
#         plt.plot(xdata[i], ydata[i], color = 'purple')
        
#     plt.show()
    
    #return a list of lists of xdata and ydata (each list is a segment of total data)
    return xdata, ydata

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def fitGauss(todayUnixTime, table, days):
    # xdata, ydata now a list of lists
    xdata, ydata = gaussPullDataWithSplit(todayUnixTime, table, days)
    
    # An array of the coefficients
    coeff_list = []

    for i in range(len(xdata)):
        a = np.mean(ydata[i])
        m = np.mean(xdata[i])
        s = np.std(xdata[i])
        
        # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
        p0 = [a, m, s]
        
        coeff, var_matrix = curve_fit(gauss, xdata[i], ydata[i], p0=p0, maxfev=5000)
        
        coeff_list.append(coeff)
        
        # Get the fitted curve
        fit_curve = gauss(xdata[i], *coeff)
            
#         plt.plot(xdata[i], ydata[i], label='Measured data', color='black')
#         plt.plot(xdata[i], fit_curve, label='Fitted data', color='red')
#         plt.show()
    
    return coeff_list, xdata

def testDayAhead(todayUnixTime, table, days):
    try:
        coeff_list, xdata = fitGauss(todayUnixTime, table, days)
        tomorrowUnixTime = todayUnixTime + MILLISECONDS_IN_ONE_DAY
    
        # Connect to the database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        realValues = []
        gaussPredictedValues = []
        xvalues = []
    
        for key in range(24):
            cursor.execute('SELECT AVG(light), AVG(unixtime) FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
            dataTuple = cursor.fetchall()
            if dataTuple[0][0] != None:
                xtemp = (dataTuple[0][1] - todayUnixTime)/100000 # - 432??
                # apply the correct coeff! coeff[x] for some x
                for i in range(len(xdata)):
                    times = xdata[i]
                    if times[len(times) - 1] >= ((xtemp - MILLISECONDS_IN_ONE_DAY) / 100000):
                        xvalues.append(xtemp)
                        realValues.append(dataTuple[0][0])
                        gaussPredictedValues.append(gauss(xtemp,*coeff_list[i]))
                        break
            else:
                print 'EMPTY REAL DATA IN TIME INTERVAL %d!' % (key)
        
        #sum up the energy errors for each segment!
        energyErr = energyError(xvalues, gaussPredictedValues, xvalues, realValues)
        
        print 'EnergyError: ', energyErr
        print 'Plotting predicted values versus real values now!'
#         print xvalues
#         plt.plot(xvalues, realValues, color='black')
#         plt.plot(xvalues, gaussPredictedValues, color='green')
#         plt.show()
        
        if energyErr > 0.3: #if it STILL doesn't work, use alternateAlgo
            print 'FAIL! energyErr too high'
            
        return energyErr
     
    # hoping to get rid of runtime errors altogether..       
    except RuntimeError:
        
        print "Gauss RuntimeError!"
        print "Plotting values which caused runtime error..."
        
        pastValues, xdata, ydata = gaussPullData(todayUnixTime, table, days)
        
        plt.plot(xdata, ydata, color='blue')
        plt.show()
        
        return 0
        
def floorMidnight(unix):
    """
    Takes in unixtime (in milliseconds!) UNIX and returns a unixtime (in milliseconds!) of the 
    closest midnight before the given UNIX time.
    """
    midnight_string = datetime.datetime.fromtimestamp(unix/1000).strftime('%Y-%m-%d')
    return int(parse(midnight_string).strftime('%s')) * 1000

if __name__ == '__main__':
    start = floorMidnight(1339289958000)
#     for i in range(7):
#         gaussPullData(start + i*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
#         gaussPullDataWithSplit(start + i*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
#     fitGauss(start + 3*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)'
    totalError = 0.0
    for i in range(10):
        totalError += testDayAhead(start + i*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
    print 'Average error: %f percent' % ((float(totalError) / 7) * 100)
