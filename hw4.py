import decimal
from typing import Optional
from sqlalchemy import String, Boolean, create_engine, ForeignKey,Numeric,select,func
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, relationship

engine = create_engine('sqlite:///:memory:')


session = Session(bind=engine)


class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(255),nullable=True)
    products: Mapped[list["Product"]] = relationship(back_populates='category')




class Product(Base):
    __tablename__ = "products"

    id:    Mapped[int] = mapped_column(primary_key=True)
    name:  Mapped[str] = mapped_column(String(100))
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10,2))
    in_stock: Mapped[bool] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'),index=True)
    category: Mapped[Category] = relationship('Category', back_populates='products')




Base.metadata.create_all(engine)


# -------------------------------------------------------------------

electronics = Category(name='Electronics', description='All type of Electronics')

books = Category(name='Books', description='All type of Books')

clothing = Category(name='Clothing', description='All type of Clothing')


products = ([
    Product(name = "Smartphone", price = decimal.Decimal("299.99"), in_stock = True, category = electronics),
    Product(name = "Laptop", price = decimal.Decimal("499.99"), in_stock = True, category = electronics),
    Product(name = "Sci-fi",price = decimal.Decimal("15.99"), in_stock = True, category = books),
    Product(name = "Jeans", price = decimal.Decimal("40.50"), in_stock = True, category= clothing),
    Product(name = "T-shirt", price = decimal.Decimal("20.00"), in_stock = True, category = clothing),
])

session.add_all(products)
session.commit()

# -------------------------------------------------------------------

categories = session.scalars(select(Category))

for category in categories:
    prod = session.scalars(select(Product).where(Product.category == category)).all()
    print(f"{category.name}: {category.description}")
    for product in prod:
        print(f"{product.name}: {product.price} €")




# -------------------------------------------------------------------

smart = session.scalars(select(Product).where(Product.name== "Smartphone")).first()
smart.price = decimal.Decimal("349.99")
session.commit()

print(f"New smartphone price: {smart.price}")


# -------------------------------------------------------------------


rows = session.execute(
    select(Category.name, func.count(Product.id).label("total"))
    .join(Product, Product.category_id == Category.id)
    .group_by(Category.id)).all()

for name, total in rows:
    print(f"{name}: {total}")


# -------------------------------------------------------------------
rows = session.execute(
    select(Category.name, func.count(Product.id).label("total"))
    .join(Product, Product.category_id == Category.id)
    .group_by(Category.id)
    .having(func.count(Product.id) > 1)).all()

for name, total in rows:
    print(f"{name}: {total}")

