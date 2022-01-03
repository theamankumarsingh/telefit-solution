import os
import telebot
import requests
import json, csv

NUTRITION_URL='https://trackapi.nutritionix.com/v2/natural/nutrients'
EXERCISE_URL='https://trackapi.nutritionix.com/v2/natural/exercise'
NUTRITIONIX_API_KEY = os.environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = os.environ['NUTRITIONIX_APP_ID']
BOT_KEY = os.environ['BOT_KEY']

headers={'Content-Type':'application/json', 'x-app-id':NUTRITIONIX_APP_ID, 'x-app-key':NUTRITIONIX_API_KEY}
user={'name':None, 'gender':None, 'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(BOT_KEY)

@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning=True
    bot.reply_to(message, 'Hello! I am TeleFit. Use me to monitor your health :D')

@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning=False
    bot.reply_to(message, 'Bye!')

@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input=message.text[6:]
    user['name']=usr_input.split(',')[0].strip()
    user['gender']=usr_input.split(',')[1].strip()
    user['weight']=usr_input.split(',')[2].strip()
    user['height']=usr_input.split(',')[3].strip()
    user['age']=usr_input.split(',')[4].strip()
    bot.reply_to(message, 'User set!')
    reply=''
    for key, value in user.items():
        reply+=str(key)+':\t'+str(value)+'\n'
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    usr_input=message.text[11:]
    data_json={
        'query':usr_input,
        'timezone':'Asia/Kolkata',
    }
    res=requests.post(NUTRITION_URL, json=data_json, headers=headers)
    if res.status_code!=400:
        l=len(res.json()['foods'])
        for i in range(l):
            data=[
                res.json()['foods'][i]['food_name'],
                str(res.json()['foods'][i]['serving_qty'])+' '+res.json()['foods'][i]['serving_unit'],
                res.json()['foods'][i]['nf_calories'],
                res.json()['foods'][i]['nf_total_fat'],
                res.json()['foods'][i]['nf_total_carbohydrate'],
                res.json()['foods'][i]['nf_protein'],
            ]
            reply=''
            reply+='Food Name: '+data[0]+'\n'
            reply+='Quantity: '+data[1]+'\n'
            reply+='Calories: '+str(data[2])+'\n'
            reply+='Fat: '+str(data[3])+'\n'
            reply+='Carbohydrate: '+str(data[4])+'\n'
            reply+='Protein: '+str(data[5])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    usr_input=message.text[10:]
    data_json={
        'query':usr_input,
        'gender':user['gender'],
        'weight_kg':user['weight'],
        'height_cm':user['height'],
        'age':user['age'],
    }
    res=requests.post(EXERCISE_URL, json=data_json, headers=headers)
    if res.status_code!=400:
        print(res.json())
        l=len(res.json()['exercises'])
        for i in range(l):
            data=[
                res.json()['exercises'][i]['name'],
                res.json()['exercises'][i]['duration_min'],
                res.json()['exercises'][i]['nf_calories'],
            ]
            reply=''
            reply+='Exercise Name: '+data[0]+'\n'
            reply+='Duration: '+str(data[1])+' minutes\n'
            reply+='Calories Burned: '+str(data[2])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')

@bot.message_handler(func=lambda message: botRunning, commands=['report'])
def getCaloriesBurn(message):
    usr_input=message.text[8:]
    bot.reply_to(message, 'Generating report...')
    bot.send_message(message.chat.id, 'CSV file:')

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand :(')

bot.infinity_polling()