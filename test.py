import pandas as pd

df=pd.read_csv('/home/thakur/test/combined/all_nasdaq.csv')

print(df)


l=['WIX', 'WLYB', 'KBH', 'TOL', 'MTH', 'ARRY', 'KEP', 'AHCO', 'PHM', 'PRK', 'KNBE']

print(l)

df_final=df[df['TICKER'].isin(l)]
print("df_final",df_final)
