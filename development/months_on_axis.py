import datetime as dt

import matplotlib.pyplot as plt

"""dates = []
for year in range(2012, 2014):
    for month in range(1, 12):
        dates.append(dt.datetime(year=year, month=month, day=1))
"""
months = []
year = 2018
for month in range(1, 13):
    months.append(dt.datetime(year=year, month=month, day=1))

y = [10, 180, 153, 80, 11, 92, 201, 74, 24, 0, 2, 1]
plt.plot(months, y)
plt.show()
