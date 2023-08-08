from fastapi import APIRouter, Request
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from api.db.db_create import engine

from ..db import db_connect
from ..servises import menus_servises

router = APIRouter()
connection = db_connect.connect()


# Добавление меню в таблицу
@router.post('/api/v1/menus', status_code=201)
async def create_menu_handler(request: Request):
    data = await request.json()
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result = menus_servises.create_menu(session, data)
        session.close()
        return result
    except Exception as e:
        session.close()
        return {'error': str(e)}


@router.get('/api/v1/menus')
async def show_all_menu_handler():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        menu_list = menus_servises.show_all_menus(session)
        session.close()
        return menu_list
    except Exception as e:
        session.close()
        return {'error': str(e)}


@router.get('/api/v1/menus/{target_menu_id}')
async def show_menu_handler(target_menu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()

    if target_menu_id is None:
        return JSONResponse(content={'detail': 'ID меню не указан'}, status_code=422)

    try:
        menu = menus_servises.show_menu_by_id(session, target_menu_id)
        if menu:
            session.close()
            return menu
        session.close()
        return JSONResponse(content={'detail': 'menu not found'}, status_code=404)

    except Exception as e:
        session.close()
        return {'error': str(e)}


@router.patch('/api/v1/menus/{target_menu_id}')
async def update_menu_handler(request: Request, target_menu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()

    data = await request.json()

    try:
        update_menu = menus_servises.update_menu_by_id(session, target_menu_id, data)
        session.close()
        return update_menu
    except Exception as e:
        session.close()
        return {'error': str(e)}


@router.delete('/api/v1/menus/{target_menu_id}')
async def delete_menu_handler(target_menu_id: str):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        success = menus_servises.delete_menu_by_id(session, target_menu_id)
        session.close()
        return success

    except Exception as e:
        session.close()
        return {'error': str(e)}


@router.delete('/api/v1/menus')
async def delete_all_menus_handler():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        success = menus_servises.delete_all_menus(session)
        session.close()
        return success

    except Exception as e:
        session.close()
        return {'error': str(e)}
