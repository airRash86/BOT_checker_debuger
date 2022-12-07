import datetime
import os
import sqlite3 as sq
import requests


dir_pa = 'PATH_your_DJANGOproj/'


#Формирование списка названий мп3 файлов
def len_Files(STORE_AFT_db):
    LST_Files = os.listdir(dir_pa + "media") 
    compare_DB_Fil = compare_LSTs(LST_Files, STORE_AFT_db)
    return compare_DB_Fil

#Сравнение двух списков(при несоответствии - возврат сигнала об этом)
def compare_LSTs(LST_Files, STORE_AFT_db):
    if len(set(STORE_AFT_db)^set(LST_Files)) == 0:
        return 'Проверка без аномалий'
    else:
        uniq_mp3 = []
        uniq_DB = []
        NOT_eq = list(set(LST_Files)^set(STORE_AFT_db))
        for i in NOT_eq:
            if i in LST_Files: uniq_mp3.append(i)
            else: uniq_DB.append(i)
        compose = uniq_mp3 + ['<-Fdb->'] + uniq_DB
        return compose 

#Тут можно ускорить cURL`ом из командной строки Линукса (но оставил так)
def ping_myS(): 
    try: 
        r = requests.get('https://rashprojs.ru/TESTING/')
        return 200
    except: return('NOT_200')

#Формирование списка директорий, ведущих к одноименным мп3 файлам            
def DB_con():
    STORE_AFT_db = []
    with sq.connect(dir_pa + 'yourDB.db')as con: 
        cur = con.cursor()
        cur.execute(f"SELECT book FROM APPbegin_voice_audio_book")
        check = cur.fetchall()
    for i in check:
        STORE_AFT_db.append(i[0])
    chech_len_Files = len_Files(STORE_AFT_db)
    ping200orNOT = ping_myS() #Пинг сайта озвучки текста
    if type(chech_len_Files) == list:
        chech_len_Files.append(ping200orNOT)
    elif type(chech_len_Files) == str and ping200orNOT != 200:
        chech_len_Files = ['<-Fdb->', ping200orNOT]
    return chech_len_Files







