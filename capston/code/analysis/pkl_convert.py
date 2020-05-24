import pickle
import pandas as pd
import json
import collections
from datetime import timedelta, date

column_names = ['Period', 'Top30']
top_words = pd.DataFrame(columns=column_names)


def convert_wordcount(filename):  # 상위 30개, filename 형식: ~20200110_20200116.pkl
    df = pd.read_pickle(filename)
    if len(df.index) < 30:
        print("rows less than 30")
    df_top = df.loc[0:29]

    word_list = []
    for index, row in df_top.iterrows():
        word_info = [row['Word'], row['Count']]
        word_list.append(word_info)

    period = filename[-21:-4]
    period = period.replace('_', '-')

    global top_words
    top_words = top_words.append({'Period': period, 'Top30': word_list}, ignore_index=True)


if __name__ == "__main__":

    convert_wordcount('wordcount_20200110_20200116.pkl')
    convert_wordcount('wordcount_20200117_20200123.pkl')
    convert_wordcount('wordcount_20200124_20200130.pkl')
    convert_wordcount('wordcount_20200131_20200206.pkl')
    convert_wordcount('wordcount_20200207_20200213.pkl')
    convert_wordcount('wordcount_20200214_20200220.pkl')
    convert_wordcount('wordcount_20200221_20200227.pkl')
    convert_wordcount('wordcount_20200228_20200305.pkl')
    convert_wordcount('wordcount_20200306_20200312.pkl')
    convert_wordcount('wordcount_20200313_20200319.pkl')
    convert_wordcount('wordcount_20200320_20200326.pkl')
    convert_wordcount('wordcount_20200327_20200402.pkl')
    convert_wordcount('wordcount_20200403_20200409.pkl')
    convert_wordcount('wordcount_20200410_20200416.pkl')
    convert_wordcount('wordcount_20200417_20200423.pkl')
    convert_wordcount('wordcount_20200424_20200430.pkl')
    convert_wordcount('wordcount_20200501_20200507.pkl')
    convert_wordcount('wordcount_20200508_20200514.pkl')

    print(top_words)

    top_words.to_pickle('wordcount_top30.pkl')
    top_words.to_csv('wordcount_top30.csv')


    """
    convert_wordcount('senti_wordcount_20200110_20200116.pkl')
    convert_wordcount('senti_wordcount_20200117_20200123.pkl')
    convert_wordcount('senti_wordcount_20200124_20200130.pkl')
    convert_wordcount('senti_wordcount_20200131_20200206.pkl')
    convert_wordcount('senti_wordcount_20200207_20200213.pkl')
    convert_wordcount('senti_wordcount_20200214_20200220.pkl')
    convert_wordcount('senti_wordcount_20200221_20200227.pkl')
    convert_wordcount('senti_wordcount_20200228_20200305.pkl')
    convert_wordcount('senti_wordcount_20200306_20200312.pkl')
    convert_wordcount('senti_wordcount_20200313_20200319.pkl')
    convert_wordcount('senti_wordcount_20200320_20200326.pkl')
    convert_wordcount('senti_wordcount_20200327_20200402.pkl')
    convert_wordcount('senti_wordcount_20200403_20200409.pkl')
    convert_wordcount('senti_wordcount_20200410_20200416.pkl')
    convert_wordcount('senti_wordcount_20200417_20200423.pkl')
    convert_wordcount('senti_wordcount_20200424_20200430.pkl')
    convert_wordcount('senti_wordcount_20200501_20200507.pkl')
    convert_wordcount('senti_wordcount_20200508_20200514.pkl')

    print(top_words)

    top_words.to_pickle('senti_wordcount_top30.pkl')
    top_words.to_csv('senti_wordcount_top30.csv')
    """

