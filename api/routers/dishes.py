import uuid

from fastapi import APIRouter, Request
from sqlalchemy import true
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from api.db.db_create import Dish, Menu, Submenu, engine

from ..db import db_connect

router = APIRouter()

# Подключение к БД
connection = db_connect.connect()


@router.post(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    status_code=201,
)
async def create_dish(request: Request, target_menu_id: str, target_submenu_id: str):
    target_submenu_id = uuid.UUID(target_submenu_id)
    target_menu_id = uuid.UUID(target_menu_id)
    data = await request.json()

    name = data.get('title')
    description = data.get('description')
    price = data.get('price')

    try:
        Session = sessionmaker(bind=engine)

        with Session() as session:
            menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
            if menu is None:
                return {'error': f'Меню с ID {target_menu_id} не найдено'}

            submenu = (
                session.query(Submenu)
                .filter(
                    Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id
                )
                .first()
            )
            if submenu is None:
                return {'error': f'Подменю с ID {target_submenu_id} не найдено'}

            new_dish = Dish(
                name=name,
                description=description,
                price=price,
                submenu_id=target_submenu_id,
            )
            session.add(new_dish)
            session.commit()

            # Access the relevant information of the newly created dish
            dish_id = str(new_dish.id)
            dish_name = new_dish.name
            dish_description = new_dish.description
            dish_price = str(new_dish.price)
            session.close()

        return {
            'title': dish_name,
            'description': dish_description,
            'id': dish_id,
            'price': dish_price,
        }
    except Exception as e:
        error_msg = str(e)
        return {'error': error_msg}


@router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def show_all_dishes(target_menu_id: str, target_submenu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    target_submenu_id = uuid.UUID(target_submenu_id)
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Проверяем, существует ли меню с указанным target_menu_id
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

        if menu is None:
            session.close()
            return []  # Возвращаем пустой список, если меню не найдено

        submenu = (
            session.query(Submenu)
            .filter_by(id=target_submenu_id, menu_id=target_menu_id)
            .first()
        )
        if submenu is None:
            session.close()
            return []  # Возвращаем пустой список, если подменю не найдено
        all_dishes = submenu.dishes

        # Создаем список словарей с информацией о каждом подменю
        dishes_list = [
            {
                'id': str(dishes.id),
                'title': dishes.name,
                'description': dishes.description,
                'price': str(dishes.price),
            }
            for dishes in all_dishes
        ]

        session.close()
        return dishes_list

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def show_dish(target_menu_id: str, target_submenu_id, target_dish_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    target_submenu_id = uuid.UUID(target_submenu_id)
    target_dish_id = uuid.UUID(target_dish_id)
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Проверяем, существует ли меню с указанным target_menu_id
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

        if menu is None:
            session.close()
            return JSONResponse(
                content={'detail': 'dish not found'},
                status_code=404,
            )

        # Теперь у нас есть menu, связанный с текущей сессией,
        # и мы можем без проблем получить доступ к его подменю
        submenu = (
            session.query(Submenu)
            .filter_by(id=target_submenu_id, menu_id=target_menu_id)
            .first()
        )
        if submenu is None:
            session.close()
            return JSONResponse(
                content={'detail': 'dish not found'},
                status_code=404,
            )

        dish = (
            session.query(Dish)
            .filter_by(id=target_dish_id, submenu_id=target_submenu_id)
            .first()
        )

        if dish:
            dish_id = str(dish.id)
            dish_name = dish.name
            dish_description = dish.description
            dish_price = str(dish.price)
            session.close()
            return {
                'id': dish_id,
                'description': dish_description,
                'price': dish_price,
                'title': dish_name,
            }

        session.close()
        return JSONResponse(
            content={'detail': 'dish not found'},
            status_code=404,
        )

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def update_dish(request: Request, target_submenu_id: str, target_dish_id: str):
    data = await request.json()

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    target_submenu_id = uuid.UUID(target_submenu_id)
    target_dish_id = uuid.UUID(target_dish_id)
    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Находим запись с указанным target_submenu_id
            dish = session.query(Dish).filter(Dish.id == target_dish_id).first()

            if dish:
                # Обновляем значения полей записи, если переданы новые значения
                if title:
                    dish.name = title
                if description:
                    dish.description = description
                if price:
                    dish.price = price
                # Фиксируем изменения в базе данных
                session.commit()
                dish_id = str(dish.id)
                dish_name = dish.name
                dish_description = dish.description
                dish_price = str(dish.price)
                session.close()
                return {
                    'id': dish_id,
                    'title': dish_name,
                    'description': dish_description,
                    'price': dish_price,
                }
            session.close()
            return JSONResponse(
                content={'detail': 'dish not found'},
                status_code=404,
            )
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {'error': error_msg}


@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def delete_dish(target_dish_id: str):
    target_dish_id = uuid.UUID(target_dish_id)
    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Получаем все записи из таблицы "menus"
            dish = session.query(Dish).filter(Dish.id == target_dish_id).first()
            session.delete(dish)
            # Фиксируем изменения в базе данных
            session.commit()
        return {'status': true, 'message': 'The dish has been deleted'}
    except Exception as e:
        error_msg = str(e)
        return {'error': error_msg}
