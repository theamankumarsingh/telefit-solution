import os
import telebot
import requests

#NUTRITIONIX_API_KEY = os.environ['NUTRITIONIX_API_KEY']
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)
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
    bot.send_message(message.chat.id, message.text[11:])
    bot.send_message(message.chat.id, 'Nutrition info:')
    bot.send_message(message.chat.id, 'Calories:')
    bot.send_message(message.chat.id, 'Fat:')
    bot.send_message(message.chat.id, 'Carbohydrates:')
    bot.send_message(message.chat.id, 'Protein:')

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    bot.send_message(message.chat.id, message.text[9:])
    bot.send_message(message.chat.id, 'Calories burned:')

@bot.message_handler(func=lambda message: botRunning, commands=['report'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    bot.send_message(message.chat.id, message.text[7:])
    bot.send_message(message.chat.id, 'CSV file:')

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand :(')

bot.infinity_polling()