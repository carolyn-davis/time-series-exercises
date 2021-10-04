#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 11:00:50 2021

@author: carolyndavis
"""

# =============================================================================
#                 #Times Series Acquire Exercises
# =============================================================================


# =============================================================================
# 1.) Using the code from the lesson as a guide and the REST API from https://python.zgulde.net/api/v1/items as
#  we did in the lesson, create a dataframe named items that has all of the data for items.
# =============================================================================
import pandas as pd
import requests
# initialize an empty list
items_list = []
# get an initial response
response = requests.get('https://python.zgulde.net/api/v1/items')
data = response.json()
# get our max page to establish our iterable
n = data['payload']['max_page']

base_url = 'https://python.zgulde.net/api/v1/items?page='

# define a for loop in a range going from 1 to n 
for i in range(1,n+1):
    # get full url, adding a string version of the page number
    url = base_url + str(i)
    # get our response
    response = requests.get(url)
    # turn our response into python dictionary
    data = response.json()
    # grab just the content out
    page_items = data['payload']['items']
    # add in this page of items to our items list
    items_list += page_items

#Looking at the items list:
items_list[0]
#output:
 # {'item_brand': 'Riceland',
 # 'item_id': 1,
 # 'item_name': 'Riceland American Jazmine Rice',
 # 'item_price': 0.84,
 # 'item_upc12': '35200264013',
 # 'item_upc14': '35200264013'}

# =============================================================================
# Now turn the data into a DataFrame:
items = pd.DataFrame(items_list)

#------------------Stores 
# set up the base url string:
base_url = 'https://python.zgulde.net'

# add on a  endpoint:
response = requests.get(base_url + '/api/v1/stores')


response.json()['payload'].keys()

#output: 
    # dict_keys(['max_page', 'next_page', 'page', 'previous_page', 'stores'])

response.json()['payload']['max_page']
#output: 1

#Turn it into a DataFrame:

stores = pd.DataFrame(response.json()['payload']['stores'])

#looking at the stores data:
stores.head()
#              store_address   store_city  store_id store_state store_zipcode
# 0   12125 Alamo Ranch Pkwy  San Antonio         1          TX         78253
# 1         9255 FM 471 West  San Antonio         2          TX         78251
# 2  2118 Fredericksburg Rdj  San Antonio         3          TX         78201
# 3          516 S Flores St  San Antonio         4          TX         78204
# 4          1520 Austin Hwy  San Antonio         5          TX         78218






# =============================================================================
# 2.)b Do the same thing, but for stores (https://python.zgulde.net/api/v1/stores)
# =============================================================================


#---------------------Sales Data...
base_url
#output: 'https://python.zgulde.net'

#get the intial response for the sales data:
response = requests.get(base_url + '/api/v1/sales')

#add on the endpoint:
end_point = response.json()['payload']['next_page']

#find the endpoint:
response.json()['payload']['max_page']
#output: 183

end_point
# /api/v1/sales?page=2'


end_point[:-1]  #-1 includes all of the rows for the data


end_point_last_page = end_point[:-1]+ str(response.json()['payload']['max_page'])
#output: '/api/v1/sales?page=183'

response.json()['payload']['max_page']
# 183




#investigating the next page key on the last page of the data:
last_page = requests.get(base_url + end_point_last_page).json()['payload']['next_page']
last_page
#casting it as a boolean:
bool(last_page)
#soutput: False

#assigning the pages for the sales data to the initial sales page:
pages = requests.get(base_url + '/api/v1/sales?page=1').json()['payload']['sales']


#assigning the endpoint to the next_page key:
endpoint = requests.get(base_url + '/api/v1/sales?page=1').json()['payload']['next_page']

# =============================================================================
# Doing the same thing Above with the While method:
# =============================================================================
# endpoint is our next page key, which we will reassign in a loop
endpoint
#ouput: : '/api/v1/sales?page=2'

while endpoint:
    # get our response:
    response = requests.get(base_url + endpoint).json()['payload']
    # change our endpoint in the loop
    endpoint = response['next_page']
    # grab the content and ass it to pages
    pages += response['sales']

#taking a look at the number of pages:
len(pages)





# =============================================================================
# 3.) Extract the data for sales (https://python.zgulde.net/api/v1/sales).
#  There are a lot of pages of data here, so your code will need to be a little
#  more complex. Your code should continue fetching data from the next page until
#  all of the data is extracted.
# =============================================================================


# =============================================================================
# The FOR Loop Version:
# =============================================================================
pages = []   #uses collector
for i in range(1,184):
    response = requests.get(base_url + '/api/v1/sales?page=' + str(i))
    sales = response.json()['payload']['sales']
    pages += sales

#turning the list of data into a DataFrame:
sales = pd.DataFrame(pages)

#looking at the data:
sales.info()
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 913000 entries, 0 to 912999
# Data columns (total 5 columns):
#  #   Column       Non-Null Count   Dtype  
# ---  ------       --------------   -----  
#  0   item         913000 non-null  int64  
#  1   sale_amount  913000 non-null  float64
#  2   sale_date    913000 non-null  object 
#  3   sale_id      913000 non-null  int64  
#  4   store        913000 non-null  int64  
# dtypes: float64(1), int64(3), object(1)
# memory usage: 34.8+ MB



# =============================================================================
# 4.) Save the data in your files to local csv files so that it will be faster to access in the future.
# =============================================================================


# sales = pd.read_csv('sales_cached.csv', index_col=0)




# =============================================================================
# 5.) Combine the data from your three separate dataframes into one large dataframe.
# =============================================================================




#Let's see how we are going to merge everything, 
#                   ESTABLISH THE KEYS:
sales.columns
#output: Index(['item', 'sale_amount', 'sale_date', 'sale_id', 'store'], dtype='object')

sales.head()
#ouput:
#    item  sale_amount                      sale_date  sale_id  store
# 0     1         13.0  Tue, 01 Jan 2013 00:00:00 GMT        1      1
# 1     1         11.0  Wed, 02 Jan 2013 00:00:00 GMT        2      1
# 2     1         14.0  Thu, 03 Jan 2013 00:00:00 GMT        3      1
# 3     1         13.0  Fri, 04 Jan 2013 00:00:00 GMT        4      1
# 4     1         10.0  Sat, 05 Jan 2013 00:00:00 GMT        5      1


#looking at the items data:
items.head()
#        item_brand  item_id  ...    item_upc12    item_upc14
# 0        Riceland        1  ...   35200264013   35200264013
# 1          Caress        2  ...   11111065925   11111065925
# 2     Earths Best        3  ...   23923330139   23923330139
# 3      Boars Head        4  ...  208528800007  208528800007
# 4  Back To Nature        5  ...  759283100036  759283100036

# [5 rows x 6 columns]

items.columns
#output:
    # Index(['item_brand', 'item_id', 'item_name', 'item_price', 'item_upc12',
    #    'item_upc14'],
    #   dtype='object')

stores.head()
#output:
#                  store_address   store_city  store_id store_state store_zipcode
# 0   12125 Alamo Ranch Pkwy  San Antonio         1          TX         78253
# 1         9255 FM 471 West  San Antonio         2          TX         78251
# 2  2118 Fredericksburg Rdj  San Antonio         3          TX         78201
# 3          516 S Flores St  San Antonio         4          TX         78204
# 4          1520 Austin Hwy  San Antonio         5          TX         78218

stores.columns
# output: Index(['store_address', 'store_city', 'store_id', 'store_state',
#        'store_zipcode'],
#       dtype='object')


#       First mergining sales to stores:
sales_plus_stores = pd.merge(
    sales,
    stores,
    how='left',
    left_on='store',
    right_on='store_id')

#check it out:
sales.shape
#output: (913000, 5)

sales_plus_stores.shape
#output: (913000, 10)   #looks like they were added successfully

sales_plus_stores.info()
#output:
#     <class 'pandas.core.frame.DataFrame'>
# Int64Index: 913000 entries, 0 to 912999
# Data columns (total 10 columns):
#  #   Column         Non-Null Count   Dtype  
# ---  ------         --------------   -----  
#  0   item           913000 non-null  int64  
#  1   sale_amount    913000 non-null  float64
#  2   sale_date      913000 non-null  object 
#  3   sale_id        913000 non-null  int64  
#  4   store          913000 non-null  int64  
#  5   store_address  913000 non-null  object 
#  6   store_city     913000 non-null  object 
#  7   store_id       913000 non-null  int64  
#  8   store_state    913000 non-null  object 
#  9   store_zipcode  913000 non-null  object 
# dtypes: float64(1), int64(4), object(5)
# memory usage: 76.6+ MB


#               Merging items with sales_plus_stores
sales_plus_all = pd.merge(
    sales_plus_stores,
    items,
    how='left',
    left_on='item',
    right_on='item_id')

sales_plus_all.head()


#Turning the complete data frame into a script for easy retrieval
sales_plus_all.to_csv('cached_everything.csv')


# =============================================================================
# # Using this stuff later:
# =============================================================================


# =============================================================================
# # pseudo-script:
# # import os
# 
# # if os.path.isfile('cached_everything.csv'):
# #     df = pd.read_csv('cached_everything.csv', index_col=0)
# # else:
# #     do all the requests and merges
# =============================================================================




# =============================================================================
# 6.) Acquire the Open Power Systems Data for Germany, which has been rapidly expanding
#  its renewable energy production in recent years. The data set includes country-wide
#  totals of electricity consumption, wind power production, and solar power production for
#  2006-2017. You can get the data here:
#      https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv
# =============================================================================
df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')

df.head()
#output:
#          Date  Consumption  Wind  Solar  Wind+Solar
# 0  2006-01-01     1069.184   NaN    NaN         NaN
# 1  2006-01-02     1380.521   NaN    NaN         NaN
# 2  2006-01-03     1442.533   NaN    NaN         NaN
# 3  2006-01-04     1457.217   NaN    NaN         NaN
# 4  2006-01-05     1477.131   NaN    NaN         NaN

df.info()
#          Date  Consumption  Wind  Solar  Wind+Solar
# 0  2006-01-01     1069.184   NaN    NaN         NaN
# 1  2006-01-02     1380.521   NaN    NaN         NaN
# 2  2006-01-03     1442.533   NaN    NaN         NaN
# 3  2006-01-04     1457.217   NaN    NaN         NaN
# 4  2006-01-05     1477.131   NaN    NaN         NaN



# =============================================================================
# 7.) Make sure all the work that you have done above is reproducible.
#     That is, you should put the code above into separate functions in the
#     acquire.py file and be able to re-run the functions and get the same data
# =============================================================================






