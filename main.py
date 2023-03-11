import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from settings import API_KEY, BOT_KEY


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
  bot.send_message(message.chat.id, f"""This bot has two models. Currently using the {current_model} model.
  
  dav3 is a weaker language model. She also doesn't remember dialogue. gpt3.5 is the model currently used in ChatGPT. Also, this model remembers the dialogue, which makes it an indispensable assistant.
  
  To change the model type /mode followed by gpt3.5 or dav3
  
  For dev3, there is a temperature setting (/temp) from 0 to 1. The higher the temperature, the less formal text the model produces. If the value is high, there may be factual errors!""")


@dp.message_handler(commands=['start'])
def help(message):
  bot.send_message(message.chat.id, f"""I am AI Bot Developed By @NitinSahay for private use Only""")



messages = [{"role": "system", "content": "You are a helpful assistant."},]

@dp.message_handler(func=lambda _:True)
def handle_message(message):
  if current_model == 'gpt3.5':
    message_dict = {"role": "user", "content": message.text }
    messages.append(message_dict)
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo", 
      messages=messages
    )
    reply = response.choices[0].message.content #response['choices'][0]['text']
    bot.send_message(chat_id=message.from_user.id,text=reply)
    messages.append({"role": "assistant", "content": reply})
  elif current_model == 'dav3':
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=message.text, 
    temperature=temp,       
    max_tokens=1000,       
    top_p=1,                
    frequency_penalty=0.0,  
    presence_penalty=0.6,   
    stop=[" Human:", " AI:"]
  )
    reply = response['choices'][0]['text']
    bot.send_message(chat_id=message.from_user.id,text=reply)


if __name__ == '__main__':
    executor.start_polling(dp)
