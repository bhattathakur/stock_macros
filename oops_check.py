#!/bin/python3
import pandas as pd
import os


all_oops=[]
dirs=['mega','large','medium','small']#,'micro','nano','snp500']
for k,j in enumerate(dirs[:]): 
    dir_name='/home/thakur/test/{}/'.format(dirs[k])
    tickers=os.listdir(dir_name)
    oops=[]
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
        open_today=today['Open'].values[0];close_today=today['Close'].values[0]
        # print(f"Yesterday's low for {tick}:\n{low_yesterday}")
        # print(f"Today's open for {tick}:\n{open_today}")
        # print(f"Today's close for {tick}:\n{close_today}")
        oops_status=True if (open_today<low_yesterday and close_today>low_yesterday) else False
        #print(f"oops_status for {tick}: {oops_status}\n")
        if oops_status:oops.append(tick)
        #snp500 stock list

    all_oops+=oops

    print(f"Tickers following OOPS condition for {j}:\n{oops}\n")
print(f"ALL Tickers following OOPS condition for:\n{all_oops}\n")

