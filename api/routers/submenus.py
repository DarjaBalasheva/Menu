from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache
from sqlalchemy.orm import sessionmaker

from api.db.db_create import engine

from ..db import db_connect
from ..db.redis_connect import connect_to_redis
from ..servises import submenus_services

router = APIRouter()
connection = db_connect.connect()

# Создание подключения к Redis
redis_client = connect_to_redis()

# Добавление подменю в таблицу


@router.post('/api/v1/menus/{target_menu_id}/submenus', status_code=201)
async def create_submenu_handler(request: Request, target_menu_id: str):
    # Очистка всего кэша
    redis_client.flushall()

    Session = sessionmaker(bind=engine)
    session = Session()

    data = await request.json()

    try:
        new_submenu = submenus_services.create_submenu(session, target_menu_id, data)
        session.close()
        return new_submenu

    except Exception as e:
        session.close()
        error_msg = str(e)
        return {'error': error_msg}


@router.get('/api/v1/menus/{target_menu_id}/submenus')
@cache(expire=60)
async def show_all_submenus_handler(target_menu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        all_submenus = submenus_services.show_all_submenus(session, target_menu_id)
        session.close()
        return all_submenus

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
@cache(expire=60)
async def show_submenu(target_menu_id: str, target_submenu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        submenu = submenus_services.show_submenu_by_id(
            session, target_menu_id, target_submenu_id
        )
        session.close()
        return submenu
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def update_submenu_handler(
    request: Request, target_menu_id: str, target_submenu_id: str
):
    # Очистка всего кэша
    redis_client.flushall()

    Session = sessionmaker(bind=engine)
    session = Session()
    data = await request.json()
    try:
        submenu = submenus_services.update_submenu_by_id(
            session, target_menu_id, target_submenu_id, data
        )
        session.close()

        return submenu
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def delete_submenu(target_menu_id: str, target_submenu_id: str):
    # Очистка всего кэша
    redis_client.flushall()

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        success = submenus_services.delete_submenu_by_id(
            session, target_menu_id, target_submenu_id
        )
        session.close()
        return success
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}
