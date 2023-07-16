#!/bin/python3
"""
Analyses NASDAQ data and saves in a file
"""
import pandas as pd
import pandas_ta as ta
import numpy as np
import mplfinance as mpf
import yfinance as yf
from talib import abstract
import os
import matplotlib.pyplot as plt
import talib
import math
from datetime import datetime

"""some function """
def change_index(df):
    """Begins the index of df from 1"""
    df.index=np.arange(1,len(df.index)+1)
    return df

#drop some columns
def drop_cols(df,cols=['HH','HL','HC','LH','LL','HV']):
    rest=df.drop(cols,axis=1)
    return rest

#get change
def get_change(cp,pct_change):
    """
    returns the change in the price based on the final price and %change
    """
    #if pct_change==np.inf:pct_change=0
    previous_price=(100*cp)/(100+pct_change)# if cp!=0 else 0
    return round(cp-previous_price,2)

#saves to txt and html
txt_folder="./TXT/{}.txt"
html_folder="./HTML/{}.html"
fmt_yahoo="https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
fmt_nasdaq="https://www.nasdaq.com/market-activity/stocks/{}"
today=datetime.now().strftime("%b-%d-%Y") #date

#html string
html_string = '''
<html>
  <head><title>NASDAQ Stock Analysis</title></head>
  <h1>{TEST} </h1>
  <h4>{DATE}</h4>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''
#with open('myhtml.html', 'w') as f:
#    f.write(html_string.format(table=demo_df.to_html(classes='mystyle')))
#

def save_txt_html(df,save,title,date,rows=100):
    df=df.head(rows)
    df['Y-LINK']=df['TICKER'].apply(lambda x: fmt_yahoo.format(x,x))
    df['N-LINK']=df['TICKER'].apply(lambda x: fmt_nasdaq.format(x))
    df.to_csv(txt_folder.format(save),sep='\t',index=True)
    with open(html_folder.format(save), 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='mystyle',justify='center',render_links=True),TEST='NASDAQ '+title,DATE=date))

save_dir="/home/thakur/test/combined/"
save_file=save_dir+'all_nasdaq.csv'
final=pd.read_csv(save_file)
final=final[final.COUNTRY=='United States']

#print("final: \n",final.head())
final=final.sort_values(by=['CP'])
final=final[final['CP']>1] #price above 1
final=final[final['AVGVOL']>0.1] # 5D AVG VOL > 100k
final=final[final['%CHG']!=np.inf] 
final=change_index(final)
#final["TURN"]=round(final["VOL"]/final["FLOAT"]*100,2)
#new order
#co=final.columns.to_list();c=co[:20]+co[23:]+co[20:23]
#final=final[c]
final['CHG']=final.apply(lambda x: get_change(x['CP'],x['%CHG']),axis=1)
##print(f"Total length: {len(final.index)}\n")
#final.to_csv("TXT/snptemp.txt",sep='\t',index=True)
#final.to_html("HTML/snptemp.html",index=True,render_links=True)
#print("final snp \n",final.head())

#ignoring some small caps
remove=['micro','nano']
final=final[~final['CATEGORY'].isin(remove)]

#top10 % TURNOVER
#final_turn=final.sort_values(by=["TURN"],ascending=False)
#final_turn=drop_cols(final_turn)
#final_turn=change_index(final_turn)
#save_txt_html(final_turn,'nasdaq_final_turn','TURN',today)  #FUNCTION

#Highest +ve Change
high_change=final.sort_values(by=['%CHG'],ascending=False)
high_change=change_index(high_change)
save_txt_html(high_change,'nasdaq_positive_change','+VE CHANGE',today)      #FUNCTION  
save_txt_html(high_change[::-1],'nasdaq_negative_change','-VE CHANGE',today)#FUNCTION
#print("high_change: \n",high_change.head(5))
#exit()

#ATR values
df_atr=final
df_atr=df_atr[(df_atr['CATEGORY']=='mega') | (df_atr['CATEGORY']=='medium') | (df_atr['CATEGORY']=='large')]
df_atr['%']=round(100*df_atr['ATR']/df_atr['CP'],2)
df_atr=df_atr.sort_values(by=['%'],ascending=False)
df_atr=drop_cols(df_atr)
df_atr=change_index(df_atr)
save_txt_html(df_atr,'nasdaq_atr','ATR%',today)#FUNCTION

#sort by rsi
df_rsi=final
df_rsi=df_rsi[(df_rsi['CATEGORY']=='mega') | (df_rsi['CATEGORY']=='medium') | (df_rsi['CATEGORY']=='large')]
df_rsi=df_rsi.sort_values(by=['RSI'],ascending=False)
df_rsi=change_index(df_rsi)
save_txt_html(df_rsi,'nasdaq_rsi_high','HIGH-RSI',today)           #FUNCTION  
save_txt_html(df_rsi[::-1],'nasdaq_rsi_low','LOW-RSI',today)      #FUNCTION  

#Highest Volume
vol_highest=final.sort_values(by=['VOL'],ascending=False)
vol_highest=change_index(vol_highest)
save_txt_html(vol_highest,'nasdaq_vol','HIGHEST VOLUME',today) #FUNCTION

#HH, HL
ti='VOL > AVGVOL5; %CHG > 0; CP > SMA5; SMA5 > SMA10'
hh=final[final['HH']==True];
hl=final[final['HL']==True];
# hc=final[final['HC']==True];
# hv=final[final['HV']==True]
df_chg=final[(final['VOL']>final['AVGVOL']) & (final['%CHG']>0) & (final['CP']>final['SMA5'])
             & (final['HH']==True) & (final['HL']==True)]
df_chg.sort_values(by=['CP'])
df_chg=change_index(df_chg)
save_txt_html(df_chg,'nasdaq_chg',ti,today) #FUNCTION

#CP>SMA50; CP>SMA200; SMA50>SMA200
ti1="CP>SMA50; CP>SMA200; SMA50>SMA200"
f1=final['CP']>final['SMA50']
f2=final['CP']>final['SMA200']
f3=final['SMA50']>final['SMA200']
df_above=final[f1 & f2 &f3]
df_above=change_index(df_above)
save_txt_html(df_above,'nasdaq_above50n200',ti1,today) # FUNCTION

#best on category
category=['mega','large','medium','small']#,'micro','nano']
print("ESCAPING SOME DATA")
for cat in category:
    ti2=cat.upper()+"=>HH; HL; HC; CP>SMA50; CP>SMA200; VOL>AVGVOL5"
    df_hl=final[(final['HH']==True) & (final['HL']==True)  & (final['CP']>final['SMA50']) & (final['CP']>final['SMA200'])
           # & (final['RSI']>40)
            & (final['HC']==True) & (final['VOL']>final['AVGVOL'])& (final['CATEGORY']==cat)]# & (final['CP']>final['SMA200'])]
    df_hl.loc[:,"SMA50-CP"]=df_hl.loc[:,"SMA50"]-df_hl.loc[:,"CP"]
    df_hl=df_hl.sort_values(by=["CP"],ascending=True)
    df_hl=change_index(df_hl)
    save_txt_html(df_hl,'nasdaq_best_'+cat,ti2,today)#FUNCTION

