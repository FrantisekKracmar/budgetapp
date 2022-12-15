import sqlite3


def listOfYears():
    db = sqlite3.connect("records.db")
    cursor = db.cursor()

    cursor.execute("SELECT DISTINCT(year) FROM records WHERE typ==0")
    listOfTuples = cursor.fetchall()

    years = []

    for i in range(len(listOfTuples)):
        x = listOfTuples[i]
        x = x[0]

        years += [x]

    return years


listOfYears = listOfYears()
