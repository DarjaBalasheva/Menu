from fastapi import FastAPI

from api.db import db_connect
from api.db.db_create import Base, engine
from api.routers.dishes import router as dishes
from api.routers.menus import router as menus
from api.routers.submenus import router as submenus

# Создаем таблицы базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Подлючение к БД
connection = db_connect.connect()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(menus)
app.include_router(submenus)
app.include_router(dishes)
