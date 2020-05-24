import pandas as pd

df1 = pd.read_pickle('corona_ex.pkl')
df2 = pd.read_pickle('wuhan_ex.pkl')
df = df1.append(df2, ignore_index=True)
df = df.sort_values(by=['DATE'])
df = df.reset_index(drop=True)

df.to_pickle('total_ex.pkl')
df.to_csv('total_ex.csv')
