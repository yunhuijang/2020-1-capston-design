import os
import sys

import numpy as np
import pandas as pd
df = pd.DataFrame

from tqdm import tqdm
from konlpy.tag import Twitter

tqdm.pandas()

query = '코로나'

def stemizer(query):
    
    print ('reading...', end = ' ')
    with open(os.path.join(os.getcwd(), query, 'test_data.txt'), 'r', encoding = 'utf-8') as f:
        data_txt = f.readlines()
    print ('Done')
    
    print ('preprocess...', end = ' ')
    data_m = [np.array(x.strip().split('\t')) for x in data_txt]
    print ('Done')
    
    print ('Make DataFrame...', end = ' ')
    data_df = df(data_m, columns = ['HEADLINE', 'SOURCE', 'DATE'])
    print ('Done')
    
    t = Twitter()
    print ('Start Stemming...', end = ' ')
    pos_ko = data_df.HEADLINE.progress_apply(lambda x: t.pos(x, stem = True))
    print ('Done')
    
    data_df['STEM'] = pos_ko
    
    save_path = os.path.join(os.getcwd(), 'processed')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        
    data_df.to_pickle(os.path.join(save_path, query + '.pkl'))
    
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ('Insufficient arguments')
        sys.exit()
        
    query = sys.argv[1].strip()
    print ('Stem {}'.format(query))
    stemizer(query)
