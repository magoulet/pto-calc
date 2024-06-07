#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import calendar as cal
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
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

    years = 6
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

            # Find last day of month
            d = dt.date(startYear+year, month+1,1)
            lastDayOfMonth = dt.date(d.year, d.month, cal.monthrange(d.year, d.month)[-1])

            # print('{:<2.0f} {:>6} {:>5.1f} {:>5.1f} {:>5.1f} {:>5.1f} {:>5.0f}'.format(startYear+year, cal.month_abbr[month+1], ppt.bal, sick.bal, vac.bal, sick.lost, sum([ppt.bal, sick.bal, vac.bal])/8))
            data.append([startYear+year, cal.month_abbr[month+1], lastDayOfMonth, ppt.bal, sick.bal, vac.bal, sick.lost/8, vac.lost/8, sum([ppt.bal, sick.bal, vac.bal])/8])

    results = pd.DataFrame(data)
    results.columns=['Year', 'Month', 'periodEnd', 'PPT', 'Sick', 'Vac', 'sickLost', 'vacLost', 'Days']
    print("PTO hours left over at end of given period\n")
    print(results[results['periodEnd'] > (dt.date.today() - dt.timedelta(2*365/12))])

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(results['periodEnd'], results['Days'], marker='o')
    ax.stackplot(results['periodEnd'], results['PPT']/8, results['Sick']/8, results['Vac']/8)
    ax.stackplot(results['periodEnd'], results['sickLost'], results['vacLost'], colors=['red', 'blue'])
    ax.set(title='Paid Time Off (days)',
           ylabel='Days',
           xlabel='Period End Date')
    ax.legend(['PTO', 'PPT', 'Sick', 'Vac', 'Lost (PPT)','Lost (Vac)'], loc='best')

    # Adding a vertical line for today's date
    today = dt.date.today()
    ax.axvline(today, color='red', linestyle='--')

    current_dir = Path(__file__).resolve().parent
    filename = 'pto_plot.png'
    file_path = current_dir / filename
    plt.savefig(file_path)
    plt.show()
