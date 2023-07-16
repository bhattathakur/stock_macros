#!/bin/python3
#reset the index
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import seaborn as sns

#for any ticker
#ticker='TSLA'
sns.set_theme()
ticker=input("Enter the ticker: ")
gap='1m'
days='6d'
df = yf.download(
tickers=[ticker],
period=days,
threads=True,
interval=gap,
group_by='ticker',
rounding=True)
#reset the index
df=df.reset_index()
S = pd.to_datetime(df.Datetime)

sty='yahoo';typ='candle'
#fig,axs=plt.subplots(5,1)
fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(16,12))
cols=axes.flat
#print(f"{cols}")
j=5
for i, g in df.groupby([(S- S[0]).astype('timedelta64[D]')]):
    g.Volume=round(g.Volume/10**6,2);
    #fig,axes=mpf.plot(g,type=typ,mav=5,volume=True,tight_layout=False,figratio=(24,12),figscale=1,
    #                returnfig=True,style=sty)
    #print(g.head())
    #print(g.dtypes)
    #g['Adj Close'].plot()
    g.plot(x='Datetime',y='Adj Close',ax=cols[j])
    #g.plot(x='Datetime',y='Volume',ax=cols[j])
    g.plot(x='Datetime',y='Volume',secondary_y=True, ax=cols[j],mark_right=False,color='g')
    #g.plot(x='Datetime',y='Volume',secondary_y=True, ax=cols[j],kind='line',mark_right=False,color='g')
    cols[j].set_ylabel("Price ($)");
    cols[j].right_ax.set_ylabel("Volume (mln)");
    xposition=cols[j].get_xticks()
    for xc in xposition:
        cols[j].axvline(x=xc, color='r', linestyle=':')
    #par='Close'
    #print(f"{j+1})Closes:\n {g[par]}")
    op=g.Open.values[0]
    cl=g.Close.values[-1]
    hi=g.High.max()
    lo=g.Low.min()
    vo=g.Volume.sum().round(2)
    st=f"\nopen   : {op}\
        \nlow    : {lo}\
           \nhigh   : {hi}\
         \nclose  : {cl}\
         \nvolume : {vo} mln"
    print(st)
    #cols[j].text(0.5,0.3,st,transform=cols[j].transAxes,color='blue',fontsize=15,fontweight='bold',horizontalalignment='left')
    cols[j].text(0.7, 0.3, st, style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.05, 'pad': 10},transform=cols[j].transAxes,color='blue',fontsize=12,fontweight='bold')
    #g['Close'].plot(ax=axes[count,count])
    j-=1
    # ax=g.plot(x='Datetime',y='Adj Close',figsize=(4,3),legend=True)
    # xposition=ax.get_xticks()
    # for xc in xposition:
    #     ax.axvline(x=xc, color='r', linestyle=':')
    #print(t)
plt.tight_layout()
fig.suptitle(ticker)
save_q=input("Do you wnat to save the plot: ")
if save_q=='y':plt.savefig(f'{ticker}.pdf')
plt.show()
