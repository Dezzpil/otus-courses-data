import time
import sqlite3
import requests
import traceback
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from grabber import grab_data

if __name__ == '__main__':
    con = sqlite3.connect("otus.db")
    cur = con.cursor()

    existed = set()
    for row in cur.execute('select * from courses'):
        existed.add(row[0])
    print(f'already grabbed: {existed}')

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }

    # открыть urls.txt и для каждой строчки делаем GET запрос
    # тело ответа грабим, все ошибки сохраняем в errors/*
    with open('eda/2025-02-27/urls.txt', 'r') as f:
        for line in f:
            url = line.strip()
            slug = url.split('/')[-1]
            if slug in existed:
                print(f'{slug}: already grabbed! skipping...')
                continue

            print(f'{slug}: requesting')
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f'{slug}: response status code {response.status_code}')
            else:
                item = None
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    item = grab_data(soup)
                except (AttributeError,ValueError,IndexError) as e:
                    error_string = traceback.format_exc()
                    # сохранить ошибку в errors/{slug}.txt и html в errors/{slug}.html
                    with open(f'errors/{slug}.txt', 'w') as ef:
                        ef.write(error_string)
                    with open(f'errors/{slug}.html', 'w') as ehf:
                        ehf.write(response.text)
                    print(f'{slug}: error while parsing')

                if item is not None:
                    # сохранить в sql
                    cur.execute('insert into courses values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [slug] + list(item.values()))
                    con.commit()
                    print(f'{slug}: saved to DB')

            print(f'{slug}: sleeping...')
            time.sleep(5)