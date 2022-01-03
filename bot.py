import os
import telebot
import requests, json

NUTRITION_URL='https://trackapi.nutritionix.com/v2/natural/nutrients'
EXERCISE_URL='https://trackapi.nutritionix.com/v2/natural/exercise'
NUTRITIONIX_API_KEY = os.environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = os.environ['NUTRITIONIX_APP_ID']
BOT_KEY = os.environ['BOT_KEY']

headers={'Content-Type':'application/json', 'x-app-id':NUTRITIONIX_APP_ID, 'x-app-key':NUTRITIONIX_API_KEY}
bot = telebot.TeleBot(BOT_KEY)
botRunning=False

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

@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    data=message.text[11:]
    data_json={
        'query':data,
        'timezone':'Asia/Kolkata',
    }
    res=requests.post(NUTRITION_URL, json=data_json, headers=headers)
    if res.status_code!=400:
        l=len(res.json()['foods'])
        for i in range(l):
            reply=''
            reply+='Food Name: '+res.json()['foods'][i]['food_name']+'\n'
            reply+='Quantity: '+str(res.json()['foods'][i]['serving_qty'])+' '+res.json()['foods'][i]['serving_unit']+'\n'
            reply+='Calories: '+str(res.json()['foods'][i]['nf_calories'])+'\n'
            reply+='Fat: '+str(res.json()['foods'][i]['nf_total_fat'])+'\n'
            reply+='Carbohydrate: '+str(res.json()['foods'][i]['nf_total_carbohydrate'])+'\n'
            reply+='Protein: '+str(res.json()['foods'][i]['nf_protein'])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    data=message.text[9:]
    data_json={
        'query':data,
        'gender':'male',
        'weight_kg':80,
        'height_cm':175,
        'age':22,
    }
    res=requests.post(EXERCISE_URL, json=data_json, headers=headers)
    if res.status_code!=400:
        print(res.json())
        l=len(res.json()['exercises'])
        for i in range(l):
            reply=''
            reply+='Exercise Name: '+res.json()['exercises'][i]['name']+'\n'
            reply+='Duration: '+str(res.json()['exercises'][i]['duration_min'])+' minutes\n'
            reply+='Calories Burned: '+str(res.json()['exercises'][i]['nf_calories'])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')

@bot.message_handler(func=lambda message: botRunning, commands=['report'])
def getCaloriesBurn(message):
    data=message.text[7:]
    bot.reply_to(message, 'Generating report...')
    bot.send_message(message.chat.id, 'CSV file:')

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand :(')

bot.infinity_polling()