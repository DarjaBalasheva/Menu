import uuid

from sqlalchemy.orm import Session

from api.db.db_create import Menu


def create_menu_in_db(session: Session, title: str, description: str) -> Menu:
    new_menu = Menu(name=title, description=description)
    session.add(new_menu)
    session.commit()
    return new_menu


def get_all_menus(session: Session) -> Menu:
    all_menus = session.query(Menu).all()
    return all_menus


def get_menu_by_id(session: Session, target_menu_id: str) -> Menu:
    target_menu_id = uuid.UUID(target_menu_id)
    menu = session.query(Menu).filter(Menu.id == target_menu_id).first()
    return menu


def update_menu_by_id_in_bd(
    session: Session, menu: Menu, title: str, description: str
) -> Menu:
    if title:
        menu.name = title
    if description:
        menu.description = description
    session.commit()
    return menu


def delete_menu_by_id_in_bd(session: Session, menu: Menu) -> bool:
    session.delete(menu)
    session.commit()
    return True
