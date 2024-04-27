# Проект на FastAPI с использованием PostgreSQL в качестве БД
<img src="https://github.com/DarjaBalasheva/fullstack-ivkhk/actions/workflows/my_workflow.yml/badge.svg">

Pet project was developed on YLab_University course.

## Description project
### Backend
#### FastAPI:
This project is using the FastAPI framework.
FastAPI is using asyng CRUD endpoint.
#### Docker:
Project is using Docker
#### Data Base:
Project is using DB MySQL and sqlAlchemy for creating DB and connecting to DB.
Tables are creating for saving information. Primary and foreign keys are using in tables.
Unique values are creating to avoid dublicates.
#### Pipfile:
Используется для управления зависимостями проекта.
#### Linters и pre-commit:
Linters black, autoflake, flake8 и pre-commit are using.
#### Virtual Environment
Virtual Environment are using to transfer secret data
#### Pytest
For testing project

## Requirements
- Git
- Docker
- Docker-compose
- Python
- Pipenv
- PostgreSQL

## Installing on mac os
- [Installing Python](https://www.python.org/downloads/macos/)
- [Installing Docker](https://www.docker.com/get-started/)
- Install Git and PostgreSQL with Homebrew.
  - Installing Homebrew
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - Installing GIT
    ```bash
    brew install git

  - Installing  homebrew/core with PostgreSQL
    ```bash
    brew tap homebrew/core
    ```
  - Installing PostgreSQL
    ```bash
    brew install postgresql
    ```
- Installing libraries
```bash
pip pipenv install
```


## Setting
- Cloning repository.

```bash
git clone git@github.com:DarjaBalasheva/Menu.git
cd Menu
```

### Setting env file
Project is having .env.deploy file for example. Change to your values.

## Start project
Run docker-compose. It can take some time. Docker-compose is configuring in such a way that tests will be launched immediately after fastapi is raised.

```bash
docker-compose up
```

or

```bash
docker-compose up -d
```
To run tests separately

```bash
docker-compose up tests15
```

## License
This priject are using license MIT.
