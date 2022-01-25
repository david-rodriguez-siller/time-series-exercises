import numpy as np
import pandas as pd
import requests

from datetime import timedelta, datetime
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

def prepare_api_df(api_data):
    '''
    This function prepares the api dataframe by converting the sale_date column into a datetype object, sets the index to sale_date, and adds further datetype columns to the dataframe.
    '''
    api_data.sale_date = pd.to_datetime(api_data.sale_date)
    api_data = api_data.set_index('sale_date').sort_index()
    api_data['month'] = api_data.index.month_name()
    api_data['day_of_week'] = api_data.index.day_name()
    api_data['sales_total'] = api_data.sale_amount * api_data.item_price
    
    return api_data

def prepare_opsd_df(opsd_germany_daily):
    '''
    This function prepares the opsd germany dataframe by converting the Date column to  a datetime object, setting the Date column as the index and adding additional columns.
    '''
    
    opsd_germany_daily.Date = pd.to_datetime(opsd_germany_daily.Date)
    opsd_germany_daily = opsd_germany_daily.set_index('Date').sort_index()
    opsd_germany_daily['month'] = opsd_germany_daily.index.month_name()
    opsd_germany_daily['year'] = opsd_germany_daily.index.year
    opsd_germany_daily = opsd_germany_daily.fillna(0)
   
    return opsd_germany_daily
