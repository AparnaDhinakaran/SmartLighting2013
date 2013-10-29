import numpy as np
import os
import sqlite3
from collections import Counter
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.integrate import simps

MILLISECONDS_IN_ONE_DAY = 86400000
MILLISECONDS_IN_THIRTY_MINUTES = 1800000
UPPER_THRESHOLD = 600
LOWER_THRESHOLD = 300
    
def gaussPullData(todayUnixTime, table, days):
    """
    Usage:
    >>> gaussPullData(1338966000000, 'nasalight2')
    
    This function pulls light data from the database table TABLE starting DAYS days 
    before TODAYUNIXTIME. It then segments the data when if there are sharp drops in
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
    del pastValues[0]
    
    all_x_data = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    all_x_data = (all_x_data - min(all_x_data))/100000 # scales unixtimes
    all_y_data = np.array([value[1] for value in pastValues]) # gets light values as y values
    
    print "all_x_data: ", all_x_data
    print "all_y_data: ", all_y_data
    
    xdata = []
    ydata = []
    xdata.append([])
    ydata.append([])
    
    runningAverage = all_y_data[0] # assumes all_y_data not empty!!
    
    for i in range(len(all_x_data)):
        if all_y_data[i] < 0.25*runningAverage:
            xdata.append([])
            ydata.append([])
            runningAverage = all_y_data[i]
        else:
            runningAverage = (runningAverage + all_y_data[i]) / 2
        xdata[len(xdata) - 1].append(all_x_data[i])
        ydata[len(ydata) - 1].append(all_y_data[i])
        
    print "xdata: ", xdata
    print "ydata: ", ydata
        
    for i in range(len(xdata)):
        plt.plot(xdata[i], ydata[i], color = 'purple')
        plt.show()
        save(str(i), ext="png", close=True, verbose=False)
    
    #return a list of lists of xdata and ydata (each list is a segment of total data)
    return xdata, ydata

if __name__ == '__main__':
#     for i in range(7):
#         gaussPullData(1339289958000 + (i)*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
    gaussPullData(1339289958000 + (0)*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)