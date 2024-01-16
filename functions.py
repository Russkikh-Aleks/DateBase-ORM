import sqlalchemy as sa
import json
from models import Publisher, Book, Shop, Sale, Stock, Base


def create_engine(module, login, password, datebase, port='5432'):
    '''Функция для создания движка'''

    DSN = f"{module}://{login}:{password}@localhost:{port}/{datebase}"
    return sa.create_engine(DSN)


def create_tables(engine):
    '''Функция для создания таблиц'''

    Base.metadata.create_all(engine)


def instantiation_from_json(file_name: str, session):
    '''Функция для создания экземпляров моделей из файла json'''

    m_dict = {'publisher': Publisher, "book": Book, "shop": Shop,
              "stock": Stock, "sale": Sale}

    # Чтение данных из файла, десериализация
    with open(file_name) as file:
        data = json.load(file)

    # Создание экземпляра моделей, сохранение в БД
    for el in data:
        fields_dict = {'id': el['pk']}
        fields_dict.update(el['fields'])
        sample = m_dict[el["model"]](**fields_dict)
        session.add(sample)
        session.commit()


def printing_purchases(pub_data: str|int, session):
    '''Функция для вывода информации о продажах по данным об издательстве'''

    print()
    print(" | ".join(['название книги'.ljust(40), 'название магазина, в котором была куплена эта книга'.ljust(55),
                      'стоимость покупки'.ljust(20), 'дата покупки'.ljust(12)]))

    q = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).select_from(
        Publisher).join(Book).join(Stock).join(Shop).join(Sale)

    if pub_data.isdigit():
        q = q.filter(Publisher.id == int(pub_data)).all()
    else:
        q = q.filter(Publisher.name == pub_data).all()

    for books, shop, price, count, date in q:
        print(f'{books: <40} | {shop: <55} | {price * count: <20} | {str(date): <12}')


def del_tables(engine):
    '''Функция для удаления таблиц'''

    Base.metadata.drop_all(engine)
