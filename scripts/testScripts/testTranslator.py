from googletrans import Translator
from langdetect import detect
translator = Translator()
ru_letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
en_letters = "abcdefghijklmnopqrstuvwxyz"
cmd3 = input("Введите текст, который вы хотите перевести: ")
if cmd3[0].lower() in ru_letters:
    translation = translator.translate(cmd3, src=detect(cmd3), dest='en').text
    print(translation.encode('utf-8', 'replace').decode())
elif cmd3[0].lower() in en_letters:
    translation = translator.translate(cmd3, src=detect(cmd3), dest='ru').text
    print(translation.encode('utf-8', 'replace').decode())
else:
    print('Я тебя не понимаю')