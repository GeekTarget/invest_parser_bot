import telebot
import urllib
from yandex_disk import YaDisk
from aiogram import Bot, Dispatcher, executor
from aiogram import types
import config
import logging
from datetime import datetime
import os
import re
from aiogram.dispatcher.filters import Command
import pytz

# Main variable

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.token)
BOT = telebot.TeleBot(config.token)
dp = Dispatcher(bot)
disk = YaDisk()
today = datetime.now().date()
tz = pytz.timezone('Europe/Moscow')
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\u200d"
                           u"\u2640-\u2642"
                           "]+", flags=re.UNICODE)


@dp.message_handler(Command('status'))
async def handle_message(message: types.Message):
    with open('status.txt', 'r') as file:
        date = file.read()[:21]
    await message.answer(f'Бот запущен\nПоследний пост : {date}')


# Обработчик текстовых сообщений
@dp.message_handler()
async def messages(message: types.Message, caption=False, img=False):
    print(message)
    now_time = datetime.now(tz).strftime("%d-%m-%Y %H:%M:%S")
    if caption != False:
        text = '  ' + emoji_pattern.sub(r'', caption) + ' - ' + img
    elif caption == False and img != False:
        text = '  ' + img
    else:
        print(message)
        if message['chat']['type'] == "supergroup":
            if message.text[-1] == ':':
                txt = str(now_time) + ' : ' + emoji_pattern.sub(r'', message['text'])
                text = '\n\n' + txt + '\n'
            else:
                text = '\n\n' + str(now_time) + ' : ' + emoji_pattern.sub(r'', message['text']) + '\n'
        else:
            print(1)
            return False
    try:
        disk.create_folder(True)
        disk.create_folder(False)
        f = open('messages.txt', 'w', encoding="utf-8")
        f.close()
        with open('messages.txt', 'a', encoding="utf-8") as messages_text:
            try:
                messages_text.write(text.encode('cp1251').decode('Windows-1251'))
            except:
                messages_text.write(text)
        with open('status.txt', 'w', encoding="utf-8") as f:
            try:
                f.write(text.encode('cp1251').decode('Windows-1251'))
            except:
                f.write(text)
        disk.add_file('messages.txt')
    except:
        try:
            disk.create_folder(False)
            f = open('messages.txt', 'w',encoding="utf-8")
            f.close()
            with open('messages.txt', 'a',encoding="utf-8") as messages_text:
                try:
                    messages_text.write(text.encode('cp1251').decode('Windows-1251'))
                except:
                    messages_text.write(text)
            with open('status.txt', 'w',encoding="utf-8") as f:
                try:
                    f.write(text.encode('cp1251').decode('Windows-1251'))
                except:
                    f.write(text)
            disk.add_file('messages.txt')
        except:
            try:
                with open('messages.txt', 'a',encoding="utf-8") as messages_text:
                    try:
                        messages_text.write(text.encode('cp1251').decode('Windows-1251'))
                    except:
                        messages_text.write(text)
                with open('status.txt', 'w',encoding="utf-8") as f:
                    try:
                        f.write(text.encode('cp1251').decode('Windows-1251'))
                    except:
                        f.write(text)
                disk.remove_file('messages.txt')
                disk.add_file('messages.txt')
            except:
                with open('messages.txt', 'a',encoding="utf-8") as messages_text:
                    try:
                        messages_text.write(text.encode('cp1251').decode('Windows-1251'))
                    except:
                        messages_text.write(text)
                with open('status.txt', 'w',encoding="utf-8") as f:
                    try:
                        f.write(text.encode('cp1251').decode('Windows-1251'))
                    except:
                        f.write(text)
                disk.add_file('messages.txt')


# Обработчик фотографий
@dp.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    if message['chat']['type'] == 'supergroup':
        document_id = message['photo'][-1].file_id  # id фотографии
        file_info = BOT.get_file(document_id)
        filename, file_extension = os.path.splitext(
            file_info.file_path)  # отделяем формат .jpg фотографии от остального
        global name
        len_file = len(disk.get_len_disk(False))
        if len_file == 0:
            number = len_file + 1
        else:
            number = disk.len_image() + 1
        if len(str(number)) == 1:
            name = '00' + str(number)
        elif len(str(number)) == 2:
            name = '0' + str(number)
        else:
            name = str(number)
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config.token}/{file_info.file_path}',
                                   name + file_extension)  # сохраняем картинку
        try:
            disk.create_folder(True)
            disk.create_folder(False)
            disk.add_file(name + file_extension)
            if message['caption']:
                caption = message['caption']
                messages('1', caption=caption, img=name + file_extension)
            else:
                messages('1', img=name + file_extension)
            os.remove(name + file_extension)
        except:
            try:
                disk.create_folder(False)
                disk.add_file(name + file_extension)
                if message['caption']:
                    caption = message['caption']
                    messages('1', caption=caption, img=name + file_extension)
                else:
                    messages('1', img=name + file_extension)
                os.remove(name + file_extension)
            except:
                disk.add_file(name + file_extension)
                if message['caption']:
                    caption = message['caption']
                    messages('1', caption=caption, img=name + file_extension)
                else:
                    messages('1', img=name + file_extension)
                os.remove(name + file_extension)


# Обработчик документов
@dp.message_handler(content_types=['document'])
def handle_documents(message):
    if message['chat']['type'] == 'supergroup':
        file_name = message["document"].file_name.split('.')
        document_id = message["document"].file_id
        file_info = BOT.get_file(document_id)
        filename, file_extension = os.path.splitext(file_info.file_path)
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{config.token}/{file_info.file_path}',
                                   file_name[0] + file_extension)
        try:
            disk.create_folder(True)
            disk.create_folder(False)
            disk.add_file(file_name[0] + file_extension)
            messages('1', img=file_name[0] + file_extension)
            os.remove(file_name[0] + file_extension)
        except:
            try:
                disk.create_folder(False)
                disk.add_file(file_name[0] + file_extension)
                messages('1', img=file_name[0] + file_extension)
                os.remove(file_name[0] + file_extension)
            except:
                disk.add_file(file_name[0] + file_extension)
                messages('1', img=file_name[0] + file_extension)
                os.remove(file_name[0] + file_extension)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
