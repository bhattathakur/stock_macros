#!/bin/python3
import pandas as pd
import os
import numpy as np
import html_template as html
all_up=[];all_down=[]

dirs=['mega','large','medium','small','micro','nano','snp500']
for k,j in enumerate(dirs[:]): 
    dir_name='/home/thakur/test/{}/'.format(dirs[k])
    tickers=os.listdir(dir_name)
    gap_up=[];gap_down=[]

    for c,i in enumerate(tickers):
        file=dir_name+i
        #print(f"File:({c+1}/{len(tickers)})--> {file}")
        df=pd.read_csv(file)
        tick=i.split('.')[0]
        #print(f"Current data for {tick}:\n{df.tail(5)}")
        yesterday=df.tail(2).head(1)
        #print(f"Second last data for {tick}:\n{yesterday}")

        today=df.tail(1)
        #print(f"Last data for {tick}:\n{today}")

        low_yesterday=yesterday['Low'].values[0]
        high_yesterday=yesterday['High'].values[0]
        #open_today=today['Open'].values[0];close_today=today['Close'].values[0]
        low_today=today['Low'].values[0];high_today=today['High'].values[0]

        # print(f"Yesterday's low for {tick}:\n{low_yesterday}")
        # print(f"Today's open for {tick}:\n{open_today}")
        # print(f"Today's close for {tick}:\n{close_today}")
        #oops_status=True if (open_today<low_yesterday and close_today>low_yesterday) else False
        #print(f"oops_status for {tick}: {oops_status}\n")
        gap_up_check=True if low_today>high_yesterday else False
        gap_down_check=True if high_today<low_yesterday else False
        if gap_up_check:gap_up.append(tick)
        if gap_down_check:gap_down.append(tick)

    print(f"Gapped up tickers for   {j}:\n{gap_up}\n")
    print(f"Gapped down tickers for   {j}:\n{gap_down}\n")
    #adding ups and downs
    all_up=all_up+gap_up;all_down=all_down+gap_down
print(f"All Gapped up   tickers:\n{all_up}\n")
print(f"All Gapped down tickers:\n{all_down}\n")

df=pd.read_csv('~/test/combined/all_nasdaq.csv')
df=df[df['CATEGORY']!='nano']
df=df[df['CATEGORY']!='micro']
df_up=df[df['TICKER'].isin(all_up)]
df_up=df_up[df['AVGVOL']>0.1]
df_up=df_up[df['VOL']>0.05]
df_up=df_up.sort_values(by=['CP'])
df_up.index=np.arange(1,df_up.shape[0]+1)
print("gap_up_df\n",df_up)

df_down=df[df['TICKER'].isin(all_down)]
df_down=df_down[df['AVGVOL']>0.1]
df_down=df_down.sort_values(by=['CP'])
df_down.index=np.arange(1,df_down.shape[0]+1)
print("gap_down_df\n",df_down)

html.save_txt_html(df_up,"nasdaq_gapped_up","nasdaq_gapped_up",rows=100)
html.save_txt_html(df_down,"nasdaq_gapped_down","nasdaq_gapped_down",rows=100)
#save in the html template
