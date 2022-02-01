import random # Подключаем модуль случайных чисел 
import datetime
import telebot # Подключаем модуль для Телеграма
import requests
import math
from bs4 import BeautifulSoup
from telebot import types # Импортируем типы из модуля, чтобы создавать кнопки

bot = telebot.TeleBot('xxxxx') # Токен

mes=["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
#message_id = ''

@bot.message_handler(content_types=['text']) # Метод, который получает сообщения и обрабатывает их
def get_text_messages(message):
    #message_id = message.from_user.id
    if message.text == "Старт":
        main_menu(message.from_user.id)
        #message_id = message.from_user.id
        '''
        bot.send_message(message_id, "Выбери доступную операцию из списка:")
        keyboard = types.InlineKeyboardMarkup()
        key_date = types.InlineKeyboardButton(text='Узнать актуальное время', callback_data='time')
        keyboard.add(key_date)
        key_kurs = types.InlineKeyboardButton(text='Курсы валют', callback_data='kurs')
        keyboard.add(key_kurs)
        key_summa = types.InlineKeyboardButton(text='Сумма нескольких элементов', callback_data='summa')
        keyboard.add(key_summa)
        key_matem = types.InlineKeyboardButton(text='Математические операции', callback_data='matem')
        keyboard.add(key_matem)
        bot.send_message(message_id, text='Выбери операцию:', reply_markup=keyboard)
        '''
        #bot.send_message(message.from_user.id, text="Ты можешь увидеть больше операций, нажав на 'Другие операции'")
        
    else:
        bot.send_message(message.from_user.id, "Добро пожаловать в тестовую программу!\nНапиши 'Старт', чтобы запустить программу.")

 
# Обработчик нажатий на кнопки

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "time":
        now=datetime.datetime.now()
        ch=str(now.day)
        mon=now.month
        ye=str(now.year)
        ho=now.hour
        if ho<10:
            ho=str(ho)
            ho="0"+ho
        else:
            ho=str(ho)
        mi=now.minute
        if mi<10:
            mi=str(mi)
            mi="0"+mi
        else:
            mi=str(mi)
        ottime = "Сегодня " + ch + " " + mes[mon-1] + " " + ye + " года."+"\n"+"Актуальное время: " + ho + ":" + mi +"."
        bot.send_message(call.message.chat.id, ottime)
        
    if call.data == "kurs":
        url="http://www.finmarket.ru/currency/rates/"
        source=requests.get(url)
        soup=BeautifulSoup(source.content, "html.parser")
        table = soup.find('div', {'class':'center_column'})

        trd=table.find("div",{"id":"ft_52148"})
        td=trd.find("div",{"class":"value"})
        textd=td.text

        tre=table.find("div",{"id":"ft_52170"})
        te=tre.find("div",{"class":"value"})
        texte=te.text

        trp=table.find("div",{"id":"ft_52146"})
        tp=trp.find("div",{"class":"value"})
        textp=tp.text
        otkurs = "Курсы валют на сегодня:"+"\n"+textd+" р. за Доллар США"+"\n"+texte+" р. за Евро"+"\n"+textp+" р. за Фунт стерлингов" 
        bot.send_message(call.message.chat.id, otkurs)

    if call.data=="matem":
        keyboardm = types.InlineKeyboardMarkup()
        keym_summa = types.InlineKeyboardButton(text='Нахождение суммы нескольких целых чисел', callback_data='summa')
        keyboardm.add(keym_summa)
        keym_razn = types.InlineKeyboardButton(text='Нахождение разности нескольких целых чисел', callback_data='razn')
        keyboardm.add(keym_razn)
        keym_proizv = types.InlineKeyboardButton(text='Нахождение произведения нескольких целых чисел', callback_data='proizv')
        keyboardm.add(keym_proizv)
        keym_exit = types.InlineKeyboardButton(text='--- Выйти в меню ---', callback_data='exitm')
        keyboardm.add(keym_exit)
        bot.send_message(call.message.chat.id, text='Выбери доступную математическую операцию:', reply_markup=keyboardm)

    if call.data=="summa":
        msgsum = bot.send_message(call.message.chat.id,"Через пробел введи числа, сумму которых необходимо найти.")
        bot.register_next_step_handler(msgsum,ssumma)

    if call.data=="razn":
        soobrazn="Через пробел введи целые числа, разность которых необходимо найти."
        soobrazn=soobrazn+"\n\nПримечание: из первого числа будут вычтены все остальные"
        soobrazn=soobrazn+"\n\nПримеры сообщений:\n15 5 20 (Ответ: -10)\n-100 -200 (Ответ: 100)"
        msgrazn = bot.send_message(call.message.chat.id, soobrazn)
        bot.register_next_step_handler(msgrazn, rrazn)

    if call.data=="proizv":
        soobproizv = "Через пробел введи целые числа, произведение которых необходимо найти."
        msgproizv = bot.send_message(call.message.chat.id, soobproizv)
        bot.register_next_step_handler(msgproizv, pproizv)

    if call.data=="exitm":
        message_id = call.message.chat.id
        main_menu(call.message.chat.id)

        
def ssumma(message):
    ms = message.text
    mss = str(ms)+" "
    mns = list(mss)
    mchs = []
    chs=""
    fals = 0
    for i in range(len(mns)):
        if mns[i] != " ":
            chs = chs+mns[i]
        else:
            try:
                int(chs)
                chs = int(chs)
                mchs.append(chs)
                chs=""
            except ValueError:
                fals = 1
    if fals == 0:
        sssum = str(sum(mchs))
        otsum = "Сумма данных элементов равна "+sssum
        bot.send_message(message.chat.id, otsum)
        main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод.")
        main_menu(message.chat.id)

def rrazn(message):
    mr = message.text
    mrs = str(mr)+" "
    mnr = list(mrs)
    mchr = []
    chr = ""
    falr = 0
    for i in range(len(mnr)):
        if mnr[i] != " ":
            chr = chr+mnr[i]
        else:
            try:
                int(chr)
                chr=int(chr)
                mchr.append(chr)
                chr=""
            except ValueError:
                falr=1
    if falr==0:
        if len(mchr) > 1:
            rrrazn = mchr[0]
            for i in range(len(mchr)-1):
                rrrazn = rrrazn-mchr[i+1]
            rrrazn = str(rrrazn)
            otrazn = "Разность данных элементов равна "+rrrazn
            bot.send_message(message.chat.id, otrazn)
            main_menu(message.chat.id)
        else:
            bot.send_message(message.chat.id, "Вы ввели только одно число.")
            main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод.")
        main_menu(message.chat.id)

def pproizv(message):
    mp = message.text
    mps = str(mp)+" "
    mnp = list(mps)
    mchp = []
    chp=""
    falp = 0
    for i in range(len(mnp)):
        if mnp[i] != " ":
            chp = chp+mnp[i]
        else:
            try:
                int(chp)
                chp = int(chp)
                mchp.append(chp)
                chp=""
            except ValueError:
                falp = 1
                break
    if falp == 0:
        ppproizv = str(math.prod(mchp))
        otproizv = "Произведение данных элементов равно "+ppproizv
        bot.send_message(message.chat.id, otproizv)
        main_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Некорректный ввод.")
        main_menu(message.chat.id)

def main_menu(message_id):
    #bot.send_message(message_id, "Выбери доступную операцию из списка:")
    keyboard = types.InlineKeyboardMarkup()
    key_date = types.InlineKeyboardButton(text='Узнать актуальное время', callback_data='time')
    keyboard.add(key_date)
    key_kurs = types.InlineKeyboardButton(text='Курсы валют', callback_data='kurs')
    keyboard.add(key_kurs)
    key_matem = types.InlineKeyboardButton(text='Математические операции', callback_data='matem')
    keyboard.add(key_matem)
    bot.send_message(message_id, text='Выбери доступную операцию:', reply_markup=keyboard)

# Запускаем постоянный опрос бота в Телеграме

bot.polling(none_stop=True, interval=0)
