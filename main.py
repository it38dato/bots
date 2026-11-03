import psycopg2
import telebot
from telebot import types
from telebot.types import Message
from googletrans import Translator
from langdetect import detect
from decouple import config
from contextlib import closing
bot = telebot.TeleBot(config('TOKEN'))
translator = Translator()
ru_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
en_letters = "abcdefghijklmnopqrstuvwxyz"
DATABASE_URL = config('DB_URL')
def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn
def insert_dictionary(words, translate):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO Dictionary (words, translate) VALUES (%s, %s)"
    cursor.execute(query, (words, translate))
    conn.commit()
    cursor.close()
    conn.close()
def insert_terms(words_id, description, translate):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO Terms (words_id, description, translate) VALUES (%s, %s, %s)"
    cursor.execute(query, (words_id, description, translate))
    conn.commit()
    cursor.close()
    conn.close()
def insert_giude(ru, ge, tge, en, ten, content):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO guide (ru, ge, tge, en, ten, content) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (ru, ge, tge, en, ten, content))
    conn.commit()
    cursor.close()
    conn.close()
def select_guide(ru, message):
    if message.text == ru:
        with closing(connect_to_db()) as conn:
            with conn.cursor() as cursor:
                #cursor.execute(f"select * from guide where ru='{ru}';")
                cursor.execute(f"select * from guide where ru like '%{ru}%';")
                for row in cursor:
                    #print(row[1])
                    bot.send_message(message.chat.id, " | "+str(row[0])+" | "+row[1]+" | "+row[2]+" | "+row[3]+" | "+row[4]+" | "+row[5]+" | "+row[6]+" | ")
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
@bot.message_handler(commands=['start'])
def start(message):
    message_user = f"Привет, <b>{message.from_user.first_name.title()}</b>! Я тестовый бот.\n" \
                   f"1. Чем полезен бот\n" \
                   f"2. Для тех кто хочет поддержать проект"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton(text="Чем полезен бот ?")
    but2 = types.KeyboardButton(text="Поддержать проект")
    markup.add(but1, but2)
    bot.send_message(message.from_user.id, message_user, reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, funcs_bot)
    bot.register_next_step_handler(message, donat_bot)
def funcs_bot(message):
    if message.text == "Чем полезен бот ?":
        message_user = "Функции бота:\n" \
                        "1. Переводчик\n" \
                        "2. Дополнить словарь\n" \
                        "3. Словарь\n" \
                        "4. Термины\n" \
                        "5. Дополнить описание\n" \
                        "6. Справочник\n" \
                        "7. Дополнить справочник\n" \
                        "8. Вывести значение из справочника"
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #button = types.InlineKeyboardButton(text='Мое портфолио', url="http://dato138it.ru")
        but1 = types.KeyboardButton("Переводчик")
        but2 = types.KeyboardButton("Дополнить словарь")
        but3 = types.KeyboardButton("Словарь")
        but4 = types.KeyboardButton("Термины")
        but5 = types.KeyboardButton("Дополнить описание")
        but6 = types.KeyboardButton("Справочник")
        but7 = types.KeyboardButton("Дополнить справочник")
        but8 = types.KeyboardButton("Вывести значение из справочника")
        key.add(but1, but2, but3, but4, but5, but6, but7, but8)
        bot.send_message(message.from_user.id, message_user, reply_markup=key, parse_mode='html')
        #bot.register_next_step_handler(message, funcs_mess)
def donat_bot(message):
    if message.text == "Поддержать проект":
        message_users = f"<b>Приветствую, уважаемый {message.from_user.first_name.title()}</b>, вы перешли в отдел поддержки нашего проекта\n" \
                        f"Мы будем благодарны материальной поддержки от вас на:\n" \
                        f"<b>1. ЮMoney</b>\n" \
                        f"<b>2. Альфа банк</b>"
        key = types.InlineKeyboardMarkup()
        but1 = types.InlineKeyboardButton(text="ЮMoney", url="http://dato138it.ru")
        but2 = types.InlineKeyboardButton(text="Альфа банк", url="http://dato138it.ru")
        key.add(but1, but2)
        bot.send_message(message.from_user.id, message_users, reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(message, funcs_bot)
@bot.message_handler(content_types=['text'])
def funcs_mess(message):
    if message.text == 'Переводчик':
        bot.send_message(message.chat.id, 'Напишите сообщение, которое нужно перевести:')
        bot.register_next_step_handler(message, translator_mess)
    elif message.text == 'Дополнить словарь':
        if message.from_user.id == int(config('ADMIN_ID')):
            bot.send_message(message.chat.id, 'Напишите 2 сообщения (предложение и его перевод), которые нужно добавить в словарь:')
            bot.register_next_step_handler(message, AddDictionary_mess1)
        else:
            bot.send_message(message.chat.id, 'У вас нет прав на добавление и удаление предложений из базы')
    elif message.text == 'Дополнить описание':
        if message.from_user.id == int(config('ADMIN_ID')):
            bot.send_message(message.chat.id, 'Напишите 3 сообщения (id - в словаре можно увидеть id, описание и его перевод), которые нужно добавить в словарь:')
            bot.register_next_step_handler(message, AddTerms_mess1)
        else:
            bot.send_message(message.chat.id, 'У вас нет прав на добавление и удаление предложений из базы')
    elif message.text == 'Словарь':
        bot.send_message(message.chat.id, 'Вывожу список слов:')
        #bot.register_next_step_handler(message, dictionary_mess)
        with closing(connect_to_db()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from Dictionary;')
                for row in cursor:
                    bot.send_message(message.chat.id, "| "+str(row[0])+" | "+row[1]+" | "+row[2]+" |")
        bot.reply_to(message, "Selected to the dictionary.")
    elif message.text == 'Термины':
        bot.send_message(message.chat.id, 'Вывожу список терминов:')
        with closing(connect_to_db()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select words, Dictionary.translate, description, Terms.translate from Dictionary inner join Terms on Dictionary.id = Terms.words_id;')
                for row in cursor:
                    bot.send_message(message.chat.id, " | "+str(row[0])+" | "+row[1]+" | "+row[2]+" | "+row[3]+" | ")
        bot.reply_to(message, "Selected to the terms.")
    elif message.text == 'Справочник':
        bot.send_message(message.chat.id, 'Вывожу Справочник:')
        with closing(connect_to_db()) as conn:
            with conn.cursor() as cursor:
                cursor.execute('select * from guide;')
                for row in cursor:
                    bot.send_message(message.chat.id, " | "+str(row[0])+" | "+row[1]+" | "+row[2]+" | "+row[3]+" | "+row[4]+" | "+row[5]+" | "+row[6]+" | ")
        bot.reply_to(message, "Selected to the guide.") 
    elif message.text == 'Дополнить справочник':
        if message.from_user.id == int(config('ADMIN_ID')):
            bot.send_message(message.chat.id, 'Напишите 6 сообщений (1 - слово / предложение на русском языке, 2 - на грузинском, 3 - его транскрипция, 4 - на английском, 5 - его транскрипция, 6 - описание), которые нужно добавить в справочник. В случае если нету значений, необходимо добавить "-".')
            bot.register_next_step_handler(message, AddGuide_mess1)
        else:
            bot.send_message(message.chat.id, 'У вас нет прав на добавление и удаление предложений из базы')
    elif message.text == 'Вывести значение из справочника':
        if message.from_user.id == int(config('ADMIN_ID')):
            bot.send_message(message.chat.id, 'Напишите 1 сообщение на русском языке, которое нужно найти в справочнике.')
            bot.register_next_step_handler(message, SelGuide_mess1)
        else:
            bot.send_message(message.chat.id, 'У вас нет прав на добавление и удаление предложений из базы')
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
def translator_mess(message):
    cmd1 = message.text
    if cmd1[0].lower() in ru_letters:
        translation = translator.translate(cmd1, src=detect(cmd1), dest='en').text
        bot.send_message(message.chat.id, translation.encode('utf-8', 'replace').decode())
    elif cmd1[0].lower() in en_letters:
        translation = translator.translate(cmd1, src=detect(cmd1), dest='ru').text
        bot.send_message(message.chat.id, translation.encode('utf-8', 'replace').decode())
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
def AddDictionary_mess1(message):
    global cmd2
    cmd2 = message.text
    bot.register_next_step_handler(message, AddDictionary_mess2)
def AddDictionary_mess2(message):
    global cmd3
    cmd3 = message.text
    insert_dictionary(cmd2, cmd3)
    bot.reply_to(message, "Info added to the dictionary.")
def AddTerms_mess1(message):
    global cmd4
    cmd4 = message.text
    bot.register_next_step_handler(message, AddTerms_mess2)
def AddTerms_mess2(message):
    global cmd5
    cmd5 = message.text
    bot.register_next_step_handler(message, AddTerms_mess3)
def AddTerms_mess3(message):
    global cmd6
    cmd6 = message.text
    insert_terms(cmd4, cmd5, cmd6)
    bot.reply_to(message, "Info added to the terms.")
def AddGuide_mess1(message):
    global cmd7
    cmd7 = message.text
    bot.register_next_step_handler(message, AddGuide_mess2)
def AddGuide_mess2(message):
    global cmd8
    cmd8 = message.text
    bot.register_next_step_handler(message, AddGuide_mess3)
def AddGuide_mess3(message):
    global cmd9
    cmd9 = message.text
    bot.register_next_step_handler(message, AddGuide_mess4)
def AddGuide_mess4(message):
    global cmd10
    cmd10 = message.text
    bot.register_next_step_handler(message, AddGuide_mess5)
def AddGuide_mess5(message):
    global cmd11
    cmd11 = message.text
    bot.register_next_step_handler(message, AddGuide_mess6)
def AddGuide_mess6(message):
    global cmd12
    cmd12 = message.text
    insert_giude(cmd7, cmd8, cmd9, cmd10, cmd11, cmd12)
    bot.reply_to(message, "Info added to the guide.")
def SelGuide_mess1(message):
    global cmd13
    cmd13 = message.text
    select_guide(cmd13, message)
    bot.reply_to(message, "Info selected to the guide.")
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
