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
- Установите Git  и PostgreSQL, если они ещё не установлены с помощью Homebrew.
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
- Установка библиотеки зависимостей
```bash
pip pipenv install
```


## Настройка
- Клонирование репозитория.

```bash
git clone git@github.com:DarjaBalasheva/Menu.git
cd Menu
```

### Настройка env файла
В качестве примера уже присутсвует файл .env.deploy для запуска докеров. Дополнительной настройки не требуется

## Запуск проекта
Запустите Docker-контейнеры с помощью docker-compose. Это моет занять некоторе время. Дождитесь, пока в консоле не появится соотвествующая информация о готовности работы БД и fastapi. Docker-compose настроен таким образом, что тесты будут запускаться сразу после поднятия fastapi.

```bash
docker-compose up
```

или

```bash
docker-compose up -d
```

Вы также можете отдельно запустить тесты использовав команду

```bash
docker-compose up tests15
```

## Лицензия
Этот проект лицензирован по лицензии MIT.
 
