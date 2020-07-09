# -*- coding: utf-8 -*-
import pyodbc

pageTemplate = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=UTF-8"
 http-equiv="content-type">
  <title>База объектов недвижимости</title>
</head>
<body>
{result}
</body>
</html>''' # NEW note '{person}' two lines up

def main():
    itemTemplateOpen = '<div>'
    itemTemplateInnerBlock = '<div style="margin-left:40px">'

    itemTemplateClose = '</div>'
    spacer = '<br>'
    objectsFromDBFlat = getObjectsFlat()
    objectsFromDBHous = getObjectsHous()
    objectsFromDBRoom = getObjectsRoom()

    result = ''
    for object in objectsFromDBFlat:
        result += itemTemplateOpen
        result += makeTextBold('Адрес: ') + str(object[1])
        result += spacer
        result += str(object[2]) +  makeTextBold(' - Тип объекта')
        result += spacer
        result += str(object[14]) +  makeTextBold(' - комнатная')
        result += itemTemplateInnerBlock
        result += makeTextBold(' Цена: ') + str(int(object[4])) + ' ₽ ' + ' | '
        result += makeTextBold('Имя: ') + str(object[6]) +  ' | '
        result += makeTextBold('Матерьял стен: ') + str(object[8]) +  ' | '
        result += makeTextBold('Этаж: ') + str(object[13]) +  ' | '
        result += makeTextBold('Всего этажей: ') + str(object[7]) +  ' | '
        result += makeTextBold('Общая площадь: ') + str(object[12]) +  ' м.кв.  | '
        result += makeTextBold('Площадь кухни: ') + str(object[15]) +  ' м.кв.  | '
        result += spacer
        result += makeTextBold('Описание: ') + str(object[3])
        result += spacer
        result += makeTextBold('Источник: ') + str(object[9])
        result += itemTemplateInnerBlock
        result += makeTextBold('URL объявления: ') + str(object[10])
        result += itemTemplateClose
        result += itemTemplateClose
        result += spacer



    for object in objectsFromDBHous:
        result += itemTemplateOpen
        result += makeTextBold('Адрес: ') + str(object[1])
        result += spacer
        result += str(object[2]) +  makeTextBold(' - Тип объекта')
        result += itemTemplateInnerBlock
        result += makeTextBold(' Цена: ') + str(int(object[4])) + ' ₽ ' + ' | '
        result += makeTextBold('Имя: ') + str(object[6]) +  ' | '
        result += makeTextBold('Матерьял стен: ') + str(object[8]) +  ' | '
        result += makeTextBold('Всего этажей: ') + str(object[7]) +  ' | '
        result += makeTextBold('Площадь дома: ') + str(object[12]) +  ' м.кв. | '
        result += makeTextBold('Площадь участка: ') + str(object[13]) +  ' соток | '
        result += makeTextBold('Расстояние до города: ') + str(object[14]) +  'км | '
        result += spacer
        result += makeTextBold('Описание: ') + str(object[3])
        result += spacer
        result += makeTextBold('Источник: ') + str(object[9])
        result += itemTemplateInnerBlock
        result += makeTextBold('URL объявления: ') + str(object[10])
        result += itemTemplateClose
        result += itemTemplateClose
        result += spacer



    for object in objectsFromDBRoom:
        result += itemTemplateOpen
        result += makeTextBold('Адрес: ') + str(object[1])
        result += spacer
        result += str(object[2]) +  makeTextBold(' - Тип объекта')
        result += itemTemplateInnerBlock
        result += makeTextBold(' Цена: ') + str(int(object[4])) + ' ₽ ' + ' | '
        result += makeTextBold('Имя: ') + str(object[6]) +  ' | '
        result += makeTextBold('Количество комнат: ') + str(object[14]) +  ' | '
        result += makeTextBold('Матерьял стен: ') + str(object[8]) +  ' | '
        result += makeTextBold('Этаж: ') + str(object[14]) +  ' | '
        result += makeTextBold('Всего этажей: ') + str(object[7]) +  ' | '
        result += makeTextBold('Площаль комнаты: ') + str(object[12]) +  ' м.кв.  | '
        result += spacer
        result += makeTextBold('Описание: ') + str(object[3])
        result += spacer
        result += makeTextBold('Источник: ') + str(object[9])
        result += itemTemplateInnerBlock
        result += makeTextBold('URL объявления: ') + str(object[10])
        result += itemTemplateClose
        result += itemTemplateClose
        result += spacer

    # for object in objectsFromDB:
    #     result += itemTemplateOpen
    #     result += str(object)
    #     result += itemTemplateClose
    #     result += spacer
    contents = pageTemplate.format(**locals())
    browseLocal(contents)

def strToFile(text, filename):
    """Write a file with the given name and the given text."""
    output = open(filename,"w", encoding="utf-8")
    output.write(text)
    output.close()

def browseLocal(webpageText, filename='tempBrowseLocal.html'):
    '''Start your webbrowser on a local file containing the text
    with given filename.'''
    import webbrowser, os.path
    strToFile(webpageText, filename)
    webbrowser.open("file:///" + os.path.abspath(filename)) #elaborated for Mac

def getObjectsFlat():
    objectsFromDBFlat = []
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM dbo.Object INNER JOIN dbo.Flat on dbo.Object.ID = dbo.Flat.FlatID")
    result = cursor.fetchall()
    result = [row for row in result]
    objectsFromDBFlat = result
    return objectsFromDBFlat


def getObjectsHous():
    objectsFromDBHouse = []
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM dbo.Object INNER JOIN dbo.House on dbo.Object.ID = dbo.House.HouseID")
    result = cursor.fetchall()
    result = [row for row in result]
    objectsFromDBHouse = result
    return objectsFromDBHouse

def getObjectsRoom():
    objectsFromDBRoom = []
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 11 for SQL Server};SERVER=USER-ПК\\SQLEXPRESS ;DATABASE=SamoilovDR_BD_Nedvizhimosti;Trusted_Connection=yes')
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM dbo.Object INNER JOIN dbo.Room on dbo.Object.ID = dbo.Room.RoomID")
    result = cursor.fetchall()
    result = [row for row in result]
    objectsFromDBRoom = result
    return objectsFromDBRoom

def makeTextBold(text):
    itemTemplateBoldSpan = '<span style="font-weight:bold">'
    itemTemplateCloseSpan = '</span>'
    return itemTemplateBoldSpan + text + itemTemplateCloseSpan

if __name__ == '__main__':
  main()