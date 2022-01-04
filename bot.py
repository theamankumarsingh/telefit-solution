import os
from os import environ
import telebot
import requests
import json
import csv

NUTRITION_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
EXERCISE_URL = 'https://trackapi.nutritionix.com/v2/natural/exercise'
NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    fields = ['Food-Name', 'Quantity', 'Calories',
              'Fat', 'Carbohydrates', 'Protein']
    filename = "nutrition_records.csv"
    with open(filename, 'w') as f_object1:
        csvwriter = csv.writer(f_object1)
        csvwriter.writerow(fields)
        f_object1.close()
    fields = ['Exercise-Name', 'Duration', 'Calories-Burned']
    filename = "exercise_records.csv"
    with open(filename, 'w') as f_object1:
        csvwriter = csv.writer(f_object1)
        csvwriter.writerow(fields)
        f_object1.close()
    bot.reply_to(
        message, 'Hello! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nStay Healthy'+'\N{flexed biceps}')


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/nutrition Units Quantity-Type Food-Name\" command to get the nutrients of a particular food. For eg: \"/nutrition 1 piece chapati\"\n\n2.1 For using the bot to get details about an exercise you need to first set the user data using the command \"/user Name, Gender, Weight(in Kg), Height (in cm), Age\". For eg: \"/user Akshat, Male, 70, 6, 19\n\n2.2 Then you can use the command \"/execise Duration-amount Duration-unit Exercise-name\" to get data about an exercise. For eg: \"/exercise 40 minutes push-ups\"\n\n3.0. You can use the command \"/reports Report-name\" to get the reports in CSV Format. For eg: \"/reports nutrition\" to get nutrition report and \"/reports exercise\" to get exercise reports or use the command \"/reports nutrition, exercise\" to get both nutrition and exercise reports\n\n4.0. You can use the command \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input = message.text[6:]
    user['name'] = usr_input.split(',')[0].strip()
    user['gender'] = usr_input.split(',')[1].strip()
    user['weight'] = usr_input.split(',')[2].strip()
    user['height'] = usr_input.split(',')[3].strip()
    user['age'] = usr_input.split(',')[4].strip()
    bot.reply_to(message, 'User set!')
    reply = ''
    for key, value in user.items():
        reply += str(key)+':\t'+str(value)+'\n'
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    usr_input = message.text[11:]
    data_json = {
        'query': usr_input,
        'timezone': 'Asia/Kolkata',
    }
    res = requests.post(NUTRITION_URL, json=data_json, headers=headers)
    if res.status_code != 400:
        l = len(res.json()['foods'])
        for i in range(l):
            data = [
                res.json()['foods'][i]['food_name'],
                str(res.json()['foods'][i]['serving_qty']) +
                ' '+res.json()['foods'][i]['serving_unit'],
                res.json()['foods'][i]['nf_calories'],
                res.json()['foods'][i]['nf_total_fat'],
                res.json()['foods'][i]['nf_total_carbohydrate'],
                res.json()['foods'][i]['nf_protein'],
            ]
            rows = [data[0], data[1], str(data[2]), str(
                data[3]), str(data[4]), str(data[5])]
            filename = "nutrition_records.csv"
            with open(filename, 'a') as f_object1:
                writer_object = csv.writer(f_object1)
                writer_object.writerow(rows)
                f_object1.close()
            reply = ''
            reply += 'Food Name: '+data[0]+'\n'
            reply += 'Quantity: '+data[1]+'\n'
            reply += 'Calories: '+str(data[2])+'\n'
            reply += 'Fat: '+str(data[3])+'\n'
            reply += 'Carbohydrate: '+str(data[4])+'\n'
            reply += 'Protein: '+str(data[5])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    usr_input = message.text[10:]
    data_json = {
        'query': usr_input,
        'gender': user['gender'],
        'weight_kg': user['weight'],
        'height_cm': user['height'],
        'age': user['age'],
    }
    res = requests.post(EXERCISE_URL, json=data_json, headers=headers)
    if res.status_code != 400:
        l = len(res.json()['exercises'])
        for i in range(l):
            data = [
                res.json()['exercises'][i]['name'],
                res.json()['exercises'][i]['duration_min'],
                res.json()['exercises'][i]['nf_calories'],
            ]
            rows = [data[0], data[1], str(data[2])]
            filename = "exercise_records.csv"
            with open(filename, 'a') as f_object2:
                writer_object = csv.writer(f_object2)
                writer_object.writerow(rows)
                f_object2.close()
            reply = ''
            reply += 'Exercise Name: '+data[0]+'\n'
            reply += 'Duration: '+str(data[1])+' minutes\n'
            reply += 'Calories Burned: '+str(data[2])+'\n'
            bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, 'Error!')


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    usr_input = message.text[9:]
    usr_input = [x.strip() for x in usr_input.split(',')]
    if ("exercise" in usr_input):
        doc = open('exercise_records.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    if ("nutrition" in usr_input):
        doc = open('nutrition_records.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    if ("exercise" not in usr_input and "nutrition" not in usr_input):
        bot.send_message(message.chat.id, 'Error!')


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
