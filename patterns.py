#!/bin/bash
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append('/home/thakur/test')
import html_template as html
import numpy as np
import talib as ta


root="/home/thakur/test/"
sources=["mega","large","medium","small"]#,"snp500"]#"micro","nano","snp500"]
single_list=[]
for c,i in enumerate(sources):
    dir_path=root+i
    print(f"{c+1}/{len(sources)} Dir Name: {dir_path}\n")
    tickers=os.listdir(dir_path)
   
    #print(f"\nTickers: {tickers}\n")
    for t,tick in enumerate(tickers):
        file=root+i+"/"+tick
        #print(f"\nTick {t+1}/{len(tickers)}: {tick}\n")
        df=pd.read_csv(file)
        df['Date']=df['Date'].apply(lambda x:x.split()[0])
        df["Date"] = pd.to_datetime(df["Date"])
        #print(f"Head:\n {df.head(5)}")
        
        #to get desired candlestick pattern
        tick=file.split('.')[0].split('/')[-1]
        
        open = df['Open']
        high = df['High']
        low = df['Low']
        close = df['Adj Close']
        
        #last row
        df=df.tail(50)
        temp_list=[]
        
        nan_in_df = df.isnull().values.any()
        
        if not nan_in_df:
            #print("inside dataframe:\n")
            kind="ema8"
            ema8 = ta.EMA(close, timeperiod=8).values[-1].round(2) #ema8
            rsi=ta.RSI(close, timeperiod=14).values[-1].round(2)
            #val=ema8.values[-1] 
            #if val==1:
            #print(f"{tick}=>{kind.upper()}=>{ema8}")
            kind='rsi'
            #print(f"{tick}=>{kind.upper()}=>{rsi}")
            kind='cp'
            cp=df.tail(1)['Adj Close'].values[0].round(2)
            #print(f"{tick}=>{kind.upper()}=>{cp}")
            
            #engulfing check
            df=df.tail(1)
            engulf = ta.CDLENGULFING(open, high, low, close).values[-1]
            enkind='engulfing'
            
            #val=integer.values[-1]
            #print(f"engulfing value: {val}")
            if engulf==0:
                enkind='-'
                #print(f"{tick}=>{kind.upper()}")
            elif engulf==100:
                enkind='bullish-'+enkind
                #print(f"{tick}=>{kind.upper()}")
            elif engulf==-100:
                enkind='bearish-'+enkind
                #print(f"{tick}=>{kind.upper()}")
        
            temp_list.extend((tick,cp,rsi,ema8,enkind.upper()))
            
            kind="morning-star"
            
            integer = ta.CDLMORNINGSTAR(open, high, low, close, penetration=0)
            val=integer.values[-1]
            #print(f"moring-star value: {val}")
            if val!=0:
                #print(f"{tick}=>{kind.upper()}")
                temp_list.append(kind.upper())
            else:
                temp_list.append("-")
                
            kind="evening-star"
            integer = ta.CDLEVENINGSTAR(open, high, low, close, penetration=0)
            val=integer.values[-1]
            if val!=0:
                #print(f"{tick}=>{kind.upper()}")
                temp_list.append(kind.upper())
            else:
                temp_list.append("-")
            
            temp_list.append(i)
            #print(f"temp_list: {temp_list}")  
            single_list.append(temp_list)
            #print(f"moring-star value: {val}")
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
            
#             #adding the values to temp_list
            
#             print(f"temp_list: {temp_list}")
#             #temp.clear()
        
#         if not nan_in_df:
#             #print("inside dataframe:\n")
#             kind="doji"
#             interger=ta.CDLDOJI(open, high, low, close)
#             val=integer.values[-1]
#             if val==1:
#                 print(f"{tick}=>{kind.upper()}")

#             kind="doji-star"
#             integer = ta.CDLDOJISTAR(open, high, low, close)
#         #val=integer.item()
#             val=integer.values[-1]
#             if val==1:
#                 print(f"{tick}=>{kind.upper()}")
            
#             kind="dragonfly-doji"
#             integer=ta.CDLDRAGONFLYDOJI(open, high, low, close)
#         #val=integer.item()
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
        
        
        
#             kind="gravestone-doji"
#             integer = ta.CDLGRAVESTONEDOJI(open, high, low, close)

#         #val=integer.item()
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
                
#             kind="hanging-man"
#             integer = ta.CDLHANGINGMAN(open, high, low, close)

#         #val=integer.item()
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
                
#             kind="inverted-hammer"  
#             integer = ta.CDLINVERTEDHAMMER(open, high, low, close)
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
            
#             kind="long-legged-doji"
#             integer = ta.CDLLONGLEGGEDDOJI(open, high, low, close)
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
                
#             kind="shooting-star"
#             integer = ta.CDLSHOOTINGSTAR(open, high, low, close)
#             val=integer.values[-1]
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
                
#             kind="engulfing"
#             integer = ta.CDLENGULFING(open, high, low, close)
#             val=integer.values[-1]
#             #print(f"engulfing value: {val}")
#             if val!=0:
#                 print(f"{tick}=>{kind.upper()}")
                
            
            
                
                
            
          
#print(f"SINGLE LIST:\n{single_list}")    
columns=["TICKER","CP","RSI","EMA8","ENGULFING","MORNING-STAR","EVENING-STAR","CATEGORY"]
temp_df=pd.DataFrame(single_list,columns=columns)
print("DONE:\n")
        # print(f"Date Type: {integer.dtype}")
        # print(f"SHOOTING STAR: {integer}")
        # print(f"          VAL: {val}")

# file=root+'+'.csv'
# df=pd.read_csv(file)
# df['Date']=df['Date'].apply(lambda x:x.split()[0])
# df["Date"] = pd.to_datetime(df["Date"])
#     #df_day.index=pd.to_datetime(df_day.index,unit='s')
# df_day.set_index("Date", inplace=True)
#     #tick
# tick=file.split('.')[0].split('/')[-1]
# open = dataframe['Open']
# high = dataframe['High']
# low = dataframe['Low']
# close = dataframe['Adj Close']

def change_df(df,ascen=True):
    df=df.sort_values(by=['CP'],ascending=ascen)
    df.index=np.arange(1,df.shape[0]+1)
    return df

#bullish=change_df(temp_df[temp_df['ENGULFING']=='BULLISH-ENGULFING'])
bullish=temp_df.loc[temp_df['ENGULFING']=='BULLISH-ENGULFING']
bullish=change_df(bullish)

html.save_txt_html(bullish,"PATTERN-BULLISH","PATTERN-BULLISH")
#bullish
#temp_df.loc[temp_df['ENGULFING']=='BULLISH-ENGULFING']


bearish=change_df(temp_df[temp_df['ENGULFING']=='BEARISH-ENGULFING'],False)
html.save_txt_html(bearish,"PATTERN-BEARISH","PATTERN-BEARSISH")
# bullish=change_df(bullish)
# bearish

morning_star=change_df(temp_df[temp_df['MORNING-STAR']=='MORNING-STAR'])
html.save_txt_html(morning_star,"PATTERN-MORNING-STAR","PATTERN-MORNING-STAR")
#morning_star

evening_star=change_df(temp_df[temp_df['EVENING-STAR']=='EVENING-STAR'],False)
html.save_txt_html(evening_star,"PATTERN-EVENING-STAR","PATTERN-EVENING-STAR")
#evening_star
