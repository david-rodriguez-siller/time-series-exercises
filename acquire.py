import pandas as pd
import requests
import os


def acq_api_data(api_data):
    '''
    This function first checks if there is currently a .csv file with its corresponding requested api file. It then pulls 
    data  into a dataframe from the site: 'https://python.zgulde.net/api/v1/items'
    '''
    if api_data not in ['sales', 'items', 'stores']:
        return 'Requested data is not available from this API. Check the documentation.'

    import os
    
    # check for local csv file
    if os.path.isfile(f'{api_data}.csv'):
        df = pd.read_csv(f'{api_data}.csv', index_col = 0)
        return df
    
    else:

        host = 'https://python.zgulde.net/'
        api = 'api/v1/'

        url = host + api + api_data

        response = requests.get(url)

        if response.ok:

            payload = response.json()['payload']

            contents = payload[api_data]

            df = pd.DataFrame(contents)

            next_page = payload['next_page']

            while next_page:
                
                url = host + next_page
                
                response = requests.get(url)

                payload = response.json()['payload']

                next_page = payload['next_page']
                contents = payload[api_data]

                df = pd.concat([df, pd.DataFrame(contents)])

                df = df.reset_index(drop = True)
                
                # Write DataFrame to a csv file.
                df.to_csv(f'{api_data}.csv')

    return df
    

def combine_dfs(sales_df, stores_df, items_df):
    '''
    This function combines the three different API dataframes into one.
    '''
    
    combined_one_two = pd.merge(sales_df, stores_df, 
                                how = 'left', 
                                left_on = 'store',
                                right_on = 'store_id')
    
    df = pd.merge(combined_one_two, items_df,
                  how = 'left',
                  left_on = 'item',
                  right_on = 'item_id')
    
    return df


def get_opsd_germany():
    '''
    This function pulls a csv file from website: https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv, 
    and stores it in a variable as a dataset.
    '''
    
    import os
    
    # check for local csv file
    if os.path.isfile('opsd_germany_daily.csv'):
        df = pd.read_csv('opsd_germany_daily.csv', index_col = 0)
        return df
    
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
        # write DataFrame to a csv file.
        df.to_csv('opsd_germany_daily.csv')
        
    return df
    
    