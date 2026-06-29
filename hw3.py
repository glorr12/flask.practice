import decimal
from typing import Optional
from sqlalchemy import String, Boolean, create_engine, ForeignKey,Numeric
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase

engine = create_engine('sqlite:///:memory:')


session = Session(bind=engine)


class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(255))



class Product(Base):
    __tablename__ = "products"

    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100))
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10,2))
    in_stock: Mapped[bool] = mapped_column(Boolean)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))




Base.metadata.create_all(engine)
