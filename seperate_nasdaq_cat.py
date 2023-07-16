#!/usr/bin/env python

# coding: utf-8

# In[1]:


# This program breaks the stocks list into different categories based on the market capitilization


# In[136]:


#libraries
import pandas as pd
import subprocess


# In[137]:


#check the timestamp of the download
command='ls -lt /home/thakur/stock_information/  | head'
subprocess.run(command,shell=True)
subprocess.run('date',shell=True)


# In[138]:


#source of all the stock list downloaded from https://www.nasdaq.com/market-activity/stocks/screener
source_file='nasdaq_all.csv'
source_root=f'/home/thakur/stock_information/{source_file}'
save_root='/home/thakur/stock_information/{}'


# In[139]:


df=pd.read_csv(source_root)


# In[140]:


print(df.head().to_string())
print(df.tail().to_string())


# In[141]:


# number of stocks 
print(f"Total stocks in the main list: {df.shape[0]}")


# In[142]:


to_million=1e6


# In[143]:


#change the market cap into million
df['Market Cap']=df['Market Cap'].div(to_million)


# In[147]:


#single function to filter the market cap
def get_market_cap(df,fil,save_file):
    '''
    returns and saves the resulting stock df based on filters
    '''
    print(20*'= '+save_file.upper()+20*' =')
    print(f"Working with filter: {fil}")
    save_loc=save_root.format('nasdaq_'+save_file+'.csv')
    temp_df=df.query(fil).reset_index(drop=True)
    print(f"Number of stocks   :  {temp_df.shape[0]}")
    print(f"Saving as          :  {save_loc}")
    temp_df.to_csv(save_loc,index=False)
    #print(f"Saving to          :  {temp_df.to_csv(save_loc,index=False)}")
    #return temp_df


# In[148]:


#market cap
market_cap=['nano','micro','small','medium','large','mega']
#filters
filters=['`Market Cap`< 50',
         '`Market Cap`> 50 & `Market Cap`< 300',
         '`Market Cap`> 300 & `Market Cap`< 2000',
         '`Market Cap`> 2000 & `Market Cap`< 10000',
         '`Market Cap`> 10000 & `Market Cap`< 200000',
         '`Market Cap`> 200000'
        ]


# In[149]:


for i in range(len(market_cap)):
    print()
    get_market_cap(df,filters[i],market_cap[i])
    print()


# In[ ]:




