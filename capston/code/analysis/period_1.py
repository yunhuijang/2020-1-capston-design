from pickle import dump, load
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#keywords based on periods

with open('senti_wordcount_top30.pkl', 'rb') as f:
    senti_data = load(f)

with open('wordcount_top30.pkl', 'rb') as fi:
    word_data = load(fi)

senti_dict_array = []
senti_dict_p1 = {}
senti_dict_p2 = {}
senti_dict_p3 = {}
senti_dict_p4 = {}
senti_dict_p5 = {}

word_dict_array = []
word_dict_p1 = {}
word_dict_p2 = {}
word_dict_p3 = {}
word_dict_p4 = {}
word_dict_p5 = {}


for i in range(3):
    for j in range(30):
        senti_dict_p1[senti_data.iloc[i][1][j][0][0]] = senti_data.iloc[i][1][j][1]
        word_dict_p1[word_data.iloc[i][1][j][0][0]] = word_data.iloc[i][1][j][1]

for i in range(3, 5):
    for j in range(30):
        senti_dict_p2[senti_data.iloc[i][1][j][0][0]] = senti_data.iloc[i][1][j][1]
        word_dict_p2[word_data.iloc[i][1][j][0][0]] = word_data.iloc[i][1][j][1]

for i in range(5, 7):
    for j in range(30):
        senti_dict_p3[senti_data.iloc[i][1][j][0][0]] = senti_data.iloc[i][1][j][1]
        word_dict_p3[word_data.iloc[i][1][j][0][0]] = word_data.iloc[i][1][j][1]

for i in range(7, 16):
    for j in range(30):
        senti_dict_p4[senti_data.iloc[i][1][j][0][0]] = senti_data.iloc[i][1][j][1]
        word_dict_p4[word_data.iloc[i][1][j][0][0]] = word_data.iloc[i][1][j][1]

for i in range(16, 18):
    for j in range(30):
        senti_dict_p5[senti_data.iloc[i][1][j][0][0]] = senti_data.iloc[i][1][j][1]
        word_dict_p5[word_data.iloc[i][1][j][0][0]] = word_data.iloc[i][1][j][1]

senti_dict_array.append(senti_dict_p1)
senti_dict_array.append(senti_dict_p2)
senti_dict_array.append(senti_dict_p3)
senti_dict_array.append(senti_dict_p4)
senti_dict_array.append(senti_dict_p5)

word_dict_array.append(word_dict_p1)
word_dict_array.append(word_dict_p2)
word_dict_array.append(word_dict_p3)
word_dict_array.append(word_dict_p4)
word_dict_array.append(word_dict_p5)

for i in range(5):
    print(i)
    print('sentiments')
    print(pd.DataFrame(sorted(senti_dict_array[i].items(), key=(lambda x:x[1]), reverse=True)))
    wc_senti = WordCloud(font_path='HANYGO230.ttf', background_color="white", width=1000, height=1000, max_words=20,
                   relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(senti_dict_array[i])
    plt.imshow(wc_senti)
    plt.savefig('senti_%d_wc.png' % i)

    print('keywords')
    print(pd.DataFrame(sorted(word_dict_array[i].items(), key=(lambda x:x[1]), reverse = True)))
    wc_key = WordCloud(font_path='HANYGO230.ttf', background_color="white", width=1000, height=1000, max_words=20,
                   relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(word_dict_array[i])
    plt.imshow(wc_key)
    plt.savefig('word_%d_wc.png'%i)
    print(" ")


