#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:05:29 2021

@author: carolyndavis
"""

# =============================================================================
#                                       PREPARE EXERCISES  
# =============================================================================


import numpy as np
import pandas as pd
from datetime import timedelta, datetime
import acquire as a

import matplotlib.pyplot as plt



store_df = a.get_groceries()



# =============================================================================
# 1.) Convert date column to datetime format.
# =============================================================================
store_df.sale_date = pd.to_datetime(store_df.sale_date.apply(lambda x: x[:-13]))

store_df.head()

# output:
#    Unnamed: 0_x  item  sale_amount  ... item_price   item_upc12   item_upc14
# 0             0     1         13.0  ...       0.84  35200264013  35200264013
# 1             1     1         11.0  ...       0.84  35200264013  35200264013
# 2             2     1         14.0  ...       0.84  35200264013  35200264013
# 3             3     1         13.0  ...       0.84  35200264013  35200264013
# 4             4     1         10.0  ...       0.84  35200264013  35200264013

# [5 rows x 18 columns]

# =============================================================================
# 2.) Plot the distribution of sale_amount and item_price.
# =============================================================================
store_df[['sale_amount', 'item_price']].hist(figsize=(20,10))





# =============================================================================
# 3.) Set the index to be the datetime variable.
# =============================================================================

store_df = store_df.set_index('sale_date').sort_index()






# =============================================================================
# 4.) Add a 'month' and 'day of week' column to your dataframe.
# =============================================================================

store_df['dow'] = store_df.index.day_name()


store_df['month'] = store_df.index.month_name()





# =============================================================================
# 5.) Add a column to your dataframe, sales_total, which is a derived from sale_amount
#  (total items) and item_price.
# =============================================================================
store_df['sales_total'] = store_df['sale_amount'] * store_df['item_price']
store_df.head()

#output:
#             Unnamed: 0_x  item  sale_amount  ...      dow    month  sales_total
# sale_date                                    ...                               
# 2013-01-01             0     1         13.0  ...  Tuesday  January        10.92
# 2013-01-01        211816    12         26.0  ...  Tuesday  January       218.40
# 2013-01-01        832656    46         27.0  ...  Tuesday  January       125.55
# 2013-01-01        213642    12         54.0  ...  Tuesday  January       453.60
# 2013-01-01        215468    12         35.0  ...  Tuesday  January       294.00

# [5 rows x 20 columns]



# =============================================================================
# 6.) Make sure all the work that you have done above is reproducible. 
# That is, you should put the code above into separate functions and
#  be able to re-run the functions and get the same results.
# =============================================================================









# =============================================================================
#                             OPS EXERCISES
# =============================================================================
opsd_df = a.get_opsd()
opsd_df.head()

#output:
#              Date  Consumption  Wind  Solar  Wind+Solar
# 0  2006-01-01     1069.184   NaN    NaN         NaN
# 1  2006-01-02     1380.521   NaN    NaN         NaN
# 2  2006-01-03     1442.533   NaN    NaN         NaN
# 3  2006-01-04     1457.217   NaN    NaN         NaN
# 4  2006-01-05     1477.131   NaN    NaN         NaN




# =============================================================================
# 1.) Convert date column to datetime format.
# =============================================================================
opsd_df['Date'] = pd.to_datetime(opsd_df.Date)
opsd_df.info()





# =============================================================================
# 2.) Plot the distribution of each of your variables.
# =============================================================================
opsd_df.hist(figsize=(25,25))







# =============================================================================
# 3.) Set the index to be the datetime variable.
# =============================================================================
opsd_df = opsd_df.set_index('Date').sort_index()
opsd_df.head()

#output:
#             Consumption  Wind  Solar  Wind+Solar
# Date                                            
# 2006-01-01     1069.184   NaN    NaN         NaN
# 2006-01-02     1380.521   NaN    NaN         NaN
# 2006-01-03     1442.533   NaN    NaN         NaN
# 2006-01-04     1457.217   NaN    NaN         NaN
# 2006-01-05     1477.131   NaN    NaN         NaN







# =============================================================================
# 4.) Add a month and a year column to your dataframe.
# =============================================================================
opsd_df['month'] = opsd_df.index.month_name()
opsd_df['year'] = opsd_df.index.year
opsd_df.head()

#output:
#             Consumption  Wind  Solar  Wind+Solar    month  year
# Date                                                           
# 2006-01-01     1069.184   NaN    NaN         NaN  January  2006
# 2006-01-02     1380.521   NaN    NaN         NaN  January  2006
# 2006-01-03     1442.533   NaN    NaN         NaN  January  2006
# 2006-01-04     1457.217   NaN    NaN         NaN  January  2006
# 2006-01-05     1477.131   NaN    NaN         NaN  January  2006

# =============================================================================
# 5.) Fill any missing values.
# =============================================================================
opsd_df.fillna(0, inplace=True)
opsd_df.head()

# output:
#                 Consumption  Wind  Solar  Wind+Solar    month  year
# Date                                                           
# 2006-01-01     1069.184   0.0    0.0         0.0  January  2006
# 2006-01-02     1380.521   0.0    0.0         0.0  January  2006
# 2006-01-03     1442.533   0.0    0.0         0.0  January  2006
# 2006-01-04     1457.217   0.0    0.0         0.0  January  2006
# 2006-01-05     1477.131   0.0    0.0         0.0  January  2006


opsd_df[opsd_df['Wind+Solar'] != (opsd_df['Wind'] + opsd_df['Solar'])]
#output:
#             Consumption     Wind   Solar  Wind+Solar     month  year
# Date                                                                
# 2010-01-01   1057.37200   48.709   0.000       0.000   January  2010
# 2010-01-02   1161.04200   24.628   0.000       0.000   January  2010
# 2010-01-03   1132.06900   22.963   0.000       0.000   January  2010
# 2010-01-04   1346.25000   59.318   0.000       0.000   January  2010
# 2010-01-05   1457.37400   41.624   0.000       0.000   January  2010
#                 ...      ...     ...         ...       ...   ...
# 2017-12-25   1111.28338  587.810  15.765     603.575  December  2017
# 2017-12-26   1130.11683  717.453  30.923     748.376  December  2017
# 2017-12-27   1263.94091  394.507  16.530     411.037  December  2017
# 2017-12-29   1295.08753  584.277  29.854     614.131  December  2017
# 2017-12-31   1107.11488  721.176  19.980     741.156  December  2017

# [2001 rows x 6 columns]

opsd_df.shape
#output = (4383, 6)


opsd_df['wind_solar_custm'] = opsd_df['Wind'] + opsd_df['Solar']
opsd_df[opsd_df['Wind+Solar'] != (opsd_df['Wind'] + opsd_df['Solar'])][['Wind', 'Solar', 'Wind+Solar', 'wind_solar_custm']]


#ouput:
# Out[61]: 
#                Wind   Solar  Wind+Solar  wind_solar_custm
# Date                                                     
# 2010-01-01   48.709   0.000       0.000            48.709
# 2010-01-02   24.628   0.000       0.000            24.628
# 2010-01-03   22.963   0.000       0.000            22.963
# 2010-01-04   59.318   0.000       0.000            59.318
# 2010-01-05   41.624   0.000       0.000            41.624
#             ...     ...         ...               ...
# 2017-12-25  587.810  15.765     603.575           603.575
# 2017-12-26  717.453  30.923     748.376           748.376
# 2017-12-27  394.507  16.530     411.037           411.037
# 2017-12-29  584.277  29.854     614.131           614.131
# 2017-12-31  721.176  19.980     741.156           741.156

# [2001 rows x 4 columns]








# =============================================================================
# 6.) Make sure all the work that you have done above is reproducible. That is, you
#  should put the code above into separate functions and be able to re-run the functions
#  and get the same results.
# =============================================================================
