from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List

class Category(Base):
    __tablename__ = "flower_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String)

    products: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = 'flower_products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('flower_categories.id'))
    category: Mapped['Category'] = relationship(back_populates='products')
