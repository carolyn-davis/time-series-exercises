#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 16:57:06 2021

@author: carolyndavis
"""



# =============================================================================
#                   ACQUIRE FUNCTIONS FOR DATA RETRIEVAL
# =============================================================================


import pandas as pd
import requests
import os


# =============================================================================
#                   ACQUIRING THE ITEMS DATA
# =============================================================================

def new_items():
    '''
    This function is specific to Zach's lol grocery dataset. It will itirate through each
    page of items and return a pandas DataFrame of all items.
    '''
    items_list = []
    base_url = 'https://python.zgulde.net/api/v1/items?page='
    response = requests.get('https://python.zgulde.net/api/v1/items')
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1,n+1):
        url = base_url + str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['items']
        items_list += page_items
        
    return pd.DataFrame(items_list)

def get_items():
    '''
    returns dataframe of all items from items.csv, or creates items.csv for you
    '''
    if os.path.isfile('items.csv'):
        df = pd.read_csv('items.csv')
    else:
        df = new_items()
        df.to_csv('items.csv', index=False)
        
    return df




# =============================================================================
#                       ACQUIRING THE STORE DATA
# =============================================================================

def new_stores():
    '''
    This function is specific to stores dataset. It will itirate through each
    page of stores and return a pandas DataFrame of all stores.
    '''   
    items_list = []
    base_url = 'https://python.zgulde.net/api/v1/stores?page='
    response = requests.get('https://python.zgulde.net/api/v1/stores')
    data = response.json()
    n = response.json()['payload']['max_page']

    for i in range(1, n+1):
        url = 'https://python.zgulde.net/api/v1/stores?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['stores']
        items_list += page_items

    return pd.DataFrame(response.json()['payload']['stores'])


def get_stores():
    '''
    This function operates on top of the new_stores function. It first searches locally for a csv file.
    If there is a local csv, it writes it into a pandas DataFrame. If there is no local csv, this function then
    calls the new_stores function, and writes that df to a local csv.
    '''
    if os.path.isfile('grocery_stores.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('grocery_stores.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_stores()
        # Cache data
        df.to_csv('grocery_stores.csv')

    return df

# =============================================================================
#                   ACQUIRE THE SALES DATA
# =============================================================================

def new_sales():
    '''
    This function is specific to Zach's lol grocery dataset. It will itirate through each
    page of sales and return a pandas DataFrame of all sales.
    '''   
    items_list = []
    base_url = 'https://python.zgulde.net/api/v1/sales?page='
    response = requests.get('https://python.zgulde.net/api/v1/sales')
    data = response.json()
    n = response.json()['payload']['max_page']

    for i in range(1, n+1):
        url = 'https://python.zgulde.net/api/v1/sales?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['sales']
        items_list += page_items
        
    return pd.DataFrame(items_list)



def get_sales():
    '''
    This function operates on top of the new_sales function. It first searches locally for a csv file.
    If there is a local csv, it writes it into a pandas DataFrame. If there is no local csv, this function then
    calls the new_sales function, and writes that df to a local csv.
    '''
    if os.path.isfile('grocery_sales.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('grocery_sales.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_sales()
        # Cache data
        df.to_csv('grocery_sales.csv')

    return df
df = get_sales()
dfw = get_items()
dfwr = get_stores()
# =============================================================================
# 
# =============================================================================
def new_groceries():
    '''
    This functions reads in three different csv files as pandas DataFrames, and merges them
    into one df. It drops unnamed columns. Cannot use with other dataframes without changing 
    the name of the csv files, and hyperparameters of how/on the tables are merged
    '''
    
    items_df = pd.read_csv('items.csv')
    stores_df = pd.read_csv('grocery_stores.csv')
    sales_df = pd.read_csv('grocery_sales.csv')
    sales_stores_df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id', how='left')
    sales_stores_items_df = pd.merge(sales_stores_df, items_df, left_on='item', right_on='item_id', how='left')
    # sales_stores_items_df = sales_stores_items_df.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0', 'store', 'item'])
    
    return sales_stores_items_df
test = new_groceries()
def get_groceries():
    '''
    This function operates on top of the new_groceries function. It first searches locally for a csv file.
    If there is a local csv, it writes it into a pandas DataFrame. If there is no local csv, this function then
    calls the new_groceries function, and writes that df to a local csv.
    '''
    if os.path.isfile('sales_stores_items.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('sales_stores_items.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_groceries()
        # Cache data
        df.to_csv('sales_stores_items.csv')

    return df

test = get_groceries()




# =============================================================================
# #                     GERMAN DATA RETRIEVAL      
# =============================================================================
def new_opsd():
    '''
    This function reads in the opsd germany dataset and returns it as a pandas DataFrame.
    '''

    OPSD = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    return OPSD


def get_opsd():
    '''
    This function operates on top of the new_opsd function. It first searches locally for a csv file.
    If there is a local csv, it writes it into a pandas DataFrame. If there is no local csv, this function then
    calls the new_opsd function, and writes that df to a local csv.
    '''
    if os.path.isfile('opsd_germany.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('opsd_germany.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_opsd()
        # Cache data
        df.to_csv('opsd_germany.csv')

    return df

