import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=40), unique=True, nullable=False)

    def __str__(self):
        return self.name.ljust(55)


class Book(Base):
    __tablename__ = "book"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(40), nullable=False)
    id_publisher = sa.Column(sa.Integer, sa.ForeignKey(
        'publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return self.title.ljust(40)


class Shop(Base):
    __tablename__ = 'shop'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(length=40), nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = 'stock'

    id = sa.Column(sa.Integer, primary_key=True)
    count = sa.Column(sa.Integer, nullable=False)
    id_book = sa.Column(sa.Integer, sa.ForeignKey('book.id'), nullable=False)
    id_shop = sa.Column(sa.Integer, sa.ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')


class Sale(Base):
    __tablename__ = 'sale'

    id = sa.Column(sa.Integer, primary_key=True)
    price = sa.Column(sa.Numeric(6, 2), nullable=False)
    date_sale = sa.Column(sa.Date, nullable=False)
    count = sa.Column(sa.Integer, nullable=False)
    id_stock = sa.Column(sa.Integer, sa.ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f"{self.count * self.price} | {self.date_sale}"
