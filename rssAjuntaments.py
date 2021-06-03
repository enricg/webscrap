from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

baseurl = 'https://tauler.seu.cat/rss.do?idens='
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

fichero = open('llista_ajuntaments.txt', 'w')
#for x in range(1,8102130009):
for x in range(1,9999999999):
    #r = requests.get(f'https://tauler.seu.cat/rss.do?idens={x}')
   r = requests.get(f'https://tauler.seu.cat/rss.do?idens={x}')
   soup = BeautifulSoup(r.content, 'lxml')
   existeix = soup.find_all('item')


   if len(existeix) > 0:
       print('si:' + str(x))
       fichero.write(baseurl+str(x)+'\n')
   else:
       print('NO: ' + str(x))

fichero.close()
