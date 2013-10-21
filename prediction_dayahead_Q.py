import numpy as np
import sqlite3
from collections import Counter
from scipy import stats
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.integrate import simps

MILLISECONDS_IN_ONE_DAY = 86400000
MILLISECONDS_IN_THIRTY_MINUTES = 1800000

def gaussPullData(todayUnixTime, table, days):
    """
    Usage:
    >>> gaussPullData(1338966000000, 'nasalight2')
    
    This function pulls light data from the database table TABLE starting DAYS days 
    before TODAYUNIXTIME. It then divides the data by 30 minute time intervals and returns
    the divided data in a map.
    
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
    
    xdata = np.array([value[0] for value in pastValues]) # gets unixtimes as x values
    xdata = (xdata - min(xdata))/100000 # scales unixtimes
    ydata = np.array([value[1] for value in pastValues]) # gets light values as y values

    return pastValues, xdata, ydata

def simplePullData(todayUnixTime, table, days):
    """
    Usage:
    >>> pullData(1338966000000, 'nasalight2')
    
    This function pulls light data from the database table TABLE starting DAYS days 
    before TODAYUNIXTIME. It then divides the data by 30 minute time intervals and returns
    the divided data in a map.
    
    NOTE: We intend to run the day ahead predictions once a day starting at midnight.
    """
    
    # Dictionary mapping integers to lists of tuples. The integers represent 30 minute
    # intervals. For example, 1 corresponds to 6:00-6:30AM, 2 corresponds to 6:30-7:00AM, etc.
    # The list of tuples contain the data for the corresponding time interval.
    # There will be about 42 values (7 days * 6 values per day) in each list.
    # Ex:
    # halfHourLight = {
    #     0: [(1338383036000.0, 250.41439403876828, 1), (1338383336000.0, 256.0541434335592, 1), ...],
    #     1: [(1338384836000.0, 265.60950866355495, 3), (1338385136000.0, 268.44930083522434, 3), ...],
    #     ....
    #     23: [....]
    # }
    halfHourLight = dict()
    
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
    
    # For each value from the last seven days, place it in the correct 30 minute time interval.
    # We do this by looking at the cluster value in the tuple.
    # Clusters 0, 1, 2 map to 6:00-6:30AM,
    # Clusters 3, 4, 5 map to 6:30-7:00AM, etc.
    for tup in pastValues:
        key = tup[2] // 3
        if not key in halfHourLight.keys():
            halfHourLight[key] = []
        halfHourLight[key].append(tup)
        
    # Return the divided data as a map
    return halfHourLight

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))


def fitGauss(todayUnixTime, table, days):
    pastValues, xdata, ydata = gaussPullData(todayUnixTime, table, days)
    a = np.mean(ydata)
    m = np.mean(xdata)
    s = np.std(xdata)
    
    # p0 is the initial guess for the fitting coefficients (A, mu and sigma above)
    p0 = [a, m, s]
    
    coeff, var_matrix = curve_fit(gauss, xdata, ydata, p0=p0, maxfev=5000)
    	
    # Get the fitted curve
    fit_curve = gauss(xdata, *coeff)
    	
    plt.plot(xdata, ydata, label='Measured data', color='black')
    plt.plot(xdata, fit_curve, label='Fitted data', color='red')
    print 'Fitted mean = ', coeff[1]
    print 'Fitted standard deviation = ', coeff[2]
    
    plt.show()
    
    return coeff, xdata
    
def simpleAlgorithm(values):
    """
    This function identifies the mode cluster from previous days. It then filters out previous
    days' data which are not part of the mode cluster. The remaining data are weighted by
    how close they are to the current time. The prediction returned is the weighted average
    of this remaining data.
    
    VALUES is a list of tuples. For example:
    [(1338383036000.0, 250.41439403876828, 1), (1338383336000.0, 256.0541434335592, 1), ...]
    """
    # Returns a list of all the cluster values [0, 0, 1, 1, 1, 1, 1, 3, 4, 5, 5, 5, ...]
    clusterValues = [value[2] for value in values]
    # Find the mode cluster number in the clusterValues list
    mode = findMode(clusterValues)
    # Filter out values with cluster MODE
    filteredValues = [value for value in values if value[2] == mode]
    # Lowest unixtime in the values list
    startUnixtime = values[0][0]
    # The differences between a data tuple's unixtime and the start unixtime in a list
    unixtimeDiffs = [float(elem[0] - startUnixtime) for elem in filteredValues]
    # The sum of all the differences
    total = sum(unixtimeDiffs)
    # A list of weight values
    weightValues = [elem / total for elem in unixtimeDiffs]

    # Creates a list of weights for each filtered value
    # weightValues = [float(value[0]) / float(mostRecentUnixTime) for value in filteredValues]
    # weightValues = [float(index) / float(len(filteredValues)) for index in range(len(filteredValues))]
    # weightValues = [1 - (0.01 * index) for index in range(len(filteredValues))]
    # weightValues = weightValues[::-1]
    # A list of the light values
    filteredValuesLight = [value[1] for value in filteredValues]
    # Return weighted average of light values
    return np.average(filteredValuesLight, weights = weightValues)

def findMode(list):
    """
    Returns the mode of a list.
    """
    # Use Python's Counter function on the list
    values = Counter(list)
    # Returns the highest occurring item
    return values.most_common(1)[0][0]
    
def approxEnergy(xvalues, yvalues):
    UPPER_THRESHOLD = 600
    LOWER_THRESHOLD = 300
    adjustedValues = []
    for value in yvalues:
        if value > 600:
            adjustedValues.append(600)
        if value < 300:
            adjustedValues.append(300)
        else:
            adjustedValues.append(value)
    xrange = xvalues[len(xvalues) - 1] - xvalues[0]
    xbar = xvalues[1] - xvalues[0]
    predArea = simps(adjustedValues, dx=xbar) #Probably need to change later, unknown dx
    return predArea
    
def energyError(predx, predy, realx, realy):
    predArea = approxEnergy(predx, predy)
    realArea = approxEnergy(realx, realy)
    return float(abs(predArea - realArea)) / realArea

def dayAhead(todayUnixTime, table):
    """
    Usage:
    >>> dayAhead(1338966000000, 'nasalight2')
    
    Returns tomorrow's predicted values in a map (divided by 30 minute time intervals).
    """
    # Pulls the data from past seven days and divides data by 30 minute time interval
    halfHourLight = simplePullData(todayUnixTime, table, 30)
    
    # Dictionary containing tomorrow's predicted values. Maps integers representing
    # 30 minute time intervals to tomorrow's predicted value for the corresponding
    # 30 minute time interval.
    predictedValues = dict()
    
    # Connect to the database (later we will store values into database)
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    # For each 30 minute interval (there are 24 of them), run the algorithm on the
    # values from the last seven days. Then, add the predicted value to the
    # predictedValues map.
    for key in range(24):
        """simpleAlgorithm works best so far!!!"""
        # SWITCH OUT DIFFERENT ALGORITHMS HERE
        # predValue = simpleLinearRegression(halfHourLight[key])
        predValue = simpleAlgorithm(halfHourLight[key])
        # predValue = multiClusterAlgorithm(halfHourLight[key])
        # predValue = weightedAverage(halfHourLight[key])
        # predValue = clusterLinearRegression(halfHourLight[key])
        # predValue = clusterAlgorithm(halfHourLight[key])
        # predValue = average(halfHourLight[key])
        predictedValues[key] = predValue
        
    # Return tomorrow's predictedValues in a map.
    return predictedValues
    
def testDayAhead(todayUnixTime, table, days):
    try:
        coeff, xdata = fitGauss(todayUnixTime, table, days)
        tomorrowUnixTime = todayUnixTime + MILLISECONDS_IN_ONE_DAY
    
        # Connect to the database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        realValues = [0]*24 # initializes an array of 24 zero's
        gaussPredictedValues = [0]*24
        xvalues = []
    
        for key in range(24):
            cursor.execute('SELECT AVG(light), AVG(unixtime) FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
            dataTuple = cursor.fetchall()
            if dataTuple[0][0] != None:
                realValues[key] = dataTuple[0][0]
                xtemp = ((dataTuple[0][1] - todayUnixTime) / 100000) - 432
                xvalues.append(xtemp)
                gaussPredictedValues[key] = gauss(xtemp,*coeff)
        
        energyErr = energyError(xvalues, gaussPredictedValues, xvalues, realValues)
        
        print 'EnergyError: ', energyErr
        print 'Plotting predicted values versus real values now!'
        print xvalues
        plt.plot(xvalues, realValues, color='black')
        plt.plot(xvalues, gaussPredictedValues, color='green')
        plt.show()
        
        if energyErr > 0.3:
            # Calculates day ahead predictions using the dayAhead function
            predictedValues = dayAhead(todayUnixTime, table)
            
            # Connect to the database
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
             
            # Calculate unixtime after 24 hours
            tomorrowUnixTime= todayUnixTime + MILLISECONDS_IN_ONE_DAY
             
            sumErrors = 0
             
            for key in range(24):
                cursor.execute('SELECT AVG(light) FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
                dataTuple = cursor.fetchall()
                percentError = abs(predictedValues[key] - dataTuple[0][0]) / dataTuple[0][0]
                sumErrors += percentError
                print 'Percentage error for key {} is {}.\n'.format(key, percentError)
                 
            print 'Average percentage error: ', sumErrors / 24
            
            
    except RuntimeError:
        
        print "Gauss RuntimeError!"
        
        pastValues, xdata, ydata = gaussPullData(todayUnixTime, table, days)
        
        plt.plot(xdata, ydata, color='blue') # funny week
        plt.show()
#         # Calculates day ahead predictions using the dayAhead function
#         predictedValues = dayAhead(todayUnixTime, table)
#         
#         # Connect to the database
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#          
#         # Calculate unixtime after 24 hours
#         tomorrowUnixTime= todayUnixTime + MILLISECONDS_IN_ONE_DAY
#          
#         sumErrors = 0
#          
#         for key in range(24):
#             cursor.execute('SELECT AVG(light) FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
#             dataTuple = cursor.fetchall()
#             percentError = abs(predictedValues[key] - dataTuple[0][0]) / dataTuple[0][0]
#             sumErrors += percentError
#             print 'Percentage error for key {} is {}.\n'.format(key, percentError)
#              
#         print 'Average percentage error: ', sumErrors / 24
        
	
# Main function (executed when you run the Python script)
if __name__ == '__main__':
#     for i in range(7):
#         testDayAhead(1339289958000 + (i)*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
        #testDayAhead(1339138800000 + (i)*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)
    testDayAhead(1339289958000 + (0)*MILLISECONDS_IN_ONE_DAY, 'nasalight2', 1)

