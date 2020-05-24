import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

"""
def return_date(str):  # str 형식: 20200110
    d = datetime.strptime(str, '%Y%m%d').date()
    # print(d.month, "/", d.day, sep='')
    return d
"""

ax = plt.gca()
df = pd.read_csv('senti_index_20200110_20200514.csv', index_col=0)
# df.to_pickle('senti_index_20200110_20200514.pkl')  # 못 만든 pkl 파일 생성함
df = df.astype({'Date': str})
df['Date'] = pd.to_datetime(df['Date'])


#df.plot(kind='line', x='Date', y='polarity', color='DarkBlue', ax=ax, figsize=(10, 7))

#df.plot(kind='line', x='Date', y='subjectivity', color='DarkBlue', ax=ax, figsize=(10, 7))

df.plot(kind='line', x='Date', y='pos_refs_per_ref', color='SkyBlue', ax=ax, figsize=(10, 7))
df.plot(kind='line', x='Date', y='neg_refs_per_ref', color='Red', ax=ax, figsize=(10, 7))
df.plot(kind='line', x='Date', y='senti_diffs_per_ref', color='Green', ax=ax, figsize=(10, 7))

#plt.title('Polarity', fontdict={'fontsize': 18})
#plt.title('Subjectivity', fontdict={'fontsize': 18})
plt.title('Positive & Negative Indicators', fontdict={'fontsize': 18})
plt.show()

