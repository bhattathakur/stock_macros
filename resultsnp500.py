#!/bin/python3
"""
Analyses S&P500 data and saves in a file
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
    deno=(100+pct_change)
    previous_price=(100*cp)/(100+pct_change) if deno!=0 else 0
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
  <head><title>SNP500 Stock Analysis</title></head>
  <h1>{TEST}</h1>
  <h4>({DATE})</h4>
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
        f.write(html_string.format(table=df.to_html(classes='mystyle',justify='center',render_links=True),TEST=title,DATE=date))


    #df.to_html(html_folder.format(save),index=True,render_links=True,justify='center',classes='mystyle')
    #df.to_xml(html_folder.format(save),stylesheet='DataFrameStyle.xsl')


info_str="{}:\n{}"
#dataframe with snp company list and other information
snp_df=pd.read_csv("/home/thakur/stock_information/snp500finalwvol.csv")
#print(info_str.format("snp500",snp_df))

#read the dataframe and calculate the values
csv_source="/home/thakur/test/snp500/"
st_list=snp_df['SYMBOL'].to_list()
#print(info_str.format("snpcsv",st_list))

#Analysing snp500

#Reading the files
ticker_list=[]           #store ticker
current_price=[]         #current price

HH=[]                    #higher high
HL=[]                    #higher low
LH=[]                    #lower high
LL=[]                    #lower low
HC=[]                    #higher close
HV=[]                    #higher volume
rsi=[]                   #rsi list
sma_5=[]                 #sma_5 list
EMA8=[]                  #ema8
sma_10=[]                 #sma_10 list
sma_21=[]                 #sma_21 list
sma_50=[]                 #sma_50 list
sma_200=[]                 #sma_200 list
vol=[]                    #vol today
avgvol=[]                 #avg volume
pt_change=[]             #% change
tr=[]                   #atr
atr=[]                #average 10 day atr
sec_list=[]             #sector
ind_list=[]             #industry
bwidth=[]               #bollinger bandwith
d=3                     #days for hh etc.
j=1                     #counter
fil="s&p-500"

for f in st_list[:]:    #read these files
    #if f not in ['AAPL']:continue
    if(j-1)%50==0:print(f"{j}/{len(st_list)} {fil} : {f}\n")
    j+=1

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

    #sma10
    sma10=round(df.tail(10)['Close'].mean(),2)
    #print(f"sma5: {sma5}")
    sma_10.append(sma10)

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

    #higher volume
    hv=df.tail(d)['Volume'].is_monotonic_increasing
    #print(f"HC: {hc}\n")
    HV.append(hv)

    #last volume
    av=(df.tail(6).head(5)['Volume'].mean())/10**6  #avg volume for past5 days excluding today
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
    #df_20=df.tail(24) #for 10 day avg atr
    #changing the parameters for using abstract library
    df.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'},inplace=True)
    atrr=abstract.ATR(df.tail(20))
    avgatr=atrr.tail(2).head(1).mean().round(2)
    #at=round(ta.atr(df_20['High'],df_20['Low'],df_20['Close']).values[-1],2)
    tran=abstract.TRANGE(df.tail(2)).mean().round(2)
    #print(f"atr: {at}")
    tr.append(tran)
    atr.append(avgatr)

    #getting the width of bband
    sd=1;period=14
    u,m,l=talib.BBANDS(df.close,timeperiod=period, nbdevup=sd, nbdevdn=sd)
    u=u.tail(1).values[0];m=m.tail(1).values[0];l=l.tail(1).values[0];w=round((u-l)/m,2)
    # print(f"u: {u}");print(f"m: {m}");print(f"l: {l}")
    # print(f"w: {w}")
    bwidth.append(w)




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
                          "SMA10":sma_10,
                          "SMA21":sma_21,
                          "SMA50":sma_50,
                          "SMA200":sma_200,
                          "VOL":vol,
                          "AVGVOL5":avgvol,
                          "CHG%":pt_change,
                          "ATR14":atr,
                          "TR":tr,
                          "W":bwidth
                         })
temp_df.to_csv("/home/thakur/test/combined/all_snp.csv",index=False)
print("Created the file /home/thakur/test/combined/all_snp.csv\n")

final=pd.concat([temp_df,snp_df],axis=1,join='inner',ignore_index=False)
final=final.drop(["SYMBOL"],axis=1)
final=final.sort_values(by=['CP'])
final=change_index(final)
final["TURN"]=round(final["VOL"]/final["FLOAT"]*100,2)
#new order
co=final.columns.to_list();c=co[:20]+co[23:]+co[20:23]
final=final[c]
final['CHG']=final.apply(lambda x: get_change(x['CP'],x['CHG%']),axis=1)
#print(f"Total length: {len(final.index)}\n")
final.to_csv("TXT/snptemp.txt",sep='\t',index=True)
#final.to_html("HTML/snptemp.html",index=True,render_links=True)
print("final snp \n",final.head())


#top10 % TURNOVER
final_turn=final.sort_values(by=["TURN"],ascending=False)
final_turn=drop_cols(final_turn)
final_turn=change_index(final_turn)
save_txt_html(final_turn,'snp_turn','TURN',today)  #FUNCTION

#Highest +ve Change
high_change=final.sort_values(by=['CHG%'],ascending=False)
high_change=change_index(high_change)
save_txt_html(high_change,'snp_positive_change','+VE CHANGE',today)      #FUNCTION  
save_txt_html(high_change[::-1],'snp_negative_change','-VE CHANGE',today)#FUNCTION

#ATR values
df_atr=final
df_atr['%']=round(100*df_atr['ATR14']/df_atr['CP'],2)
df_atr=df_atr.sort_values(by=['%'],ascending=False)
df_atr=drop_cols(df_atr)
df_atr=change_index(df_atr)
save_txt_html(df_atr,'snp_atr','ATR%',today)#FUNCTION

#Highest Volume
vol_highest=final.sort_values(by=['VOL'],ascending=False)
vol_highest=change_index(vol_highest)
save_txt_html(vol_highest,'snp_volume','HIGHEST VOLUME',today) #FUNCTION

#HH, HL
ti=' SNP VOL > AVGVOL5; %CHG > 0; CP > SMA5; SMA5 > SMA10)'
hh=final[final['HH']==True];
hl=final[final['HL']==True];
# hc=final[final['HC']==True];
# hv=final[final['HV']==True]
df_chg=final[(final['VOL']>final['AVGVOL5']) & (final['CHG%']>0) & (final['CP']>final['SMA5'])&(final['SMA5']>final['SMA10'])
             & (final['HH']==True) & (final['HL']==True)]
df_chg.sort_values(by=['CP'])
df_chg=change_index(df_chg)
save_txt_html(df_chg,'snp_chg',ti,today) #FUNCTION

#CP>SMA50; CP>SMA200; SMA50>SMA200
ti1=" SNP(CP>SMA50; CP>SMA200; SMA50>SMA200)"
f1=final['CP']>final['SMA50']
f2=final['CP']>final['SMA200']
f3=final['SMA50']>final['SMA200']
df_above=final[f1 & f2 &f3]
df_above=change_index(df_above)
save_txt_html(df_above,'snp_above50n200',ti1,today) # FUNCTION

#best
ti2=" SNP(HH; HL; HC; CP>SMA50; VOL>AVGVOL5)"
df_hl=final[(final['HH']==True) & (final['HL']==True)  & (final['CP']>final['SMA50'])
            #& (final['EMA8']>final['CP'])
            & (final['HC']==True) & (final['VOL']>final['AVGVOL5'])]# & (final['CP']>final['SMA200'])]
df_hl.loc[:,"SMA50-CP"]=df_hl.loc[:,"SMA50"]-df_hl.loc[:,"CP"]
df_hl=df_hl.sort_values(by=["CP"],ascending=True)
df_hl=change_index(df_hl)
save_txt_html(df_hl,'snp_best',ti2,today)#FUNCTION



