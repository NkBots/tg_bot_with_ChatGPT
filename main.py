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

current_model = 'gpt-3.5-turbo'

@dp.message_handler(commands=['help'])
async def help(message):
  await bot.send_message(message.chat.id, f"""This bot has two models. dav3 is a weaker language model. She also doesn't remember dialogue. gpt3.5 is the model currently used in ChatGPT. Also, this model remembers the dialogue, which makes it an indispensable assistant.
  
  To change the model type /mode followed by gpt3.5 or dav3""")


@dp.message_handler(commands=['start'])
async def help(message):
  await bot.send_message(message.chat.id, f"""I am AI Bot Developed By @NitinSahay for private use Only""")



@dp.message_handler(lambda message: True)
async def handle_message(message):
    
    user_id = message.chat.id

    
    spam = 'Dont Spam please wait Some second'

    
    if contex_history.get(user_id) == None:

        
        response = await generate_response(message.text)

       
        contex_history[user_id] = [message.text]
    else:

        contex_history[user_id] += [message.text]
        len_history = len(contex_history[user_id])

        
        if len_history > 1:

            
            if contex_history[user_id][-1].lower().strip() == contex_history[user_id][-2].lower().strip():
                del contex_history[user_id][-1]
                await bot.send_message(chat_id=user_id, reply_to_message_id=message.message_id, text=spam)
                return

                
        if len(contex_history[user_id]) > 9:
            del contex_history[user_id][0]

        
        response = await generate_response(message.text + ' ' + '\n'.join(contex_history.get(user_id)))

    if response['text']:
        await bot.send_message(chat_id=user_id, reply_to_message_id=message.message_id, text=response['text'])



async def generate_response(text):
    prompt = f"{text}"
    max_tokens = 1024
    # Запрос
    response = openai.Completion.create(
        model=current_model,
        prompt=prompt,
        temperature=0.9,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    return {'text': response.choices[0].text}


if __name__ == '__main__':
    executor.start_polling(dp)
