#!/bin/bash

# Проверяем наличие файла variables.txt
if [ -f "variables.txt" ]; then
    # Используем 'source' для чтения переменных из файла в текущую оболочку
    source variables.txt
    # Удаляем символ возврата каретки '\r' из переменной VENV_NAME
    VENV_NAME=$(echo "$VENV_NAME" | tr -d '\r')
else
    echo "Ошибка: Файл variables.txt не найден!"
    exit 1
fi
# Теперь переменные VENV_NAME доступны
echo "Значение VENV_NAME: $VENV_NAME"
# Полный путь к виртуальному окружению (в домашней директории)
VENV_PATH="$HOME/$VENV_NAME"
echo "Активация виртуального окружения..."
# Активация окружения в текущем процессе скрипта
source "$VENV_PATH/bin/activate"
# Проверка успешности активации
if [ $? -ne 0 ]; then
    echo "Ошибка при активации. Возможно, путь $VENV_PATH/bin/activate неверен."
    exit 1
fi
echo "Виртуальное окружение активировано. Список доступных библиотек в виртуальном окружении $VENV_PATH:"
pip list
echo "Запуск проекта $START_PROJECT:"
START_PROJECT=$(echo "$START_PROJECT" | tr -d '\r')
python3 "$START_PROJECT"
echo "Примечание: после завершения этого скрипта окружение будет деактивировано в вашей основной консоли, так как изменения окружения изолированы внутри скрипта."
