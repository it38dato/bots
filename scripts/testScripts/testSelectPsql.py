import psycopg2
from contextlib import closing

with closing(psycopg2.connect(dbname='YourNameDB', user='YourUser', password='YourPassword', host='YourIP')) as conn:
    with conn.cursor() as cursor:
        cursor.execute('select words, Dictionary.translate, description, Terms.translate from Dictionary inner join Terms on Dictionary.id = Terms.words_id')
        for row in cursor:
            print(row)

