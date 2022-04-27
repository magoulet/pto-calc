#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar as cal
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from pto_classes import *

def readTransactions(filename, sheetName):
    df = pd.read_excel(filename, engine="odf", sheet_name=sheetName, usecols='C:G', index_col=[0,1])
    return df


def tenure(year, month, startMonth, tenureYear):
    if year > 0 and ((month - startMonth)%12 == 0):
        tenureYear += 1
    return tenureYear


if __name__ == '__main__':
    ppt = PPT()
    sick = Sick()
    vac = Vac()

    filename = 'amazon_vacation_schedule.ods'
    used = readTransactions(filename, 'baseline')

    years = 4
    months = 12
    startMonth = 3
    startYear  = 2021
    tenureYear = 0
    data = []
    # print('{:<} {:>4} {:>5} {:>5} {:>5} {:>5} {:>5}'.format('Year', 'Month', 'PPT', 'Sick', 'Vac', 'Lost', 'Days'))

    for year in range(years):
        for month in range(months):
            if (year == 0 and month >= startMonth) or year > 0:
                tenureYear = tenure(year, month, startMonth, tenureYear)

                ppt.use(used.loc[year, month]['ppt'], year, month)
                vac.use(used.loc[year, month]['vac'], year, month)
                sick.use(used.loc[year, month]['sick'], year, month)

                ppt.forward(year, month, sick)
                vac.forward(tenureYear)
                sick.forward(year, month)

            # print('{:<2.0f} {:>6} {:>5.1f} {:>5.1f} {:>5.1f} {:>5.1f} {:>5.0f}'.format(startYear+year, cal.month_abbr[month+1], ppt.bal, sick.bal, vac.bal, sick.lost, sum([ppt.bal, sick.bal, vac.bal])/8))
            data.append([startYear+year, cal.month_abbr[month+1], dt.date(startYear+year, month+1,1), ppt.bal, sick.bal, vac.bal, sick.lost/8, vac.lost/8, sum([ppt.bal, sick.bal, vac.bal])/8])

    results = pd.DataFrame(data)
    results.columns=['Year', 'Month', 'periodStart', 'PPT', 'Sick', 'Vac', 'sickLost', 'vacLost', 'Days']
    print(results)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(results['periodStart'], results['Days'], marker='o')
    ax.stackplot(results['periodStart'], results['PPT']/8, results['Sick']/8, results['Vac']/8)
    ax.stackplot(results['periodStart'], results['sickLost'], results['vacLost'], colors=['red', 'blue'])
    ax.set(title='Paid Time Off (days)',
           ylabel='Days',
           xlabel='Date')
    ax.legend(['PTO', 'PPT', 'Sick', 'Vac', 'Lost (PPT)','Lost (Vac)'], loc='best')
    plt.show()
