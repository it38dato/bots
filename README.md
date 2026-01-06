<p>
    <strong>Task:</strong><br>
    Разработать Телеграм-бот для перевода слов и фраз на разные языки.&nbsp;<br>
    - Определение языка текста<br>
    - Перевод слов и предложений&nbsp;<br>
    - Обработка ошибок (некорректный ввод, ошибки API)&nbsp;<br>
    - Логирование действий пользователя&nbsp;<br>
    - Контейнеризация через Docker<br>
    <strong>Decision:</strong><br>
    Работаю в системе Ubuntu.&nbsp;<br>
    Для запуска проекта использую скрипты:<br>
    - checkPython.sh - проверяет версию Python и устанавливает Python в зависимости от дистрибутива Linux.<br>
    - checkEnv.sh - при необоходимости устанавливает переменную окружения и устанавливает библиотеки, которые зависят от проекта.<br>
    - startPyProjects.sh - для запуска проекта.<br>
    - dato38itbot.service &nbsp;- для настройки службы запуска бота<br>
    - startService.sh - Для запуска бота<br>
    - stopService.sh - Для остановки бота<br>
    основные команды для работы с проектом:<br>
    - chmod +x yourFile.sh<br>
    - pwd<br>
    - ./yourFile.sh<br>
    - python3 yourFile.py<br>
    - source envTelegaTranslator/bin/activate<br>
    основной скрипт "main.py". Запустить его можно скриптом "startPyProjects.sh" заменив параметры.<br>
    скрипты "yourFile.sh" запускаются с правами на исполнение. "executeFile.sh" дает права на исполнение файлов". Скрипт запросит путь к файлу, которому нужно дать права.&nbsp;<br>
    в файле "variables.txt" находятся переменные, которые используются в скриптах. в файле нужно вносить изменения. в VENV_NAME нужно добавить имя виртуального окружения. в REQUIREMENTS_FILE нужно добавить имя файла требований (по умолчанию это названия библиотек будет в файле "requirements.txt"). в START_PROJECT нужно добавить имя файла проекта с раширением .py, который вы запускаете.&nbsp;<br>
    в файле "requirements.txt" находятся библиотеки, которые зависят от проекта. файл должен находиться рядом со скриптом "checkEnv.sh".<br>
    Подключение к БД, ключи от токена и id админки telegram бота будет хранится в .env. для запуска бота необоходимо заполнить свои данные<br>
    файл dato38itbot.service должен находится в директории /etc/systemd/system/. Запустить службу можно скриптом startService.sh. остановить stopService.sh. В файлах нужно заменить параметры.&nbsp;<br>
    В файлах начинающихся с test*.py проекты, которые выполнялись пошагово для создания программы:<br>
    1. написать консольное меню, которое будет предлагать какие действия нужно выполнить. Для запуска проекта использую скрипт в терминале "testMenu.py"<br>
    2. написать скрипт, в котором бот будет переводить слова - с английского на русский и с русского на английский. Для запуска проекта использую скрипт в терминале "testTranslator.py"<br>
    3. написать консольное меню, в котором бот будет переводить слова с русского на английский. Для запуска проекта использую скрипт в терминале "testMenuTranslator.py". Добавил возможность в функцию меню, переводить с русского на английский язык. в момент запуска в меню нужно выбрать translator - translate и написать текст на русском, который нужно перевести.<br>
    4. Написать телеграм бот с меню кнопками<br>
    В файле testTranslatorMenuTelebot.py необоходимо заменить TOKEN. в командной строке выполнить запрос через python "testTranslatorMenuTelebot.py":<br>
    source envTelegaTranslator/bin/activate<br>
    python3 testTranslatorMenuTelebot.py<br>
    В телеграмме уже будет активна кнопка переводчик. тот же функционал выполняет, что и скрипт "testMenuTranslator.py" - Уже будет переводить слова и предложения.<br>
    5. Необходимо настроить БД PostgreSql и сделать таким образом, чтобы бот отображал информацию из БД. провести миграцию БД с локального тестового сервера в облачный вируальный сервер.<br>
    Все процедуры с БД выполняются в терминале.<br>
    Таблицы БД будут такими:<br>
    Разработать&nbsp;<br>
    Словарь<br>
    id | words | translate<br>
    1 | Текст1 | Text1<br>
    2 | Текст2 | Text2<br>
    3 | Текст3 | Text3<br>
    Термины<br>
    id | words_id | description | translate<br>
    1 | 1 | Текст4 | Text4<br>
    2 | 3 | Текст5 | Text5<br>
    - Настроить БД можно следующим командами:<br>
    createdb YourNameDB<br>
    psql -U YourUser -d YourNameDB -h YourIP<br>
    GRANT ALL PRIVILEGES ON DATABASE YourNameDB to YourUser;<br>
    ALTER DATABASE YourNameDB OWNER TO YourUser;<br>
    \l+<br>
    cat /etc/postgresql/14/main/pg_hba.conf<br>
    ...<br>
    host YourNameDB YourUser YourIP/24 md5<br>
    systemctl restart postgresql<br>
    - Создать таблицы в БД:<br>
    psql -U YourUser -d YourNameDB -h YourIP<br>
    CREATE TABLE dictionary (<br>
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,<br>
    words VARCHAR(1000),<br>
    translate VARCHAR(1000)<br>
    );<br>
    CREATE TABLE Terms (<br>
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,<br>
    words_id INT,<br>
    description VARCHAR(1000),<br>
    translate VARCHAR(1000),<br>
    CONSTRAINT fk_YourNameDB<br>
    FOREIGN KEY(words_id)<br>
    REFERENCES dictionary(id)<br>
    );<br>
    INSERT INTO dictionary (words, translate)<br>
    VALUES ('Текст1', 'Text1'), ('Текст2', 'Text2'), ('Текст3', 'Text3');<br>
    INSERT INTO Terms (words_id, description, translate)<br>
    VALUES (1, 'Текст4', 'Text4'), (3, 'Текст5','Text5');<br>
    - выполнить запрос:<br>
    select words, dictionary.translate, description, Terms.translate<br>
    from dictionary<br>
    inner join Terms<br>
    on dictionary.id = Terms.words_id;<br>
    - Миграция базы с одного сервера на другой:<br>
    pg_dump -Fc -v --username=YourUser --dbname=YourNameDB -f datapsql2.dump<br>
    scp datapsql2.dump YourUser@YourIP:/home/YourUser/<br>
    pg_restore -v --no-owner --port=5432 --username=YourUser --dbname=YourNameDB datapsql2.dump<br>
    - в командной строке выполнить запрос через python "testSelectPsql.py":<br>
    source envTelegaTranslator/bin/activate<br>
    python3 testSelectPsql.py<br>
    6. написать функцию в боте, что пользователь мог добавлять информацию в БД через телеграм.<br>
    в командной строке выполнить запрос через python "testPsqlTelebot.py":<br>
    source envTelegaTranslator/bin/activate<br>
    python3 testPsqlTelebot.py<br>
    проверить что добавилиьс можно в телеграме, а можно и в БД выполни в запрос:<br>
    select * from Dictionary;<br>
    в Файле нужно заменить параметры БД и ключи токена.
</p>