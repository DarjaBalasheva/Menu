from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

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
@cache(expire=30)
async def root():
    return {'message': 'Hello World'}


app.include_router(menus)
app.include_router(submenus)
app.include_router(dishes)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url('redis://redis', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
