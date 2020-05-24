import pickle
import pandas as pd
import json
import collections
from datetime import timedelta, date, datetime


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def word_sentiment(dic, wordname):
    result = ['None', 'None']
    wordname = wordname.strip(" ")
    for i in range(0, len(dic)):
        if dic[i]['word'] == wordname:
            result.pop()
            result.pop()
            result.append(dic[i]['word_root'])
            result.append(dic[i]['polarity'])

    r_word = result[0]
    s_word = result[1]

    # print('어근 : ' + r_word)
    # print('극성 : ' + s_word)

    return s_word


def word_freq(df, s_year, s_month, s_day, e_year, e_month, e_day):  # 특정 기간 단어 빈도수 계산
    # 예외처리하기(start/end date), start/end date 같아도 가능
    date_list = []
    start_dt = date(s_year, s_month, s_day)
    end_dt = date(e_year, e_month, e_day)
    for dt in daterange(start_dt, end_dt):
        date_list.append(dt.strftime("%Y%m%d"))
    df_date = df[df['DATE'].isin(date_list)]

    container = collections.Counter()
    for index, row in df_date.iterrows():
        container.update(row['STEM'])

    word_df = pd.DataFrame.from_dict(container, orient='index').sort_values(by=0, ascending=False).reset_index()
    word_df = word_df.rename(columns={"index": "Word", 0: "Count"})
    word_df.to_pickle('wordcount_{}_{}.pkl'.format(date_list[0], date_list[-1]))

    print(date_list[0], date_list[-1], "done")


def senti_word_freq(df, dict, s_year, s_month, s_day, e_year, e_month, e_day):  # 특정 기간 감성어 빈도수 계산
    # 예외처리하기(start/end date), start/end date 같아도 가능
    date_list = []
    start_dt = date(s_year, s_month, s_day)
    end_dt = date(e_year, e_month, e_day)
    for dt in daterange(start_dt, end_dt):
        date_list.append(dt.strftime("%Y%m%d"))
    df_date = df[df['DATE'].isin(date_list)]

    container = collections.Counter()
    for index, row in df_date.iterrows():
        i = 0
        a = row['STEM']
        while i <= len(a) - 1:
            if (word_sentiment(dict, a[i][0]) == 'None') or (word_sentiment(dict, a[i][0]) == '0'):
                del a[i]
            else:
                # print(a[i][0], word_sentiment(dict, a[i][0]))
                i += 1
        container.update(row['STEM'])

    word_df = pd.DataFrame.from_dict(container, orient='index').sort_values(by=0, ascending=False).reset_index()
    word_df = word_df.rename(columns={"index": "Word", 0: "Count"})
    word_df.to_pickle('senti_wordcount_{}_{}.pkl'.format(date_list[0], date_list[-1]))

    print(date_list[0], date_list[-1], "done")


def senti_index(df, dict, s_year, s_month, s_day, e_year, e_month, e_day):
    column_names = ['Date', 'None', '+2', '+1', '0', '-1', '-2', 'polarity', 'subjectivity', 'pos_refs_per_ref',
                    'neg_refs_per_ref', 'senti_diffs_per_ref']
    senti_data = pd.DataFrame(columns=column_names)

    # 예외처리하기(start/end date), start/end date 같아도 가능
    date_list = []
    start_dt = date(s_year, s_month, s_day)
    end_dt = date(e_year, e_month, e_day)
    for dt in daterange(start_dt, end_dt):
        date_list.append(dt.strftime("%Y%m%d"))
    for day in date_list:
        sense_none = 0
        sense_p2 = 0
        sense_p1 = 0
        sense_0 = 0
        sense_n1 = 0
        sense_n2 = 0

        df_date = df.loc[df['DATE'] == day]
        for index, row in df_date.iterrows():
            for tup in row['STEM']:
                if word_sentiment(dict, tup[0]) == 'None':
                    sense_none += 1
                elif word_sentiment(dict, tup[0]) == '2':
                    sense_p2 += 1
                elif word_sentiment(dict, tup[0]) == '1':
                    sense_p1 += 1
                elif word_sentiment(dict, tup[0]) == '0':
                    sense_0 += 1
                elif word_sentiment(dict, tup[0]) == '-1':
                    sense_n1 += 1
                elif word_sentiment(dict, tup[0]) == '-2':
                    sense_n2 += 1
                else:
                    print("SentimentReturnError")

        total = sense_none + sense_p2 + sense_p1 + sense_0 + sense_n1 + sense_n2
        p = sense_p2 + sense_p1
        n = sense_n1 + sense_n2
        polarity = (p - n) / (p + n)
        subjectivity = (p + n) / total
        pos_refs_per_ref = p / total
        neg_refs_per_ref = n / total
        senti_diffs_per_ref = (p - n) / total

        senti_data = senti_data.append({'Date': day, 'None': sense_none, '+2': sense_p2, '+1': sense_p1, '0': sense_0, '-1': sense_n1, '-2': sense_n2, 'polarity': polarity, 'subjectivity': subjectivity, 'pos_refs_per_ref': pos_refs_per_ref, 'neg_refs_per_ref': neg_refs_per_ref, 'senti_diffs_per_ref': senti_diffs_per_ref}, ignore_index=True)

        """
        print([sense_none, sense_p2, sense_p1, sense_0, sense_n1, sense_n2])
        print("polarity: ", round(polarity, 2))
        print("subjectivity: ", round(subjectivity, 2))
        print("pos_refs_per_ref: ", round(pos_refs_per_ref, 2))
        print("neg_refs_per_ref: ", round(neg_refs_per_ref, 2))
        print("senti_diffs_per_ref: ", round(senti_diffs_per_ref, 2))
        """
        print(day, "done")

    senti_data.to_pickle('senti_index_{}_{}.pkl'.format(date_list[0], date_list[-1]))
    senti_data.to_csv('senti_index_{}_{}.csv'.format(date_list[0], date_list[-1]))








if __name__ == "__main__":
    with open('total_ex.pkl', 'rb') as f:
        p_data = pickle.load(f)
    data = pd.DataFrame(p_data)

    with open('data/SentiWord_info.json', encoding='utf-8-sig', mode='r') as f:
        KNU = json.load(f)

    """
    word_freq(data, 2020, 1, 10, 2020, 1, 16)
    word_freq(data, 2020, 1, 17, 2020, 1, 23)
    word_freq(data, 2020, 1, 24, 2020, 1, 30)
    word_freq(data, 2020, 1, 31, 2020, 2, 6)
    word_freq(data, 2020, 2, 7, 2020, 2, 13)
    word_freq(data, 2020, 2, 14, 2020, 2, 20)
    word_freq(data, 2020, 2, 21, 2020, 2, 27)
    word_freq(data, 2020, 2, 28, 2020, 3, 5)
    word_freq(data, 2020, 3, 6, 2020, 3, 12)
    word_freq(data, 2020, 3, 13, 2020, 3, 19)
    word_freq(data, 2020, 3, 20, 2020, 3, 26)
    word_freq(data, 2020, 3, 27, 2020, 4, 2)
    word_freq(data, 2020, 4, 3, 2020, 4, 9)
    word_freq(data, 2020, 4, 10, 2020, 4, 16)
    word_freq(data, 2020, 4, 17, 2020, 4, 23)
    word_freq(data, 2020, 4, 24, 2020, 4, 30)
    word_freq(data, 2020, 5, 1, 2020, 5, 7)
    word_freq(data, 2020, 5, 8, 2020, 5, 14)
    """

    """
    senti_word_freq(data, KNU, 2020, 1, 10, 2020, 1, 16)
    senti_word_freq(data, KNU, 2020, 1, 17, 2020, 1, 23)
    senti_word_freq(data, KNU, 2020, 1, 24, 2020, 1, 30)
    senti_word_freq(data, KNU, 2020, 1, 31, 2020, 2, 6)
    senti_word_freq(data, KNU, 2020, 2, 7, 2020, 2, 13)
    senti_word_freq(data, KNU, 2020, 2, 14, 2020, 2, 20)
    senti_word_freq(data, KNU, 2020, 2, 21, 2020, 2, 27)
    senti_word_freq(data, KNU, 2020, 2, 28, 2020, 3, 5)
    senti_word_freq(data, KNU, 2020, 3, 6, 2020, 3, 12)
    senti_word_freq(data, KNU, 2020, 3, 13, 2020, 3, 19)
    senti_word_freq(data, KNU, 2020, 3, 20, 2020, 3, 26)
    senti_word_freq(data, KNU, 2020, 3, 27, 2020, 4, 2)
    senti_word_freq(data, KNU, 2020, 4, 3, 2020, 4, 9)
    senti_word_freq(data, KNU, 2020, 4, 10, 2020, 4, 16)
    senti_word_freq(data, KNU, 2020, 4, 17, 2020, 4, 23)
    senti_word_freq(data, KNU, 2020, 4, 24, 2020, 4, 30)
    senti_word_freq(data, KNU, 2020, 5, 1, 2020, 5, 7)
    senti_word_freq(data, KNU, 2020, 5, 8, 2020, 5, 14)
    """

    senti_index(data, KNU, 2020, 1, 10, 2020, 5, 14)

