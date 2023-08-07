import uuid
from sqlalchemy.dialects.postgresql import UUID
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
from sqlalchemy.orm import declarative_base, relationship
import os

load_dotenv()

USERNAME = os.environ.get("db_user_login")
PASSWORD = os.environ.get("db_user_password")
DBNAME = os.environ.get("db_name")
HOST = os.environ.get("db_host")

engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}/{DBNAME}", echo=True)

Base = declarative_base()


class Menu(Base):
    __tablename__ = "menus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String)
    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete-orphan"
    )

    def submenus_count(self):
        return len(self.submenus)

    def dishes_count(self):
        return sum(submenu.dishes_count() for submenu in self.submenus)


class Submenu(Base):
    __tablename__ = "submenus"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete-orphan"
    )

    def dishes_count(self):
        return len(self.dishes)


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    description = Column(String)
    price = Column(Float, default=None)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
    submenu = relationship("Submenu", back_populates="dishes")


# Вспомогательное ограничение
# чтобы блюдо не могло находиться в 2-х подменю одновременно
SubmenuDishConstraint = "uq_submenu_dish_constraint"


class SubmenuDish(Base):
    __tablename__ = "submenu_dishes"
    id = Column(Integer, primary_key=True)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"))

    # Ограничиваем уникальность пары (submenu_id, dish_id)
    __table_args__ = (
        UniqueConstraint("submenu_id", "dish_id", name=SubmenuDishConstraint),
    )


Base.metadata.create_all(engine)
