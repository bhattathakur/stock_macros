#!/bin/python3
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import os
import subprocess,shlex



ft=20*"x"
now=datetime.now()
d=now.strftime("%m/%d/%Y")
#getting each category list
print("running the file seperate_nasdaq_cat.py\n")
os.system('python3 /home/thakur/test/seperate_nasdaq_cat.py')
#filtering the ticks before download
print("running the file filterticks.py\n")
os.system('python3 /home/thakur/test/filterticks.py')
#check the status of the last downloaded file
print('Last updated NASDAQ list:\n')
command="ls /home/thakur/stock_information/ -lt | head -7 | tail -5 | awk '{print $6,$7,$8,$9}'"
#subprocess.run(shlex.split(command))
os.system(command)
print("\n")



print(f"{ft} DATE:{d} {ft}")
#default='y'
#ask=input(f"Do you want to Download the data on {d}?: y/n: ")or default
#if(ask=='n'):
#    print("quitting...")
#    quit()
#


root="/home/thakur/stock_information/"
save_dir="/home/thakur/test/"



def yahoo_download(fil,save):
    """Downloads the files from yahoo for the given category of the nasdaq and saves to the save dir"""
    
    print(f"\nWorking with {fil}:\n")
    time.sleep(5) #sleep for 5 seconds
    st_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['Symbol'])#[:5]  #list of files to be downloaded
    st_list=[i.strip() for i in st_list]
    print(f"st_list:\n{st_list}")
    
    
    #Download all tickers
    print(f"\nDowloading {fil} from yahoo finance...\n")
    data = yf.download(
    tickers=st_list,
    period='52wk',
    threads=True,
    group_by='ticker',
    rounding=True)
    
    #save to csv files
    print(f"Saving to {save}...\n")
    for i in st_list:
        df=data[i]
        df.to_csv(save+i+".csv")
        print(f"{i}.csv created !")
        #print(f"{i} head:\n")
        #print(df.head(1))
    

directories=["mega/","large/","medium/","small/","micro/","nano/"]
input_files=["nasdaq_mega", "nasdaq_large","nasdaq_medium","nasdaq_small","nasdaq_micro","nasdaq_nano",]
error_flage=[]
#i=0
t1=datetime.now()
for i in range(6):
    #if i in [0,1,2,3,4]:continue
    #yahoo_download(input_files[i], save_dir+directories[i])

    try:
        yahoo_download(input_files[i], save_dir+directories[i])

    except:
        err="Error while downloading {} files".format(i)
        error_flage.append(err)
        print(err)

#printing errros if exists
if not error_flage:
    print("No error!")
else:
    for i in error_flage:print("{}\n".format(i))

t2=datetime.now()

time_taken=round((t2-t1).total_seconds()/60.0,2)

print(f"Time Taken {time_taken} mins\n")
