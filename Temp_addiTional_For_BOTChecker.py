import sqlite3 as sq
import os
import datetime
import time
import requests


dir_pa = 'PATH_your_DJANGOproj/'


def del_inDB(name):
    with sq.connect(dir_pa + 'db.sqlite3')as con:   
        cur = con.cursor()
        try:
            cur.execute(F"SELECT * FROM APPbegin_voice_audio_book WHERE book = '{name}'")
            check = cur.fetchone()
            if check != None:
                try:
                    cur.execute(F'DELETE FROM APPbegin_voice_audio_book WHERE book = "{name}"')
                    return 1
                except:
                    return 0
            else:
                return 0
        except:
            return 0

#Ежевечернее удаление мп3 файлов с дальнейшим удалением соответствующих записей из БД
def dayly_check():
    dayNow = datetime.datetime.now().strftime("%A") #Название текущего дня
    for F in os.scandir(dir_pa + 'media/'): 
        time.sleep(0.1)
        if F.is_file():
            Temp = F.name.split('_') #Пример названия файла: 30_10_22_[17-44-19]_Monday_Filename.mp3
            if Temp[4] != dayNow:
                p = dir_pa + 'media/' + F.name
                os.remove(p)
                DinDB = del_inDB(F.name)
            else:
                INT_hour_23 = int(Temp[3].split('-')[0].replace('[',''))
                if INT_hour_23 < 23 and INT_hour_23 != 22:
                    p = dir_pa + 'media/' + F.name
                    os.remove(p)
                    DinDB = del_inDB(F.name)

#Удаление мп3 файла после ручной команды из ТГ бота
def del_MP3s(LST):
    coun = 0
    for i in LST:
        p = dir_pa + 'media/' + i
        try:
            os.remove(p)
            coun += 1
        except:
            coun = 0
    if len(LST) == coun:
        return 1
    else:
        return 0

#Удаление из БД после ручной команды из ТГ бота
def push_DelDB(LST):
    coun = 0
    for i in LST:
        Try = del_inDB(i)
        if Try == 1:
            coun += 1
        else:
            coun = 0
    if len(LST) == coun:
        return 1
    else:
        return 0

#Отправка msg в ТГ канал (после импорта фун-я может быть использована разными ботами)  
def send(arg, TOKEN):
    url = "https://api.telegram.org/bot"
    channel_id = idTgChannel 
    url += TOKEN
    METHOD = url + "/sendMessage"
    r = requests.post(METHOD, data={
         "chat_id": channel_id,
         "text": arg
          })

   
    
    
    
    
    
    
