#!/bin/python3
import pandas as pd
import numpy as np
from datetime import date

#read the file
#marknasdaq_mega120922.csv
output_files=["marknasdaq_mega", "marknasdaq_large","marknasdaq_medium","marknasdaq_small","marknasdaq_micro","marknasdaq_nano"]
save_dir="/home/thakur/test/combined/"
today=date.today()
today=today.strftime("%m%d%y")
#overide due to delay analysis
#today='120922'

print("Combining the mark data .. \n")
#print(f"Today: {today}\n")

print(f"Working on the data on {today}")
df_mega=pd.read_csv(save_dir+output_files[0]+today+".csv")
df_large=pd.read_csv(save_dir+output_files[1]+today+".csv")
df_medium=pd.read_csv(save_dir+output_files[2]+today+".csv")
df_small=pd.read_csv(save_dir+output_files[3]+today+".csv")
df_micro=pd.read_csv(save_dir+output_files[4]+today+".csv")
df_nano=pd.read_csv(save_dir+output_files[5]+today+".csv")

#giving name to the category
df_mega['CATEGORY']="mega";df_large['CATEGORY']="large";df_medium["CATEGORY"]="medium";df_small["CATEGORY"]="small"
df_micro['CATEGORY']="micro";df_nano['CATEGORY']="nano"

#
df_total=pd.concat([df_mega,df_large,df_medium,df_small,df_micro,df_nano])
df_total.index=np.arange(1,len(df_total.index)+1)
print(f"df_total:\n{df_total}")

#saving all in a file
save_file=save_dir+'all_mark.csv'
print(f"Saving all nasdaq in the file: {save_file}")

df_total.to_csv(save_file,index=False)
