import uuid

from fastapi import FastAPI, Request
from sqlalchemy import true
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse
from routers.menus import router as menus
from routers.submenus import router as submenus
from routers.dishes import router as dishes
from db_create import engine, Base, Menu, Submenu, Dish
import db_connect

# Создаем таблицы базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI()
connection = db_connect.connect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(menus)
app.include_router(submenus)
app.include_router(dishes)



