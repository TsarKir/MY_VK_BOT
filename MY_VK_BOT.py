#!/usr/bin/env python
# coding: utf-8

# In[146]:


import time
import requests
import random

from bs4 import BeautifulSoup as BS
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from transliterate import translit
import psycopg2

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Афиша', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Погода', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Валюта', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Сменить город', color=VkKeyboardColor.POSITIVE)

afisha_keyboard = VkKeyboard(one_time=True)
afisha_keyboard.add_button('Афиша на сегодня', color=VkKeyboardColor.PRIMARY)
afisha_keyboard.add_button('Афиша на завтра', color=VkKeyboardColor.POSITIVE)

weather_keyboard = VkKeyboard(one_time=True)
weather_keyboard.add_button('Погода на завтра', color=VkKeyboardColor.PRIMARY)
weather_keyboard.add_button('Погода на сегодня', color=VkKeyboardColor.POSITIVE)

cities_kudago = {'Екатеринбург': 'ekb',
 'Казань': 'kzn',
 'Москва': 'msk',
 'Нижний Новгород': 'nnv',
 'Новосибирск': 'nsk',
 'Санкт-Петербург': 'spb'}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}

def afisha_5_events (city_kudago,date):
    def afisha_randomizer():
        i = 0
        randomizer = []
        while i !=5:
            randomizer.append(random.randint(0, len(l.json()['results'])))
            i+=1
        return randomizer
    kudago_get = 'https://kudago.com/public-api/v1.4/events/?'+        'lang=&fields=site_url,price,short_title&expand=&order_by=&page_size=10000&text_format=&ids=&location='+        city_kudago+'&actual_since='+date+'&actual_until=&is_free=&categories=&lon=&lat=&radius='
    l = requests.get(kudago_get, headers = headers)
    randomizer = afisha_randomizer()
    first_event = l.json()['results'][randomizer[0]]["short_title"] + "\n"        + l.json()['results'][randomizer[0]]["site_url"] + "\n"        + l.json()['results'][randomizer[0]]['price'] + "\n\n"
    second_event = l.json()['results'][randomizer[1]]["short_title"] + "\n"        + l.json()['results'][randomizer[1]]["site_url"] + "\n"        + l.json()['results'][randomizer[1]]['price'] + "\n\n"
    third_event = l.json()['results'][randomizer[2]]["short_title"] + "\n"        + l.json()['results'][randomizer[2]]["site_url"] + "\n"        + l.json()['results'][randomizer[2]]['price'] + "\n\n"
    forth_event = l.json()['results'][randomizer[3]]["short_title"] + "\n"        + l.json()['results'][randomizer[3]]["site_url"] + "\n"        + l.json()['results'][randomizer[3]]['price'] + "\n\n"
    last_event = l.json()['results'][randomizer[4]]["short_title"] + "\n"        + l.json()['results'][randomizer[4]]["site_url"] + "\n"        + l.json()['results'][randomizer[4]]['price'] + "\n\n"
    return first_event + second_event + third_event + forth_event + last_event

def weather(city_eng):
    token_weatherapi = 'YOUR TOKEN'
    weather_url = 'http://api.weatherapi.com/v1/forecast.json?key='+token_weatherapi+        '&q='+city_eng+'&days=2&aqi=no&alerts=no'
    l = requests.get(weather_url, headers = headers)
    return [
        l.json()['forecast']['forecastday'][0]['day']['avgtemp_c'],
        l.json()['forecast']['forecastday'][1]['day']['avgtemp_c']
    ]

def currency():
    CBR_url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='
    l = requests.get(CBR_url, headers = headers)
    soup = BS(l.text, 'lxml')
    USD = "1 USD = " + str(soup.find_all('value')[13].text) + " руб." + "\n"
    EUR = "1 EUR = " + str(soup.find_all('value')[14].text) + " руб. " + "\n"
    GBP = "1 GBP = " + str(soup.find_all('value')[2].text) + " руб. " + "\n"
    CNY = "1 CNY = " + str(soup.find_all('value')[22].text) + " руб." + "\n"
    JPY = "1 JPY = " + str(soup.find_all('value')[42].text) + " руб."  
    return USD + EUR + GBP + CNY + JPY

def insert_in_table(user_id, chosen_city, city, city_kudago, city_eng):
    
    try:
        connection = psycopg2.connect(user = '',password = '',host = 'l',database = '')
    
        with connection.cursor() as cursor:
            cursor.execute("INSERT into users (user_ids, chosen_city, city, city_kudago, city_eng) VALUES (%s,%s,%s,%s,%s);", (user_id,chosen_city,city,city_kudago, city_eng))
        connection.commit()
        
    except Exeption as ex:
        print ('Error',ex)
    finally:
        if connection:
            connection.close()
            
def is_chosen (user_id):
    try:
        connection = psycopg2.connect(user = '',password = '',host = 'l',database = '')

        with connection.cursor() as cursor:
            cursor.execute("SELECT chosen_city FROM users WHERE user_ids = %s;", [user_id])
            return cursor.fetchone()
        
    except Exception as ex:
        print ('Error',ex)
    finally:
        if connection:
            connection.close()
            
def select_city_eng (user_id):
    try:
        connection = psycopg2.connect(user = '',password = '',host = 'l',database = '')

        with connection.cursor() as cursor:
            cursor.execute("SELECT city_eng FROM users WHERE user_ids = %s;", [user_id])
            return cursor.fetchone()
        
    except Exception as ex:
        print ('Error',ex)
    finally:
        if connection:
            connection.close()
            
def select_city_kudago (user_id):
    try:
        connection = psycopg2.connect(user = '',password = '',host = 'l',database = '')

        with connection.cursor() as cursor:
            cursor.execute("SELECT city_kudago FROM users WHERE user_ids = %s;", [user_id])
            return cursor.fetchone()
        
    except Exception as ex:
        print ('Error',ex)
    finally:
        if connection:
            connection.close()

def not_chosen(user_id):
    try:
        connection = psycopg2.connect(user = '',password = '',host = 'l',database = '')

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_ids = %s;", [user_id])
        connection.commit()
        
    except Exception as ex:
        print ('Error',ex)
    finally:
        if connection:
            connection.close()
            
token = 'YOUR TOKEN'
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text == '/start': 
            if event.from_user:
                vk.users.get(user_ids=event.user_id)
                vk.messages.send(
                user_id=event.user_id, message="Привет! Я очень полезный бот,"+\
                    "помогу тебе выбрать куда сходить, узнать погоду и курсы основных валют "+\
                    " чтобы продолжить введи свой город", 
                    random_id = random.randint(0, 10000))
        elif event.text == 'Афиша':
            if event.from_user:
                vk.messages.send(
                user_id=event.user_id, message="Прислать тебе афишу на сегодня или на завтра?", 
                    random_id = random.randint(0, 10000), keyboard = afisha_keyboard.get_keyboard())
        elif event.text == 'Афиша на сегодня':
                vk.messages.send(
                user_id=event.user_id, message="Подбираю для тебя интересные мероприятия, пожалуйста, подожди чуть-чуть", 
                    random_id = random.randint(0, 10000))
                vk.messages.send(
                user_id=event.user_id, message=afisha_5_events(select_city_kudago (event.user_id)[0],str(int(time.time()))), 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())
        elif event.text == 'Афиша на завтра':
                vk.messages.send(
                user_id=event.user_id, message="Подбираю для тебя интересные мероприятия, пожалуйста, подожди чуть-чуть", 
                    random_id = random.randint(0, 10000))
                vk.messages.send(
                user_id=event.user_id, message=afisha_5_events(select_city_kudago (event.user_id)[0],str(int(time.time())+86400)), 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())
        elif event.text == 'Погода':
            if event.from_user:
                vk.messages.send(
                user_id=event.user_id, message="Тебя интересует погода сегодня или завтра?", 
                    random_id = random.randint(0, 10000), keyboard = weather_keyboard.get_keyboard())
        elif event.text == 'Погода на сегодня':
            if event.from_user:
                vk.messages.send(
                user_id=event.user_id, message='Сегодня ' + str(weather(select_city_eng (event.user_id)[0])[0]) + ' градусов по Цельсию', 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())
        elif event.text == 'Погода на завтра':
            if event.from_user:
                vk.messages.send(
                user_id=event.user_id, message= 'Завтра ' + str(weather(select_city_eng (event.user_id)[0])[1]) + ' градусов по Цельсию', 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())
        elif event.text == 'Валюта':
            if event.from_user:
                vk.messages.send(
                user_id=event.user_id, message='Курсы основных валют сегодня:\n' + currency(), 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())  
        elif event.text == 'Сменить город':
            if event.from_user:
                not_chosen(event.user_id)
                vk.messages.send(
                user_id=event.user_id, message="Введи свой город", 
                    random_id = random.randint(0, 10000))
        else:
            if is_chosen(event.user_id) == None:
                if event.from_user:
                    if event.text == 'Москва':
                        city_eng = 'Moscow'
                        city = event.text
                        city_kudago = cities_kudago[event.text]
                    elif event.text == 'Санкт-Петербург':
                        city_eng = 'Saint-Petersburg'
                        city = event.text
                        city_kudago = cities_kudago[event.text]
                    else:
                        city = event.text
                        city_eng = translit(event.text, 'uk')
                        if event.text not in cities_kudago:
                            city_kudago = cities_kudago['Москва']
                            vk.messages.send(
                            user_id=event.user_id, message="К сожалению, твоего города нет в моей базе мероприятий:(\n"+\
                                "Буду присылать тебе афишу города Москвы", random_id = random.randint(0, 10000))
                        else:
                            city_kudago = cities_kudago[event.text]
                    insert_in_table(event.user_id, '1', city, city_kudago, city_eng)
                    vk.messages.send(
                    user_id=event.user_id, message="Отлично! Твой город: " + city + " Чем тебе помочь?", 
                        random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())
            else:
                vk.messages.send(
                user_id=event.user_id, message="Я не понимаю тебя:( Давай ты выберешь, чем я смогу тебе помочь?", 
                    random_id = random.randint(0, 10000), keyboard = keyboard.get_keyboard())


# In[ ]:




