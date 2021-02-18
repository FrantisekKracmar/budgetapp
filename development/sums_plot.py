import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style
style.use('seaborn-bright')
import datetime as dt

db = sqlite3.connect('records.db')
cursor = db.cursor()
    
"""   FUNGUJE
cursor.execute("SELECT SUM(amount) FROM records WHERE typ==0 and month=1")
#data=cursor.fetchall()
soucet=cursor.fetchone()
####Parametricky dotaz"""

"""   FUNGUJE
month=1
dbQuery="SELECT SUM(amount) FROM records WHERE typ==0 and month=%s" % month
cursor.execute(dbQuery)
soucet=cursor.fetchone()"""

def updateExpSums(year): #updates values for graphs for given year
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    allCategories=[]
    
    for category in range(1,8): #for all categories; 8 means 7 categories
        singleCategory=[]
        months=[1,2,3,4,5,6,7,8,9,10,11,12]
        
        for month in range(len(months)): #for all months with single category
            dbQuery="SELECT SUM(amount) FROM records WHERE typ==0 and year=%s and month=%s and category=%s" % (year, month+1, category)
            cursor.execute(dbQuery)
            soucet=cursor.fetchone()
            if soucet[0]==None:
                soucet=0
            else:
                soucet=soucet[0]
            
            singleCategory.append(soucet)
        
        allCategories.append(singleCategory)
    return(allCategories)
    
def graph_data(year):
    allCategories=updateExpSums(year)
    colors=['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
    #defines months
    months=[]
    for month in range(1, 13):
        months.append(dt.datetime(year=year, month=month, day=1))
        
    #defines ymax for y_axis
    yMax=0
    for cat in range(len(allCategories)):
        if max(allCategories[cat])>yMax:
            yMax=max(allCategories[cat])
        else:    
            yMax=yMax
    
    #handles graph
    plt.title('Monthly sums of categories during the year %s' % year)
    plt.xlabel('Month')
    plt.ylabel('Amount [Kč]')
    plt.axis([months[0], months[11], 0, yMax])
    plt.xticks(rotation=45)
    
    for category in range(0,7):
        plt.plot(months, allCategories[category], colors[category])
    
    categories=["Living", "Travel", "Food", "Shopping", "Services", "Household", "Misc"]
    plt.legend(categories, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    plt.show

graph_data(2019)


def updateIncSums(year):
    db = sqlite3.connect('records.db')
    cursor = db.cursor()
    
    allMonths=[]
    months=[1,2,3,4,5,6,7,8,9,10,11,12]
    
    for month in range(len(months)): #for all months within single category
        dbQuery="SELECT SUM(amount) FROM records WHERE typ==1 and year=%s and month=%s" % (year, month+1)
        cursor.execute(dbQuery)
        soucet=cursor.fetchone()
        
        if soucet[0]==None:
            soucet=0
        else:
            soucet=soucet[0]
        print(soucet)
        
        allMonths.append(soucet)
    
    return(allMonths)
    
#x=updateExpSums(2018)

"""def graph_data():
    cursor.execute('SELECT amount FROM records WHERE typ==0')
    amounts=[]
    for row in cursor.fetchall():
        #print(row[0])
        amounts.append(row[0])
    plt.plot(amounts, '-')
    plt.show()
 
#graph_data()
#allCategories=updateSums(2018)"""