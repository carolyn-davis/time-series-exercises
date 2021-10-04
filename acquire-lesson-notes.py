#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:34:49 2021

@author: carolyndavis
"""

import requests




response = requests.get('http://request-inspector.glitch.me/')
response
#<Response [200]>
#^^^ outout returns a python object that represents an HTTP response 
#This response has several properties:
    # .ok: a boolean that indicates that the response was successful (the server sent back a 200 response code)
    # .status_code: a number indicating the HTTP response status code
    #.text: the raw response text
response.ok    
#True

response.status_code
#200

response.text
# '{"method":"GET","query":{},"body":{}}'


# EXAMPLE: JSON API

url = 'https://swapi.dev/api/people/5'
response = requests.get(url)
print(response.text)

#Output returns a JSON object:
    
# {"name":"Leia Organa","height":"150","mass":"49","hair_color":"brown","skin_color":"light",
#  "eye_color":"brown","birth_year":"19BBY","gender":"female","homeworld":"https://swapi.dev/api/planets/2/",
#  "films":["https://swapi.dev/api/films/1/","https://swapi.dev/api/films/2/","https://swapi.dev/api/films/3/",
#           "https://swapi.dev/api/films/6/"],"species":[],"vehicles":["https://swapi.dev/api/vehicles/30/"],
#  "starships":[],"created":"2014-12-10T15:20:09.791000Z","edited":"2014-12-20T21:17:50.315000Z",
#  "url":"https://swapi.dev/api/people/5/"}



data = response.json()
print(type(data))
data

# =============================================================================
# #.json method on the response object to get a data structure we can work with:
# =============================================================================
# Now we have a disctionary we can work with:
    
    
# {'name': 'Leia Organa',
#  'height': '150',
#  'mass': '49',
#  'hair_color': 'brown',
#  'skin_color': 'light',
#  'eye_color': 'brown',
#  'birth_year': '19BBY',
#  'gender': 'female',
#  'homeworld': 'https://swapi.dev/api/planets/2/',
#  'films': ['https://swapi.dev/api/films/1/',
#   'https://swapi.dev/api/films/2/',
#   'https://swapi.dev/api/films/3/',
#   'https://swapi.dev/api/films/6/'],
#  'species': [],
#  'vehicles': ['https://swapi.dev/api/vehicles/30/'],
#  'starships': [],
#  'created': '2014-12-10T15:20:09.791000Z',
#  'edited': '2014-12-20T21:17:50.315000Z',
#  'url': 'https://swapi.dev/api/people/5/'}



#Looking at Another API:
    #Starting with just the base URL":

base_url = 'https://python.zgulde.net'
print(requests.get(base_url).text)

#Output: {"api":"/api/v1","help":"/documentation"}
#provides some documentation so lets make a request so that we can take a look at it:
    
response = requests.get(base_url + '/documentation')
print(response.json()['payload'])


# =============================================================================
# The API accepts GET requests for all endpoints, where endpoints are prefixed
# with
# 
#     /api/{version}
# 
# Where version is "v1"
# 
# Valid endpoints:
# 
# - /stores[/{store_id}]
# - /items[/{item_id}]
# - /sales[/{sale_id}]
# 
# All endpoints accept a `page` parameter that can be used to navigate through
# the results.
# =============================================================================
#Takeaway: Based on this, lets look at the ite,s. We will make a request, and explore the 
    #   shape of the response that we get back:

response = requests.get('https://python.zgulde.net/api/v1/items')

data = response.json()
data.keys()
#Output: dict_keys(['payload', 'status'])


data['payload'].keys()
# dict_keys(['items', 'max_page', 'next_page', 'page', 'previous_page'])



print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])
#Output:
# max_page: 3
# next_page: /api/v1/items?page=2

#Takeaways: the response has some built in properties that tell us how to get subsequent pages
#drill down in the data structure, response will be the proverbial wrapper around the [items] property


data['payload']['items'][:2]
#output:
 #    [{'item_brand': 'Riceland',
 #  'item_id': 1,
 #  'item_name': 'Riceland American Jazmine Rice',
 #  'item_price': 0.84,
 #  'item_upc12': '35200264013',
 #  'item_upc14': '35200264013'},
 # {'item_brand': 'Caress',
 #  'item_id': 2,
 #  'item_name': 'Caress Velvet Bliss Ultra Silkening Beauty Bar - 6 Ct',
 #  'item_price': 6.44,
 #  'item_upc12': '11111065925',
 #  'item_upc14': '11111065925'}]
 
 #Now turn this into a PANDAS dataframe



import pandas as pd

df = pd.DataFrame(data['payload']['items'])
df.head()

# output:
#            item_brand  item_id  ...    item_upc12    item_upc14
# 0        Riceland        1  ...   35200264013   35200264013
# 1          Caress        2  ...   11111065925   11111065925
# 2     Earths Best        3  ...   23923330139   23923330139
# 3      Boars Head        4  ...  208528800007  208528800007
# 4  Back To Nature        5  ...  759283100036  759283100036

#Takeaways:
    #Now that the data has been retrieved from the first page, we can extract the data
    # from the next page, from the API and add it onto our dataframe (df)
    


response = requests.get(base_url + data['payload']['next_page'])
data = response.json()

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])
#output:max_page: 3
# next_page: /api/v1/items?page=3


#Repeat the process one more time:
response = requests.get(base_url + data['payload']['next_page'])
data = response.json()

print('max_page: %s' % data['payload']['max_page'])
print('next_page: %s' % data['payload']['next_page'])

df = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()
#output:
#     max_page: 3
# next_page: None  << bc the APT says None for nexty page, we can stop making requests
                    #  Assume that we have all of the [items] data

df.shape