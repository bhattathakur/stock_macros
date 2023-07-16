#!/bin/python3
"""
This program creates the html pages with tick's increment in daily, weekly, or monthly basis
"""

#libraries
import pandas as pd
from datetime import datetime
import sys
import os
sys.path.append('/home/thakur/test')
import html_template as html
import numpy as np


#today
today=datetime.now().strftime('%m%d%y')
#today='100722'
def get_status_df(file,days=3):
    """
    Checks whether the df is increasing for days, weeks and months and retrns the list.
    """
    #read the file
    df_day=pd.read_csv(file)
    df_day['Date']=df_day['Date'].apply(lambda x:x.split()[0])
    df_day["Date"] = pd.to_datetime(df_day["Date"])
    #df_day["Date"]=df_day["Date"].apply(lambda x:x.strftime("%Y-%m-%d"))
    df_day.set_index("Date", inplace=True)
    #df_day.index=pd.to_datetime(df_day.index,unit='s')
    #tick
    tick=file.split('.')[0].split('/')[-1]

    #get the dataframe
    df_daily=df_day['Adj Close'].tail(days)
    df_monthly=df_day['Adj Close'].resample(rule='BM').last().tail(days)
    df_weekly=df_day['Adj Close'].resample(rule='W').last().tail(days+1)
    #print(50*'==')
    #print("Daily  :\n",df_daily)
    #print("Weekly :\n",df_weekly)
    #print("Monthly:\n",df_monthly)

    #checking the status
    month_increasing=df_monthly.is_monotonic_increasing
    month_decreasing=df_monthly.is_monotonic_decreasing
    week_increasing=df_weekly.is_monotonic_increasing
    week_decreasing=df_weekly.is_monotonic_decreasing
    day_increasing=df_daily.is_monotonic_increasing
    day_decreasing=df_daily.is_monotonic_decreasing

    chk_day="up" if day_increasing else "down" if day_decreasing else "none"
    chk_week="up" if week_increasing else "down" if week_decreasing else "none"

    chk_month="up" if month_increasing else "down" if month_decreasing else "none"
    #print([tick,chk_day,chk_week,chk_month])
    return [tick,chk_day,chk_week,chk_month]


def get_multiple_df(df,save_name):
    d_up=(df['DAILY']=='up');d_down=(df['DAILY']=='down')
    w_up=(df['WEEKLY']=='up');w_down=(df['WEEKLY']=='down')
    m_up=(df['MONTHLY']=='up');m_down=(df['MONTHLY']=='down')
    #day up, week up, month up
    condition1=((d_up) & (w_up) & (m_up))
    df_1=df[condition1]
    #print(f"df_duwupmup:\n{df_1}")
    #opening the combined dataframe from the nasdaq
    root='/home/thakur/test/combined/nasdaq_'+save_name+today+'.csv'
    df_all=pd.read_csv(root)
    #print("df:\n",df_all.head())
    temp="up_dwm_"+save_name
    #temp=save_name+"_dwm_up"
    #print(f"save_name: {temp}")
    vol_limit=0.05
    if not df_1.empty:
        df_1=df_all[df_all['TICKER'].isin(df_1['TICKER'].to_list())]
        df_1=df_1[(df_1['CP']>1.0)&(df_1['%CHG']>0.0) & (df_1['AVGVOL']>vol_limit)]
        df_1=df_1.sort_values(by=['CP'])
        df_1.index=np.arange(1,df_1.shape[0]+1)
        html.save_txt_html(df_1,temp,temp) #df,save,title,rows=100
    #df_1.to_csv(csb_folder.format(temp))

    #day up, week up
    condition2=((d_up) & (w_up))
    df_2=df[condition2]
    #print(f"df_dup_wup:\n{df_2}")
    #temp=save_name+"_dw_up"
    temp="up_dw_"+save_name
    #print(f"save_name: {temp}")
    if not df_2.empty:
        df_2=df_all[df_all['TICKER'].isin(df_2['TICKER'].to_list())]
        df_2=df_2[(df_2['CP']>1.0)& (df_2['%CHG']>0.0) & (df_2['AVGVOL']>vol_limit)]
        df_2=df_2.sort_values(by=['CP'])
        df_2.index=np.arange(1,df_2.shape[0]+1)
        html.save_txt_html(df_2,temp,temp) #df,save,title,rows=100

    #week up, month up
    condition3=((m_up) & (w_up))
    df_3=df[condition3]
    #print(f"df_wup_mup:\n{df_3}")
    #temp=save_name+"_wm_up"
    temp="up_dw_"+save_name
    print(f"save_name: {temp}")
    if not df_3.empty:
        df_3=df_all[df_all['TICKER'].isin(df_3['TICKER'].to_list())]
        df_3=df_3[(df_3['CP']>1.0) & (df_3['%CHG']>0.0) & (df_3['AVGVOL']>vol_limit)]
        df_3=df_3.sort_values(by=['CP'])
        df_3.index=np.arange(1,df_3.shape[0]+1)
        html.save_txt_html(df_3,temp,temp) #df,save,title,rows=100

    #month up
    condition4=((d_up)&(m_up))
    df_4=df[condition4]
    #print(f"df_dup_mup:\n{df_4}")
    #temp=save_name+"_dm_up"
    temp="up_dm_"+save_name
    print(f"save_name: {temp}")
    if not df_4.empty:
        df_4=df_all[df_all['TICKER'].isin(df_4['TICKER'].to_list())]
        df_4=df_4[(df_4['CP']>1.0) & (df_4['%CHG']>0.0) & (df_4['AVGVOL']>vol_limit)]
        df_4=df_4.sort_values(by=['CP'])
        df_4.index=np.arange(1,df_4.shape[0]+1)
        html.save_txt_html(df_4,temp,temp) #df,save,title,rows=100

#file_dirs=["/home/thakur/test/mega/","/home/thakur/test/large/","/home/thakur/test/medium/","/home/thakur/test/"]
root="/home/thakur/test/"
sources=["mega","medium","large","small"]#,"micro","nano"]#,"snp500"]
file_dirs=[root+i+"/" for i in sources]
columns=['TICKER','DAILY','WEEKLY','MONTHLY']
for c,d in enumerate(file_dirs):
    print(f"{c+1}/{len(sources)}) Working for {sources[c]} ...\n")
    save_file=sources[c]
    print(f"save_file: {save_file}\n")
    temp=[]
    tickers=os.listdir(d)
    for tick in tickers:
        file=d+tick
        temp.append(get_status_df(file))
    #print(f"temp: {temp}\n")
    test=pd.DataFrame(temp,columns=columns)
    get_multiple_df(test,save_file)
