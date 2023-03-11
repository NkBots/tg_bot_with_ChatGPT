import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from settings import API_KEY, BOT_KEY

# Логгирование
logging.basicConfig(level=logging.INFO)

# Устанавливаем API_KEY для OpenAI
openai.api_key = API_KEY

# Токен для Telegram бота
bot = Bot(token=BOT_KEY)

# Диспетчер
dp = Dispatcher(bot)

# История сообщений
contex_history = {}

# Модель обработки данных в ChatGPT
model = 'text-davinci-003'


# Хэндлер на команду /start
@dp.message_handler(commands=['start'])
async def start(message):
    if message['language_code'] == 'en':
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Привет {message.from_user.first_name}. Я отвечу практически на любой твой вопрос. Что ты хочешь узнать?'
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'Hello {message.from_user.first_name}. I will answer almost any of your questions. What do you want to know?'
        )


@dp.message_handler(lambda message: True)
async def handle_message(message):
    # id пользователя
    user_id = message.chat.id

    # Сообщение при повторной отправке запроса
    spam = 'Не надо спамить, просто немного подожди. Запрос обрабатывается...' \
        if message.from_user.language_code == 'en' \
        else 'Don`t spam, just relax and wait...'

    # Проверяем есть были ли сообщения от пользователя
    if contex_history.get(user_id) == None:

        # Запрос данных и добавление сообщения в историю
        response = await generate_response(message.text)

        # Сохраняем в историю текст сообщения и дату запроса
        contex_history[user_id] = [message.text]
    else:

        contex_history[user_id] += [message.text]
        len_history = len(contex_history[user_id])

        # Проверяем на спам - повторная отправка сообщения
        if len_history > 1:

            # Проверяем, что в прошлый раз не было такого же сообщения
            if contex_history[user_id][-1].lower().strip() == contex_history[user_id][-2].lower().strip():
                del contex_history[user_id][-1]
                await bot.send_message(chat_id=user_id, reply_to_message_id=message.message_id, text=spam)
                return

                # Проверяем, что в истории не более 10 сообщений, если больше, то удаляем самое старое
        if len(contex_history[user_id]) > 9:
            del contex_history[user_id][0]

        # Получаем ответ
        response = await generate_response(message.text + ' ' + '\n'.join(contex_history.get(user_id)))

    if response['text']:
        await bot.send_message(chat_id=user_id, reply_to_message_id=message.message_id, text=response['text'])


# Генерируем ответ на основе входящего текста и текущего контекста диалога
async def generate_response(text):
    prompt = f"{text}"
    max_tokens = 1024
    # Запрос
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )
    return {'text': response.choices[0].text}


if __name__ == '__main__':
    executor.start_polling(dp)
