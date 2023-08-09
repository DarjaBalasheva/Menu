from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.servises import submenus_services

from ..db import dishes_repository

not_submenu = JSONResponse(content={'detail': 'dishes not found'}, status_code=404)


def create_dishes(
    session: Session, target_menu_id: str, target_submenu_id: str, data: dict[str, str]
) -> dict[str, str]:

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')

    submenu = submenus_services.check_submenu(session, target_menu_id, target_submenu_id)

    if submenu:
        new_dishes = dishes_repository.create_dish_in_db(
            session, submenu, title, description, price
        )
        return {
            'id': str(new_dishes.id),
            'title': new_dishes.name,
            'description': new_dishes.description,
            'price': str(new_dishes.price)
        }
    return not_submenu


def show_all_dishes(session: Session, target_menu_id: str, target_submenu_id: str) -> list[dict[str, str]]:
    submenu = submenus_services.check_submenu(session, target_menu_id, target_submenu_id)

    if submenu:
        all_dishes = dishes_repository.get_all_dishes(session, submenu)
        dishes_list = [
            {
                'id': str(dish.id),
                'title': dish.name,
                'description': dish.description,
                'price': str(dish.price),
            }
            for dish in all_dishes
        ]
        return dishes_list
    else:
        return []


def show_dish_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str, target_dish_id: str
) -> list[dict[str, str]]:
    submenu = submenus_services.check_submenu(session, target_menu_id, target_submenu_id)

    if submenu:
        dish = dishes_repository.get_dish_by_id(
            session, target_submenu_id, target_dish_id
        )
        if dish:
            return {
                'id': str(dish.id),
                'title': dish.name,
                'description': dish.description,
                'price': str(dish.price),
            }
        else:
            return JSONResponse(
                content={'detail': 'dish not found'}, status_code=404
            )
    else:
        return not_submenu


def update_dish_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str, target_dish_id: str, data: dict[str, str]
) -> dict[str, str]:

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')

    submenu = submenus_services.check_submenu(session, target_menu_id, target_submenu_id)

    if submenu:
        dish = dishes_repository.get_dish_by_id(
            session, target_submenu_id, target_dish_id
        )

        if dish:
            update_dish = dishes_repository.update_dish_by_id_in_bd(
                session, dish, title, description, price
            )

            return {
                'id': str(update_dish.id),
                'title': update_dish.name,
                'description': update_dish.description,
                'price': str(update_dish.price),
            }

        return dish

    return not_submenu


def delete_dish_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str, target_dish_id: str
) -> list[dict[str, str]]:
    submenu = submenus_services.check_submenu(session, target_menu_id, target_submenu_id)

    if submenu:
        dish = dishes_repository.get_dish_by_id(
            session, target_submenu_id, target_dish_id
        )

        if dish:
            dishes_repository.delete_dish_by_id_in_bd(session, dish)
            return {'status': True, 'message': 'The dish has been deleted'}

        else:
            return JSONResponse(
                content={'detail': 'dish not found'}, status_code=404
            )

    return not_submenu
