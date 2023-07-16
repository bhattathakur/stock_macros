import yfinance as yf
import pandas as pd
import time
from datetime import datetime



ft=20*"x"
now=datetime.now()
d=now.strftime("%m/%d/%Y")

print(f"{ft} DATE:{d} {ft}")
ask=input(f"Do you want to Download the Sector data on and before {d}?: y/n: ")
if(ask=='n'):
    print("quitting...")
    quit()



root="/home/thakur/stock_information/"
save_dir="/home/thakur/test/"



def yahoo_download(fil,save):
    """Downloads the files from yahoo for the given category of the nasdaq and saves to the save dir"""
    
    print(f"\nWorking with {fil}:\n")
    time.sleep(5) #sleep for 5 seconds
    st_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['Symbol'])#[:5]  #list of files to be downloaded
    st_list=[i.strip() for i in st_list]
    more=['SPY']
    st_list+=more
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
    

directories=["/home/thakur/stock_information/"]
input_files=["sectors"]
error_flage=[]
#i=0
for i in range(1):
    #if not i in [0,1]:continue
    #yahoo_download(input_files[i], save_dir+directories[i])

    try:
        yahoo_download(input_files[i], save_dir+"sector/")

    except:
        err="Error while downloading {} files".format(i)
        error_flage.append(err)
        print(err)

#printing errros if exists
if not error_flage:
    print("No error!")
else:
    for i in error_flage:print("{}\n".format(i))

