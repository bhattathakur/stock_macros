#!/bin/python3
#This program figures out the TTM possible candidates for the given period and standard deviation
#def of squeeze
import os
import pandas as pd
import talib

def in_squeze(df):
    return df['lowerbband']>df['lower_keltnear'] and df['upperbband']<df['upper_keltnear']

def check_consolidation(root,downperiod=200,period=10,multiplier=1.0,test_days=10):
    print(f"NOTE --> multiplier {multiplier}")
    print(f"     --> period     {period}\n")
    files=os.listdir(root)                #files at dir
    save_df=root.split("/")[0]+"squeeze"  #save df
    save_df=dict()                        #save df dic
    #print(f"save_df: {save_df}")
    #downperiod=200                        #total data to be used
    #period=10         #period for sma
    #multiplier=1.0
    #test_days=10     #df taken to 
    for i in files:
        symbol=i.split(".")[0]
    #if symbol!='AAPL':continue                  #limit for test
    #print(f"SYMBOL: {symbol}")
        df=pd.read_csv(root+i).tail(downperiod)     #data used to calculate parameters
        close=df.Close;low=df.Low;high=df.High      #close,low,high
        upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=period, nbdevup=2, nbdevdn=2, matype=0)
    #getting the bband and adding in the dataframe df
    
        df['upperbband']=upperband.round(2);df['lowerbband']=lowerband.round(2)
        df['ATR']=talib.ATR(high,low,close).round(2) #getting ATR and adding in the dataframe
    
        smatest='SMA'+str(period)                   #string to sma
        df[smatest]=talib.SMA(close,timeperiod=period).round(2) #SMA to the df

    
    #keltnear Band
        df['lower_keltnear']=round(df[smatest]-df['ATR']*multiplier,2)  #lower keltnear band
        df['upper_keltnear']=round(df[smatest]+df['ATR']*multiplier,2)  #upper keltnear band
    
    
    #only getting the dataframe for last test_days
        df=df.tail(test_days)

        df['squeeze_on']=df.apply(in_squeze,axis=1)
    
        df=df[df['squeeze_on']==True]
    #if df['df']
        if not df.empty and (df.squeeze_on.sum()==test_days):
            #print(f"Head of {symbol}\n {df.tail(20)}\n")
            save_df[symbol]=df
        return save_df


dirs=['snp500','mega','large','medium','small','micro','nano']
for c,i in enumerate(dirs):
    print(30*'+-+')
    print(f"{c+1}/{len(dirs)} Working for {i}\n")
    root=i+'/'    #dir to read
    test_save_df=check_consolidation(root,multiplier=2,period=10)
    print(f"INTERESTED {i.upper()}:\n {list(test_save_df.keys())}")
