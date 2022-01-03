import os
import telebot

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

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand :(')

bot.polling()