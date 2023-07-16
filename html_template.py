#!/bin/python3
#save to html
from datetime import datetime


txt_folder="/home/thakur/test/TXT/{}.txt"
html_folder="/home/thakur/test/HTML/{}.html"
fmt_yahoo="https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch"
fmt_nasdaq="https://www.nasdaq.com/market-activity/stocks/{}"
fmt_finviz="https://finviz.com/quote.ashx?t={}"

root="/home/thakur/stock_information/"
save_dir="/home/thakur/test/combined/"
source_dir="/home/thakur/test/"

#html string
html_string = '''
<html>
  <head><title>Stock Analysis</title></head>
  <h1>{TEST}</h1>
  <h4>{DATE}</h4>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''

to=datetime.now().strftime('%b-%d-%Y')

def save_txt_html(df,save,title,rows=100):
    print("Creating html and txt files\n")
    df=df.head(rows)
    df.loc[:,'Y-LINK']=df['TICKER'].apply(lambda x: fmt_yahoo.format(x,x))
    df.loc[:,'Y-LINK']=df['TICKER'].apply(lambda x: fmt_yahoo.format(x,x))
    df.loc[:,'N-LINK']=df['TICKER'].apply(lambda x: fmt_nasdaq.format(x))
    #df['F-LINK']=df['TICKER'].apply(lambda x: fmt_finviz.format(x))
    #df['N-LINK']=df['TICKER'].apply(lambda x: fmt_nasdaq.format(x))
    #df['F-LINK']=df['TICKER'].apply(lambda x: fmt_finviz.format(x))
    df.to_csv(txt_folder.format(save),sep='\t',index=True)
    with open(html_folder.format(save), 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='mystyle',justify='center',render_links=True),TEST=title,DATE=to))

