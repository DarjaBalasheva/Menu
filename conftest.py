import pytest
import httpx
import uuid

import pytest_asyncio

from db_create import engine, Menu, Base

BASE_URL = "http://api_server:8000/api/v1/menus"

import pytest_asyncio

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from dotenv import load_dotenv
import os

# Load environment variables from .env
# load_dotenv()
#
# USERNAME = os.environ.get("db_user_login")
# PASSWORD = os.environ.get("db_user_password")
# DBNAME = os.environ.get("db_name")
# HOST = os.environ.get("db_host")  # Use the container hostname
#
# # Create the engine using the container hostname
# TEST_DB_URL = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}", echo=True)
# Фикстура для создания httpx.AsyncClient
@pytest_asyncio.fixture
@pytest.mark.asyncio
async def api_client():
    async with httpx.AsyncClient() as client:
        yield client

# Фикстура для создания меню
@pytest_asyncio.fixture
@pytest.mark.asyncio
async def created_menu_id(api_client):
    data = {
        "title": "Тестовое меню",
        "description": "Это тестовое меню.",
    }
    response = await api_client.post(BASE_URL, json=data)
    assert response.status_code == 201
    menu_id = response.json()["id"]
    yield menu_id
    # Удаляем меню после завершения теста
    await api_client.delete(f"{BASE_URL}/{menu_id}")

# Фикстура для создания подменю
@pytest.fixture
@pytest.mark.asyncio
async def created_submenu(api_client, created_menu_id):
    data = {
        "title": "Тестовое подменю",
        "description": "Это тестовое подменю.",
    }
    response = await api_client.post(f"{BASE_URL}/{created_menu_id}/submenus", json=data)
    assert response.status_code == 201
    data = response.json()
    submenu_id = data["id"]
    return submenu_id

from sqlalchemy.orm import Session
