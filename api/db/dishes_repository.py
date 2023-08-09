import uuid

from sqlalchemy.orm import Session

from api.db.db_create import Dish, Submenu


def create_dish_in_db(
    session: Session, submenu: Submenu, title: str, description: str, price: str
) -> Dish:

    new_dish = Dish(name=title, description=description, price=price, submenu=submenu)
    session.add(new_dish)
    session.commit()

    return new_dish


def get_all_dishes(session: Session, submenu: Submenu) -> list[Dish]:
    dishes = submenu.dishes
    return dishes


def get_dish_by_id(
    session: Session, target_submenu_id: str, target_dish_id: str
) -> Dish:
    target_submenu_id = uuid.UUID(target_submenu_id)
    target_dish_id = uuid.UUID(target_dish_id)
    dish = (
        session.query(Dish)
        .filter_by(id=target_dish_id, submenu_id=target_submenu_id)
        .first()
    )

    return dish


def update_dish_by_id_in_bd(
    session: Session, dish: Dish, title: str, description: str, price: str
) -> Dish:

    if title:
        dish.name = title
    if description:
        dish.description = description
    if price:
        dish.price = price

    session.commit()

    return dish


def delete_dish_by_id_in_bd(session: Session, dish: Dish) -> bool:
    session.delete(dish)
    session.commit()
    return True
