#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:15:39 2021

@author: carolyndavis
"""

# =============================================================================
#            Modeling Exercises with the SAAS dataset     
# =============================================================================
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from matplotlib.dates import DateFormatter
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime
import statsmodels.api as sm


from sklearn.metrics import mean_squared_error
from math import sqrt


from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.api import Holt
import warnings
warnings.filterwarnings("ignore")

# =============================================================================
# Functions Utilized in this Exercises 
# =============================================================================

def evaluate(target_var):
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

def plot_and_eval(target_var):
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label = 'Train', linewidth = 1)
    plt.plot(validate[target_var], label = 'Validate', linewidth = 1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()

def append_eval_df(model_type, target_var):
    rmse = evaluate(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var], 'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)

def make_predictions():
    yhat_df = pd.DataFrame({'amount': [amounts],
                           }, index = validate.index)
    return yhat_df






#Acquiring the Data
df = pd.read_csv('saas.csv')
df.columns=['date','cust_id','invoice_id','sub_type','amount']
df['date'] = pd.to_datetime(df.date)

df = df.groupby(['date']).amount.sum().reset_index()

df = df[df.index!='2016-02-29']
df = df.set_index('date').sort_index()


#seeing if everything worked 
df.head()
#output;
#              amount
# date               
# 2014-01-31  35850.0
# 2014-02-28  37190.0
# 2014-03-31  38295.0
# 2014-04-30  39255.0
# 2014-05-31  40355.0
# =============================================================================
# # 1.) Split data (train/validate/test) and resample by any period, except daily,
# #  and aggregate using the sum.
# =============================================================================


#50% of the data will be train
train_size = int(len(df) * .5)

#30% validate
validate_size = int(len(df) * .3)

#20% is allocated to test
test_size = int(len(df) - train_size - validate_size)

validate_end_index = train_size + validate_size

# The big split into train, validation, test
train = df[: train_size]
validate = df[train_size : validate_end_index]
test = df[validate_end_index : ]

#double checking the sizes match up 

train.shape, validate.shape, test.shape
#output: 
# ((24, 1), 
# (14, 1), 
# (10, 1))

#check those lens!
len(train) + len(validate) + len(test) == len(df)
#True---> gucci gang



#ensure that these values are the same
print(df.head(1) ==train.head(1))
#             amount
# date              
# 2014-01-31    True

pd.concat([train.tail(1), validate.head(1)])
pd.concat([validate.tail(1), test.head(1)])
#output:
#              amount
# date               
# 2017-02-28  53440.0
# 2017-03-31  53480.0


pd.concat([test.tail(1), df.tail(1)])
#output:
#              amount
# date               
# 2017-12-31  53805.0
# 2017-12-31  53805.0

# =============================================================================
# Visualizing the train, validate, test
# =============================================================================
for col in train.columns:
    plt.figure(figsize=(12,4))
    plt.plot(train[col])
    plt.plot(validate[col])
    plt.plot(test[col])
    plt.ylabel(col)
    plt.title(col)
    plt.show()






# =============================================================================
# 2.) Forecast, plot and evaluate using each of the 4 parametric based methods we discussed:
# =============================================================================



# =============================================================================
# Simple Average
# =============================================================================
amounts = round(train['amount'].mean(),2)

yhat_df = make_predictions()

yhat_df.head()

#output:
#               amount
# date                
# 2016-01-31  45568.54
# 2016-02-29  45568.54
# 2016-03-31  45568.54
# 2016-04-30  45568.54
# 2016-05-31  45568.54

#visualize the train data set
for col in train.columns:
    plot_and_eval(col)


#make an empty df to append model results to 
eval_df = pd.DataFrame(columns=['model_type', 'target_var', 'rmse'])





#append the results from the simple avg model to an empty dataframe
for col in train.columns:
    eval_df = append_eval_df(model_type='simple_average', 
                             target_var = col)

#check out the eval_df
eval_df.head()
#output:
#        model_type target_var    rmse
# 0  simple_average     amount  7181.0


# =============================================================================
# Moving Average
# =============================================================================
period = 2

amounts = round(train['amount'].rolling(period).mean().iloc[-1], 2)


yhat_df = make_predictions()
yhat_df.head(3)

#outpiut:
#              amount
# date               
# 2016-01-31  51382.5
# 2016-02-29  51382.5
# 2016-03-31  51382.5



#visualize the moving avg
for col in train.columns:
    plot_and_eval(col)


#append the results to eval_df 
for col in train.columns:
    eval_df = append_eval_df(model_type='2 month moving average', 
                             target_var = col)

#check out the eval_df
eval_df

#output:
#                model_type target_var    rmse
# 0          simple_average     amount  7181.0
# 1  2 month moving average     amount  1455.0

#Takeaway: Moving Avg Appears to perform better

# =============================================================================
# 4,6,8,10,12  Month Moving Average
# =============================================================================
periods = [4, 6, 8, 10, 12]

for p in periods:
    amounts = round(train['amount'].rolling(p).mean().iloc[-1], 2)
    yhat_df = make_predictions()
    model_type = str(p) + ' month moving average'
    eval_df = append_eval_df(model_type = model_type,
                             target_var = 'amount'
                            )
#check out the eval_df for all montly moving averages
eval_df

#output:
#                 model_type target_var    rmse
# 0           simple_average     amount  7181.0
# 1   2 month moving average     amount  1455.0
# 2   4 month moving average     amount  1533.0
# 3   6 month moving average     amount  1847.0
# 4   8 month moving average     amount  2259.0
# 5  10 month moving average     amount  2696.0
# 6  12 month moving average     amount  3164.0

#Takeaway: 2month moving avg is so far performing the best


# =============================================================================
# Add the winners to their own df
# =============================================================================
min_rmse_amount = eval_df.groupby('target_var')['rmse'].min()[0]

#appending the top model or min rmse to the new min_rmse df
eval_df[((eval_df.rmse == min_rmse_amount)
        )]
#output:
#                model_type target_var    rmse
# 1  2 month moving average     amount  1455.0



# =============================================================================
# Holt's Linear Trend Model
# =============================================================================


#first lets check out the seasonality
for col in train.columns:
    print(col,'\n')
    _ = sm.tsa.seasonal_decompose(train[col].resample('M').mean()).plot()
    plt.show()


#make and fit the Holt model
for col in train.columns:
    model = Holt(train[col], exponential = False)
    model = model.fit(smoothing_level = .1, 
                      smoothing_slope = .1, 
                      optimized = False)
    yhat_items = model.predict(start = validate.index[0], 
                               end = validate.index[-1])
    yhat_df[col] = round(yhat_items, 2)
    
    
#visualize the model    
for col in train.columns:
    plot_and_eval(target_var = col)
    
    
#apppending the Holt results to the eval df    
for col in train.columns:
    eval_df = append_eval_df(model_type = 'Holts', 
                             target_var = col)

#check the eval_df 
# eval_df
#                 model_type target_var    rmse
# 0           simple_average     amount  7181.0
# 1   2 month moving average     amount  1455.0
# 2   4 month moving average     amount  1533.0
# 3   6 month moving average     amount  1847.0
# 4   8 month moving average     amount  2259.0
# 5  10 month moving average     amount  2696.0
# 6  12 month moving average     amount  3164.0
# 7                    Holts     amount  8103.0

#Takeaway: 2 month avg is still in first place




# =============================================================================
# Based on previous year/month/etc., this is up to you
# =============================================================================

train = df[:'2015']
validate = df['2016']
test = df['2017']


yhat_df = round(train['2015'] + train.diff(1).mean(),2)


pd.concat([yhat_df.head(1), validate.head(1)])
#output:
#               amount
# date                
# 2015-01-31  47625.65
# 2016-01-31  51955.00


yhat_df.index = validate.index

len(yhat_df)
#output: 12 perfecto


#visulaize and appending the result for the model to eval_Df
for col in train.columns:
    plot_and_eval(target_var = col)
    eval_df = append_eval_df(model_type = 'previous year', target_var = col)

#check it out
eval_df

#                 model_type target_var    rmse
# 0           simple_average     amount  7181.0
# 1   2 month moving average     amount  1455.0
# 2   4 month moving average     amount  1533.0
# 3   6 month moving average     amount  1847.0
# 4   8 month moving average     amount  2259.0
# 5  10 month moving average     amount  2696.0
# 6  12 month moving average     amount  3164.0
# 7                    Holts     amount  8103.0
# 8            previous year     amount  2539.0


#takeaway: 2 month moving average is still the winner


# =============================================================================
# Visualize all of the models in comparison of performance
# =============================================================================
for col in train.columns:
    x = eval_df[eval_df.target_var == col]['model_type']
    y = eval_df[eval_df.target_var == col]['rmse']
    plt.figure(figsize=(12, 6))
    sns.barplot(x, y)
    plt.title(col)
    plt.ylabel('RMSE')
    plt.xticks(rotation=45)
    plt.show()
    
    
    
yhat_df = validate + train.diff(1).mean()
yhat_df.index = test.index


rmse_amount = round(sqrt(mean_squared_error(test['amount'], yhat_df['amount'])), 0)


for col in train.columns:
    plot_and_eval(col)
    
    
print(rmse_amount)