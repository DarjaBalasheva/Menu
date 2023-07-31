import uuid

from fastapi import Request, APIRouter
from sqlalchemy import true
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from db_create import engine, Menu, Submenu
import db_connect

router = APIRouter()
connection = db_connect.connect()


# Добавление подменю в таблицу
@router.post("/api/v1/menus/{target_menu_id}/submenus", status_code=201)
async def create_submenu(request: Request, target_menu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    data = await request.json()

    title = data.get("title")
    description = data.get("description")

    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)
        session = Session()

        # Создаем новый объект подменю
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
        if menu is None:
            return JSONResponse(
                content={
                    "detail": "menu not found",
                },
                status_code=404,
            )

        # Добавляем новое  подменю в сессию
        new_submenu = Submenu(
            name=title, description=description, menu_id=target_menu_id
        )
        session.add(new_submenu)
        session.commit()
        submenu_id = str(new_submenu.id)
        submenu_name = new_submenu.name
        submenu_description = new_submenu.description
        dishes_count = new_submenu.dishes_count()
        session.close()
        return {
            "id": submenu_id,
            "title": submenu_name,
            "description": submenu_description,
            "dishes_count": dishes_count,
        }
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}


@router.get("/api/v1/menus/{target_menu_id}/submenus")
async def show_all_submenus(target_menu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        # Проверяем, существует ли меню с указанным target_menu_id
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

        if menu is None:
            session.close()
            return []  # Возвращаем пустой список, если меню не найдено

        # Теперь у нас есть menu, связанный с текущей сессией,
        # и мы можем без проблем получить доступ к его подменю
        all_submenus = menu.submenus

        # Создаем список словарей с информацией о каждом подменю
        submenu_list = [
            {
                "id": str(submenu.id),
                "title": submenu.name,
                "description": submenu.description,
                "dishes_count": submenu.dishes_count(),
            }
            for submenu in all_submenus
        ]

        session.close()
        return submenu_list

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {"error": error_msg}


@router.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def show_submenu(target_menu_id: str, target_submenu_id: str):
    target_menu_id = uuid.UUID(target_menu_id)
    target_submenu_id = uuid.UUID(target_submenu_id)
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        menu = session.query(Menu).filter(Menu.id == target_menu_id).first()

        if menu:
            submenu = (
                session.query(Submenu)
                .filter_by(id=target_submenu_id, menu_id=target_menu_id)
                .first()
            )

            if submenu:
                submenu_id = str(submenu.id)
                submenu_name = submenu.name
                submenu_description = submenu.description
                dishes_count = submenu.dishes_count()

                session.close()
                return {
                    "id": submenu_id,
                    "title": submenu_name,
                    "description": submenu_description,
                    "dishes_count": dishes_count,
                }

        # If submenu is not found, return a 404 response
        session.close()
        return JSONResponse(
            content={"detail": "submenu not found"},
            status_code=404,
        )

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {"error": error_msg}


@router.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def update_submenu(request: Request, target_submenu_id: str):
    target_submenu_id = uuid.UUID(target_submenu_id)
    data = await request.json()

    title = data.get("title")
    description = data.get("description")

    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Находим запись с указанным target_submenu_id
            submenu = (
                session.query(Submenu).filter(Submenu.id == target_submenu_id).first()
            )

            if submenu:
                # Обновляем значения полей записи, если переданы новые значения
                if title:
                    submenu.name = title
                if description:
                    submenu.description = description
                # Фиксируем изменения в базе данных
                session.commit()
                submenu_id = submenu.id
                submenu_name = submenu.name
                submenu_description = submenu.description
                dishes_count = submenu.dishes_count()
                return {
                    "message": f"Информация для подменю с ID {target_submenu_id} успешно обновлена",
                    "id": submenu_id,
                    "title": submenu_name,
                    "description": submenu_description,
                    "dishes_count": dishes_count,
                }
            return JSONResponse(
                content={"detail": "submenu not found"},
                status_code=404,
            )
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}


@router.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_submenu(target_submenu_id: str):
    target_submenu_id = uuid.UUID(target_submenu_id)
    try:
        # Создаем сессию для взаимодействия с базой данных
        Session = sessionmaker(bind=engine)

        with Session() as session:
            # Получаем все записи из таблицы "menus"
            submenu = (
                session.query(Submenu).filter(Submenu.id == target_submenu_id).first()
            )
            session.delete(submenu)
            # Фиксируем изменения в базе данных
            session.commit()
        return {"status": true, "message": "The submenu has been deleted"}
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}
