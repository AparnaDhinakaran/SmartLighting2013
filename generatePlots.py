import numpy as np
import os
import sqlite3
import matplotlib.pyplot as plt
import datetime
from time import strftime
from dateutil.parser import parse

MILLISECONDS_IN_ONE_DAY = 86400000

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
        
def generatePlots(table):

    # Connect to the database
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT MIN(unixtime), MAX(unixtime) FROM %s' % (table))
    unixtimedata = cursor.fetchall()
    minunixtime = unixtimedata[0][0]
    maxunixtime = unixtimedata[0][1]
    
    prev_string = datetime.datetime.fromtimestamp(int(minunixtime/1000)).strftime('%Y-%m-%d')
    prev = int(parse(prev_string).strftime('%s')) * 1000
    
    midnight = prev + MILLISECONDS_IN_ONE_DAY

    while (midnight < maxunixtime):
        cursor.execute('SELECT unixtime FROM %s WHERE unixtime >= %s AND unixtime < %s' % (table, prev, midnight))
        xdata = cursor.fetchall()
        xdata = np.array(xdata)
        xdata = (xdata - prev) / 100000 # Scale the unixtimes
        
        cursor.execute('SELECT light FROM %s WHERE unixtime >= %s AND unixtime < %s' % (table, prev, midnight))
        ydata = cursor.fetchall()
        
        plt.plot(xdata, ydata, color='purple')
        plt.xlabel("Unixtime")
        plt.ylabel("Light Values")
        
        title = datetime.datetime.fromtimestamp(int(prev/1000)).strftime('%Y-%m-%d')
        path = "./" + table + "/" + title
        save(path, ext="png", close=True, verbose=False)
        
        prev = midnight
        midnight += MILLISECONDS_IN_ONE_DAY


if __name__ == '__main__':
    allTables = ['nasalight1','nasalight2','nasalight3','nasalight4','nasalight5','nasalight6','nasalight7','nasalight8','nasalight9','light1','light2','light3','light4','light5','light6','light7','light8','light9','light10']
    for table in allTables:
        generatePlots('nasalight1')

