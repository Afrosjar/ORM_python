import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)

    def __str__(self):
        return f'Publisher: {self.id}: {self.name}'


class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f'Book: {self.id}: {self.title}: {self.id_publisher}'


class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), unique=True, nullable=False)

    def __str__(self):
        return f' Shop {self.id}: {self.name}'


class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer)
    book = relationship(Book, backref="book_ids")
    shop = relationship(Shop, backref="shop_ids")

    def __str__(self):
        return f'Stock {self.id} Book_id: {self.id_book} Shop_id: {self.id_shop} Count: {self.count}'


class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    date_sale = sq.Column(sq.DateTime)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)
    stock = relationship(Stock, backref="stock_ids")

    def __str__(self):
        return f'Sale: {self.id} Price: {self.price} Date:{self.date_sale} Stock: {self.id_stock} Count: {self.count}'


def create_table(engine):
    """Метод создает все таблицы. Если таблицы уже есть - не создаст повторно"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
