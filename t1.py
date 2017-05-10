import time
import random
import datetime
import telepot
import weather
import sys
import psycopg2
from wit import Wit

def db_adduser(chat_id):
    msg = "insert into user_id (telegram_id) values (%s)" %chat_id
    try:
        cur = conn.cursor()
        cur.execute(msg)
        conn.commit()
    except :
        #print("add into db fail {0}").format(e)
        buff = 0

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    db_adduser(chat_id)

    print ('%s sent command: %s' % (chat_id,command))

    if command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == 'weather now':
        ans = weather.weather_now("Hsinchu")
        bot.sendMessage(chat_id, ans)
    elif command == 'weather':
        ans = weather.weather_forecast("Hsinchu")
        bot.sendMessage(chat_id, ans)
    else :
        resp = wit_client.message(command)
        if 'intent' in resp['entities']:
            bool_weather =  False
            bool_forecast = False
            for i in resp['entities']['intent']:
                if i['value'] == 'la_weather':
                    bool_weather = True
                elif i['value'] == 'forecast':
                    bool_forecast = True
            if bool_weather == True:
                if bool_forecast == True:
                    ans = weather.weather_forecast(resp['entities']['location'][0]['value'])
                    bot.sendMessage(chat_id,ans)
                else:
                    ans = weather.weather_now(resp['entities']['location'][0]['value'])
                    bot.sendMessage(chat_id,ans)

def wit_send(request, response):
    print(response['text'])
token_file = open("token.txt","r")  #file to store token
tokens = token_file.read().split('\n')
wit_actions = { 'send' : wit_send, }
wit_token = tokens[0] 
wit_client = Wit(access_token=wit_token, actions=wit_actions)
bot = telepot.Bot(tokens[1])
bot.message_loop(handle)
print ('I am listening ...')
try:
    conn = psycopg2.connect(database="telegram_ai", user = "telegram_ai", password = "iamchris", host = "127.0.0.1", port = "5432")
except:
    print("connect db error")

while 1:
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        bot.sendMessage(238121749, weather.weather_now('Hsinchu') )
    time.sleep(50)

