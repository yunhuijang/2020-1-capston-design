import pickle
import pandas as pd


out = ['Punctuation', 'Determiner', 'Suffix', 'Modifier', 'Josa', 'Eomi']


def exclude(stem):  # stem: 기사 하나의 stem
    i = 0
    while i <= len(stem) - 1:
        if stem[i][1] in out:
            del stem[i]
        else:
            i += 1


if __name__ == "__main__":
    with open('corona.pkl', 'rb') as f:
        p_data = pickle.load(f)
    df = pd.DataFrame(p_data)

    for index, row in df.iterrows():
        exclude(row['STEM'])

    df.to_pickle('corona_ex.pkl')

    with open('wuhan.pkl', 'rb') as f:
        p_data = pickle.load(f)
    df = pd.DataFrame(p_data)

    for index, row in df.iterrows():
        exclude(row['STEM'])

    df.to_pickle('wuhan_ex.pkl')

