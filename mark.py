#!/bin/python3
import pandas as pd
import yfinance as yf
import pandas_ta as ta
from datetime import datetime
import math
import subprocess
import os

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
    previous_price=(100*cp)/(100+pct_change)
    return round(cp-previous_price,2)

#saves to txt and html
txt_folder="./TXT/{}.txt"
html_folder="./HTML/{}.html"
fmt_yahoo="https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
fmt_nasdaq="https://www.nasdaq.com/market-activity/stocks/{}"
fmt_finviz="https://finviz.com/quote.ashx?t={}"

root="/home/thakur/stock_information/"
save_dir="/home/thakur/test/combined/"
source_dir="/home/thakur/test/"

#html string
html_string = '''
<html>
  <head><title>Mark Stock Analysis</title></head>
  <h1>{TEST}</h1>
  <h4>{DATE}</h4>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''
#with open('myhtml.html', 'w') as f:
#    f.write(html_string.format(table=demo_df.to_html(classes='mystyle')))
#
to=datetime.now().strftime('%b-%d-%Y')

def save_txt_html(df,save,title,rows=100):
    df=df.head(rows)
    df['Y-LINK']=df['TICK'].apply(lambda x: fmt_yahoo.format(x,x))
    df['N-LINK']=df['TICK'].apply(lambda x: fmt_nasdaq.format(x))
    df['F-LINK']=df['TICK'].apply(lambda x: fmt_finviz.format(x))
    df.to_csv(txt_folder.format(save),sep='\t',index=True)
    with open(html_folder.format(save), 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='mystyle',justify='center',render_links=True),TEST=title,DATE=to))


ft=20*"="
now=datetime.now()
d=now.strftime("%m/%d/%Y")

print(f"{ft} DATE:{d} {ft}")
#ask=input(f"Do you want to run mark.py to get data on {d}?: y/n: ")
#if(ask!='y'):
#    print("quitting...")
#    quit()
#



df_rs=pd.read_csv('https://raw.githubusercontent.com/skyte/rs-log/main/output/rs_stocks.csv')
def get_rs_value(ticker):
    if ticker in list(df_rs['Ticker']):
        return (df_rs.loc[df_rs['Ticker']==ticker]['Percentile'].values[0])
    else:
        return 0


def data_combine(fil,csv_source,save_file):
    """creates the dataframe of stocks which meet mark's crietrion"""

    print(f"Working with {fil}:\n")
    df_temp=pd.read_csv(root+fil+".csv",keep_default_na=False)  #list of files  downloaded
    df_temp=df_temp[df_temp['Country']=='United States']
    st_list=list(df_temp['Symbol'])  #list of files  downloaded
    #st_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['Symbol'])  #list of files  downloaded
    #df_rss=pd.read_csv(root+fil+".csv",keep_default_na=False)  #list of files  downloaded
    st_list=[i.strip() for i in st_list]
    name_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['Name'])  #company Name
    #country_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['Country'])  #country Name
    #ipo_list=list(pd.read_csv(root+fil+".csv",keep_default_na=False)['IPO Year'])     #IPO Year
    #print(f"st_list:\n{st_list}")


    #Reading the files
    ticker_list=[]           #store ticker
    name=[]                  #name
    current_price=[]         #current price
    rsi=[]                   #rsi list
    sma_50=[]                #sma_5 list
    sma_150=[]               #sma_50 list
    sma_200=[]                #sma_200 list
    week_low=[]             #52 week low
    week_high=[]            #52 week high
    rs_value=[]               #rs value
    sma_200past20=[]          #sma 200 past 20
    sector=[]                #sector
    industry=[]              #industry
    pt_change=[]            #pct change
    country_list=[]
    ipo_year=[]

    j=1
    for c,f in enumerate(st_list):    #read these files

        print(f"{j}/{len(st_list)} {fil} : {f}\n")
        j+=1
        #print("source dir\t",csv_source)
        df=pd.read_csv(csv_source+f+".csv",keep_default_na=True)
        #df.fillna(0,inplace=True)



        cp=df.tail(1)['Close'].values[0]                  #current-price
        #print(f"Current Price: {cp}\n")
        try:
            rs=df.ta.rsi()[-1:].round(2).values[0]            #rsi
        except:
            rs=0
        #rs=0 if math.isnan(rs_t) else rs_t
        #print(f"rsi: {rs}\n")
        sma50=round(df.tail(50)['Close'].mean(),2)        #sma-50
        #print(f"sma-50 {sma50}\n")
        sma150=round(df.tail(150)['Close'].mean(),2)      #sma-150
        #print(f"sma-150 {sma150}\n")
        sma200=round(df.tail(200)['Close'].mean(),2)      #sma-200
        #5day average volume > 100K
        vol5=round(df.tail(5)['Volume'].mean(),2)      #sma-200
        #print(f"sma-200 {sma200}\n")
        sma200past20=round(df['Close'][:-20].tail(200).mean(),2)      #sma-200 past 20
        #print(f"sma-200 past 20 {sma200past20}\n")
        week52_high=df['High'].max()                     #52-week high
        #print(f"52 week high: {week52_high}\n")
        #print("head of Low\n",df['Low'].head())
        week52_low=df['Low'].min(skipna=True)                       #52-week low

        pct=round((df.tail(2)['Close'].pct_change().values[1])*100,2)
        #print(f"%Change:\n {pct}")
        #pct=2
        #pt_change.append(pct)
        #print(f"52 week low: {week52_low}\n")

        rsval=get_rs_value(f)                            #rs value
        #print(f"rs_value of {f}: {rsval}\n")
        #company name
        cname=name_list[c].replace('Common Stock','').replace('Inc.','')
        #cname=cname.strip('Common Stock Inc.')

        #cname.replace('Common Stock','')
        #NOTE with 5 day avg volume < 100K ignored

        if cp>sma150 and cp>sma200 and vol5>100000:
            if(sma150>sma200):
                if(sma200>sma200past20):
                    if(sma50>sma150 and sma50>sma200):
                        if(cp>sma50):
                            if(cp>1.30*week52_low):
                                if(cp<1.25*week52_high):
                                    print(f"{f} meets the criterion!")
                                    print(20*"0000")
                                    ticker_list.append(f)
                                    name.append(cname)
                                    #company name
                                    #m=df.loc[df.Symbol==f]['Name'].values[0].strip('Common Stock Inc.')
                                    #name_list
                                    current_price.append(cp)
                                    rsi.append(rs)
                                    sma_50.append(sma50)
                                    sma_150.append(sma150)
                                    sma_200.append(sma200)
                                    sma_200past20.append(sma200past20)
                                    week_high.append(week52_high)
                                    week_low.append(week52_low)
                                    rs_value.append(rsval)
                                    pt_change.append(pct)
                                    if f in list(df_rs['Ticker']):sector.append(df_rs.loc[df_rs['Ticker']==f]['Sector'].values[0])
                                    else:sector.append('N/A')
                                    

                                    if f in list(df_rs['Ticker']):industry.append(df_rs.loc[df_rs['Ticker']==f]['Industry'].values[0])
                                    else:industry.append('N/A')
#                                    if f in list(df_rss['Symbol']):country_list.append(df_rss.loc[df_rss['Symbol']==f]['Country'].values[0])
#                                    else:country_list.append('N/A')
#                                    if f in list(df_rss['Symbol']):ipo_year.append(df_rss.loc[df_rss['Symbol']==f]['IPO Year'].values[0])
#                                    else:ipo_year.append('N/A')





        #create the pandas dataframe and save it
        mark_df=pd.DataFrame({
            "TICK":ticker_list,
            "CP":current_price,
            "CHG%":pt_change,
            "RSI":rsi,
            "SMA50":sma_50,
            "SMA150":sma_150,
            "SMA200":sma_200,
            "SMA200PAST20":sma_200past20,
            "52WKHIGH":week_high,
            "52WKLOW":week_low,
            "RS":rs_value,
            "SECTOR":sector,
            "INDUSTRY":industry,
            "NAME":name
#            "COUNTRY":country_list,
#            "IPO-YEAR":ipo_year
        })
    print(f"{fil} Data Frame:\n")

    mark_df.to_csv(save_file,index=False)
    print(mark_df)



input_files=["nasdaq_mega", "nasdaq_large","nasdaq_medium","nasdaq_small","nasdaq_micro","nasdaq_nano"]
directories=["mega/","large/","medium/","small/","micro/","nano/"]
today=datetime.today()
today=today.strftime("%m%d%y")
#today='091722'
print(f"Today: {today}\n")
#n=0
for n in range(6):
    #pass
    #if n!=5: continue
    data_combine(input_files[n],source_dir+directories[n],save_dir+"mark"+input_files[n]+today+".csv")

#save all in a textfile
text_file="/home/thakur/test/combined/mark-all"+today+".txt"
if os.path.exists(text_file):
    print(f"{text_file} exists!\nDeleting...")
    os.remove(text_file)

fmt_str="https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
fmt_nasdaq="https://www.nasdaq.com/market-activity/stocks/{}"
def clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)

#make clickable link for the column
def make_clickable(val):
    return '<a target ="_blank" href="{}">{}</a>'.format(val,"link")
    #target="_blank" opens the window to new window
    #can use val inplace to "link" to print the exact link

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'green'
    return 'color: %s' % color

#def fmt_str(x):return "https://finance.yahoo.com/quote/{x}?p={x}&.tsrc=fin-srch"
with open(text_file,'a')as ff:
    for n in range(6):
        #if n!=5: continue
        f="mark"+input_files[n]+".csv"
        print(100*'+');print(f"\nWORKING........... {f}\n");print(100*'+');
        ff.write(100*'+');ff.write(f"\nWORKING .............. {f}\n");ff.write(100*'+');ff.write("\n")
        df=pd.read_csv(save_dir+"mark"+input_files[n]+today+".csv",usecols=['TICK','CP','CHG%','RSI','RS','SECTOR','NAME'])
        df.sort_values(by="CP",inplace=True)
        l=df.shape[0] #size
        df.index=range(1,l+1)

        #df.style.format({'link':make_clickable})
        #df['link'] = df.apply(lambda x:clickable(x['link'], x['TICK']), axis=1)

        #if n!=0:head=False
        head=True
        ff.write(df.to_string(index=True,header=head));ff.write("\n")

        tit="MARK "+input_files[n].upper()
        save_txt_html(df,'mark_'+input_files[n],tit)#save in html and ascii

        #df['Y-LINK']=df['TICK'].apply(lambda x:fmt_str.format(x,x))
        #df['N-LINK']=df['TICK'].apply(lambda x:fmt_nasdaq.format(x))
        ##df['Link'] = df.apply(lambda x:clickable(x['Y-LINK'], x['TICK']), axis=1)
        ##df=df.style
        #html_name="/home/thakur/test/HTML/mark"+input_files[n]+".html"
        #df.to_html(html_name,render_links=True)

        #print(df)
print(f"File Created: {text_file}\nDONE!")
