# Установка базового образа Python
FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

# Установка postgresql и его разработческих заголовков
RUN apt update && apt install -y gnupg2 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7FCC7D46ACCC4CF8 && apt update && apt install -y libpq-dev postgresql-server-dev-15

# Установка зависимостей для компиляции пакетов
RUN apt-get update && apt-get install -y build-essential

# Установка pipenv
RUN pip install pipenv

# Копирование кода приложения
COPY . .

# Установка зависимостей с помощью pipenv
RUN pipenv lock && pipenv install --system --deploy

RUN chmod a+x docker/*.sh
# Запуск приложения FastAPI
#CMD uvicorn main:app --host 0.0.0.0 --port 8000
