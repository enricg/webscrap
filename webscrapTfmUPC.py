from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#direcció inicial = 'https://upcommons.upc.edu/handle/2099.1/4237/discover?rpp=10&etal=0&group_by=none&page=2&filtertype_0=type&filter_relational_operator_0=equals&filter_0=Master+thesis'
#direcció inicial  = 'https://upcommons.upc.edu/handle/2099.1/20411/recent-submissions'

baseurl = 'https://upcommons.upc.edu/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }

productlinks = []
#for x in range(1,1155):
for x in range(0,7):
   r = requests.get(f'https://upcommons.upc.edu/handle/2099.1/20411/recent-submissions?offset={x*12}')
   #r = requests.get(f'https://upcommons.upc.edu/handle/2099.1/4237/discover?rpp=10&etal=0&group_by=none&page={x}&filtertype_0=type&filter_relational_operator_0=equals&filter_0=Master+thesis')
   soup = BeautifulSoup(r.content, 'lxml')
   productlist = soup.find_all('li', class_='ds-artifact-item')
   #productlist = soup.find_all('div', class_='ds-artifact-item')

   for item in productlist:
       if 'src' in item.img.attrs:
           productlinks.append(baseurl + item.a['href'])

projectesllista = []
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    titol= soup.find('h2', class_='page-header').text.strip()
    autor= soup.find('div', class_='simple-item-view-authors item-page-field-wrapper table').text.strip()
    tutor= soup.find('div', class_='simple-item-view-description item-page-field-wrapper table').a
    if tutor is not None:
        tutor= tutor.text
    tipus= soup.find('div', class_='simple-item-view-description item-page-field-wrapper table').next_sibling.next_sibling.contents[2]
    any_entregat= soup.find('div', class_='simple-item-view-date word-break item-page-field-wrapper table').contents[2]
    descripcio= soup.find('div', class_='expandable')
    if descripcio is not None:
        descripcio= descripcio.text
    nom_arxiu= soup.find('div', class_='arxius_item').a
    if nom_arxiu is not None:
        nom_arxiu= nom_arxiu.text
    arxiu= soup.find('div', class_='arxius_item').a.get('href')
    coleccio= soup.find('div', class_='simple-item-view-collections item-page-field-wrapper table').a
    if coleccio is not None:
        coleccio= coleccio.text

    projecte = {
            'titol': titol,
            'autor': autor,
            'tutor': tutor,
            'tipus': tipus,
            'any_entregat': any_entregat,
            'descripcio': descripcio,
            'nom_arxiu': nom_arxiu,
            'arxiu': arxiu,
            'coleccio': coleccio
    }

    projectesllista.append(projecte)
    urlretrieve(baseurl+projecte['arxiu'], projecte['nom_arxiu']+".pdf")
    print('Guardant: ', projecte['titol'])
    time.sleep(15)

df = pd.DataFrame(projectesllista)
#print(df.head(10))
df.to_csv('llistaProjectes.csv')



#print(titol, autor, tutor, tipus, any_entregat, descripcio, descripcio, arxiu, coleccio)
#print(nom_arxiu)
