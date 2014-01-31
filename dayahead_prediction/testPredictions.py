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

def simpleLinearRegression(values):
    """
    This function takes a list of data tuples representing previous days' data
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
    # Tomorrow's unixtime
    tomorrow = x[0] + MILLISECONDS_IN_ONE_DAY
    return slope * tomorrow + intercept

def clusterLinearRegression(values):
    """
    Filters values by mode cluster. Then performs a simple linear regression.
    """
    # Returns a list of all the cluster values [0, 0, 1, 1, 1, 1, 1, 3, 4, 5, 5, 5, ...]
    clusterValues = [value[2] for value in values]
    # Find the mode cluster number in the clusterValues list
    mode = findMode(clusterValues)
    # Filter out values with cluster MODE
    filteredValues = [value for value in values if value[2] == mode]
    return simpleLinearRegression(filteredValues)    

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
    print weightValues
    # A list of the light values
    filteredValuesLight = [value[1] for value in filteredValues]
    # Return weighted average of light values
    return np.average(filteredValuesLight, weights = weightValues)

def clusterAlgorithm(values):
    """
    This function returns a weighted average of light values (no filtering by cluster).
    The weights are constructed by frequency of the cluster (if a data value belongs
    in cluster 0, and cluster 0 occurs 50% of the time, the weight of the data value
    is 50.
    """
    clusterMap = dict()
    for value in values:
        if value[2] not in clusterMap.keys():
            clusterMap[value[2]] = []
        clusterMap[value[2]].append(value)
    frequency = [float(len(clusterMap[value[2]])) for value in values]
    total = sum(frequency)
    weightValues = [freq / total for freq in frequency]
    print sum(weightValues)
    lightValues = [value[1] for value in values]
    return np.average(lightValues, weights = weightValues)    
    
def multiClusterAlgorithm(values):
    """
    This function identifies the mode cluster from the last 14 days.
    
    VALUES is a list of tuples. For example:
    [(1338383036000.0, 250.41439403876828, 1), (1338383336000.0, 256.0541434335592, 1), ...]
    """
    clusterMap = dict()
    # Lowest unixtime in the values list
    startUnixtime = values[0][0]
    # Separate values into separate clusters in the map, clusterMap
    for value in values:
        if value[2] not in clusterMap.keys():
            clusterMap[value[2]] = []
        clusterMap[value[2]].append(value)
    
    # An array of the predicted values per cluster
    clusterPredicted = []
    # An array of unixtime averages per cluster
    unixtimeAverage = []
    
    # Generate predicted value for each cluster using a weighted average
    # Adds predicted value for each cluster to clusterPredicted and adds
    # the unixtime average for each cluster to unixtimeAverage
    for key in clusterMap.keys():
        clusterLength = len(clusterMap[key])  
        totalUnixtime = sum([elem[0] for elem in clusterMap[key]])
        unixtimeAverage.append(float(totalUnixtime) / float(clusterLength))
        
        clusterLight = [elem[1] for elem in clusterMap[key]]

        totalDistanceFromStart = sum([elem[0] - startUnixtime for elem in clusterMap[key]])
        clusterWeightValues = [float(elem[0] - startUnixtime) / float(totalDistanceFromStart) for elem in clusterMap[key]]
        
        predicted = np.average(clusterLight, weights = clusterWeightValues)
        clusterPredicted.append(predicted)
    
    print clusterPredicted
    total = sum([elem - startUnixtime for elem in unixtimeAverage])
    # Create weighted values based on unixtime average per cluster
    weightValues = [float(elem - startUnixtime) / float(total) for elem in unixtimeAverage]
    print weightValues
    # Return a weighted average across clusters
    return np.average(clusterPredicted, weights = weightValues)

def weightedAverage(values):
    """
    Returns weighted average of all values (no filtering by cluster).
    """
    # Lowest unixtime in the values list
    startUnixtime = values[0][0]
    # The differences between a data tuple's unixtime and the start unixtime in a list
    unixtimeDiffs = [float(elem[0] - startUnixtime) for elem in values]
    # The sum of all the differences
    total = sum(unixtimeDiffs)
    # A list of weight values
    weightValues = [elem / total for elem in unixtimeDiffs]

    # Creates a list of weights for each filtered value
    # weightValues = [float(value[0]) / float(mostRecentUnixTime) for value in filteredValues]
    # weightValues = [float(index) / float(len(filteredValues)) for index in range(len(filteredValues))]
    # weightValues = [1 - (0.01 * index) for index in range(len(filteredValues))]
    # weightValues = weightValues[::-1]
    print weightValues
    # A list of the light values
    valuesLight = [value[1] for value in values]
    # Return weighted average of light values
    return np.average(valuesLight, weights = weightValues)

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

def average(values):
    lightValues = [value[1] for value in values]
    return np.average(lightValues)

def dayAhead(todayUnixTime, table):
    """
    Usage:
    >>> dayAhead(1338966000000, 'nasalight2')
    
    Returns tomorrow's predicted values in a map (divided by 30 minute time intervals).
    """
    # Pulls the data from past seven days and divides data by 30 minute time interval
    halfHourLight = pullData(todayUnixTime, table, 30)
    
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

def testDayAhead(todayUnixTime, table):
    # Calculates day ahead predictions using the dayAhead function
    predictedValues = dayAhead(todayUnixTime, table)
    
    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    # Calculate unixtime after 24 hours
    tomorrowUnixTime= todayUnixTime + MILLISECONDS_IN_ONE_DAY
    print 'tomorrowUnixTime: ', tomorrowUnixTime, '\n'
    
    sumErrors = 0
    
    for key in range(24):
        cursor.execute('SELECT AVG(light) FROM %s WHERE unixtime <= %d AND unixtime >= %d AND cluster <= %d AND cluster >= %d' %(table, tomorrowUnixTime, todayUnixTime, key * 3 + 2, key * 3))
        realValue = cursor.fetchall()
        print 'predictedValue: ', predictedValues[key]
        print 'realValue: ', realValue[0][0]
        percentError = abs(predictedValues[key] - realValue[0][0]) / realValue[0][0]
        sumErrors += percentError
        print 'Percentage error for key {} is {}.\n'.format(key, percentError)
        
    print 'Average percentage error: ', sumErrors / 24

# Main function (executed when you run the Python script)
if __name__ == '__main__':
    testDayAhead(1339593858000, 'nasalight2')
    # testDayAhead(1339138800000, 'nasalight2')
        
        
        