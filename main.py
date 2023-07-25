import uuid

from fastapi import FastAPI, Request
from sqlalchemy import true
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from db_create import engine, Menu, Submenu, Dish
import db_connect

app = FastAPI()
connection = db_connect.connect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Добавление меню в таблицу
@app.post("/api/v1/menus", status_code=201)
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


@app.get("/api/v1/menus")
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


@app.get("/api/v1/menus/{target_menu_id}")
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


@app.patch("/api/v1/menus/{target_menu_id}")
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


@app.delete("/api/v1/menus/{target_menu_id}")
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


@app.delete("/api/v1/menus")
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


# Добавление подменю в таблицу
@app.post("/api/v1/menus/{target_menu_id}/submenus", status_code=201)
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


@app.get("/api/v1/menus/{target_menu_id}/submenus")
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


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
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


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
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


@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
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


@app.post(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    status_code=201,
)
async def create_dish(request: Request, target_menu_id: str, target_submenu_id: str):
    target_submenu_id = uuid.UUID(target_submenu_id)
    target_menu_id = uuid.UUID(target_menu_id)
    data = await request.json()

    name = data.get("title")
    description = data.get("description")
    price = data.get("price")

    try:
        Session = sessionmaker(bind=engine)

        with Session() as session:
            menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
            if menu is None:
                return {"error": f"Меню с ID {target_menu_id} не найдено"}

            submenu = (
                session.query(Submenu)
                .filter(
                    Submenu.id == target_submenu_id, Submenu.menu_id == target_menu_id
                )
                .first()
            )
            if submenu is None:
                return {"error": f"Подменю с ID {target_submenu_id} не найдено"}

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
            "title": dish_name,
            "description": dish_description,
            "id": dish_id,
            "price": dish_price,
        }
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
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
                "id": str(dishes.id),
                "title": dishes.name,
                "description": dishes.description,
                "price": str(dishes.price),
            }
            for dishes in all_dishes
        ]

        session.close()
        return dishes_list

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {"error": error_msg}


@app.get(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}"
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
                content={"detail": "dish not found"},
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
                content={"detail": "dish not found"},
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
                "id": dish_id,
                "description": dish_description,
                "price": dish_price,
                "title": dish_name,
            }

        session.close()
        return JSONResponse(
            content={"detail": "dish not found"},
            status_code=404,
        )

    except Exception as e:
        error_msg = str(e)
        session.close()
        return {"error": error_msg}


@app.patch(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}"
)
async def update_dish(request: Request, target_submenu_id: str, target_dish_id: str):
    data = await request.json()

    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
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
                    "id": dish_id,
                    "title": dish_name,
                    "description": dish_description,
                    "price": dish_price,
                }
            session.close()
            return JSONResponse(
                content={"detail": "dish not found"},
                status_code=404,
            )
    except Exception as e:
        error_msg = str(e)
        session.close()
        return {"error": error_msg}


@app.delete(
    "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}"
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
        return {"status": true, "message": "The dish has been deleted"}
    except Exception as e:
        error_msg = str(e)
        return {"error": error_msg}
