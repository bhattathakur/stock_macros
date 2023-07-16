#!/bin/python3
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import talib
from datetime import datetime
import os

root="/home/thakur/stock_information/"
save_dir="/home/thakur/test/combined/"
source_dir="/home/thakur/test/"

ft=20*"0"
now=datetime.now()
d=now.strftime("%m/%d/%Y")


print(f"\n{ft} DATE:{d} {ft}")
print("Getting combined DataFrame for all\n")
#ask=input(f"\nDo you want to Combine the data on {d}?: y/n: ")
#if(ask!='y'):
#    print("quitting...\n")
#    quit()


def data_combine(fil,csv_source,save_file,d=3):
    """Returns the combined data files from ghe given information. Note d is monotonic in(de)crease days!"""
    
    print(f"Working with {fil}:\n")
    dff=pd.read_csv(root+fil+".csv",keep_default_na=False)  #dataframe
    st_list=list(dff['Symbol'])       #list of files  downloaded
    st_list=[i.strip() for i in st_list]

    #st_list=list(pd.read_csv(root+fil+".csv")['Symbol'])  #list of files  downloaded
    #print(f"st_list:\n{st_list}")
    
    
    #Reading the files
    ticker_list=[]           #store ticker
    current_price=[]         #current price
    ipo=list(dff['IPO Year'])#IPO date
    country=list(dff['Country'])#country

    HH=[]                    #higher high
    HL=[]                    #higher low
    LH=[]                    #lower high
    LL=[]                    #lower low
    HC=[]                    #higher close
    rsi=[]                   #rsi list
    sma_5=[]                 #sma_5 list
    sma_21=[]                 #sma_21 list
    sma_50=[]                 #sma_50 list
    sma_200=[]                 #sma_200 list
    vol=[]                    #vol today
    avgvol=[]                 #avg volume
    pt_change=[]             #% change
    atr=[]                   #atr
    sec_list=[]                   #sector
    ind_list=[]                   #industry
    HV=[]                     #higher volume
    EMA8=[]                 #EMA8

 
    j=1
    for f in st_list:#[:5]:    #read these files
        #if j==2:break
        print(f"{j}/{len(st_list)} {fil} : {f}\n")
        j+=1
        #read the file
        #industry and sector 
        sec=dff.loc[dff['Symbol']==f]["Sector"].values[0]

        ind=dff.loc[dff['Symbol']==f]["Industry"].values[0]
        sec_list.append(sec);ind_list.append(ind)
        #print(f"{f}\t{sec}\t{ind}\n")

        #print("source dir\t",csv_source)
        df=pd.read_csv(csv_source+f+".csv")
        df.fillna(0,inplace=True)
        
        #print the tail
        #print(f"Tail of {i}\n {df.tail(1)}")
       
        #ticker
        ticker_list.append(f)
        
        #current price 
        cp=round(df.tail(1)['Close'].values[0],2)
        #print(f"Current Price: {cp}")
        current_price.append(cp)
        
        #higher high
        hh=df.tail(d)['High'].is_monotonic_increasing
        #print(f"HH: {hh}\n")
        HH.append(hh)
        
        ##higher low
        hl=df.tail(d)['Low'].is_monotonic_increasing
        #print(f"HL: {hl}\n")
        HL.append(hl)
        
        #lower high
        lh=df.tail(d)['High'].is_monotonic_decreasing
        #print(f"LH: {lh}\n")
        LH.append(lh)
        
        ##lower low
        ll=df.tail(d)['Low'].is_monotonic_decreasing
        #print(f"LL: {ll}\n")
        LL.append(ll)
        
        #higher close
        hc=df.tail(d)['Close'].is_monotonic_increasing
        #print(f"HC: {hc}\n")
        HC.append(hc)

        #higher volume
        hv=df.tail(d)['Volume'].is_monotonic_increasing
        #print(f"HC: {hc}\n")
        HV.append(hv)
        
        
        #rsi
        rs=df.ta.rsi()[-1:].round(2).values[0]
        #print(f"rs\t{rs}")
        rsi.append(rs)
        
        #sma5
        sma5=round(df.tail(5)['Close'].mean(),2)
        #print(f"sma5: {sma5}")
        sma_5.append(sma5)

        #ema8
        ema8=round(talib.EMA(df.tail(100)['Close'],timeperiod=8).values[-1],2)
        EMA8.append(ema8)
        
        #sma21
        sma21=round(df.tail(21)['Close'].mean(),2)
        #print(f"sma21: {sma21}")
        sma_21.append(sma21)
        
        #sma50
        sma50=round(df.tail(50)['Close'].mean(),2)
        #print(f"sma50: {sma50}")
        sma_50.append(sma50)
        
        #sma200
        sma200=round(df.tail(200)['Close'].mean(),2)
        #print(f"sma200: {sma200}")
        sma_200.append(sma200)
        
        #last volume
        v=(df.tail(1)['Volume'].values[0])/10**6
        v=round(v,2)
        vol.append(v)
        #print(f"today's volume {v} thousands")
        
        #last volume
        av=(df.tail(5)['Volume'].mean())/10**6
        av=round(av,2)
        avgvol.append(av)
        #print(f"today's volume {av} thousands")

        #pct change
        pct=round((df.tail(2)['Close'].pct_change().values[1])*100,2)
        #print(f"%Change:\n {pct}")
        #pct=2
        pt_change.append(pct)
        #pct_change.append(pct)
        #print(f"%Change: {pct}")
        
        #atr value
        df_20=df.tail(20)
        at=round(ta.atr(df_20['High'],df_20['Low'],df_20['Close']).values[-1],2)
        #print(f"atr: {at}")
        atr.append(at)

        #check if volume increases for 3 consecutive period

        
        
        
        
    #create the data-frame
    temp_df=pd.DataFrame({"TICKER":ticker_list,
                          "CP":current_price,
                          "EMA8":EMA8,
                          "HH":HH,
                          "HL":HL,
                          "LH":LH,
                          "LL":LL,
                          "HC":HC,
                          "HV":HV,
                          "RSI":rsi,
                          "SMA5":sma_5,
                          "SMA21":sma_21,
                          "SMA50":sma_50,
                          "SMA200":sma_200,
                          "VOL":vol,
                          "AVGVOL":avgvol,
                          "%CHG":pt_change,
                          "ATR":atr,
                          "SECTOR":sec_list,
                          "INDUSTRY":ind_list,
                          "IPO":ipo,
                          "COUNTRY":country,
                         })
    temp_df.to_csv(save_file,index=False)   
    print(f"Done with {fil}\n")


input_files=["nasdaq_mega", "nasdaq_large","nasdaq_medium","nasdaq_small","nasdaq_micro","nasdaq_nano"]
directories=["mega/","large/","medium/","small/","micro/","nano/"]    
today=datetime.today()
today=today.strftime("%m%d%y")
#today='040523'
print(f"Today: {today}\n")
#n=0
for n in range(6):
    #if n!=5: continue
    data_combine(input_files[n],source_dir+directories[n],save_dir+input_files[n]+today+".csv")
    #try:
    #    data_combine(input_files[n],source_dir+directories[n],save_dir+input_files[n]+today+".csv")
    #except:
    #    pass
        #print("Error occured !")
        #continue
    
    
    
#print("Files Created!\n")
#os.listdir('save_dir')
