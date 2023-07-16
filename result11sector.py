#!/bin/python3
'''
Sector information results
'''

#libraries
import pandas as pd
import numpy as np
import pandas_ta as ta
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
today=datetime.now().strftime("%m/%d/%Y")


#data download
st_df=pd.read_csv("/home/thakur/stock_information/sectors.csv")  #11 sectors
st_list=st_df["TICKER"].to_list()
#Download all tickers
save="/home/thakur/test/sector/"
print(f"\nDowloading {st_list} data from yahoo finance...\n")
data = yf.download(
tickers=st_list,
period='52wk',
threads=True,
group_by='ticker',
rounding=True)

#save to csv filesb
#print(f"Saving to {save}...\n")
for i in st_list:
    df=data[i]
    df.to_csv(save+i+".csv")
    print(f"{i}.csv created !")

print("\ncreating the dataframe\n")
#Reading the files
ticker_list=[]           #store ticker
current_price=[]         #current price

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
sec_list=[]             #sector
ind_list=[]             #industry
d=3                     #days for hh etc.
j=1                     #counter
fil="sector"
csv_source="/home/thakur/test/sector/"
for f in st_list:#[:5]:    #read these files
    print(f"{j}/{len(st_list)} {fil} : {f}\n")
    j+=1

    #print("source dir\t",csv_source)
    df=pd.read_csv(csv_source+f+".csv")

    #head of the file
    #print(f"Last lines of the file {f}\n")
    df.fillna(0,inplace=True)

    #print the tail
    #print(f"Tail of {f}\n {df.tail(5)}")

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
    av=(df.tail(d)['Volume'].mean())/10**5
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
    df_20=df.tail(24) #for 10 day avg atr
    #at=round(ta.atr(df_20['High'],df_20['Low'],df_20['Close']).values[-1],2)
    at=round(ta.atr(df_20['High'],df_20['Low'],df_20['Close']).mean(),2)
    #print(f"atr: {at}")
    atr.append(at)




#create the data-frame
temp_df=pd.DataFrame({"TICKER":ticker_list,
                          "CP":current_price,
                          "HH":HH,
                          "HL":HL,
                          "LH":LH,
                          "LL":LL,
                          "HC":HC,
                          "RSI":rsi,
                          "SMA5":sma_5,
                          "SMA21":sma_21,
                          "SMA50":sma_50,
                          "SMA200":sma_200,
                          "VOL":vol,
                          "AVGVOL":avgvol,
                          "%CHG":pt_change,
                          "AVG10ATR":atr,
                         })

temp_df.to_csv('/home/thakur/test/combined/all_sectors.csv',index=False)
temp_df["SECTOR"]=st_df["SECTOR"];temp_df["SUBINDUSTRY"]="N/A";temp_df["NAME"]="N/A"
#temp_df=temp_df[(temp_df['HH']==True)&(temp_df['HL']==True)]
temp_df=temp_df.sort_values(by=['RSI'],ascending=False)
#temp_df=change_index(temp_df)
#temp_df.set_index('TICKER',inplace=True)
#temp_df.head(25)
plot_df=temp_df[['TICKER','RSI','VOL','%CHG','AVG10ATR']]
#plot_df.loc[:,'%CHG']=plot_df.loc[:,'%CHG'].multiply(10)
#plot_df.reset_index(inplace=True)
columns=plot_df.columns.to_list()
x=columns[0];y=columns[1:]


# sns.set_style("whitegrid", {
#     "ytick.major.size": 0.1,
#     "ytick.minor.size": 0.05,
#     'grid.linestyle': '--'
#  })

# Apply the default theme
sns.set_theme()
#sns.bar(plot_df)
# sns.barplot(data=plot_df,x='TICKER',y='RSI')
# sns.barplot(data=plot_df,x='TICKER',y='VOL')
f, axs = plt.subplots(2, 2, figsize=(15, 10), gridspec_kw=dict(width_ratios=[4, 4]))
cols=axs.flat
for i,j in enumerate(y):
    sns.barplot(data=plot_df,x=x,y=y[i],ax=cols[i])
f.suptitle(f"SECTOR {today}")
#plt.grid(color='r')
f.tight_layout()
print("Saving the plot ")
f.savefig("sector.pdf")

