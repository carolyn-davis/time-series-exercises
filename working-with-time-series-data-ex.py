#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 12:23:05 2021

@author: carolyndavis
"""
from vega_datasets import data
data.sf_temps()


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydataset

df = data.sf_temps()
df.head()

# =============================================================================
#    temp                date
# 0  47.8 2010-01-01 00:00:00
# 1  47.4 2010-01-01 01:00:00
# 2  46.9 2010-01-01 02:00:00
# 3  46.5 2010-01-01 03:00:00
# 4  46.0 2010-01-01 04:00:00
# =============================================================================
df.info()
df = df.set_index('date')
# =============================================================================
# 1.) Resample by the day and take the average temperature.
#  Visualize the average temperature over time.
# =============================================================================

df.resample('D').mean().plot(title='Average temp over time')





# =============================================================================
# 2.) Write the code necessary to visualize the minimum temperature over time.
# =============================================================================
df.resample('D').min().plot(title='min temp over time')




# =============================================================================
# 3.)Write the code necessary to visualize the maximum temperature over time
# =============================================================================
df.resample('D').max().plot(title='max temp over time')





# =============================================================================
# 4.)Which month is the coldest, on average?
# =============================================================================
df.resample('D').mean().resample('M').mean().sort_values('temp').index[0]
#output: Timestamp('2010-01-31 00:00:00')
l = [1, 2, 3]
l[-1]
#output = 3





# =============================================================================
# 5.)Which month has the highest average temperature?
# =============================================================================

df.resample('M').mean().sort_values('temp').index[-1]
#ouput: Timestamp('2010-09-30 00:00:00')






# =============================================================================
# 6.) Resample by the day and calculate the min and max temp for the day
#  (Hint: .agg(['min', 'max'])). Use this resampled dataframe to calculate the
#  change in temperature for the day. Which month has the highest daily temperature
#  variability?
# =============================================================================
daily = df.temp.resample('D').agg(['min', 'max'])
daily['delta_temp'] = daily['max'] - daily['min']
daily.head()
#output:
#              min   max  delta_temp
# date                              
# 2010-01-01  45.8  53.3         7.5
# 2010-01-02  46.0  53.4         7.4
# 2010-01-03  46.1  53.5         7.4
# 2010-01-04  46.1  53.6         7.5
# 2010-01-05  46.1  53.8         7.7

daily.resample('M').delta_temp.mean().sort_values().index[-1]
#output = Timestamp('2010-09-30 00:00:00')




# =============================================================================
#                       SEATTLE WEATHER EXXERCISES
# =============================================================================


# =============================================================================
# 1.) Which year and month combination has the highest amount of precipitation?
# =============================================================================
sea_df = data.seattle_weather()
sea_df.head()
#ouput:
#             date  precipitation  temp_max  temp_min  wind  weather
# 0 2012-01-01            0.0      12.8       5.0   4.7  drizzle
# 1 2012-01-02           10.9      10.6       2.8   4.5     rain
# 2 2012-01-03            0.8      11.7       7.2   2.3     rain
# 3 2012-01-04           20.3      12.2       5.6   4.7     rain
# 4 2012-01-05            1.3       8.9       2.8   6.1     rain

sea_df.set_index('date').groupby('weather').resample('Y').size().unstack(0)
#ouput:
# weather     drizzle    fog   rain  snow    sun
# date                                          
# 2012-12-31     31.0    5.0  191.0  21.0  118.0
# 2013-12-31     16.0   82.0   60.0   2.0  205.0
# 2014-12-31      0.0  151.0    3.0   NaN  211.0
# 2015-12-31      7.0  173.0    5.0   NaN  180.0

sea_df['year'] = sea_df.date.dt.year
sea_df['month'] = sea_df.date.dt.month

sea_df.groupby(['year', 'month']).precipitation.sum().sort_values().tail()
#ouput:
#     year  month
# 2012  3        183.0
#       11       210.5
# 2015  11       212.6
# 2014  3        240.0
# 2015  12       284.5
# Name: precipitation, dtype: float64

# =============================================================================
# 2.) Visualize the amount of monthly precipitation over time.
# =============================================================================
sea_df.set_index('date').resample('M').precipitation.sum().plot()



# =============================================================================
# 3.) Visualize the amount of wind over time. Choose a time interval you think is appropriate.
# =============================================================================
sea_df.set_index('date').wind.resample('5W').mean().plot()






# =============================================================================
# 4.) Which year-month combination is the windiest?
# =============================================================================

sea_df.groupby(['year', 'month']).wind.mean().sort_values().tail()
#output:
#     year  month
# 2012  2        3.903448
# 2014  11       3.983333
# 2012  3        4.248387
# 2015  12       4.341935
# 2014  2        4.528571
# Name: wind, dtype: float64




# =============================================================================
# 5.)What's the sunniest year? (Hint: which day has the highest number
#     of days where weather == sun?)
# =============================================================================
sea_df[sea_df.weather == 'sun'].groupby('year').size()
#ouput = 
# year
# 2012    118
# 2013    205
# 2014    211
# 2015    180
# dtype: int64



# =============================================================================
# 6.) In which month does it rain the most?
# =============================================================================
sea_df.groupby('month').precipitation.sum().sort_values().tail(1)
#output:
# month
# 11    642.5
# Name: precipitation, dtype: float64

# =============================================================================
# 7.)Which month has the most number of days with a non-zero amount of precipitation?
# =============================================================================
sea_df['did_rain'] = sea_df.precipitation > 0

sea_df.groupby('month').did_rain.sum().sort_values().tail(1)

#output:
# month
# 12    81
# Name: did_rain, dtype: int64


# =============================================================================
#                   FLIGHTS EXERCISES
# =============================================================================

flight_df = data.flights_20k()
flight_df.head()

#outpu:
#                      date  delay  distance origin destination
# 0 2001-01-13 14:56:00     32       417    SAN         SJC
# 1 2001-01-31 16:40:00     -5      1093    FLL         ISP
# 2 2001-02-11 18:39:00      3       293    LBB         DAL
# 3 2001-01-10 21:00:00    -15       550    MSY         MCO
# 4 2001-03-30 21:45:00     -2       229    STL         IND


# =============================================================================
# 1.) Convert any negative delays to 0.
# =============================================================================
pd.Series([-1, 0, 1, 2, 3]).clip(lower=0, upper=2)
#output:
# 0    0
# 1    0
# 2    1
# 3    2
# 4    2
# dtype: int64


s = pd.Series([-1, 0, 1, 2, 3])
s.where(s >= 0, 0)
#output:
# 0    0
# 1    0
# 2    1
# 3    2
# 4    3
# dtype: int64
# =============================================================================
# 2.) Which hour of the day has the highest average delay?
# =============================================================================
flight_df.delay = np.where(flight_df.delay < 0, 0, flight_df.delay)
flight_df.groupby(flight_df.date.dt.hour).delay.mean().sort_values().tail(3)

#output:
# date
# 0    127.916667
# 1    170.000000
# 3    302.500000
# Name: delay, dtype: float64






# =============================================================================
# 3.) Does the day of the week make a difference in the delay amount?
# =============================================================================
flight_df.groupby(flight_df.date.dt.day_name()).delay.mean().sort_values()
#output:
# date
# Monday        7.165772
# Saturday      8.431498
# Tuesday       9.410866
# Sunday       10.413542
# Wednesday    11.032478
# Thursday     12.821322
# Friday       17.757596
# Name: delay, dtype: float64
#Yes there is a higher delay on thursdays measured based off the data
# =============================================================================
# 4.) Does the month make a difference in the delay amount?
# =============================================================================

flight_df.groupby(flight_df.date.dt.month).delay.mean().sort_values()
#output:
# date
# 3     9.875287
# 1    11.301592
# 2    12.306106
# Name: delay, dtype: float64
#Yes clearly the month of december has a higher difference in delay amount compared to the 
#other months