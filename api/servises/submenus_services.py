from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api.servises import menus_servises

from ..db import submenus_repository

not_menu = JSONResponse(content={'detail': 'submenu not found'}, status_code=404)


def create_submenu(
    session: Session, target_menu_id: str, data: dict[str, str]
) -> dict[str, str]:
    title = data.get('title')
    description = data.get('description')

    menu = menus_servises.check_menu(session, target_menu_id)

    if menu:
        new_submenu = submenus_repository.create_submenu_in_db(
            session, target_menu_id, title, description
        )
        return {
            'id': str(new_submenu.id),
            'title': new_submenu.name,
            'description': new_submenu.description,
            'dishes_count': new_submenu.dishes_count(),
        }
    return not_menu


def show_all_submenus(session: Session, target_menu_id: str) -> list[dict[str, str]]:
    menu = menus_servises.check_menu(session, target_menu_id)

    if menu:
        all_submenus = submenus_repository.get_all_submenus(session, menu)
        submenu_list = [
            {
                'id': str(submenu.id),
                'title': submenu.name,
                'description': submenu.description,
                'dishes_count': submenu.dishes_count(),
            }
            for submenu in all_submenus
        ]
        return submenu_list
    else:
        return not_menu


def show_submenu_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str
) -> list[dict[str, str]]:
    menu = menus_servises.check_menu(session, target_menu_id)

    if menu:
        submenu = submenus_repository.get_submenu_by_id(
            session, target_menu_id, target_submenu_id
        )
        if submenu:
            return {
                'id': str(submenu.id),
                'title': submenu.name,
                'description': submenu.description,
                'dishes_count': submenu.dishes_count(),
            }
        else:
            return JSONResponse(
                content={'detail': 'submenu not found'}, status_code=404
            )
    else:
        return not_menu


def update_submenu_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str, data: dict[str, str]
) -> dict[str, str]:

    title = data.get('title')
    description = data.get('description')

    menu = menus_servises.check_menu(session, target_menu_id)

    if menu:
        submenu = submenus_repository.get_submenu_by_id(
            session, target_menu_id, target_submenu_id
        )

        if submenu:
            update_submenu = submenus_repository.update_submenu_by_id_in_bd(
                session, submenu, title, description
            )

            return {
                'id': str(update_submenu.id),
                'title': update_submenu.name,
                'description': update_submenu.description,
                'dishes_count': update_submenu.dishes_count(),
            }

        return submenu

    return not_menu


def delete_submenu_by_id(
    session: Session, target_menu_id: str, target_submenu_id: str
) -> list[dict[str, str]]:
    menu = menus_servises.check_menu(session, target_menu_id)

    if menu:
        submenu = submenus_repository.get_submenu_by_id(
            session, target_menu_id, target_submenu_id
        )
        if submenu:
            submenus_repository.delete_submenu_by_id_in_bd(session, submenu)
            return {'status': True, 'message': 'The submenu has been deleted'}

        else:
            return JSONResponse(
                content={'detail': 'submenu not found'}, status_code=404
            )

    return not_menu


def check_submenu(session: Session, target_menu_id: str, target_submenu_id: str) -> list[dict[str, str]]:
    submenu = submenus_repository.get_submenu_by_id(session, target_menu_id, target_submenu_id)
    if submenu:
        return submenu
    else:
        return None
