import sqlite3
import os.path
import random

if os.path.exists("records.db") is False:
    db = sqlite3.connect("records.db")
    cursor = db.cursor()

    cursor.execute(
        "create table records (id INTEGER PRIMARY KEY, typ TEXT, category TEXT, year INTEGER, month INTEGER, day INTEGER, amount INTEGER, note TEXT, indexExp INTEGER, indexInc INTEGER)"  # noqa: E501
    )
    db.commit()
    db.close()

    print("Database of records does not exist, making new")


def addRecord(expinc, category, year, month, day, amount, note):
    db = sqlite3.connect("records.db")
    cursor = db.cursor()

    # var for indexing individual types
    if expinc == 0:  # 0 is for expense, 1 for income
        indexExp = newIndex(0)  # this var should increase!
        indexInc = 0

    else:
        indexExp = 0
        indexInc = newIndex(1)  # this var should increase!

    # add a record to the db
    cursor.execute(
        """INSERT INTO records(typ, category, year, month, day, amount, note, indexExp, indexInc) VALUES(?,?,?,?,?,?,?,?,?)""",  # noqa: E501
        (expinc, category, year, month, day, amount, note, indexExp, indexInc),
    )
    db.commit()
    db.close()


def newIndex(expinc):
    db = sqlite3.connect("records.db")
    cursor = db.cursor()

    if expinc == 0:
        cursor.execute("SELECT MAX(indexExp) FROM records WHERE typ==0")
    else:
        cursor.execute("SELECT MAX(indexInc) FROM records WHERE typ==1")

    maxIndexRecord = cursor.fetchone()
    if maxIndexRecord[0] is None:
        newIndex = 1
    else:
        newIndex = maxIndexRecord[0] + 1

    db.commit()
    db.close()

    return newIndex


for i in range(0, 500):
    ei = random.randint(0, 1)
    if ei == 0:
        cat = random.randint(1, 7)
    else:
        cat = 0
    year = 2019
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    amount = random.randint(1, 1000)
    note = "random_generated"
    addRecord(ei, cat, year, month, day, amount, note)
