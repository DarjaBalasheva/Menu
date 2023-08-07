import uuid
from typing import List, Dict
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..db.db_create import Menu, Submenu, Dish
from ..db import db_connect
from ..db import menus_repository


def create_menu(session: Session, data: Dict[str, str]) -> Dict[str, str]:
    title = data.get("title")
    description = data.get("description")

    new_menu = menus_repository.create_menu_in_db(session, title, description)
    return {
        "id": str(new_menu.id),
        "title": new_menu.name,
        "description": new_menu.description,
        "submenus_count": new_menu.submenus_count(),
        "dishes_count": new_menu.dishes_count(),
    }


def show_all_menus(session: Session) -> List[Dict[str, str]]:
    all_menus = menus_repository.get_all_menus(session)
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
    return menu_list


def show_menu_by_id(session: Session, target_menu_id: str) -> List[Dict[str, str]]:
    menu = menus_repository.get_menu_by_id(session, target_menu_id)
    if menu:
        return {
            "id": str(menu.id),
            "title": menu.name,
            "description": menu.description,
            "submenus_count": menu.submenus_count(),
            "dishes_count": menu.dishes_count(),
        }
    else:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)


def update_menu_by_id(session: Session, target_menu_id: str, data: Dict[str, str]) -> List[Dict[str, str]]:
    title = data.get("title")
    description = data.get("description")
    menu = menus_repository.get_menu_by_id(session, target_menu_id)
    if menu:
        update_menu = menus_repository.update_menu_by_id_in_bd(session, menu, title, description)
        return {
            "id": str(update_menu.id),
            "title": update_menu.name,
            "description": update_menu.description,
            "submenus_count": update_menu.submenus_count(),
            "dishes_count": update_menu.dishes_count(),
        }
    else:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)


def delete_menu_by_id(session: Session, target_menu_id: str) -> List[Dict[str, str]]:
    menu = menus_repository.get_menu_by_id(session, target_menu_id)
    if menu:
        menus_repository.delete_menu_by_id_in_bd(session, menu)
        return {"status": True, "message": "All menus have been deleted"}
    else:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)


def delete_all_menus(session: Session) -> bool:
    menus = menus_repository.get_all_menus(session)
    for menu in menus:
        delete_menu_by_id(session, menu)

def check_menu(session: Session, target_menu_id: str) -> List[Dict[str, str]]:
    menu = menus_repository.get_menu_by_id(session, target_menu_id)
    if menu:
        return menu
    else:
        return None