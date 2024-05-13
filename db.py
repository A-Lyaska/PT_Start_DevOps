import logging
import psycopg2
from psycopg2 import Error

logging.basicConfig(
    filename='app.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, encoding="utf-8"
)

connection = None
try:
    connection = psycopg2.connect(user="postgres",
                                  password="Qq12345",
                                  host="192.168.19.163",
                                  port="5432", 
                                  database="mydatabase")

    cursor = connection.cursor()
    cursor.execute("Delete from users where name = 'Сергей';")
    connection.commit()
    cursor.execute("SELECT * FROM users;")
    data = cursor.fetchall()
    for row in data:
        print(row)  
    logging.info("Команда успешно выполнена")
except (Exception, Error) as error:
    logging.error("Ошибка при работе с PostgreSQL: %s", error)
finally:
    if connection is not None:
        cursor.close()
        connection.close()