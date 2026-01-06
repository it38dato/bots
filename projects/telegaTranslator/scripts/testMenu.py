def fun(t1, b, t2, l, t3):
    while True:    
        cmd1 = input("Привет!\nЯ тестовый бот.\nВыбери программу, которую ты хочешь выполнить\n(0, translator, dictionary): ")
        if cmd1 == "0":
            break
        elif cmd1 == t1:
            while True:
                cmd2 = input("Что именно нужно сделать\n(translate, back): ")
                if cmd2 == b:
                    print('Вы вернулись в главное меню')
                    break
                elif cmd2 == t2:
                    print("Здесь программа переведет вам текст")
                else:
                    print("Я такую команду не знаю")
        elif cmd1 == "dictionary":
            while True:
                cmd2 = input("Что именно нужно сделать\n(list,term,back): ")
                if cmd2 == b:
                    print('Вы вернулись в главное меню')
                    break
                elif cmd2 == l:
                    print("Вывести список слов")
                elif cmd2 == t3:
                    print("Выбрать слово их списка")
                else:
                    print("Я такую команду не знаю")
        else:
            print("Я такую команду не знаю")
    return t1
print(fun("translator","back","translate","list","term"))
