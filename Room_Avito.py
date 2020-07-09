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
    Prise = float(Prise)

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
    FloorCount = float(FloorCount)

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
    TotalRooms = soup.find('div', class_='item-params').find(text='Комнат в квартире: ').parent.next_sibling
    TotalRooms = TotalRooms.strip('-комнатные ')
    TotalRooms = int(TotalRooms)

  except:
    TotalRooms = 0
    print(TotalRooms)

  try:
    RoomArea = soup.find('div', class_='item-params').find(text='Площадь комнаты: ').parent.next_sibling
    RoomArea = RoomArea.strip(' м² ').strip()
    RoomArea = float(RoomArea)

  except:
    RoomArea = 0
    print(RoomArea)

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



  RoomID = soup.find('div', class_='item-view-search-info-redesign').find('span').text
  RoomID = RoomID.lstrip('№ ').lstrip()
  RoomID = int(RoomID)



  Phone = ''

  print('Цена',Prise)
  print('Имя',FullName)
  print('Этаж',Floor)
  print('Этажей в доме',FloorCount)
  print('Матерьял стен',WallMaterial)
  print('Всего комнат',TotalRooms)
  print('Размер комнаты',RoomArea)
  print('Адрес',Address)
  print('Описание объекта',Description)
  print('ID Объявления',RoomID)

  cursor.execute(""" INSERT INTO dbo.Object (ID, Address, Category, Description, Price, Phone, FullName, FloorCount, WallMaterial, Source, URL) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
  RoomID, Address, 'Комната', Description, Prise, Phone, FullName, FloorCount, WallMaterial, 'Авито', url)
  print('object inserted')

  cursor.execute("""
  INSERT INTO dbo.Room (RoomID,RoomArea, TotalRooms, Floor) VALUES (?,?,?,?)""",
  RoomID, RoomArea, TotalRooms, Floor)

  print('room inserted')

  cursor.execute(
    """
    DELETE FROM dbo.URLS WHERE url = ?
    """,
    url
  )
  cnxn.commit()
  print('url deleted')

def runRoomParse():
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
  cursor = cnxn.cursor()
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'room' ")

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
  cursor.execute("SELECT TOP 3 url FROM dbo.URLS WHERE source = 'https://www.avito.ru' AND type = 'room' ")

  currentUrls = cursor.fetchall()
  currentUrls = [row[0] for row in currentUrls]
  random.shuffle(currentUrls)
  for url in currentUrls:
    html = get_html(url)
    get_data(html, url, cursor, cnxn)
    randTime = random.randint(15, 30)
    time.sleep(randTime)


if __name__ == '__main__':
  main()