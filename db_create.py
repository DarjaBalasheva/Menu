from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
    Float,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import os

load_dotenv()

USERNAME = os.environ.get(
    "db_user_login"
)  # Получаем значение переменной окружения 'db_host'
PASSWORD = os.environ.get(
    "db_user_password"
)  # Получаем значение переменной окружения 'db_user_password'
DBNAME = os.environ.get("db_name")  # Получаем значение переменной окружения 'db_name'

engine = create_engine(
    f"postgresql://{USERNAME}:{PASSWORD}@localhost/{DBNAME}", echo=True
)

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String)
    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )


class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String)
    price = Column(Float, default=None)
    submenu_id = Column(Integer, ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")


# Вспомогательное ограничение
# чтобы блюдо не могло находиться в 2-х подменю одновременно
SubmenuDishConstraint = "uq_submenu_dish_constraint"


class SubmenuDish(Base):
    __tablename__ = "submenu_dishes"
    id = Column(Integer, primary_key=True)
    submenu_id = Column(Integer, ForeignKey("submenus.id"))
    dish_id = Column(Integer, ForeignKey("dishes.id"))

    # Ограничиваем уникальность пары (submenu_id, dish_id)
    __table_args__ = (
        UniqueConstraint("submenu_id", "dish_id", name=SubmenuDishConstraint),
    )


Base.metadata.create_all(engine)
