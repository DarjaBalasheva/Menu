#!/bin/bash

# Копирование alembic.ini в контейнер
cd /app

uvicorn main:app --host 0.0.0.0 --port 8000