from fastapi import FastAPI
from routers.menus import router as menus
from routers.submenus import router as submenus
from routers.dishes import router as dishes
from db_create import engine, Base
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
