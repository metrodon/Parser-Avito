import requests
import pyodbc
import Room_Avito

from bs4 import BeautifulSoup
from pprint import pprint
links = []

def get_html(url):
  r = requests.get(url)
  return r.text


def get_page_data(html):
  soup = BeautifulSoup(html, 'lxml')

  ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item__line')
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()

  cursor.execute("SELECT URL FROM dbo.Object")
  objectUrls = cursor.fetchall()
  objectUrls = [row[0] for row in objectUrls]

  cursor.execute("SELECT url FROM dbo.URLS")
  persistentUrls = cursor.fetchall()
  persistentUrls = [row[0] for row in persistentUrls]

  persistentUrls = objectUrls + persistentUrls

  for ad in ads:

    try:
      title = ad.find('div', class_='item_table-wrapper').find('a', class_='snippet-link').get('title')
      print(title)
    except:
      title = ''
      print(title)
    try:
      url = 'https://www.avito.ru' + ad.find('div', class_='item_table-wrapper').find('a', class_='snippet-link').get('href')
      print(url + '\n')
      linkSet = []



      if (url not in persistentUrls):
        linkSet.append(url)
        linkSet.append('https://www.avito.ru')
        linkSet.append('room')
        links.append(linkSet)

    except:
      url = ''
      print(url + '\n')

def goForObject(url):
  html = get_html(url)



def insertLinks():
  avitolink = 'https://www.avito.ru'
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()
  for link in links:
    cursor.execute("""  INSERT INTO dbo.URLS VALUES (?, ?, ?) """, link)
    cursor.commit()

def getFreshUrls():
  url = 'https://www.avito.ru/kostroma/komnaty/prodam-ASgBAgICAUSQA7wQ?cd=1'
  html = get_html(url)
  get_page_data(html)
  insertLinks()

