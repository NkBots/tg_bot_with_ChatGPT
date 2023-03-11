import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from settings import API_KEY, BOT_KEY
import settings
import csv
import telebot
import re

logging.basicConfig(level=logging.INFO)


openai.api_key = API_KEY


bot = Bot(token=BOT_KEY)


dp = Dispatcher(bot)


contex_history = {}


#model = 'text-davinci-003'

models = {
    'gpt3.5': 'gpt-3.5-turbo',
    'dav3': 'text-davinci-003'
}

current_model = 'gpt3.5'

@dp.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, f"""This bot has two models. dav3 is a weaker language model. She also doesn't remember dialogue. gpt3.5 is the model currently used in ChatGPT. Also, this model remembers the dialogue, which makes it an indispensable assistant.
  
  To change the model type /mode followed by gpt3.5 or dav3""")


@dp.message_handler(commands=['start'])
def help(message):
  bot.send_message(message.chat.id, f"""I am AI Bot Developed By @NitinSahay for private use Only""")




