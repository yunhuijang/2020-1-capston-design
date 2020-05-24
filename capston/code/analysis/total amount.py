from pickle import dump, load
import pandas as pd
from matplotlib import pyplot as plt

#total amount of information

with open('senti_wordcount_top30.pkl', 'rb') as f:
    senti_data = load(f)

with open('wordcount_top30.pkl', 'rb') as fi:
    word_data = load(fi)

total_amount = pd.DataFrame(columns= ('period', 'amount'))

period_array = []
amount_array = []

for j in range(len(word_data)):
    n = 0
    period_array.append(word_data.iloc[j][0])
    for k in range(30):
        n += word_data.iloc[j][1][k][1]
    amount_array.append(n)

total_amount['period'] = period_array
total_amount = total_amount.set_index('period')
total_amount['amount'] = amount_array
print(total_amount)
total_amount.plot()
plt.title('Amount of keyword informantion about COVID-19')
plt.ylabel('# of keywords')
plt.show()

