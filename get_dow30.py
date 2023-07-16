#!/bin/python3
#to create the dow-30 directory 
import os
import pandas as pd
import yfinance as yf

snp_df=pd.read_csv("/home/thakur/stock_information/dow.csv",keep_default_na=False)['Symbol'].tolist() #dow 30
print(f"DOW30: \n{len(snp_df)}")
snp_df=[i.replace(".","-") for i in snp_df]
save_loc="/home/thakur/test/dow30/"

print(f"SAVE DIR: {save_loc}")

#unfound=snp_df.copy()
#print("unfound\n",unfound)

base="/home/thakur/test/"
files=["mega/","large/","medium/","small/","micro/","nano/"]

for c,i in enumerate(snp_df):
    if c%50==0:print(f"{c+1}/{len(snp_df)} Checking for ->{i}..")
    #i.replace(".","-")
    #if i=='BRK.B' 'BF.B']
    f=i+".csv"
    loc1=base+files[0]+f
    loc2=base+files[1]+f
    loc3=base+files[2]+f
    loc4=base+files[3]+f
    loc5=base+files[4]+f
    if os.path.exists(loc1):
        #print(f"file {f} exists @: {loc1}\n") 
        c1="cp "+loc1+" "+save_loc 
        os.system(c1) 
        #unfound.remove(i)
    elif os.path.exists(loc2):
        #print(f"file {f} exists @: {loc2}\n") 
        c2="cp "+loc2+" "+save_loc 
        os.system(c2) 
        #unfound.remove(i)
    elif os.path.exists(loc3):
        #print(f"file {f} exists @: {loc3}") 
        c3="cp "+loc3+" "+save_loc 
        os.system(c3) 
        #unfound.remove(i)
    elif os.path.exists(loc4):
        #print(f"file {f} exists @: {loc4}") 
        c4="cp "+loc4+" "+save_loc 
        os.system(c4) 
        #unfound.remove(i)
    elif os.path.exists(loc5):
        #print(f"file {f} exists @: {loc5}") 
        c5="cp "+loc5+" "+save_loc 
        os.system(c5) 
        #unfound.remove(i)

##download and save BRK-B and BF-B
#dlist=['BRK-B','BF-B']
#
#data = yf.download(
#     tickers=dlist,
#     period='52wk',
#     threads=True,
#     group_by='ticker',
#     rounding=True)
#
#for i in dlist:
#    df=data[i]
#    df.to_csv(save_loc+i+".csv")
#    print(f"{i}.csv created @{save_loc}!")
#
#
#unfound=snp_df
#print("unfound\n",unfound)
