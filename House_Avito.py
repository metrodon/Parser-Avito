# -*- coding: utf-8 -*-
import requests
import re
import sys
import pyodbc
import time
import random

from bs4 import BeautifulSoup

def get_html(url):
  r = requests.get(url)
  return r.text

def get_data(html, url, cursor, cnxn):
  soup = BeautifulSoup(html, 'lxml')

  try:
    Price = soup.find('div', itemprop='offers').find('span', class_='js-item-price').text
    Prise = Price.split()
    Prise = ''.join(Prise)
    Prise = int(Prise)

  except:
    Prise = 0
    print(Prise)

  try:
    FullName = soup.find('span', 'sticky-header-seller-text').text

  except:
    FullName = ''
    print(FullName)

  try:
    DistanceToTheCity = soup.find('div', class_='item-params').find(text='Расстояние до города: ').parent.next_sibling
    DistanceToTheCity = DistanceToTheCity.strip(' км ').strip()
    DistanceToTheCity = float(DistanceToTheCity)

  except:
    DistanceToTheCity = 0
    print(DistanceToTheCity)


  try:
    FloorCount = soup.find('div', class_='item-params').find(text='Этажей в доме: ').parent.next_sibling
    FloorCount = FloorCount.strip()
    FloorCount = int(FloorCount)

  except:
    FloorCount = 0
    print(FloorCount)

  try:
    WallMaterial = soup.find('div', class_='item-params').find(text='Материал стен: ').parent.next_sibling
    WallMaterial = WallMaterial.strip()

  except:
    WallMaterial = 'Бревно'
    print(WallMaterial)

  try:
    HouseArea = soup.find('div', class_='item-params').find(text='Площадь дома: ').parent.next_sibling
    HouseArea = HouseArea.strip(' м² ').strip()
    HouseArea = float(HouseArea)

  except:
    HouseArea = 0
    print(HouseArea)


  try:
    LandArea = soup.find('div', class_='item-params').find(text='Площадь участка: ').parent.next_sibling
    LandArea = LandArea.strip(' сот. ').strip()
    LandArea = float(LandArea)

  except:
    LandArea = 0
    print(LandArea)

  try:
    Address = soup.find('span', class_='item-address__string').text
    Address = Address.lstrip().rstrip()

  except:
    Address = ''
    print(Address)

  try:
    Description = soup.find('div', class_='item-description').find('div', itemprop='description').text
    Description = Description.lstrip()

  except:
    Description = ''
    print(Description)

  HouseID = soup.find('div', class_='item-view-search-info-redesign').find('span').text
  HouseID = HouseID.lstrip('№ ').lstrip()
  HouseID = int(HouseID)



  Phone = ''

  print(Prise)
  print(FullName)
  print(DistanceToTheCity)
  print(FloorCount)
  print(WallMaterial)
  print(HouseArea)
  print(LandArea)
  print(Address)
  print(Description)
  print(HouseID)
  print(Phone)

  cursor.execute(""" INSERT INTO dbo.Object (ID, Address, Category, Description, Price, Phone, FullName, FloorCount, WallMaterial, Source, URL) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
  HouseID, Address, 'Дом', Description, Prise, Phone, FullName, FloorCount, WallMaterial, 'Авито', url)
  print('object inserted')

# 10 - Сущностей 9 Спарсено  + 1 Телефон не спарсен
  cursor.execute("""
  INSERT INTO dbo.House (HouseID, HouseArea, LandArea, DistanceToTheCity) VALUES (?,?,?,?)""",
  HouseID, HouseArea, LandArea, DistanceToTheCity)


  print('house inserted')


  cursor.execute(
    """
    DELETE FROM dbo.URLS WHERE url = ?
    """,
    url
  )
  cnxn.commit()
  print('url deleted')

def runHouseParse():
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'house' ")

  currentUrls = cursor.fetchall()
  currentUrls = [row[0] for row in currentUrls]
  random.shuffle(currentUrls)
  for url in currentUrls:
    html = get_html(url)
    get_data(html, url, cursor, cnxn)
    randTime = random.randint(6, 13)
    time.sleep(randTime)

def main():
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'house' ")

  currentUrls = cursor.fetchall()
  currentUrls = [row[0] for row in currentUrls]
  random.shuffle(currentUrls)
  print(currentUrls)
  sys.exit()
  for url in currentUrls:
    print(url)
    html = get_html(url)
    get_data(html, url, cursor, cnxn)
    randTime = random.randint(15, 30)
    # time.sleep(randTime)
    sys.exit()


if __name__ == '__main__':
  main()