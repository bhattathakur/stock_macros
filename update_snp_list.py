#!/bin/python3
import pandas as pd

#link for snp500 list
wiki_snp_link='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

web_table=pd.read_html(wiki_snp_link)
snp_new=web_table[0] #desired table
snp_new.replace('BF.B','BF-B',inplace=True)
snp_new.replace('BRK.B','BRK-B',inplace=True)

#snp_new.head()

withvol='/home/thakur/stock_information/snp500finalwvol.csv' #red the old data
snp_old=pd.read_csv(withvol)
#snp_old.head()

#figuring out which of the previous stocks are in the new list
old_set=set(snp_old['SYMBOL'].to_list())


#figuring out which of the previous stocks are in the new list
new_set=set(snp_new['Symbol'].to_list())


newly_added=list(new_set-old_set)
#newly_added

removed=list(old_set-new_set)
#removed

# removed=removed[2:]
# removed

#removing from the old data frame
old_updated=snp_old[~snp_old.SYMBOL.isin(removed)]
#old_updated

to_be_added=snp_new[snp_new.Symbol.isin(newly_added)]
#exit
#Need to include the volume for newly added !
volume=[412.94,367.7,608.91,846.66,431.56,2080]
to_be_added.loc[:,'Volume']=volume

#to_be_added

to_be_added=to_be_added[['Symbol','Security','GICS Sector','GICS Sub-Industry','Volume']]
to_be_added.columns=old_updated.columns
#to_be_added

df_final=old_updated.append(to_be_added,ignore_index=True)
df_final=df_final.sort_values(by=['SYMBOL'])
#df_final

df_final.to_csv("/home/thakur/stock_information/snp500finalwvol.csv",index=False)
