from CONFIG import *
import asyncio
import logging
import json
import aiogram
from random import *
from aiogram import Bot, types
from aiogram.types import message
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from generate_images import *

with open('key_words.json', 'r') as keywords_json: # импортирование файла json
    keywords = json.load(keywords_json)
    #print(keywords["1891 - 1916"])

logging.basicConfig(level=logging.INFO) # Логирование, чтобы не пропустить важные сообщения
bot = Bot(token=TOKEN) # Объект бота
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) # Обработка команды /start
async def cmd_start(message: types.Message):
    await message.answer(text_hello)

@dp.message_handler() # Обработка полученных параметров
async def da(message: types.Message):
    s = message.text
    req = s.split('\n') # Запись полученных параметров в список
    print(req)
    json_data = ''
    user_data = int(req[0])
    if user_data >= 1891 and user_data <= 1916:
        json_data = '1891 - 1916'
    if user_data >= 1917 and user_data <= 1940:
        json_data = '1917 — 1940'
    if user_data >= 1941 and user_data <= 1945:
        json_data = '1941 — 1945'
    if user_data >= 1946 and user_data <= 1965:
        json_data = '1946 — 1965'
    if user_data >= 1966 and user_data <= 1985:
        json_data = '1966 — 1985'
    if user_data >= 1986 and user_data <= 1992:
        json_data = '1986 — 1992'
    if user_data >= 1993 and user_data <= 2014:
        json_data = '1993 — 2014'

    media = []
    descr_first_city = f'настоящее фото города {req[0]} в {req[1]}'
    descr_second_city = f'настоящее фото города {req[0]} в {req[2]}'
    numb = 2 # счетчик для изображений города отправителя и города получателя
    numb2 = 5  # счетчик для изображений эпохи НЕ ГОРОДОВ
    for i in range(numb):
        if i == 0:
            get_images(1, descr_first_city, i)
        if i == 1:
            get_images(1, descr_second_city, i)
        await bot.send_message(message.chat.id, f'Создано изображений:\n{i + 1} из {numb2}')
    for i in range(numb):
        adres = '/Users/krllggnv/Desktop/images_for_hse_project/my-image' + str(i) + '.jpeg'
        photo = open(adres, 'rb')
        media.append(types.InputMediaPhoto(photo))
    for i in range(2, numb2):
        descr_epoha = keywords[json_data][randint(0, len(keywords[json_data]) - 1)]
        get_images(1, descr_epoha, i)
        print(descr_epoha)
        await bot.send_message(message.chat.id, f'Создано изображений:\n{i + 1} из {numb2}')
    for i in range(2, numb2):
        adres = '/Users/krllggnv/Desktop/images_for_hse_project/my-image' + str(i) + '.jpeg'
        photo = open(adres, 'rb')
        media.append(types.InputMediaPhoto(photo))
    await bot.send_chat_action(message.chat.id,
                               types.ChatActions.UPLOAD_DOCUMENT)  # Устанавливаем action "Uploading a document..."
    await bot.send_media_group(message.chat.id, media=media) # Отправка группы коллекций эпохи


if __name__ == '__main__':
    executor.start_polling(dp)