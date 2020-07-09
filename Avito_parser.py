import Flat_Avito
import Room_Avito
import House_Avito
import Avito_parser_URL_Flat
import Avito_parser_URL_House
import Avito_parser_URL_Room
import time
import random

def main():
  randTime = random.randint(5, 9)

  Avito_parser_URL_Flat.getFreshUrls()
  time.sleep(randTime)

  Avito_parser_URL_House.getFreshUrls()
  time.sleep(randTime)

  Avito_parser_URL_Room.getFreshUrls()
  time.sleep(randTime)

  Flat_Avito.runFlatParse()
  Room_Avito.runRoomParse()
  House_Avito.runHouseParse()


if __name__ == '__main__':
  main()