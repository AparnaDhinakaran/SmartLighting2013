"""Contains the functions which perform day ahead predictions."""

import numpy as np
import sqlite3
from collections import Counter
from scipy import stats

MILLISECONDS_IN_ONE_DAY = 86400000
MILLISECONDS_IN_THIRTY_MINUTES = 1800000

def pullData(todayUnixTime, table, days):
    """
    Usage:
    >>> pullData(1338966000000, 'nasalight2')
    
    This function pulls light data from the database table TABLE starting from seven days 
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

def simpleLinearRegression(values):
    """
    This function takes a list of data tuples representing the last seven days' data
    for a particular 30 minute time interval and returns a predicted value for the
    same 30 minute time interval for the next day using linear regression.
    
    VALUES is a list of tuples. For example:
    [(1338383036000.0, 250.41439403876828, 1), (1338383336000.0, 256.0541434335592, 1), ...]
    """
    # A list of x values (unixtime values)
    x = [value[0] for value in values]
    # A list of y values (light values)
    y = [value[1] for value in values]
    # Use scipy.stats to calculate linear regression values
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    
    tomorrow = x[0] + MILLISECONDS_IN_ONE_DAY
    return slope * tomorrow + intercept

def simpleAlgorithm(values):
    """
    This function identifies the mode cluster from the last 14 days.
    
    VALUES is a list of tuples. For example:
    [(1338383036000.0, 250.41439403876828, 1), (1338383336000.0, 256.0541434335592, 1), ...]
    """
    # Returns a list of all the cluster values [0, 0, 1, 1, 1, 1, 1, 3, 4, 5, 5, 5, ...]
    clusterValues = [value[2] for value in values]
    # Find the mode cluster number in the clusterValues list
    mode = findMode(clusterValues)
    # Filter out values with cluster MODE
    filteredValues = [value for value in values if value[2] == mode]
    # Return weighted average (most recent values get higher weights)
    mostRecentUnixTime = values[len(values) - 1][0]
    # Creates a list of weights for each filtered value
    weightValues = [float(value[0]) / float(mostRecentUnixTime) for value in filteredValues]
    filteredValuesLight = [value[1] for value in filteredValues]
    return np.average(filteredValuesLight, weights = weightValues)

def findMode(list):
    """
    Returns the mode of a list.
    """
    # Use Python's Counter function on the list
    values = Counter(list)
    # Returns the highest occurring item
    return values.most_common(1)[0][0]

"""
ADD MORE ALGORITHMS HERE!
"""

def dayAhead(todayUnixTime, table):
    """
    Usage:
    >>> dayAhead(1338966000000, 'nasalight2')
    
    Returns tomorrow's predicted values in a map (divided by 30 minute time intervals).
    """
    # Pulls the data from past seven days and divides data by 30 minute time interval
    halfHourLight = pullData(todayUnixTime, table, 14)
    
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
        # SWITCH OUT DIFFERENT ALGORITHMS HERE
        #predValue = simpleLinearRegression(halfHourLight[key])
        predValue = simpleAlgorithm(halfHourLight[key])
        predictedValues[key] = predValue
        
    # Return tomorrow's predictedValues in a map.
    return predictedValues

def testDayAhead(todayUnixTime, table):
    # Calculates day ahead predictions using the dayAhead function
    predictedValues = dayAhead(todayUnixTime, table)
    print 'predictedValues: ', predictedValues, '\n'
    
    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    # Calculate unixtime after 24 hours
    tomorrowUnixTime= todayUnixTime + MILLISECONDS_IN_ONE_DAY
    print 'tomorrowUnixTime: ', tomorrowUnixTime, '\n'
    
    for key in range(1, 24):
        cursor.execute('SELECT light FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
        realValue = cursor.fetchall()
        print 'predictedValue: ', predictedValues[key]
        print 'realValue: ', realValue[0][0]
        percentError = abs(predictedValues[key] - realValue[0][0]) / realValue[0][0]
        print 'percentError: ', percentError
        print 'Percentage error for key {} is {}.\n'.format(key, percentError)
    

# Main function (executed when you run the Python script)
if __name__ == '__main__':
    testDayAhead(1339593858000, 'nasalight2')
        
        
        