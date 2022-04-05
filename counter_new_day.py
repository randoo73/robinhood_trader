# %M = Minutes
# %d = two digit day of month

# Creat a txt  or csv file to store the transactionCounter Number in.
# It appears to count ok through each run, but resets between runs.
# Create a way to recall the old number from the external file to continue the days increment.
# Need to make sure the counter starts over at the start of the new day.

import datetime
from time import sleep
import sqlite3



def transactionCounter():
    counter = 0
    today = 0
    transactionNumber = 0
    
    # Get the day number
    getDateTime = datetime.datetime.now()
    todaysDate = (getDateTime.strftime("%Y%m%d"))
    todaysDateInt = int(todaysDate)
    
    # Open the database
    connection = sqlite3.connect('stocks.db')
    cursor = connection.cursor()
    
    # Get the largest number in the Transaction Number column
    openMax = '''SELECT MAX(Transaction_Number) FROM Open_Orders'''
    closedMax = '''SELECT MAX(Transaction_Number) FROM Closed_Orders'''
    cursor.execute(openMax)
    openMaxResult = cursor.fetchone()[0]
    if(openMaxResult is None):
        openMaxResult = 100000000
    #print(openMaxResult)
    openMaxStr = str(openMaxResult)
    
    cursor.execute(closedMax)
    closedMaxResult = cursor.fetchone()[0]
    if(closedMaxResult is None):
        closedMaxResult = 100000000
    closedMaxStr = str(closedMaxResult)
    
    if(openMaxResult > closedMaxResult):
        day = int(openMaxStr[:8])
        #print("Day = ", day)
        #print(type(day))
        #print("Todays Date = ", todaysDateInt)
        #print(type(todaysDateInt))

        if(day == todaysDateInt):
            transactionNumber = openMaxResult + 1
            print("Test1", transactionNumber)
            return transactionNumber
        else:
            transactionNumber = int(todaysDate + "0001")
            print("Test2", transactionNumber)
            return transactionNumber
    else:
        day = int(closedMaxStr[:8])
        #print("Day = ", day)
        #print("Todays Date = ", todaysDate)

        if(day == todaysDate):
            transactionNumber = closedMaxResult + 1
            print("Test3", transactionNumber)
            return transactionNumber
        else:
            transactionNumber = int(todaysDate + "0001")
            print("Test4", transactionNumber)
            return transactionNumber
        
transactionCounter()