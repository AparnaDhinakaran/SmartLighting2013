import time

def make_unix_timestamp(date_string, time_string):
    """This command converts string format of date into unix timstamps."""
    format = '%Y %m %d %H %M %S'
    return time.mktime(time.strptime(date_string + " " + time_string, format))
    
def isLeapYear( year):
    """This command checks if a year is a leap year."""
    if (year % 400 == 0) :
        return True
    elif (year % 100 == 0) :
        return False
    elif (year % 4 == 0):
        return True
    else:
        return False              
  
def daysInMonth(month,year):
    """This command determines the number of days in a month"""
    if (month == 2):
        if (isLeapYear(year)):
            return 29
        else:
            return 28
    elif (month in [1, 3, 5, 7, 8, 10, 12]):
        return 31
    else: 
        return 30
 
def dayInYear(month, day, year):
    """This command determines what day of the year that particular day is."""
    current = 1
    numberOfDays = day
    while (current < month):
        numberOfDays = numberOfDays + daysInMonth(current, year)
        current = current + 1
    return numberOfDays

def arrayofdaysmonthsyears(month1, day1, year1, month2, day2, year2):
    """This code returns the days and months and years in between 2
        different days. It returns them in three different arrays so
        that printing all the days in between 2 days is possible. """
    daysleftinmonth2 = daysInMonth(month2, year2) - day2 + 1
    if year1 == year2:
            if month1 == month2:
                monthsinbetween = 0
            else:
              monthsinbetween= month1 - month2 - 1
    else:
        monthsleftinyear2 = 12 - month2 - 1
        monthsinbetween = monthsleftinyear2 + (12 *(year1 - (year2+1))) + month1
    dayarray = []
    montharray = []
    yeararray= []
    if year1 == year2:
        if month2 == month1:
          currentdays = day1 - day2 + 1
        else:
            currentdays = daysleftinmonth2
    else:
        currentdays = daysleftinmonth2        
    currentday = day2
    currentmonth = month2
    currentyear = year2
    while currentdays > 0:
        dayarray.append(currentday)
        montharray.append(currentmonth)
        yeararray.append(currentyear)
        currentdays = currentdays - 1
        currentday = currentday + 1
    fullmonths = monthsinbetween
    currentmonth = month2 + 1
    while fullmonths > 0:
        if currentmonth > 12:
              currentmonth = 1
              currentyear = currentyear + 1
        daystoadd = daysInMonth(currentmonth, currentyear)
        currentdaytoadd = 1
        while daystoadd > 0:
            dayarray.append(currentdaytoadd)
            montharray.append(currentmonth)
            yeararray.append(currentyear)
            currentdaytoadd = currentdaytoadd + 1
            daystoadd = daystoadd - 1
        currentmonth = currentmonth + 1
        fullmonths = fullmonths - 1
    daysinday1 = day1
    finaldaytoadd = 1
    if month2 != month1 or year1 != year2:
          while daysinday1 > 0:
              dayarray.append(finaldaytoadd)
              montharray.append(month1)
              yeararray.append(year1)
              finaldaytoadd = finaldaytoadd + 1
              daysinday1 = daysinday1 - 1
    return [dayarray, montharray, yeararray]

def arrayofdays(month1,day1,year1,month2,day2,year2):
    """This code returns just the days between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[0]

def arrayofmonths(month1,day1,year1,month2,day2,year2):
    """This code returns just the months between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[1]

def arrayofyears(month1,day1,year1,month2,day2,year2):
    """This code returns just the years between two different dates"""
    return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[2]

