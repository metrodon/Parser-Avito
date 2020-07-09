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
    Floor = soup.find('div', class_='item-params').find(text='Этаж: ').parent.next_sibling
    Floor = Floor.strip()
    Floor = int(Floor)

  except:
    Floor = '0'
    print(Floor)


  try:
    FloorCount = soup.find('div', class_='item-params').find(text='Этажей в доме: ').parent.next_sibling
    FloorCount = FloorCount.strip()
    FloorCount = int(FloorCount)

  except:
    FloorCount = 0
    print(FloorCount)

  try:
    WallMaterial = soup.find('div', class_='item-params').find(text='Тип дома: ').parent.next_sibling
    WallMaterial = WallMaterial.strip()

  except:
    WallMaterial = 'Кирпичный'
    print(WallMaterial)

  try:
    NumberOfRooms = soup.find('div', class_='item-params').find(text='Количество комнат: ').parent.next_sibling
    NumberOfRooms = NumberOfRooms.strip('-комнатные ')
    NumberOfRooms = int(NumberOfRooms)

  except:
    NumberOfRooms = 0
    print(NumberOfRooms)

  try:
    FlatArea = soup.find('div', class_='item-params').find(text='Общая площадь: ').parent.next_sibling
    FlatArea = FlatArea.strip(' м² ').strip()
    FlatArea = float(FlatArea)

  except:
    FlatArea = 0
    print(FlatArea)

  try:
    KitchenArea = soup.find('div', class_='item-params').find(text='Площадь кухни: ').parent.next_sibling
    KitchenArea = KitchenArea.strip(' м² ').strip()
    KitchenArea = float(KitchenArea)

  except:
    KitchenArea = 0
    print(KitchenArea)

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



  FlatID = soup.find('div', class_='item-view-search-info-redesign').find('span').text
  FlatID = FlatID.lstrip('№ ').lstrip()
  FlatID = int(FlatID)



  Phone = ''

  print('Цена',Prise)
  print('Имя',FullName)
  print('Этаж',Floor)
  print('Этажей в доме',FloorCount)
  print('Матерьял стен',WallMaterial)
  print('Количество комнат',NumberOfRooms)
  print('Площадь квартиры',FlatArea)
  print('Площадь кухни',KitchenArea)
  print('Адрес',Address)
  print('Описание объекта',Description)
  print('ID Объявления',FlatID)

  cursor.execute(""" INSERT INTO dbo.Object (ID, Address, Category, Description, Price, Phone, FullName, FloorCount, WallMaterial, Source, URL) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
    # 1827220663,'Костромская область, Кострома, ул. Шагова, 150Б','Квартира','Продаеться 3х кв. ул/пл. ул. Шагова 150б, 5п9, комнаты на разные стороны, трубы ПВХ, счетчики. Развитая инфраструктура, школы 15 гимназия, садик , магазины, остановки. С/узел разделен, батареи во всей квартире заменены. Прямая продажа. Остаеться кухонный гарнитур, встроенный шкаф, прихожая, межкомнатных двери новые ',2850000,' ','Ольга',2,'панельный','Авито','https://www.avito.ru/kostroma/kvartiry/3-k_kvartira_67_m_59_et._1827220662')
  FlatID, Address, 'Квартира', Description, Prise, Phone, FullName, FloorCount, WallMaterial, 'Авито', url)
  print('object inserted')


  cursor.execute("""
  INSERT INTO dbo.Flat (FlatID, FlatArea, Floor, NumberOfRooms, KitchenArea) VALUES (?,?,?,?,?)""",
  FlatID, FlatArea, Floor, NumberOfRooms, KitchenArea)


  print('flat inserted')


  cursor.execute(
    """
    DELETE FROM dbo.URLS WHERE url = ?
    """,
    url
  )
  cnxn.commit()
  print('url deleted')

def runFlatParse():
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'apartment' ")

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
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'apartment'")

  currentUrls = cursor.fetchall()
  currentUrls = [row[0] for row in currentUrls]
  random.shuffle(currentUrls)
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