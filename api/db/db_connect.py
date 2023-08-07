import psycopg2
from psycopg2 import OperationalError
from os import environ
from dotenv import load_dotenv
import time

load_dotenv()


def connect():
    while True:
        try:
            connection = psycopg2.connect(
                host=environ["db_host"],
                user=environ["db_user_login"],
                password=environ["db_user_password"],
                dbname=environ["db_name"],
            )

            if connection:
                print("Успешное подключение к базе данных PostgreSQL")
                return connection
        except OperationalError as e:
            print(f"Ошибка подключения к базе данных PostgreSQL: {e}")

            # Ждем перед следующей попыткой подключения
            time.sleep(5)
