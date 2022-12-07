import telebot
from telebot import types
import requests
import datetime
import time
from Temp_addiTional_For_BOTChecker import * 
from scheduler import DB_con
import threading
import schedule

TOKEN = <your_TOKEN>


# t.me/Checker_RashProjs_bot
# @BOT_Checker_RashProjs

bot = telebot.TeleBot(TOKEN)

    
dir_TXT_Files = 'PATH_To_TXT_STORE/'


#Очистка .TXT файла(ов)
def clr_oldTXT(*args):  
    for i in args:
        open(dir_TXT_Files + i, 'w').close()
        
#Фиксация в .TXT файлы названия мп3 файлов и строк в БД,
#которые подлежат удалению; а также какой статус отклика сайта: 200 или нет        
def w_newTXT(unp_uniq_mp3, unp_uniq_DB, pop200orNOT):  
    if unp_uniq_mp3:                                                                        
        with open(dir_TXT_Files + "unp_uniq_mp3.txt", "a") as File:
            for i in unp_uniq_mp3:
                File.write(str(i)+'\n')
    if unp_uniq_DB:
        with open(dir_TXT_Files + "unp_uniq_DB.txt", "a") as File:
            for i in unp_uniq_DB:
                File.write(str(i)+'\n')
    with open(dir_TXT_Files + "w200orNOT.txt", "a") as File:
        File.write(str(pop200orNOT))

#Распаковка названия мп3 файлов, строк в БД и отклика сайта 
def unpacking(compose):     
    pop200orNOT = compose.pop()
    unp_uniq_mp3 = compose[:compose.index ('<-Fdb->')]
    unp_uniq_DB = compose[compose.index ('<-Fdb->')+1:]
    clr_oldTXT("unp_uniq_mp3.txt", "unp_uniq_DB.txt", "w200orNOT.txt")
    w_newTXT(unp_uniq_mp3, unp_uniq_DB, pop200orNOT)

#Обработчик msg из канала для общего пинга нескольких ботов
@bot.channel_post_handler()  
def hello(message):
    if message.chat.id == idTgChannel and message.text == 'TOTAL':
        time.sleep(1.5)
        try:
            chech_Files_DB = DB_con()   #Запуск проверки бэкенда сайта rashprojs.ru/voiceworker/
            mark = '🚀Проверка без аномалий!\n-----\n'
            if chech_Files_DB != 'Проверка без аномалий':
                unpack = unpacking(chech_Files_DB)
                comp_F_DB()
                mark = 'ℹ️Есть новости. Жди MSG в личку\n-----\n'   
        except:
            mark = '⚠ALARM, во время опроса сервисов что-то пошло не так.\n-----\n'
        time.sleep(0.05)
        send(F'{mark} Третий (Чекер) 5288033405 - ✅ONLINE"', TOKEN) #Отправка отчета о состоянии бэка сайта в канал для общего пинга нескольких ботов

#Почти "универсальная" функция)  
def swhoORdeling_From_DBorMP3orResp(mode, nameFile): # 0 - вывод в сообщении админу, 1 - удалене из БД строк и из папки media мп3 файлов
    with open(dir_TXT_Files + nameFile) as F:
        lines = [line.rstrip('\n') for line in F]
    if mode == 0:
        show = ''
        for j in lines:
            show += j+'\n'
        return show
    elif mode == 1 and nameFile == "unp_uniq_DB.txt":
        if len(lines) == 0:
            return 2
        push_DDB = push_DelDB(lines)
        if push_DDB == 1:
            clr_oldTXT("unp_uniq_DB.txt")
            return 1
        else:
            return 0
    elif mode == 1 and nameFile == "unp_uniq_mp3.txt":
        if len(lines) == 0:
            return 2
        dMP3 = del_MP3s(lines)
        if dMP3 == 1:
            clr_oldTXT("unp_uniq_mp3.txt")
            return 1
        else:
            return 0

#Формирование подробного отчета с возможностью удаления "лишних" мп3 файлов и(или) строк в БД,
#высалка в личку админу    
def comp_F_DB():
    showDB = swhoORdeling_From_DBorMP3orResp(0, "unp_uniq_DB.txt")
    showFiles = swhoORdeling_From_DBorMP3orResp(0, "unp_uniq_mp3.txt")
    showResp = swhoORdeling_From_DBorMP3orResp(0, "w200orNOT.txt")
    BUTT_Del = types.InlineKeyboardMarkup()
    canc = types.InlineKeyboardButton(text = "✅ok", callback_data = 'norm')
    LSTargs_ForBUTT = []
    show_in_mess = '📡Response: ' + showResp +'\nСписок на удаление (может быть пуст)\n-----\n'
    if showDB:
        d_DB = types.InlineKeyboardButton(text = "⛔📜Del DB", callback_data = 'Del_DB')
        show_in_mess += '📜Удаление из БД:\n' + showDB + '-----\n'
        LSTargs_ForBUTT.insert(0, d_DB)
    if showFiles:
        d_Fil = types.InlineKeyboardButton(text = "⛔📢Del mp3", callback_data = 'Del_mp3')
        show_in_mess += '📢Удаление из MP3:\n' + showFiles 
        LSTargs_ForBUTT.insert(0, d_Fil)
    LSTargs_ForBUTT.append(canc)
    args_ForBUTT = tuple(LSTargs_ForBUTT)
    BUTT_Del.add(*args_ForBUTT) # распаковал кортеж
    bot.send_message(TG_id_admin, show_in_mess, reply_markup=BUTT_Del)

#Обработка нажатия на inline кнопки
@bot.callback_query_handler(func = lambda call: True)
def ans_Inline(call):
    if call.data == 'Del_mp3':
        DelFil = swhoORdeling_From_DBorMP3orResp(1, "unp_uniq_mp3.txt")
        if DelFil == 1:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅mp3 файлы почищены")
        elif DelFil == 2:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="❗Чистка окончена! Хватит тыкать!")
        elif DelFil == 0:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠Во время ручного удаления MP3-файлов что-то пошло не так: попробуй TOTAL в чат повторно чуть позже")
    elif call.data == 'Del_DB':
        DelDB = swhoORdeling_From_DBorMP3orResp(1, "unp_uniq_DB.txt")
        if DelDB == 1:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅БД почищена")
        elif DelDB == 2:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="❗Чистка окончена! Хватит тыкать!")
        elif DelDB == 0:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠Во время ручного удаления из БД что-то пошло не так: попробуй TOTAL в чат повторно чуть позже")
    elif call.data == 'norm':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='✅Готово') #удаление инлайн клавы
        pass
    bot.answer_callback_query(callback_query_id=call.id) #это чтобы иконка часов не висела на кнопке 

#Если захочется пингануть руками
@bot.message_handler(content_types=['text'])
def abc(message):
    bot.send_message(message.chat.id, 'Работаю!')
    
# ------------ Блок ежевечерней автоматической проверки бэка сайта с автоудалением накопившиихся за сутки мп3 файлов и соответствующих им записей в БД,\
def layer():                            #а также с автозапуском пинга остальных ботов, "висящих" в канале для общего пинга нескольких ботов (команда: TOTAL)
    dayly_check()
    send(F'Бот-Чекер - ✅ONLINE\nЕжевечернюю проверку провёл.\nКоманда: TOTAL', TOKEN)
    
schedule.every().day.at("23:09:45").do(layer) #Это можно делать через Джанго сигнал (знаю об этом только в теории), но оставил так
def go():
    while 1:
        schedule.run_pending()
        time.sleep(1)

TTT = threading.Thread(target=go, name="daily")
TTT.start()
# --------------

while True:
    try:
        print('Три-два-раз, Дебаг-БОТ СТАРТАНУЛ')
        bot.polling(none_stop=True, timeout=123)
    except:
        time.sleep(5)
        continue





