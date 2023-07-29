import uuid

from fastapi import FastAPI, Request, APIRouter
from sqlalchemy import true
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from db_create import engine, Base, Menu, Submenu, Dish
import db_connect

router = APIRouter()
connection = db_connect.connect()

# Добавление меню в таблицу
@router.post("/api/v1/menus", status_code=201)
async def create_menu(request: Request):
    data = await request.json()  # Обрабатывает json из боди

    # Достаём значения title и description
    title = data.get("title")
    description = data.get("description")

    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)
        session = Session()

        # Создаем новый объект меню
        new_menu = Menu(name=title, description=description)

        # Добавляем новое меню в сессию
        session.add(new_menu)

        # Фиксируем изменения в базе данных
        session.commit()
        menu_id = str(new_menu.id)
        menu_name = new_menu.name
        menu_description = new_menu.description
        submenus_count = new_menu.submenus_count()
        dishes_count = new_menu.dishes_count()
        session.close()
        return {
            "id": menu_id,
            "title": menu_name,
            "description": menu_description,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/api/v1/menus")
async def show_all_menu():
    Session = sessionmaker(bind=engine)
    session = Session()
    all_menus = session.query(Menu).all()
    menu_list = [
        {
            "id": str(menu.id),
            "title": menu.name,
            "description": menu.description,
            "submenus_count": menu.submenus_count(),
            "dishes_count": menu.dishes_count(),
        }
        for menu in all_menus
    ]
    session.close()
    return menu_list


@router.get("/api/v1/menus/{target_menu_id}")
async def show_menu(target_menu_id: str):
    if target_menu_id is None:
        return JSONResponse(content={"detail": "ID меню не указан"}, status_code=422)

    Session = sessionmaker(bind=engine)
    session = Session()
    target_menu_id = uuid.UUID(target_menu_id)
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

    if menu:
        menu_id = str(menu.id)
        menu_name = menu.name
        menu_description = menu.description
        submenus_count = menu.submenus_count()
        dishes_count = menu.dishes_count()
        session.close()
        return {
            "id": menu_id,
            "title": menu_name,
            "description": menu_description,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count,
        }

    session.close()
    return JSONResponse(
        content={
            "detail": "menu not found",
        },
        status_code=404,
    )


@router.patch("/api/v1/menus/{target_menu_id}")
async def update_menu(request: Request, target_menu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    data = await request.json()

    title = data.get("title")
    description = data.get("description")

    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Находим запись с указанным menu_id
            menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

            if menu:
                # Обновляем значения полей записи, если переданы новые значения
                if title:
                    menu.name = title
                if description:
                    menu.description = description
                # Фиксируем изменения в базе данных
                session.commit()
                menu_id = str(menu.id)
                menu_name = menu.name
                menu_description = menu.description
                submenus_count = menu.submenus_count()
                dishes_count = menu.dishes_count()
                session.close()
                return {
                    "id": menu_id,
                    "title": menu_name,
                    "description": menu_description,
                    "submenus_count": submenus_count,
                    "dishes_count": dishes_count,
                }
            return JSONResponse(
                content={
                    "detail": "menu not found",
                },
                status_code=404,
            )
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}


@router.delete("/api/v1/menus/{target_menu_id}")
async def delete_menu(target_menu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Получаем все записи из таблицы "menus"
            menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
            session.delete(menu)

            # Фиксируем изменения в базе данных
            session.commit()

        return {"status": true, "message": "The menu has been deleted"}
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}


@router.delete("/api/v1/menus")
async def delete_all_menus():
    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Получаем все записи из таблицы "menus"
            all_submenus = session.query(Submenu).all()

            # Удаляем все записи из таблицы "menus"
            for submenu in all_submenus:
                session.delete(submenu)

            # Фиксируем изменения в базе данных
            session.commit()

        return {"message": "Все подменю успешно удалены из базы данных"}
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}