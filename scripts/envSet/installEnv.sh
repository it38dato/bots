#!/bin/bash

# Проверяем наличие утилиты jq для парсинга JSON
if ! command -v jq &> /dev/null; then
    echo "Ошибка: утилита 'jq' не найдена. Установите её (например, sudo apt install jq)."
    exit 1
fi

CONFIG_FILE="config.json"

# Проверяем существование файла конфигурации
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Ошибка: Файл конфигурации $CONFIG_FILE не найден!"
    exit 1
fi

# 1. Определяем домашнюю директорию текущего пользователя
USER_HOME=$HOME

# 2. Читаем параметры из config.json с подстановкой значений по умолчанию
PROJECT_NAME=$(jq -r '.project_name // "testProject"' "$CONFIG_FILE")
[ "$PROJECT_NAME" == "null" ] || [ -z "$PROJECT_NAME" ] && PROJECT_NAME="testProject"

PROJECT_PATH=$(jq -r '.project_path // ""' "$CONFIG_FILE")
[ "$PROJECT_PATH" == "null" ] || [ -z "$PROJECT_PATH" ] && PROJECT_PATH="$USER_HOME"

ENV_NAME=$(jq -r '.env_name // "envTestProject"' "$CONFIG_FILE")
[ "$ENV_NAME" == "null" ] || [ -z "$ENV_NAME" ] && ENV_NAME="envTestProject"

ENV_PATH=$(jq -r '.env_path // ""' "$CONFIG_FILE")
[ "$ENV_PATH" == "null" ] || [ -z "$ENV_PATH" ] && ENV_PATH="$USER_HOME"

# Читаем библиотеки (массив преобразуем в строку через пробел)
LIBRARIES=$(jq -r '.libraries | join(" ")' "$CONFIG_FILE")

# Читаем параметры прокси
PROXY=$(jq -r '.proxy // ""' "$CONFIG_FILE")
[ "$PROXY" == "null" ] && PROXY=""

# Полные пути к проекту и окружению
FULL_PROJECT_PATH="$PROJECT_PATH/$PROJECT_NAME"
FULL_ENV_PATH="$ENV_PATH/$ENV_NAME"

echo "=== Запуск настройки Python проекта ==="
echo "Директория проекта: $FULL_PROJECT_PATH"
echo "Директория окружения VENV: $FULL_ENV_PATH"

# 3. Создаем директорию проекта
mkdir -p "$FULL_PROJECT_PATH"

# 4. Создаем виртуальное окружение
python3 -m venv "$FULL_ENV_PATH"

# 5. Активируем виртуальное окружение
source "$FULL_ENV_PATH/bin/activate"

# 6. Обновляем pip внутри окружения
if [ -z "$PROXY" ]; then
    pip install --upgrade pip
else
    pip install --upgrade pip --proxy "$PROXY"
fi

# 7. Установка библиотек
if [ -n "$LIBRARIES" ]; then
    echo "Установка библиотек: $LIBRARIES"
    if [ -z "$PROXY" ]; then
        pip install $LIBRARIES
    else
        echo "Используется прокси: $PROXY"
        pip install $LIBRARIES --proxy "$PROXY"
    fi
else
    echo "Список библиотек пуст. Пропуск установки."
fi

# Создаем базовый файл структуры в проекте
echo "# Project $PROJECT_NAME" > "$FULL_PROJECT_PATH/README.md"
touch "$FULL_PROJECT_PATH/main.py"

echo "=== Настройка успешно завершена! ==="
echo "Для начала работы перейдите в проект: cd $FULL_PROJECT_PATH"
echo "И активируйте окружение: source $FULL_ENV_PATH/bin/activate"

