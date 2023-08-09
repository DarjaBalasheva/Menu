from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache
from sqlalchemy.orm import sessionmaker

from api.db.db_create import engine

from ..db import db_connect
from ..db.redis_connect import connect_to_redis
from ..servises import dishes_servises

router = APIRouter()

# Подключение к БД
connection = db_connect.connect()

# Создание подключения к Redis
redis_client = connect_to_redis()


@router.post(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    status_code=201,
)
async def create_dish_handler(request: Request, target_menu_id: str, target_submenu_id: str):
    # Очистка всего кэша
    redis_client.flushall()

    data = await request.json()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        new_dish = dishes_servises.create_dishes(session, target_menu_id, target_submenu_id, data)
        session.close()
        return new_dish
    except Exception as e:
        session.close()
        error_msg = str(e)
        return {'error': error_msg}


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
@cache(expire=60)
async def show_all_dishes(target_menu_id: str, target_submenu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:

        dishes = dishes_servises.show_all_dishes(session, target_menu_id, target_submenu_id)

        session.close()

        return dishes

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
@cache(expire=60)
async def show_dish(target_menu_id: str, target_submenu_id, target_dish_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        dish = dishes_servises.show_dish_by_id(session, target_menu_id, target_submenu_id, target_dish_id)
        session.close()
        return dish

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def update_dish(request: Request, target_menu_id: str, target_submenu_id: str, target_dish_id: str):
    # Очистка всего кэша
    redis_client.flushall()

    data = await request.json()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        update_dish = dishes_servises.update_dish_by_id(
            session, target_menu_id, target_submenu_id, target_dish_id, data)
        session.close()
        return update_dish
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def delete_dish(target_menu_id: str, target_submenu_id: str, target_dish_id: str):
    # Очистка всего кэша
    redis_client.flushall()

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        success = dishes_servises.delete_dish_by_id(session, target_menu_id, target_submenu_id, target_dish_id)
        session.close()
        return success
    except Exception as e:
        error_msg = str(e)
        return {'error': error_msg}
