import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import time, random
import os
import pandas as pd
from datetime import datetime, timedelta


def master(query, s_date, e_date):
    date_list = pd.date_range(start = s_date, end = e_date)
    
    for date in date_list:
        print ('Crawling date : {}'.format(date))
        date_str = date.strftime('%Y%m%d')
        crawler(query, date_str)
        print ('Crawling date : {} DONE'.format(date))

def crawler(query, date, max_news = 4000):
    if query == '우한 폐렴':
        max_news = 4000
    
    date = str(date)
    date_formatted = date[:4] + '.' + date[4:6] + '.' + date[6:]
    page = 1

    save_path = os.path.join(os.getcwd(), query)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    while page < max_news:
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=1&ds=" + date_formatted + "&de=" + date_formatted + "&nso=so%3Ar%2Cp%3Afrom" + date_formatted.replace('.', '') + "to" + date_formatted.replace('.', '') + "%2Ca%3A&start=" + str(page)

        #header 추가
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }
        req = requests.get(url,headers=header)
        print(page, url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        
        #max_news_from_web = (int(soup.find('div', class_ = 'title_desc all_my').text.split('/')[0].strip('').split('-')[-1]))
        #if page > max_news_from_web:
        #    break

        # 저장 경로를 입력합니다.
        data_f = open(os.path.join(save_path, 'data_final.txt'), 'a', encoding = 'utf-8')
        error_f = open(os.path.join(save_path, 'error_final.txt'), 'a')
        for dl_soup in soup.select('div > div > div > ul > li > dl'):
            try :
                title = dl_soup.select('dt > a')[0]['title'].replace('\t', ' ')
                source = dl_soup.find('dd').find('span').find(text = True, recursive = False).replace('\t', ' ')
                date = (dl_soup.select('dd > span')[1].next_sibling.strip().replace('.', ''))
                if date.endswith('전'):
                    date = date.replace('전', '').strip()
                    if date.endswith('시간'):
                        date = date.replace('시간', '').strip()
                        date = datetime.now() - timedelta(hours = int(date)) - timedelta(days = 1)
                        date = date.strftime('%Y%m%d')
                    elif date.endswith('일'):
                        date = date.replace('일', '').strip()
                        date = datetime.now() - timedelta(days = int(date)) - timedelta(days = 1)
                        date = date.strftime('%Y%m%d')
                    elif date.endswith('분'):
                        date = date.replace('분', '').strip()
                        date = datetime.now() - timedelta(minutes = int(date)) - timedelta(days = 1)
                        date = date.strftime('%Y%m%d')
                    elif date.endswith('초'):
                        date = date.replace('초', '').strip()
                        date = datetime.now() - timedelta(seconds = int(date)) - timedelta(days = 1)
                        date = date.strftime('%Y%m%d')
                    else:
                        raise ValueError('not valid unit')
                        
                msg = title + '\t' + source + '\t' + date + '\n'
                data_f.write(msg)
    #             print (msg)
            except Exception as e:
                msg = str(e) + '\t' + url
                error_f.write(msg)
    #             print (msg)
                continue
        page += 10  
        data_f.close()
        error_f.close()
        
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print ('Insufficient arguments')
        sys.exit()
        
    query = sys.argv[1].strip().replace("'", '')
    if query not in ['코로나', '우한 폐렴']:
        print ('not valid query: {}'.format(query))
        sys.exit()
    s_date = sys.argv[2].strip()
    e_date = sys.argv[3].strip()
    
    print ('searching {} from {} to {}'.format(query, s_date, e_date))
    master(query, s_date, e_date)
