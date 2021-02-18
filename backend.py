import sqlite3
import os.path
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
style.use('seaborn-bright')

"""
Co to vlastne umi:
    1)Vlozit zaznam z prikazove radky
    2)Sumy nad vsemi zaznamy
    3)Seznam roku pro uzivatelsky vyber
    4)Vytvoreni seznamu kategorii
    5)Uzivatelske rozhrani - shell
    6)Grafy pro zvoleny rok z nabidky
"""

"""database="records.db"

#tohle by mohlo fungovat
def connectDB(dbName):
    db = sqlite3.connect(dbName)
    cursor = db.cursor()
#tohle taky
def disconnectDB(dbName):
    db.commit()
    db.close()"""

def createDB():
    """IF database does not exist, makes a new one"""
    if os.path.exists("records.db") == False:
        # connect to database
        db = sqlite3.connect('records.db')
        cursor = db.cursor()

        # createa new db
        cursor.execute('create table records (id INTEGER PRIMARY KEY, typ TEXT, category TEXT, year INTEGER, month INTEGER, day INTEGER, amount INTEGER, note TEXT, indexExp INTEGER, indexInc INTEGER)')
       
        # execute and close
        db.commit()
        db.close()
    
        print("Database of records does not exist, making a new one.")

def addRecord(expinc, category, year, month, day, amount, note):
    """Adds a new record to database"""
    # connect to database
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    # variables for indexing individual types
    if expinc == 0: # 0 is for expense, 1 for income
        indexExp = newIndex(0) #this var should increase!
        indexInc = 0
        
    else:
        indexExp = 0
        indexInc = newIndex(1) # this var should increase!
        
    # add a record to the db       
    cursor.execute('''INSERT INTO records(typ, category, year, month, day, amount, note, indexExp, indexInc) VALUES(?,?,?,?,?,?,?,?,?)''', (expinc, category, year, month, day, amount, note, indexExp, indexInc))
    db.commit()
    db.close()

def newIndex(expinc):
    """Increase new index for individual types of records"""
    # connect to database
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    # find maximum index for expenses
    if expinc == 0:
        cursor.execute("SELECT MAX(indexExp) FROM records WHERE typ==0")

    # find maximum index for incomes
    else:
        cursor.execute("SELECT MAX(indexInc) FROM records WHERE typ==1")

    maxIndexRecord = cursor.fetchone()

    # handle if maximum index is None
    if maxIndexRecord[0] == None:
        newIndex = 1
    else:
        newIndex = maxIndexRecord[0]+1
    
    db.commit()
    db.close()
    
    return(newIndex)

def updateExpSums(year):
    """Update expenses sums for given year"""
    # connect to database
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    allCategories = []
    
    for category in range(1,8): #for all categories; 8 means 7 categories
        singleCategory = []
        months = [1,2,3,4,5,6,7,8,9,10,11,12]
        
        for month in range(len(months)): #for all months within single category
            dbQuery = "SELECT SUM(amount) FROM records WHERE typ==0 and year==%s and month==%s and category==%s" % (year, month+1, category) # proč month+1??
            cursor.execute(dbQuery)
            soucet = cursor.fetchone()
            
            if soucet[0] == None:
                soucet = 0

            else:
                soucet = soucet[0]
            
            singleCategory.append(soucet)
        
        allCategories.append(singleCategory)

    return(allCategories)

def updateIncSums(year):
    """Update incomes sums for given year"""
    # connect to database
    db = sqlite3.connect('records.db')
    cursor = db.cursor()    
    
    allMonths = []
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    
    for month in range(len(months)): #for all months
        dbQuery = "SELECT SUM(amount) FROM records WHERE typ==1 and year=%s and month=%s" % (year, month+1) #bylo month +1
        cursor.execute(dbQuery)
        soucet = cursor.fetchone()
        
        if soucet[0] == None:
            soucet = 0

        else:
            soucet = soucet[0]

        #print(soucet)
        
        allMonths.append(soucet)
    
    return(allMonths)

### Monthly sums of categories during given year 
def graph_data(year, categories):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    allCategories = updateExpSums(year)
    
    # define months
    months = []

    for month in range(1, 13):
        months.append(dt.datetime(year=year, month=month, day=1))
        
    # define ymax for y_axis
    yMax = 0

    for cat in range(len(allCategories)):
        if max(allCategories[cat]) > yMax:
            yMax = max(allCategories[cat])

        else:    
            yMax = yMax
    
    # handle graph
    plt.title('Monthly sums of categories during the year %s' % year)
    plt.xlabel('Month')
    plt.ylabel('Amount [Kc]')
    plt.axis([months[0], months[11], 0, yMax])
    plt.xticks(rotation=45)

    # plot data
    for category in range(0,7):
        plt.plot(months, allCategories[category], colors[category])
    
    # legend settings
    plt.legend(categories, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    # show graph
    plt.show(block=True)
    
def listOfYears():
    """Return list of years with existing expenses records"""
    # connect to database
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    cursor.execute("SELECT DISTINCT(year) FROM records WHERE typ==0")
    listOfTuples = cursor.fetchall()
    
    years = []
    
    for i in range(len(listOfTuples)):
        x = listOfTuples[i]
        x = x[0]
        
        years += [x]
    
    return(years)


### Main menu in shell
def userInterface():
    """First main menu in shell"""
    global categories
    
    print("Welcome to my Awesome app")
    print(" ")
    print("Main menu:")
    print("1...Add a new record")
    print("2...Show some graphs")
    print("3...settings")

    userInput = int(input("What would you like to do?(1-3): "))
    
    if userInput == 1:
        userNewRecord()
    elif userInput == 2:
        print(" ")
        print("Existing data for years: ")
        
        # Lets user choose for which year do sumups
        years = listOfYears()
        for year in range(len(years)):
            print(years[year])
        year = int(input("Which year do you want to see the sums for?: "))
        
        # Handles given non existing year or other BS
        try:
            years.index(year)
        except ValueError:
            print("Sorry, there are no available data for year %s" %year)
            "Do nothing"
        else:      
            graph_data(year, categories)
            
    elif userInput == 3:
        print("Sorry, you can't change anything :(")
    else:
        print("Please input number from 1 to 3")

### Shell user interface for new record
def userNewRecord():
    print("--------------------------")
    print("You are adding a new record")
    expinc = int(input('0 for expense, 1 for income: '))
    print("--------------------------")

    if expinc == 0:
        for i in range(len(categories)):
            print("%s...%s" % (i+1, categories[i]))
        category = int(input('Number of category: '))

    else:
        category = int()

    year = int(input('Year: '))
    month = int(input('Month: '))
    date = int(input('Day: '))
    amount = int(input('Amount: '))
    note = input('Note: ')
    addRecord(expinc, category, year, month, date, amount, note)




#User categories
categories=["Living", "Travel", "Food", "Shopping", "Services", "Household", "Misc"]


"##### MAIN PROGRAM #####"
#userInterface()