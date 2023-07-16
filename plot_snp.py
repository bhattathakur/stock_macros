#!/usr/bin/env python
# coding: utf-8


# In[1]:


import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


# In[21]:


#plot for the advances and others
choose=['TICKER', 'CP', 'RSI','VOL', 'AVGVOL5', 'CHG%', 'ATR14','TR']
     #  'SECTOR', 'INDUSTRY', 'CATEGORY']
#df=pd.read_csv('/home/thakur/test/combined/all_nasdaq.csv')[choose]
df=pd.read_csv('/home/thakur/test/combined/all_snp.csv')[choose]
category=['mega','large','medium','small']
df=df[(df.CP>5) & (df.VOL>0.1) & (df['CHG%']!=np.inf)]
df.insert(loc=7,column='ATR/CP',value=round(df['ATR14']/df['CP']*100,2))
df.head(20)


# In[25]:


rows=30
df_change_up=df.sort_values(by=['CHG%'],ascending=False).loc[:,['TICKER','CHG%','CP']].head(rows)
df_change_down=df.sort_values(by=['CHG%'],ascending=True).loc[:,['TICKER','CHG%','CP']].head(rows)
df_rsi_up=df.sort_values(by=['RSI'],ascending=False).loc[:,['TICKER','RSI','CP']].head(rows)
df_rsi_down=df.sort_values(by=['RSI'],ascending=True).loc[:,['TICKER','RSI','CP']].head(rows)
df_atr_up=df.sort_values(by=['ATR14'],ascending=False).loc[:,['TICKER','ATR14','CP']].head(rows)
df_atr_down=df.sort_values(by=['ATR14'],ascending=True).loc[:,['TICKER','ATR14','CP']].head(rows)
df_atrpc_up=df.sort_values(by=['ATR/CP'],ascending=False).loc[:,['TICKER','ATR/CP','CP']].head(rows)
df_atrpc_down=df.sort_values(by=['ATR/CP'],ascending=True).loc[:,['TICKER','ATR/CP','CP']].head(rows)
df_volume_up=df.sort_values(by=['VOL'],ascending=False).loc[:,['TICKER','VOL','CP']].head(rows)
#df_change_up=df_change_up.loc[:,['TICKER','%CHG']]
df_atr_up.head()


# In[26]:


#df_change_up.head()


# In[30]:


today=datetime.today().strftime("%m/%d/%Y")

fig,axs=plt.subplots(3,2,figsize=(20,10))
fig.suptitle(f"SNP {today}")
bbox=dict(facecolor='red', alpha=0.5,ha='center')
#positive change
bars=axs[0,0].bar(df_change_up['TICKER'],df_change_up['CHG%'],color='green')
axs[0,0].set_ylabel('%CHG UP')
axs[0,0].tick_params(axis='x', labelrotation=60)
axs[0,0].bar_label(bars,rotation=30)
cp=df_change_up['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[0,0].text(label_x_pos, 0, s=f'{cp[c]}', ha='center',
  va='bottom',rotation=30,color='k',backgroundcolor='pink',fontweight='bold',fontsize=6)
  #axs[0,0].text(label_x_pos, height, s=f'{cp[c]}',bbox=bbox)
#axs[0,0].bar_label(bar0,label=[str(x) for x in df_change_up['CP'].to_list()])
#axs[0,0].bar_label()

#negative change
bars=axs[0,1].bar(df_change_down['TICKER'],df_change_down['CHG%'],color='r')
axs[0,1].set_ylabel('%CHG DOWN')
axs[0,1].tick_params(axis='x', labelrotation=60)
axs[0,1].bar_label(bars,rotation=-30)
cp=df_change_down['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[0,1].text(label_x_pos, 1.5, s=f'{cp[c]}', ha='center',
  va='bottom',rotation=90,color='k',backgroundcolor='pink',fontsize=6,fontweight='bold')

#rsi up
bars=axs[1,0].bar(df_rsi_up['TICKER'],df_rsi_up['RSI'],color='g')
axs[1,0].set_ylabel('RSI UP')
axs[1,0].axhline(y=70,linestyle='--')
axs[1,0].tick_params(axis='x', labelrotation=60)
axs[1,0].bar_label(bars,rotation=30)
cp=df_rsi_up['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[1,0].text(label_x_pos, 5.0, s=f'{cp[c]}', ha='center',
  va='bottom',rotation=90,color='k',backgroundcolor='pink',fontsize=6,fontweight='bold')


#atr
bars=axs[1,1].bar(df_atr_up['TICKER'],df_atr_up['ATR14'],color='g')
axs[1,1].set_ylabel('ATR UP')
#axs[1,1].axhline(y=30,linestyle='--')
axs[1,1].tick_params(axis='x', labelrotation=60)
axs[1,1].bar_label(bars,rotation=30)
cp=df_atr_up['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[1,1].text(label_x_pos, 2.0, s=f'{cp[c]}', ha='center',
  va='bottom',rotation=30,color='k',backgroundcolor='pink',fontsize=6,fontweight='bold')

#atr_pct
bars=axs[2,0].bar(df_atrpc_up['TICKER'],df_atrpc_up['ATR/CP'],color='r')
axs[2,0].set_ylabel('ATR% UP')
#axs[1,1].axhline(y=50,linestyle='--')
axs[2,0].tick_params(axis='x', labelrotation=60)
axs[2,0].bar_label(bars,rotation=30)
cp=df_atrpc_up['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[2,0].text(label_x_pos, 2.0, s=f'{cp[c]}', ha='center',
  va='bottom',rotation=30,color='k',backgroundcolor='pink',fontsize=6,fontweight='bold')

#volume
bars=axs[2,1].bar(df_volume_up['TICKER'],df_volume_up['VOL'],color='g')
axs[2,1].set_ylabel('VOLUME UP')
#axs[1,1].axhline(y=50,linestyle='--')
axs[2,1].tick_params(axis='x', labelrotation=60)
axs[2,1].bar_label(bars,rotation=30)
cp=df_volume_up['CP'].to_list()
for c,bar in enumerate(bars):
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  axs[2,1].text(label_x_pos, 2.0, s=f'{cp[c]}', ha='center',
                va='bottom',rotation=90,color='k',backgroundcolor='pink',fontsize=6,fontweight='bold')



plt.tight_layout()
plt.savefig("plt_snp.pdf")
