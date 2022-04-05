import datetime
import shutil
from counter_new_day import transactionCounter
import sqlite3


########################################################

def database_buy(stockSymbol, currentPriceFloat, roundedSharesBought, ownedShareFloat, transactionCost):
    
    getDateTime = datetime.datetime.now()
    transactionDate = getDateTime.strftime("%Y-%m-%d")
    # transactionDate = datetime('now', 'localtime')
    

    connection = sqlite3.connect('stocks.db')

    cursor = connection.cursor()

    stock_table = '''CREATE TABLE IF NOT EXISTS Open_Orders(
    Transaction_Number INTEGER NOT NULL PRIMARY KEY,
    Transaction_Date DATE,
    Stock_Symbol TEXT,
    Share_Price REAL,
    Share_Quantity REAL,
    Shares_Owned REAL,
    Transaction_Cost REAL
    )'''

    cursor.execute(stock_table)
    
    connection.commit()
    
    connection.close()

    # Generate the Transaction Number for the Database
    transactionNumber = transactionCounter()
    
# Re-open table to apply changes
    connection = sqlite3.connect('stocks.db')

    cursor = connection.cursor()

    cursor.execute('''INSERT INTO Open_Orders (
    Transaction_Number,
    Transaction_Date,
    Stock_Symbol,
    Share_Price,
    Share_Quantity,
    Shares_Owned,
    Transaction_Cost
    )
    VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
    )''',(
        transactionNumber,
        transactionDate,
        stockSymbol,
        currentPriceFloat,
        roundedSharesBought,
        ownedShareFloat,
        transactionCost
        )
        )

    connection.commit()
    
    connection.close()
    
########################################################

def database_sell(stockSymbol, currentPriceFloat, roundedSharesSold, transactionCost):

    getDateTime = datetime.datetime.now()
    transactionDate = getDateTime.strftime("%Y-%m-%d")
    # transactionDate = datetime('now', 'localtime')
    
    connection = sqlite3.connect('stocks.db')

    cursor = connection.cursor()
    
    stock_table = '''CREATE TABLE IF NOT EXISTS Closed_Orders(
    Transaction_Number INTEGER NOT NULL PRIMARY KEY,
    Transaction_Date DATE,
    Stock_Symbol TEXT,
    Share_Price REAL,
    Shares_Sold REAL,
    Transaction_Cost REAL
    )'''

    cursor.execute(stock_table)
    
    connection.commit()
    
    connection.close()

    # Generate the Transaction Number for the Database
    transactionNumber = transactionCounter()
    
    # Re-open table to apply changes
    connection = sqlite3.connect('stocks.db')

    cursor = connection.cursor() 

    del_entries = "DELETE FROM Open_Orders WHERE Stock_Symbol = " + "'" + stockSymbol + "'"
    
    cursor.execute(del_entries)

#    https://docs.python.org/3/library/sqlite3.html

    cursor.execute('''INSERT INTO Closed_Orders (
    Transaction_Number,
    Transaction_Date,
    Stock_Symbol,
    Share_Price,
    Shares_Sold,
    Transaction_Cost
    )
    VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
    )''',(
        transactionNumber,
        transactionDate,
        stockSymbol,
        currentPriceFloat,
        roundedSharesSold,
        transactionCost
        )
        )

    connection.commit()
    
    connection.close()

    
    print("Transaction Number:", transactionNumber)

########################################################

def backup():
    
    getDateTime = datetime.datetime.now()
    starttime = getDateTime
    today = getDateTime.strftime(" %b %d, %Y")
    todayNumerical = getDateTime.strftime("%Y-%m-%d")
    
    # Creates a Back-up copy of the Spreadsheet
    
    strToday = str(todayNumerical)
    
    # Backup Spreadsheet
    shutil.copyfile('stocks.xlsx', '/home/randy/git/robinhoodapi/backups/stocks' + '_' + str(todayNumerical) + '.xlsx')
    
    # Backup Database
    shutil.copyfile('stocks.db', '/home/randy/git/robinhoodapi/backups/stocks' + '_' + str(todayNumerical) + '.db')
