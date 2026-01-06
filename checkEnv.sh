#!/bin/bash

# Проверяем наличие файла variables.txt
if [ -f "variables.txt" ]; then
    # Используем 'source' для чтения переменных из файла в текущую оболочку
    source variables.txt

    # Удаляем символ возврата каретки '\r' из переменной VENV_NAME
    VENV_NAME=$(echo "$VENV_NAME" | tr -d '\r')
    # Также можно удалить из других переменных, если они есть
    REQUIREMENTS_FILE=$(echo "$REQUIREMENTS_FILE" | tr -d '\r')

else
    echo "Ошибка: Файл variables.txt не найден!"
    exit 1
fi
# Теперь переменные VENV_NAME и REQUIREMENTS_FILE доступны
echo "Значение VENV_NAME: $VENV_NAME"
echo "Значение REQUIREMENTS_FILE: $REQUIREMENTS_FILE"

# Полный путь к виртуальному окружению (в домашней директории)
VENV_PATH="$HOME/$VENV_NAME"
echo "Создание виртуального окружения в $VENV_PATH..."
# Создание виртуального окружения
python3 -m venv "$VENV_PATH"
# Проверка успешности создания
if [ $? -ne 0 ]; then
    echo "Ошибка при создании виртуального окружения. Убедитесь, что python3 и модуль venv установлены."
    exit 1
fi
echo "Активация виртуального окружения..."
# Активация окружения в текущем процессе скрипта
source "$VENV_PATH/bin/activate"
# Проверка успешности активации
if [ $? -ne 0 ]; then
    echo "Ошибка при активации. Возможно, путь $VENV_PATH/bin/activate неверен."
    exit 1
fi
echo "Виртуальное окружение активировано. Запуск pip install..."
# Запуск pip install 
# Пока окружение активно, pip будет устанавливать пакеты в него, а не глобально
pip install -r "$REQUIREMENTS_FILE"
echo "Установка пакетов завершена. Список доступных библиотек в виртуальном окружении $VENV_PATH:"
pip list
echo "Интерпретатор Python:"
which python
echo "Примечание: после завершения этого скрипта окружение будет деактивировано в вашей основной консоли, так как изменения окружения изолированы внутри скрипта."
