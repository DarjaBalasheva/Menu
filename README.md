# Проект на FastAPI с использованием PostgreSQL в качестве БД
<img src="https://github.com/DarjaBalasheva/fullstack-ivkhk/actions/workflows/my_workflow.yml/badge.svg">

Этот проект является учебным в рамках прохождения курсов в YLab_University.


## Требования
- Git
- Docker
- Docker-compose
- Python
- Pipenv
- PostgreSQL

## Установка на mac os
- [Установка Python](https://www.python.org/downloads/macos/)
- [Установка Docker](https://www.docker.com/get-started/)
- Установите Git, если он ещё не установлен с помощью Homebrew.
  - Установка Homebrew
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - Установка GIT
    ```bash
    brew install git
    
  - Установка репозиторий homebrew/core, который содержит PostgreSQL
    ```bash
    brew tap homebrew/core
    ```
  - Установка PostgreSQL
    ```bash
    brew install postgresql
    ```
- Клонирование репозитория.
```bash
git clone git@github.com:DarjaBalasheva/Menu.git
cd Menu
```

- Установка библиотеки зависимостей
```bash
pip pipenv install
```
## Настройка
### Настройка env файла
Перед запуском проекта необходимо настроить переменные окружения.
Переименуйте файл .env.example в .env

- Активация виртуального окружение pipenv
```bash
pipenv shell
```

## Запуск проекта
Запустите Docker-контейнеры с помощью docker-compose. Это моет занять некоторе время. Дождитесь, пока в консоле не появится соотвествующая информация о готовности работы БД.
```bash
docker-compose up 
```
Запустите скрипт создания БД
```bash
python3  db_create.py
```
Запустите FastAPI
```bash
uvicorn main:app --reload
```
После успешного запуска контейнеров вы сможете получить доступ к веб-приложению FastAPI по адресу http://localhost:8000.

## Лицензия
Этот проект лицензирован по лицензии MIT.
 
