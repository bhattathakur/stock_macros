#!/bin/python3
import os
"""
This program removes the spaces around the ticker and also changes . to -.
Done once new file is downloaded
"""
import pandas as pd

root='/home/thakur/stock_information/'
files=['mega','large','medium','small','micro','nano']

#removing the stocks which are already in the folders 
def check_empty(path):
    """
    checks if the dir is empty or not
    """
    if len(os.listdir(path))==0:print(path+" is empty!\n")
    else:print(path+" is not empty!\n")


for i in files:
    check_empty("/home/thakur/test/"+i)
    command='rm -rf /home/thakur/test/'+i+'/*'
    print("Running the command:\n",command)
    os.system(command)
    check_empty("/home/thakur/test/"+i)

    #chk_empty='find /home/thakur/test/'+i+' -maxdepth 0 -empty -exec echo {} is empty.\;'
    #print("Running the command:\n",chk_empty)
    #os.system(chk_empty)

#os.sys.exit(0)


#make sure dirs are empty    
#for i in files:
#find large/ -maxdepth 0 -empty -exec echo {} is empty. \


for i in files:
    print(f"\nFiltering {i}...\n")
    file=root+"nasdaq_"+i+".csv"
    df=pd.read_csv(file,keep_default_na=False)
    print("\ndf-head\n",df.head(3))
    df.Symbol=df.Symbol.apply(lambda x:x.strip() if type(x) is str else x)
    df.Symbol=df.Symbol.apply(lambda x:x.replace('/','-') if type(x) is str else x)
    df.to_csv(file,index=False)
print("\nDONE\n")
