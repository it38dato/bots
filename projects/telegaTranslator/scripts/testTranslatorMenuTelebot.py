import telebot
from telebot import types
from googletrans import Translator
from langdetect import detect
TOKEN='YourToken'
bot = telebot.TeleBot(TOKEN)
translator = Translator()
ru_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
en_letters = "abcdefghijklmnopqrstuvwxyz"
@bot.message_handler(commands=["start"])
def start(message):
    message_user = f"Привет, <b>{message.from_user.first_name.title()}</b>! Я тестовый бот.\n" \
                   f"<b>Выбери программу, которую ты хочешь выполнить:</b>\n" \
                   f"1. Чем полезен данный бот\n" \
                   f"2. Функции бота (что может данный бот)\n" \
                   f"3. Для тех кто хочет поддержать нас и наш проект"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(text="Чем полезен бот ?")
    item2 = types.KeyboardButton(text="Функции бота")
    item3 = types.KeyboardButton(text="Поддержать проект")
    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id, message_user, reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, impact_KEYBORD_bot)
    bot.register_next_step_handler(message, fuctional_KEYBORD_bot)
    bot.register_next_step_handler(message, donat_user_bot)
def impact_KEYBORD_bot(message):
    if message.text == "Чем полезен бот ?":
        message_user = "Этот бот много чем будет полезен для вас. Ознакомьтесь с функционалом бота чтобы понять это." \
                       " В этого бота со временем мы будем внедрять новые фичи и полезные функции. Чтобы узнавать о новых фишках бота, слидите за нашим Telegramm каналом"
        key = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Мое портфолио', url="http://.ru")
        key.add(button)
        bot.send_message(message.from_user.id, message_user, reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(message, fuctional_KEYBORD_bot)
        bot.register_next_step_handler(message, donat_user_bot)
def fuctional_KEYBORD_bot(message):
    if message.text == 'Функции бота':
        message_user = "<b>Добро пожаловать главное меню бота</b>\n\n" \
                       "В скором будущем мы будем добавлять сюда новые функции!"
        key = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button0 = types.KeyboardButton("Переводчик")
        button1 = types.KeyboardButton("Словарь")
        key.add(button0, button1)
        bot.send_message(message.from_user.id, message_user, reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(message, impact_KEYBORD_bot)
        bot.register_next_step_handler(message, donat_user_bot)
        bot.register_next_step_handler(message, translate_message)
        bot.register_next_step_handler(message, dictionary_message)
def donat_user_bot(message):
    if message.text == "Поддержать проект":
        message_users = f"<b>Приветствую  уважаемый {message.from_user.first_name.title()}</b>, вы перешли в отдел поддержки нашего проекта \n\n" \
                        f"Мы будем благодарны любой поддержки от вас. И также благодарим, что вы пользуетесь нашим ботом - это главная ваша поддержка для нас!\n\n" \
                        f"Мы принимаем материальную поддержку на:\n" \
                        f"<b>1. Donationalerts</b>\n" \
                        f"<b>2. PAYEER</b>\nномер счёта для пополнения: P1091200672\n" \
                        f"<b>3. QIWI</b>\n" \
                        f"<b>4. Тинькофф банк</b>"
        key = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton(text="Donationalerts", url="https://ССЫЛКА_НА_ДОНАТ")
        button1 = types.InlineKeyboardButton(text="PAYEER", url="https://ССЫЛКА_НА_КОШЕЛЕК")
        button2 = types.InlineKeyboardButton(text="QIWI", url="https://ССЫЛКА_НА_КИВИ")
        button3 = types.InlineKeyboardButton(text="Тинькофф банк", url="https://ССЫЛКА_НА_БАНК")
        key.add(button0, button1, button2, button3)
        bot.send_message(message.from_user.id, message_users, reply_markup=key, parse_mode='html')
        bot.register_next_step_handler(message, impact_KEYBORD_bot)
        bot.register_next_step_handler(message, fuctional_KEYBORD_bot)
@bot.message_handler(content_types=['text'])
def translate_message(message):
    if message.text == 'Переводчик':
        bot.send_message(message.chat.id, 'Напишите сообщения а я переведу его')
        bot.register_next_step_handler(message, translate_message_step_2)
def translate_message_step_2(message):
    cmd3 = message.text
    if cmd3[0].lower() in ru_letters:
        translation = translator.translate(cmd3, src=detect(cmd3), dest='en').text
        bot.send_message(message.chat.id, translation.encode('utf-8', 'replace').decode())
    elif cmd3[0].lower() in en_letters:
        translation = translator.translate(cmd3, src=detect(cmd3), dest='ru').text
        bot.send_message(message.chat.id, translation.encode('utf-8', 'replace').decode())
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
def dictionary_message(message):
    if message.text == 'Словарь':
        bot.send_message(message.chat.id, 'list | term')
        #text = message.text
        #bot.send_message("TEST")
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
