import psycopg2
import telebot
from telebot import types
from telebot.types import Message
TOKEN='YourKey'
bot = telebot.TeleBot(TOKEN)
DATABASE_URL = "postgres://YourUser:YourPassword@YourIP:5432/YourNameDB"
def connect_to_db():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn
def insert_data(words, translate):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "INSERT INTO Dictionary (words, translate) VALUES (%s, %s)"
    cursor.execute(query, (words, translate))
    conn.commit()
    cursor.close()
    conn.close()
@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    words = "Текст4"
    translate = "Text4"
    insert_data(words, translate)
    bot.reply_to(message, "Add Info in Doctionary.")
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)