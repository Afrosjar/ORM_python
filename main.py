import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_table, Publisher, Shop, Book, Stock, Sale
import json

with open('initialization.txt') as f:
    password, login, db = f.readline().split()

DSN = f'postgresql://{login}:{password}@localhost:5432/{db}'
engine = sqlalchemy.create_engine(DSN)

create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

author = input('Введите ID или имя автора(пример: Pearson или Reilly или 1 или 2 , чтобы узнать продажи :  ')
if author.isalnum():
    subq = session.query(Publisher.name).filter(Publisher.name.ilike(f'%{author}%')).subquery()
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Book.publisher).join(Stock).join(Shop).\
            join(Sale).join(subq, Publisher.name.ilike(f'%{author}%')):
        print(f'{c[0]:<40}| {c[1]:<10}| {c[2]:<10}| {c[3]}')
if author.isdigit():
    subq = session.query(Publisher.id).filter(Publisher.id == author).subquery()
    for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Book.publisher).join(Stock).join(
            Shop). \
            join(Sale).join(subq, Publisher.id== author):
        print(f'{c[0]:<40}| {c[1]:<10}| {c[2]:<10}| {c[3]}')



session.close()
