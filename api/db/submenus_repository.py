import uuid
from typing import List, Dict

from sqlalchemy.orm import Session
from api.db.db_create import engine, Base, Menu, Submenu


def create_submenu_in_db(session: Session, target_menu_id: str, title: str, description: str) -> Submenu:
    target_menu_id = uuid.UUID(target_menu_id)

    new_submenu = Submenu(
            name=title, description=description, menu_id=target_menu_id
        )
    session.add(new_submenu)
    session.commit()

    return new_submenu

def get_all_submenus(session: Session, menu: Menu) -> List[Submenu]:
    submenus = menu.submenus

    return submenus

def get_submenu_by_id(session: Session, target_menu_id: str, target_submenu_id: str) -> Submenu:
    target_menu_id = uuid.UUID(target_menu_id)
    target_submenu_id = uuid.UUID(target_submenu_id)
    submenu = (
        session.query(Submenu)
        .filter_by(id=target_submenu_id, menu_id=target_menu_id)
        .first()
    )

    return submenu

def update_submenu_by_id_in_bd(session: Session, submenu: Submenu, data: Dict[str, str]) -> Menu:
    title = data.get("title")
    description = data.get("description")

    if title:
        submenu.name = title
    if description:
        submenu.description = description
    session.commit()
    return submenu

def delete_submenu_by_id_in_bd(session: Session, submenu: Submenu) -> bool:
    session.delete(submenu)
    session.commit()
    return True