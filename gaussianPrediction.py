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

startTestTimes = {'light1': 1355632459000, 'light2': 1355628435000, 'light3': 1355628599000, 'light4': 1355628673000}

#taken from http://www.jesshamrick.com/2012/09/03/saving-figures-from-pyplot/
def save(path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.
 
    Parameters
    ----------
    path : string
        The path (and filename, without the extension) to save the
        figure to.
 
    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.
 
    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.
 
    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.
 
    """
    
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'
 
    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
 
    # The final path to save to
    savepath = os.path.join(directory, filename)
 
    if verbose:
        print("Saving figure to '%s'..." % savepath),
 
    # Actually save the figure
    plt.savefig(savepath)
    
    # Close it
    if close:
        plt.close()
 
    if verbose:
        print("Done")

def approxEnergy(xvalues, yvalues):
    adjustedValues = []
    for value in yvalues:
        if value > UPPER_THRESHOLD:
            adjustedValues.append(UPPER_THRESHOLD)
        if value < LOWER_THRESHOLD:
            adjustedValues.append(LOWER_THRESHOLD)
        else:
            adjustedValues.append(value)
    if len(xvalues) > 1:
        xbar = xvalues[1] - xvalues[0]
        predArea = simps(adjustedValues, dx=xbar) #Probably need to change later, unknown dx
    else:
        predArea = 0
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
    cursor.execute('SELECT unixtime, light, cluster FROM %s WHERE unixtime < %d AND unixtime >= %d AND cluster >= %d' %(table, todayUnixTime, beforeUnixTime, 0))
    
    # pastValues is a list of data tuples from the last seven days.
    # Each tuple looks like: (unixtime, light, cluster)
    pastValues = cursor.fetchall()
    
    all_x_data = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    all_x_data = (all_x_data - beforeUnixTime)/100000 # scales unixtimes
    
    all_y_data = np.array([value[1] for value in pastValues]) # gets light values as y values
    
    plt.plot(all_x_data, all_y_data, color = 'red')
    # plt.show()
    plt.xlabel("Unixtime")
    plt.ylabel("Light Values")
    
    title = datetime.datetime.fromtimestamp(int(todayUnixTime/1000)).strftime('%Y-%m-%d')
    path = "./" + table + "/" + title + "_gauss_runtime_error"
    save(path, ext="png", close=True, verbose=False)
    
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
    cursor.execute('SELECT unixtime, light, cluster FROM %s WHERE unixtime < %d AND unixtime >= %d AND cluster >= %d' %(table, todayUnixTime, beforeUnixTime, 0))
    
    # pastValues is a list of data tuples from the last seven days.
    # Each tuple looks like: (unixtime, light, cluster)
    pastValues = cursor.fetchall()
    
    all_x_data = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    all_x_data = (all_x_data - beforeUnixTime)/100000 # scales unixtimes
    
    all_y_data = np.array([value[1] for value in pastValues]) # gets light values as y values
    
    xdata = []
    ydata = []
    xdata.append([])
    ydata.append([])
    
    if len(all_x_data) > 0:
        runningAverage = all_y_data[0]
        
        for i in range(len(all_x_data)):
            x = all_x_data[i]
            y = all_y_data[i]
            if y < 0.5*runningAverage:
                print "splitting data!"
                xdata.append([])
                ydata.append([])
                runningAverage = y
            else:
                runningAverage = (runningAverage + y) / 2
            xdata[len(xdata) - 1].append(x)
            ydata[len(ydata) - 1].append(y)
            
              
        for i in range(len(xdata)):
            plt.plot(xdata[i], ydata[i], color = 'purple')
            print xdata[i]
            print ydata[i]
          
    # plt.show()
    plt.xlabel("Unixtime")
    plt.ylabel("Light Values")
    
    title = datetime.datetime.fromtimestamp(int(todayUnixTime/1000)).strftime('%Y-%m-%d')
    path = "./" + table + "/" + title + "_prevday"
    save(path, ext="png", close=True, verbose=False)
    
    #return a list of lists of xdata and ydata (each list is a segment of total data)
    return xdata, ydata

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def fitGauss(todayUnixTime, table, days):
    # xdata, ydata now a list of lists
    xdata, ydata = gaussPullDataWithSplit(todayUnixTime, table, days)
    
    # Since gaussPullDataWithSplit might return [[]], [[]] if there was no data from previous day
    if len(xdata[0]) > 0:
    
        # An array of the coefficients
        coeff_list = []
        filtered_xdata = []
    
        for i in range(len(xdata)):
            a = np.mean(ydata[i])
            m = np.mean(xdata[i])
            s = np.std(xdata[i])
            
            # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
            p0 = [a, m, s]
            
            try:
                coeff = curve_fit(gauss, xdata[i], ydata[i], p0=p0, maxfev=5000)[0] # TypeError or RuntimeError
                
                coeff_list.append(coeff)
                filtered_xdata.append(xdata[i])
                
                # Get the fitted curve
                fit_curve = gauss(xdata[i], *coeff)
                    
                plt.plot(xdata[i], ydata[i], label='Measured data', color='black')
                plt.plot(xdata[i], fit_curve, label='Fitted data', color='blue')
                
                plt.xlabel("Unixtime")
                plt.ylabel("Light Values")
                
                title = datetime.datetime.fromtimestamp(int(todayUnixTime/1000)).strftime('%Y-%m-%d')
                path = "./" + table + "/" + title + "_split" + str(i)
                save(path, ext="png", close=True, verbose=False)
                
            except TypeError:
                print "TypeError for split %d!" % (i)
                continue
            
            except RuntimeError:
                 
                print "Gauss RuntimeError for split %d!" % (i)
                 
                continue
        
        return coeff_list, filtered_xdata
    
    else:
        return [], []

def testDayAhead(todayUnixTime, table, days):
#     try:
    coeff_list, xdata = fitGauss(todayUnixTime, table, days)
    if len(xdata) > 0:
        tomorrowUnixTime = todayUnixTime + MILLISECONDS_IN_ONE_DAY
    
        # Connect to the database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        realValues = []
        gaussPredictedValues = []
        xvalues = []
    
        for key in range(24):
            cursor.execute('SELECT AVG(light), AVG(unixtime) FROM %s WHERE unixtime < %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
            dataTuple = cursor.fetchall()
            if dataTuple[0][0] != None:
                xtemp = (dataTuple[0][1] - todayUnixTime)/100000 # - 432??
                # apply the correct coeff! coeff[x] for some x
                for i in range(len(xdata)):
                    times = xdata[i]
                    if times[len(times) - 1] >= ((xtemp - MILLISECONDS_IN_ONE_DAY) / 100000):
                        xvalues.append(xtemp)
                        realValues.append(dataTuple[0][0])
                        gaussPredictedValues.append(gauss(xtemp,*coeff_list[i])) # this may give runtime error
                        break
            else:
                print 'EMPTY REAL DATA IN TIME INTERVAL %d!' % (key)
        
        if len(realValues) > 1:
            #sum up the energy errors for each segment!
            energyErr = energyError(xvalues, gaussPredictedValues, xvalues, realValues)
            
            print 'EnergyError: ', energyErr
            
            if energyErr > 0.3: #if it STILL doesn't work, use alternateAlgo
                print 'FAIL! energyErr too high'
                plt.plot(xvalues, realValues, color='black')
                plt.plot(xvalues, gaussPredictedValues, color='red')
            else:
                plt.plot(xvalues, realValues, color='black')
                plt.plot(xvalues, gaussPredictedValues, color='green')
                # plt.show()
                
            plt.xlabel("Unixtime")
            plt.ylabel("Light Values")
            
            title = datetime.datetime.fromtimestamp(int(todayUnixTime/1000)).strftime('%Y-%m-%d')
            path = "./" + table + "/" + title + "_predicted_vs_real"
            save(path, ext="png", close=True, verbose=False)
        
            return energyErr
        else:
            print 'NOT ENOUGH REAL DATA!'

            plt.xlabel("Unixtime")
            plt.ylabel("Light Values")
            title = datetime.datetime.fromtimestamp(int(todayUnixTime/1000)).strftime('%Y-%m-%d')
            path = "./" + table + "/" + title + "_predicted_vs_real"
            save(path, ext="png", close=True, verbose=False)
            
            return 0
        
    else:
        return 0

        
def floorMidnight(unix):
    """
    Takes in unixtime (in milliseconds!) UNIX and returns a unixtime (in milliseconds!) of the 
    closest midnight before the given UNIX time.
    """
    midnight_string = datetime.datetime.fromtimestamp(int(unix)/1000).strftime('%Y-%m-%d')
    return int(parse(midnight_string).strftime('%s')) * 1000

def testTable(table):
    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT MIN(unixtime), MAX(unixtime) FROM %s' % (table))
    unixtimedata = cursor.fetchall()
    minunixtime = unixtimedata[0][0]
    maxunixtime = unixtimedata[0][1]
    
#     prev = floorMidnight(minunixtime)
#     print prev
#     
#     midnight = prev + MILLISECONDS_IN_ONE_DAY 
    
    midnight = floorMidnight(startTestTimes[table])
    
    daysToTest = 5
    
    totalError = 0.0
    
#     while midnight < maxunixtime:
    for i in range(daysToTest):
        totalError += testDayAhead(midnight, table, 1)
        midnight += MILLISECONDS_IN_ONE_DAY
        
    print 'Average error for %s over %d days: %f percent' % (table, daysToTest, (float(totalError) / daysToTest) * 100)
          

if __name__ == '__main__':
    allTables = ['light1']#, 'light2', 'light3', 'light4']#, 'light2', 'light3', 'light4']#,'light5','light6','light7','light8','light9','light10']
    for table in allTables:
        testTable(table)
        
